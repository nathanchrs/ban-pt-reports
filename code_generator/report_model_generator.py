# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""# -*- coding: utf-8 -*-

from odoo import models, fields, api
${refresh_imports}

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review')
    year = fields.Selection(string='Tahun', required=True, selection=[(year, str(year)) for year in range(2010, 2050)])
    prodi = fields.Many2one(string='Prodi', required=True, comodel_name='itb.academic_program')
    description = fields.Text(string='Keterangan')

    refresh_date = fields.Datetime(string='Waktu pemutakhiran terakhir', default=fields.datetime.now())

${one2many_fields}

    @api.multi
    def write(self, values):
        "Set state to 'pending_review' if object is edited"
        values['state'] = 'pending_review'
        return super(Report, self).write(values)

    @api.multi
    def approve(self):
        "Set state to 'approved'; bypass edit object check"
        super(Report, self).write({'state': 'approved'})

    @api.multi
    def refresh(self):
        "Load or refresh report data from iBOS, then update the refresh_date"

${refresh_calls}

        self.write({'refresh_date': fields.datetime.now()})
""")

refresh_import_template = string.Template("from . import ${model_name}")
one2many_field_template = string.Template(
"    ${model_name} = fields.One2many(comodel_name='banpt_report_generator.${model_name}', inverse_name='report')"
)
refresh_call_template = string.Template(
"        ${model_name}.refresh(self)"
)

def generate_report_model(models, directory):
    refresh_imports = []
    one2many_fields = []
    refresh_calls = []
    for model in models:
        model_params = dict(model_name=model['name'])
        refresh_imports.append(refresh_import_template.substitute(model_params))
        one2many_fields.append(one2many_field_template.substitute(model_params))
        refresh_calls.append(refresh_call_template.substitute(model_params))

    view_template_params = dict(
        refresh_imports=string.join(refresh_imports, '\n'),
        one2many_fields=string.join(one2many_fields, '\n'),
        refresh_calls=string.join(refresh_calls, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, 'report.py')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
