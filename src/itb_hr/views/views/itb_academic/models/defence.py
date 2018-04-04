from odoo import models, fields, api, exceptions


class Defence(models.Model):
    _name = 'itb.academic_defence' 
    _rec_name = 'thesis_id'
    
    start = fields.Datetime()
    finish = fields.Datetime()
    location = fields.Char()
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    tester_ids = fields.One2many('itb.academic_tester','defence_id',string='Testers')

 
class Tester(models.Model):
    _name = 'itb.academic_tester'
    _rec_name = 'partner_id'
    
    defence_id = fields.Many2one('itb.academic_defence',index=True,required=True,ondelete='cascade',string='Defence')
    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    sequence = fields.Integer()
    role = fields.Selection([('lead','Lead'),('assistant','Assistant')],default='lead')
