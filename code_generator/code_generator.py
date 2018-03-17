# -*- coding: utf-8 -*-

from os import listdir, path
import re
import pprint
import string
from model_view_generator import generate_model_view

ignore_model_files = ['__init__.py', 'report.py']
model_directory = '../src/banpt_report_generator/models'
generated_model_views_directory = './generated/model_views'

if __name__ == "__main__":

    pp = pprint.PrettyPrinter(indent=2)

    # List model files

    model_files = [f[:-3] for f in listdir(model_directory) if path.isfile(path.join(model_directory, f)) and f not in ignore_model_files and f[-3:] == '.py']
    print 'Generating views for models:'
    pp.pprint(model_files)

    # Read and parse model fields, then generate model views

    field_pattern = re.compile("^\s*([a-zA-Z0-9_]+) = fields\.([a-zA-Z0-9_]+)\((.*)\)\s*$")

    for model_file in model_files:
        model_path = path.join(model_directory, model_file + '.py')
        model_fields = []

        for i, line in enumerate(open(model_path)):
            for match in re.finditer(field_pattern, line):
                model_fields.append(match.groups())
        
        generate_model_view(
            name=model_file,
            title=string.capwords(model_file),
            fields=[f[0] for f in model_fields],
            directory=generated_model_views_directory
        )

