from odoo import models, fields, api, exceptions

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    counselor_ids = fields.One2many('itb.academic_counselor','employee_id',string='Counselor')
    instructor_ids = fields.One2many('itb.academic_instructor','employee_id',string='Teaching')
    supervisor_ids = fields.One2many('itb.academic_supervisor','employee_id',string='Supervisor')
    performance_ids = fields.One2many('itb.academic_performance','employee_id',string='Performance')
