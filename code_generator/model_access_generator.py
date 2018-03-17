# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink

report_manager_report,report.report_manager,model_banpt_report_generator_report,report_manager,1,1,1,1
report_viewer_report,report.report_viewer,model_banpt_report_generator_report,report_viewer,1,0,0,0

${model_accesses}
""")

model_access_template = string.Template(
"""report_manager_${model_name},${model_name}.report_manager,model_banpt_report_generator_${model_name},report_manager,1,1,1,1
report_viewer_${model_name},${model_name}.report_viewer,model_banpt_report_generator_${model_name},report_viewer,1,0,0,0"""
)

def generate_model_access(models, directory):
    model_accesses = []
    for model in models:
        model_accesses.append(model_access_template.substitute(dict(model_name=model['name'])))

    view_template_params = dict(
        model_accesses=string.join(model_accesses, '\n\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, 'ir.model.access.csv')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
