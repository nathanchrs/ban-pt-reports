from odoo import models, fields, api, exceptions


class Counselor(models.Model):
    _name = 'itb.academic_counselor'
    _rec_name = 'partner_id'
    _order = 'semester_id desc,student_id'

    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Student')
    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    semester_id = fields.Many2one('itb.academic_semester',index=True,ondelete='cascade',string='Semester')
    semester = fields.Char(related='semester_id.name',string='Semester',store=True)
    student_id = fields.Char(related='partner_id.student_id',string='Student ID',store=True)