from odoo import models, fields, api, exceptions


class Catalog(models.Model):
    _name = 'itb.academic_catalog'
    
    name = fields.Char(index=True,required=True)
    name_en = fields.Char(index=True)
    fullname = fields.Char(index=True)
    fullname_en = fields.Char(index=True,string='Full Name (English)')
    code = fields.Char(index=True, required=True)
    credit = fields.Integer()
    note = fields.Text()
    note_en = fields.Text(string='Note (English)')
    syllabus = fields.Text()
    syllabus_en = fields.Text(string='Syllabus(English)')
    output = fields.Text()
    closing = fields.Char()
    grading = fields.Char()
    year = fields.Integer(index=True)
    active = fields.Boolean(default=True)   
    research_id = fields.Many2one('itb.hr_research_group',index=True,string='Research Group')
    topic_ids = fields.One2many('itb.academic_topic','catalog_id',string='Topics')
    catalog_outcome_ids = fields.One2many('itb.academic_catalog_outcome','catalog_id',string='Outcomes')
    evaluation_ids = fields.One2many('itb.academic_evaluation','catalog_id',string='Evaluations')


class Catalog_Outcome(models.Model):
    _name = 'itb.academic_catalog_outcome'
    _rec_name = 'outcome_id'
    
    intensity = fields.Selection([('low','Low'),('medium','Medium'),('high','High')],'Intensity',default='medium')
    active = fields.Boolean(default=True)
    catalog_id = fields.Many2one('itb.academic_catalog',index=True,required=True,ondelete='cascade',string='Catalog')
    outcome_id = fields.Many2one('itb.academic_outcome',index=True,required=True,ondelete='cascade',string='Outcome')
