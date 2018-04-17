from odoo import models, fields, api, exceptions

class Duty(models.Model):
    _name = 'itb.hr_duty'
    
    name = fields.Char(index=True)
    start = fields.Date(index=True)
    finish = fields.Date(index=True)
    location = fields.Char()
    reference = fields.Char(index=True)
    reference_partner = fields.Char()
    note = fields.Text()
    state = fields.Selection([('draft','Draft'),('valid','Valid')], 'Status', default='draft', required=True, readonly=True, copy=False,index=True)
    employee_ids = fields.One2many('itb.hr_duty_employee','duty_id',string='Employees',index=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    
class Duty_Employee(models.Model):
    _name = 'itb.hr_duty_employee'
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee', string="Name")
    duty_id = fields.Many2one('itb.hr_duty',ondelete='cascade',required=True,index=True)
    duty = fields.Char(related='duty_id.name')
    start = fields.Date(related='duty_id.start')
    finish = fields.Date(related='duty_id.finish')
    reference = fields.Char(related='duty_id.reference')