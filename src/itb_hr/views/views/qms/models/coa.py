from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime



class coa(models.Model):
    _name = 'qms.coa'
    _rec_name = 'parameter_id'

    source = fields.Char()
    makloon_id = fields.Many2one('qms.makloon', string='Makloon')
    production_id = fields.Many2one('qms.production', string='Production')
    product_id = fields.Many2one('product.product',domain="[('sale_ok','=',True)]",string='Product',index=True)
    partner_id = fields.Many2one('res.partner',string='Partner',index=True)
    date = fields.Date()
    reference = fields.Char()
    parameter_id = fields.Many2one('qms.parameter',string='Parameter',index=True,required=True)
    specification = fields.Char(related='parameter_id.specification',store=True)
    result = fields.Float(required=True,group_operator="avg")
    comply = fields.Boolean(compute='_set_comply',store=True,default=False)


    @api.depends('result')
    def _set_comply(self):
        for record in self:
            if record.result >= record.parameter_id.min and record.result <= record.parameter_id.max:
                record.comply = True


    @api.model
    def create(self, vals):
        if 'production_id' in vals and vals['production_id']:            
            vals['source'] = 'production'
            production = self.env['qms.production'].browse([vals['production_id']])
            vals['product_id'] = production.product_id.id
            vals['date'] = str(production.date)
            vals['reference'] = production.name
        
        if 'makloon_id' in vals and vals['makloon_id']:
            vals['source'] = 'makloon'
            makloon = self.env['qms.makloon'].browse([vals['makloon_id']])
            vals['partner_id'] = makloon.partner_id.id
            vals['product_id'] = makloon.product_id.id
            vals['date'] = str(makloon.date)
            vals['reference'] = makloon.name

        new_record = super(coa, self).create(vals)
        return new_record



class parameter(models.Model):
    _name = 'qms.parameter'
    _sql_constraints = [ 
        ('parameter_uniq', 
         'UNIQUE (name,product_id)', 
         'Parameter of product can not duplicate!')]

    product_id = fields.Many2one('product.product',string='Product')
    name = fields.Char(required=True)
    min = fields.Float(required=True)
    max = fields.Float(required=True)
    specification = fields.Char(required=True)
    active = fields.Boolean(default=True)
    external = fields.Boolean()


    @api.constrains('max','min')
    def _validate_max(self):
        for record in self:
            if record.min and record.max:
                if record.max < record.min:
                     raise ValidationError("Max must be greater than Min")