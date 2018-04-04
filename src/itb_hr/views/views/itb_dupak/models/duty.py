from odoo import models, fields, api, exceptions

class Duty_Employee(models.Model):
    _inherit = 'itb.hr_duty_employee'

    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','=','duty')]")