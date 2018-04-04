from odoo import models, fields, api, exceptions


class Offering(models.Model):
    _name = 'itb.academic_offering'
    
    name = fields.Char(index=True)
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')])
    semester_id = fields.Many2one('itb.academic_semester',index=True,required=True,string='Semester')
    program_id = fields.Many2one('itb.academic_program',index=True,required=True,string='Program')
    catalog_ids = fields.Many2many('itb.academic_catalog',relation='itb_academic_offering_catalog_rel',string='Catalog')