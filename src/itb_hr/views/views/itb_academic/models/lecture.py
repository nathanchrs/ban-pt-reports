from odoo import models, fields, api, exceptions

class Lecture(models.Model):
    _name = 'itb.academic_lecture'
    
    name = fields.Char()
    start = fields.Datetime(required=True)
    finish = fields.Datetime(required=True)
    location = fields.Char()
    session = fields.Integer()
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')
    group_id = fields.Many2one('itb.academic_group',index=True,required=True,ondelete='cascade',string='Group')
    topic_id = fields.Many2one('itb.academic_topic',string='Topic')
    instructor_ids = fields.Many2many('itb.academic_instructor',relation='itb_academic_lecture_instructor_rel')