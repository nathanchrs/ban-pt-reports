from odoo import models, fields, api, exceptions


class Instructor(models.Model):
    _name = 'itb.academic_instructor'
    _rec_name = 'partner_id'
    _order = 'start desc'
    
    role = fields.Selection([('core','Core'),('assistant','Assistant'),('guest','Guest'),('intern','Intern')])    
    course_id = fields.Many2one('itb.academic_course',index=True,required=True,ondelete='cascade',string='Course')
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    lecture_ids = fields.Many2many('itb.academic_lecture',relation='itb_academic_lecture_instructor_rel')
    semester = fields.Char(related='course_id.semester_id.name',string='Semester',store=True)
    credit = fields.Integer(related='course_id.catalog_id.credit',string='Credit',store=True)
    start = fields.Date(related='course_id.semester_id.start',string='Start',store=True)