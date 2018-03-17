# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""# -*- coding: utf-8 -*-

# Python package definition file
# Import all model classes here

from . import report

${model_imports}
""")

model_import_template = string.Template("from . import ${model_name}")


def generate_model_init(models, directory):
    model_imports = []
    for model in models:
        model_imports.append(model_import_template.substitute(
            dict(model_name=model['name'])))

    view_template_params = dict(
        model_imports=string.join(model_imports, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, '__init__.py')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
