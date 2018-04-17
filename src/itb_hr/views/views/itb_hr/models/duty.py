from odoo import models, fields, api, exceptions

class Duty(models.Model):
    _name = 'itb.hr_duty'
    
    name = fields.Char(index=True)
    start = fields.Date(index=True)
    finish = fields.Date(index=True)
    location = fields.Char()
    reference = fields.Char(index=True)
    reference_partner = fields.Char()
    source = fields.Char()
    note = fields.Text()
    is_foreign = fields.Boolean()
    state = fields.Selection([('draft','Draft'),('valid','Valid')], 'Status', default='draft', required=True, readonly=True, copy=False,index=True)
    employee_ids = fields.One2many('itb.hr_duty_employee','duty_id',string='Employees',index=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    employee_name = fields.Char(compute='get_name', string='Employee Name',store=True, readonly=True)
    
    @api.multi
    def action_state_draft(self):
        self.state = 'draft'

    @api.multi
    def action_state_valid(self):
        self.state = 'valid'

    @api.multi
    def get_name(self):
        name=self.employee_ids.employee_id.mapped('name')
        self.employee_name = ','.join(name)

    @api.multi
    def get_allname(self):
        duty = self.env['itb.hr_duty'].search([])
        for rec in duty:
            duty_emp = self.env['itb.hr_duty_employee'].search([('duty_id.id','=',rec.id)])
            jum=0
            for dat in duty_emp:
                if dat.name_emp:
                    if jum == 0 :
                        nama = str(dat.name_emp)
                    else:
                        nama = str(nama) + ',' + str(dat.name_emp)
                    jum += 1
            rec.write({'employee_name' : nama,})

            
class Duty_Employee(models.Model):
    _name = 'itb.hr_duty_employee'
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee', string="Name")
    duty_id = fields.Many2one('itb.hr_duty',ondelete='cascade',required=True,index=True)
    duty = fields.Char(related='duty_id.name')
    start = fields.Date(related='duty_id.start')
    finish = fields.Date(related='duty_id.finish')
    reference = fields.Char(related='duty_id.reference')
    source = fields.Char(related='duty_id.source')
    research_group = fields.Char(related='employee_id.research_group_id.name', string='Research Group', store=True)
    name_emp = fields.Char(related='employee_id.name', string='Employee Name', store=True)