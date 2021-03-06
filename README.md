# csv_utils

`csv_utils` are a suite of CSV modules for working with csv (delimited) files.

## Utilities
Current list of modules includes...

#### CSVHandler
Allows for loading a csv file, and provides functions for updating 1..n rows.

*Example(s)*

{{insert examples here}

#### CSVJinjaView
This utility allows you to create templated files from a CSV.  The utility uses the Jinja template engine.  Click [here](https://jinja.palletsprojects.com/en/2.10.x/) for more details on how to create Jinja templates.

*Example(s)*

```bash
python3 csv_utils/csv_jinja.py -c /tmp/example.csv-t templates/patient-resource-delete.j2
```

## Installing
With git:
```bash
git clone https://github.com/dmorand17/csv_utils
cd csv_utils
virtualenv venv OR mkvirtualenv <env>
source venv/bin/activate OR workon <env>
pip install -r requirements.txt
```

With pip (_not yet implemented_):
```bash
pip install csv_utils
```

### Install locally to use module
```bash
pip install -e .
```