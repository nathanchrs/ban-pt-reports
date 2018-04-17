from odoo import models, fields, api, exceptions

class Employment(models.Model):
    _name = 'itb.hr_employment'
    
    name = fields.Selection([('bhmn','BHMN'),('calon bhmn','Calon BHMN'),('pns','PNS'),('cpns','CPNS'),('prajabatan','Prajabatan'),('kontrak','Kontrak')],default="bhmn")
    reference = fields.Char()
    signed_by = fields.Char()
    start = fields.Date()
    finish = fields.Date()
    decision = fields.Date()
    employee_id = fields.Many2one('hr.employee', string='Employee')
    research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)
