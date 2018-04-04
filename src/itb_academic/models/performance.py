from odoo import models, fields, api, exceptions

class Performance(models.Model):
    _name = 'itb.academic_performance'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    course_id = fields.Many2one('itb.academic_course',index=True,ondelete='cascade',string='Course')
    group = fields.Char()
    respondents = fields.Integer()
    participants = fields.Integer()
    q1 = fields.Float()
    q2 = fields.Float()
    q3 = fields.Float()
    q4 = fields.Float()
    q5 = fields.Float()
    q6 = fields.Float()
    q7 = fields.Float()
    q8 = fields.Float()
    q9 = fields.Float()
    q10 = fields.Float()
    q11 = fields.Float()