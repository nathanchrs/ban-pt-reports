from odoo import models, fields, api, exceptions
   

class Rubric(models.Model):
    _name = 'itb.academic_rubric'
    
    name = fields.Char(index=True,required=True)
    code = fields.Char(index=True,required=True)
    note = fields.Text()
    active = fields.Boolean(default=True)
    criteria_ids = fields.One2many('itb.academic_rubric_criteria','rubric_id',string='Rubric Detail')
    

class Rubric_Criteria(models.Model):
    _name = 'itb.academic_rubric_criteria'
    
    name = fields.Char()
    max_score = fields.Integer()
    rubric_id = fields.Many2one('itb.academic_rubric',index=True,required=True,ondelete='cascade',string='Rubric')
    level_ids = fields.One2many('itb.academic_rubric_level','criteria_id',string='Rubric Level')
    


class Rubric_Level(models.Model):
    _name = 'itb.academic_rubric_level'
    
    name = fields.Char()
    score = fields.Integer()
    criteria_id = fields.Many2one('itb.academic_rubric_criteria',index=True,required=True,ondelete='cascade',string='Rubric Criteria')