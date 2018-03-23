# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""# -*- coding: utf-8 -*-
# pylint: skip-file

# Odoo module definition file for BAN-PT Report Generator.

{
    # Module metadata
    'name': "BAN-PT Report Generator",
    'version': '1.0',
    'author': "I01K01",
    'category': 'BAN-PT',
    'application': True,
    'description': 'BAN-PT accreditation report generator for STEI ITB',

    # List of module dependencies of this module.
    'depends': ['base', 'web', 'itb_academic', 'itb_hr'],

    # Data files always loaded at installation.
    # Add all non-Python files required by this module here.
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # Add view files here
        'views/report_views.xml',

${view_files}

        # This line must be last (after all other view files)
        'views/banpt_report_generator.xml'
    ],

    # Data files containing optionally loaded demonstration data.
    'demo': []
}
""")

view_file_template = string.Template("        'views/${model_name}_views.xml',")


def generate_module_manifest(models, directory):
    view_files = []
    for model in models:
        view_files.append(view_file_template.substitute(
            dict(model_name=model['name'])))

    view_template_params = dict(
        view_files=string.join(view_files, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, '__manifest__.py')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
