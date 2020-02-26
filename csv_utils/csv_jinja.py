import jinja2
import os
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

    def render_template(self, template_name, csv, **kwargs):
        # print("csv type {}".format(type(csv)))
        return self.env.get_template(template_name,globals=kwargs.get('template_globals')).render(rows=csv, **kwargs)

    def render_template_to_list(self, template_name, csv, fieldnames, rowkey, **kwargs):
        # print("csv type {}".format(type(csv)))
        # print(csv)
        template = self.env.get_template(template_name,globals=kwargs.get('template_globals'))
        # [print(row) for row in csv]

        return [dict(key=rowkey(row), template=template.render(rows=[row], fieldnames=fieldnames, **kwargs)) for row in csv]

# For testing
if __name__ == '__main__':
    csvhandler = CSVHandler('samples/sample-input.csv')

    csv_jinja = CSVJinja()
    rendered = csv_jinja.render_template("samples/sample-csvrows.j2",csvhandler.rows())
    print(rendered)

    key = lambda r: '-'.join([r[key] for key in ["name","gender"]])
    rendered = csv_jinja.render_template_to_list("samples/sample.j2",csvhandler.rows(),csvhandler.headers(),rowkey=key)
    print(rendered)