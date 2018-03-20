# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review') 
    year = fields.Selection(string='Tahun', required=True, selection=[(year, str(year)) for year in range(2010, 2050)])
    prodi = fields.Char(string='Prodi', required=True)
    description = fields.Text(string='Keterangan')

    refresh_date = fields.Datetime(string='Waktu pemutakhiran terakhir', default=fields.datetime.now())

${one2many_fields}

    @api.multi
    def write(self, values, ignore_state_change=False):
        # Set state to 'pending_review' if object is edited
        values['state'] = 'pending_review'
        return super(Report, self).write(values)

    @api.one
    def approve(self):
        # Set state to 'approved'; bypass edit object check
        super(Report, self).write({'state': 'approved'})

    @api.one
    def refresh(self):

        # TODO: generate reports here based on year and prodi

        self.write({'refresh_date': fields.datetime.now()})
""")

one2many_field_template = string.Template(
"    ${model_name} = fields.One2many(comodel_name='banpt_report_generator.${model_name}', inverse_name='report')"
)

def generate_report_model(models, directory):
    one2many_fields = []
    for model in models:
        model_params = dict(model_name=model['name'])
        one2many_fields.append(one2many_field_template.substitute(model_params))

    view_template_params = dict(
        one2many_fields=string.join(one2many_fields, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, 'report.py')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
