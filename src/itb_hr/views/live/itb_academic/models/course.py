from odoo import models, fields, api, exceptions


class Course(models.Model):
    _name = 'itb.academic_course'

    name = fields.Char(index=True)
    participant_amount = fields.Integer()
    grade_publish = fields.Boolean()
    catalog_id = fields.Many2one('itb.academic_catalog',index=True,required=True,string='Catalog',ondelete='cascade')
    program_id = fields.Many2one('itb.academic_program',index=True,required=True,string='Program')
    semester_id = fields.Many2one('itb.academic_semester',index=True,required=True,string='Semester',ondelete='cascade')
    instructor_ids = fields.One2many('itb.academic_instructor','course_id',string='Instructors')
    participant_ids = fields.One2many('itb.academic_participant','course_id',string='Participants')
    group_ids = fields.One2many('itb.academic_group','course_id',string='Groups')
    lecture_ids = fields.One2many('itb.academic_lecture','course_id',string='Lectures')
    attendance_ids = fields.One2many('itb.academic_attendance','course_id',string='Attendances')
