# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class product(models.Model):
    _inherit = 'product.product'

    manufacturer_id = fields.Many2one('res.partner',domain="[('role','=','vendor')]",string='Manufacturer')
    vendor_ids = fields.Many2many('res.partner',domain="[('role','=','vendor')]",string='Vendors')
    material_ids = fields.One2many('qms.materials','product_id',string='Materials')
    site_id = fields.Many2one('qms.site',string='Produced in')
    variant_ids = fields.One2many('qms.variant','product_id',string='Variants')



class variant(models.Model):
    _name = 'qms.variant'

    product_id = fields.Many2one('product.product',string='Product')
    name = fields.Char(string='SKU',required=True)
    conversion = fields.Float(required=True,string='CTN to MT')
    life = fields.Integer(required=True,string='Shelf Life')



class materials(models.Model):
    _name = 'qms.materials'
    _rec_name = 'material_id'
    _sql_constraints = [ 
        ('material_uniq', 
         'UNIQUE (product_id, material_id,partner_id)', 
         'Material must be unique!')] 

    product_id = fields.Many2one('product.product',string='Product',required=True)
    partner_id = fields.Many2one('res.partner',domain="[('role','=','vendor')]",string='Vendor',required=True)
    material_id = fields.Many2one('product.product',string='Material',required=True, domain="[('id','!=',product_id)]")
    quantity = fields.Selection([('major','major'),('minor','minor'),('moderate','moderate')],default='minor',index=True)
    critical = fields.Boolean(default=False,index=True)


class site(models.Model):
    _name = 'qms.site'

    name = fields.Char(required=True)