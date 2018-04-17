from odoo import models, fields, api, exceptions

class Attendance(models.Model):
    _name = 'itb.academic_attendance'
    
    session = fields.Integer()
    attend =  fields.Selection([('attend','Attend'),('absent','Absent'),('sick','Sick'),('permit','Permit')])   
    lecture_id = fields.Many2one('itb.academic_lecture',index=True,required=True,string='Lecture')
    day = fields.Datetime(related='lecture_id.start')
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')