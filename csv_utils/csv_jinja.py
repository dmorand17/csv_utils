import jinja2
import os
import sys
import argparse
from datetime import datetime
from csv_utils.csv_handler import CSVHandler

class CSVJinja:
    def __init__(self, env=None, template_path=None, env_options=None):
        if env is None:
            if env_options is None:
                env_options = {}
            if 'trim_blocks' not in env_options:
                env_options['trim_blocks'] = True
            if 'lstrip_blocks' not in env_options:
                env_options['lstrip_blocks'] = True
            if 'loader' not in env_options:
                env_options['loader'] = jinja2.FileSystemLoader([os.getcwd() if template_path is None else template_path, os.path.realpath(__file__)])
            env = jinja2.Environment(**env_options)
        self.env = env
        self.default_datetime_fmt = "%Y%m%d"
        self._register_filters()        

    def _register_filters(self):
        filters = {
            'bool': 'not implemented',
            'date': 'not implemented',
            'dateformat': self.dateformat
        }
        self.env.filters.update(filters)        
   
    def add_filters(self, filters):
        self.env.filters.update(filters)

    def add_globals(self,env_globals):
        self.env.globals.update(env_globals)

    def dateformat(self, dt, input_format=None, fmt=None):
        if type(dt) == str:
            date_parsed = datetime.strptime(dt,input_format)    
            return date_parsed.strftime(fmt or self.default_datetime_fmt)
        if type(dt) == datetime:
            return dt.strftime(fmt or self.default_datetime_fmt)

    def render_template(self, template, csv, **kwargs):
        # print("csv type {}".format(type(csv)))
        return self.env.get_template(template,globals=kwargs.get('template_globals')).render(rows=csv, **kwargs)

    def render_template_to_list(self, template, csv, fieldnames, rowkey, **kwargs):
        # print("csv type {}".format(type(csv)))
        # print(csv)
        template = self.env.get_template(template,globals=kwargs.get('template_globals'))
        # [print(row) for row in csv]

        return [dict(key=rowkey(row), template=template.render(rows=[row], fieldnames=fieldnames, **kwargs)) for row in csv]

def parse_args():
    parser = argparse.ArgumentParser(description='This script will render a file based on a jinja template (j2)')
    parser.add_argument('-v','--verbose', help='Enable verbose logging', action='store_true')
    parser.add_argument('-c', '--csv', help='csv input mapping file', required=True, action='store')
    parser.add_argument('--template-dir', help='template directory to find templates', default='templates', action='store')
    parser.add_argument('-t', '--templates', help='template filename', required=True, action='store', nargs='+')
    return parser.parse_args()

def test():
    csvhandler = CSVHandler('samples/sample-input.csv')

    csv_jinja = CSVJinja()
    rendered = csv_jinja.render_template("samples/sample-csvrows.j2",csvhandler.rows())
    print(rendered)

    key = lambda r: '-'.join([r[key] for key in ["name","gender"]])
    rendered = csv_jinja.render_template_to_list("samples/sample.j2",csvhandler.rows(),csvhandler.headers(),rowkey=key)
    print(rendered)

def main():
    args = parse_args()
    csvhandler = CSVHandler(args.csv)
    csv_jinja = CSVJinja()
    # print (f"CSVJinja options: {csv_jinja.env.trim_blocks}")
    # print (f"CSVJinja options: {csv_jinja.env.lstrip_blocks}")

    for template in args.templates:
        rendered = csv_jinja.render_template(template,csvhandler.rows())
        print(rendered)

# For testing
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main()
    else:
        test()