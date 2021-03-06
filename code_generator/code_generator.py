# -*- coding: utf-8 -*-

from os import listdir, path
import re
import string
from model_view_generator import generate_model_view
from report_view_generator import generate_report_view
from report_model_generator import generate_report_model
from model_access_generator import generate_model_access
from model_init_generator import generate_model_init
from module_manifest_generator import generate_module_manifest

ignore_model_files = ['__init__.py', 'report.py']
module_directory = '../src/banpt_report_generator'
model_directory = module_directory + '/models'
security_directory = module_directory + '/security'
view_directory = module_directory + '/views'

if __name__ == "__main__":

    # List model files

    model_files = [f[:-3] for f in listdir(model_directory) if path.isfile(path.join(model_directory, f)) and f not in ignore_model_files and f[-3:] == '.py']
    model_files.sort()
    print 'Generating views for models:'

    # Read and parse model fields, then generate model views

    title_pattern = re.compile('^\s*_title\s*=\s*["\'](.*)[\'"]\s*$')
    field_pattern = re.compile('^\s*([a-zA-Z0-9_]+) = fields\.([a-zA-Z0-9_]+)\((.*)\)\s*$')

    models = []
    for model_file in model_files:
        model_path = path.join(model_directory, model_file + '.py')
        model_fields = []
        model_title = string.capwords(model_file)

        for i, line in enumerate(open(model_path)):
            match_title = re.match(title_pattern, line)
            if match_title:
                model_title = match_title.groups()[0]
            for match in re.finditer(field_pattern, line):
                model_fields.append(match.groups())

        models.append(dict(name=model_file, title=model_title))
        print '- ' + model_file + ': ' + model_title
        
        generate_model_view(
            name=model_file,
            title=model_title,
            fields=[f[0] for f in model_fields],
            directory=view_directory
        )

    generate_report_view(models=models, directory=view_directory)
    generate_report_model(models=models, directory=model_directory)
    generate_model_access(models=models, directory=security_directory)
    generate_model_init(models=models, directory=model_directory)
    generate_module_manifest(models=models, directory=module_directory)
