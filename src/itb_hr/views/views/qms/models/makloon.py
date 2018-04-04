from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class makloon(models.Model):
    _name = 'qms.makloon'

    partner_id = fields.Many2one('res.partner',domain="[('role','=','vendor')]",string='Vendor',required=True)
    product_id = fields.Many2one('product.product',domain="[('vendor_ids','in',partner_id)]",string='Product',required=True)
    coa_ids = fields.One2many('qms.coa','makloon_id',string='Certificate of Analysis')
    coa = fields.Boolean()
    name = fields.Char(string='PO Ref',required=True)
    date = fields.Date(required=True)
    sku = fields.Many2one('qms.variant',domain="[('product_id','=',product_id)]",string='SKU')
    batch = fields.Char()
    quantity = fields.Integer(required=True)
    reject = fields.Integer()
    release = fields.Integer(compute='_get_release',store=True)
    quantity_mt = fields.Float(compute='_get_mt',store=True, string='Quantity (MT)')
    reject_mt = fields.Float(compute='_get_mt',store=True, string='Reject (MT)')
    release_mt = fields.Float(compute='_get_mt',store=True, string='Release (MT)')
    expire = fields.Date()
    analysis_date = fields.Date(string='Analysis Date')
    nc = fields.Integer(compute='_get_nc',store=True, string='Non-Comply')
    state = fields.Selection([('run','Run'),('hold','Hold'),('release','Release')],default='run')


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


    @api.depends('coa_ids')
    def _get_nc(self):
        for record in self:
            if record.coa_ids:
                nc = record.coa_ids.filtered(lambda x: x.comply == False)
                if nc:
                    record.nc = len(nc)


    @api.onchange('sku','date')
    def set_expire(self):
        for record in self:
            if record.date and record.sku:
                date_dt = datetime.strptime(record.date, "%Y-%m-%d")
                if record.sku.life:
                    record.expire = date_dt + relativedelta(months=+record.sku.life)


    def create_coa(self):
        self.ensure_one()
        coas = []
        parameters = self.env['qms.parameter'].search([('product_id','=',self.product_id.id),('active','=',True),('external','=',False)])
        if parameters:
            for x in parameters: 
                output = (0,0,{'source':'makloon','makloon_id': self.id,'partner_id':self.partner_id.id,'product_id':self.product_id.id,'date':self.date,'reference':self.name,'parameter_id':x.id,'result':0})
                coas.append(output)

            self.write({'coa_ids': [(2,coa.id) for coa in self.coa_ids]})  
            self.write({'coa':True,'coa_ids':coas})
