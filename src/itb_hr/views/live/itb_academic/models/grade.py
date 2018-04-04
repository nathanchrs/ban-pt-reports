from odoo import models, fields, api, exceptions


class Grade(models.Model):
    _name = 'itb.academic_grade'
    _rec_name = 'partner_id'
    
    grade = fields.Selection([('a','A'),('ab','AB'),('b','B'),('bc','BC'),('c','C'),('d','D'),('e','E'),('t','T')])
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')
