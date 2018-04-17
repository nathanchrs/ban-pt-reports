from odoo import models, fields, api, exceptions

class Participant(models.Model):
    _name = 'itb.academic_participant'
    _rec_name = 'partner_id'
    
    grade = fields.Selection([('a','A'),('ab','AB'),('b','B'),('bc','BC'),('c','C'),('d','D'),('e','E'),('f','F'),('p','P'),('t','T')])
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')
    group_ids = fields.Many2many('itb.academic_group',relation='itb_academic_participant_group_rel')    
    is_guest = fields.Boolean()
    is_transript = fields.Boolean()
    
    
class Participant_Group(models.Model):
    _name = 'itb.academic_group'

    name = fields.Char(index=True,required=True)
    schedule = fields.Char()
    quota = fields.Integer()
    amount = fields.Integer()
    partner_id = fields.Many2one('res.partner',index=True,string='Instructor')
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')
    participant_ids = fields.Many2many('itb.academic_participant',relation='itb_academic_participant_group_rel')