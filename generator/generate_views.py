# -*- coding: utf-8 -*-

from os import listdir, path
import re
import pprint

ignore_model_files = ['__init__.py', 'report.py']
model_directory = '../src/banpt_report_generator/models'

if __name__ == "__main__":

    pp = pprint.PrettyPrinter(indent=2)

    model_files = [f[:-3] for f in listdir(model_directory) if path.isfile(path.join(model_directory, f)) and f not in ignore_model_files and f[-3:] == '.py']
    print 'Generating views for models:'
    pp.pprint(model_files)

    field_pattern = re.compile("^\s*([a-zA-Z0-9_]+) = fields\.([a-zA-Z0-9_]+)\((.*)\)\s*$")
    model_fields = {}

    for model_file in model_files:
        model_path = path.join(model_directory, model_file + '.py')
        model_fields[model_file] = {}
        model_fields[model_file] = []
        for i, line in enumerate(open(model_path)):
            for match in re.finditer(field_pattern, line):
                model_fields[model_file].append(match.groups())

    print 'Model fields:'
    pp.pprint(model_fields)
                
