from odoo import models, fields, api, exceptions



class Curriculum(models.Model):
    _name = 'itb.academic_curriculum'
    
    name = fields.Char(index=True,required=True)
    program_id = fields.Many2one('itb.academic_program',index=True,required=True,string='Program')
    year = fields.Integer(index=True)
    curriculum_line_ids = fields.One2many('itb.academic_curriculum_line','curriculum_id',string='Catalogs')


class Curriculum_Line(models.Model):
    _name = 'itb.academic_curriculum_line'
    _rec_name = 'catalog_id'

    curriculum_id = fields.Many2one('itb.academic_curriculum',index=True,required=True,string='Curriculum',ondelete='cascade')
    catalog_id = fields.Many2one('itb.academic_catalog',index=True,required=True,string='Catalog',ondelete='cascade')
    concentration = fields.Char()
    semester = fields.Integer(index=True)
    code = fields.Char(related='catalog_id.code',readonly=True)
    year = fields.Integer(related='catalog_id.year',readonly=True)
    credit = fields.Integer(related='catalog_id.credit',readonly=True)
    category = fields.Selection([('wajib','wajib'),('opsional', 'opsional'),('opsional-luar','opsional-luar'),('opsional-external','opsional-external')], 'Category',default='wajib')
    category2 = fields.Selection([(1,'Mata kuliah reguler'),(2, 'Mata kuliah TA/KP')], 'Category2',default=1)