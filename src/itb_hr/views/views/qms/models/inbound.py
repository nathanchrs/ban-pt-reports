from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class inbound(models.Model):
    _name = 'qms.inbound'

    partner_id = fields.Many2one('res.partner',string='Vendor',domain="[('role','=','vendor')]")
    product_id = fields.Many2one('product.product',domain="[('vendor_ids','in',partner_id)]",string='Product')
    sku = fields.Many2one('qms.variant',domain="[('product_id','=',product_id)]",string='SKU')
    name = fields.Char(string='PO/BL Ref',required=True)
    receipt = fields.Date()
    eta = fields.Date(string='ETA',required=True)
    ata = fields.Date(string='ATA')
    temperature = fields.Float()
    quantity = fields.Integer(required=True)
    reject = fields.Integer()
    release = fields.Integer(compute='_get_release',store=True)
    quantity_mt = fields.Float(compute='_get_mt',store=True, string='Quantity (MT)')
    reject_mt = fields.Float(compute='_get_mt',store=True, string='Reject (MT)')
    release_mt = fields.Float(compute='_get_mt',store=True, string='Release (MT)')
    state = fields.Selection([('run','Run'),('hold','Hold'),('release','Release')],default='run')
    expire = fields.Date(required=True)
    latency = fields.Integer(compute='_get_latency',store=True, string='Latency(Day)')


    @api.depends('eta','ata')
    def _get_latency(self):
        for record in self:
            if record.eta and record.ata:
                eta_dt = datetime.strptime(record.eta, "%Y-%m-%d")
                ata_dt = datetime.strptime(record.ata, "%Y-%m-%d")
                if ata_dt > eta_dt:
                    latency = ata_dt - eta_dt
                    record.latency = latency.days

    
    @api.depends('quantity','reject')
    def _get_release(self):
        for record in self:
            if record.reject:
                record.release = record.quantity - record.reject
            else:
                record.release = record.quantity


    @api.depends('quantity','reject','release','sku')
    def _get_mt(self):
        for record in self:
            if record.sku.conversion:
                if record.quantity:
                    record.quantity_mt = record.sku.conversion * record.quantity
                if record.reject:
                    record.reject_mt = record.sku.conversion * record.reject
                if record.release:
                    record.release_mt = record.sku.conversion * record.release