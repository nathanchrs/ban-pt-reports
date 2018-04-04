from odoo import models, fields, api, exceptions


class Program(models.Model):
    _name = 'itb.academic_program'
    
    name = fields.Char(index=True,required=True)
    name_en = fields.Char(index=True, required=True, string="Name (Eglish)")
    prefix = fields.Char()
    degree = fields.Selection([('d3','Diploma'),('s1','Undergraduate'),('s2','Master'),('s3','Doctoral'),('non','Non Degree')],'Degree',default='s1')
    active = fields.Boolean(default=True)
    outcome_ids = fields.Many2many('itb.academic_outcome',relation='itb_academic_program_outcome_rel',string='Outcomes')    
    curriculum_ids = fields.One2many('itb.academic_curriculum','program_id',string='Curriculum')