from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from datetime import datetime


class res_partner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.Many2many('product.product',domain="[('purchase_ok','=',True)]",string='Products')
    certification_ids = fields.One2many('qms.certification','partner_id',string='Certifications')
    role = fields.Selection([('vendor','Vendor'),('employee','Employee'),('contact','Contact')], default='contact', required=True)
    vendor = fields.Selection([('material','Material'),('makloon','Makloon'),('importer','Importer')], default='material')
    auditor = fields.Selection([('none','None'),('junior','Junior'),('senior','Senior')], default='none')
    dummy = fields.Text()





class certification(models.Model):
    _name = 'qms.certification'
    _rec_name = 'partner_id'
    
    partner_id = fields.Many2one('res.partner',string='Vendor')
    organization = fields.Char(required=True)
    reference = fields.Char(required=True)
    lppom_reference = fields.Char(string='LPPOM Ref')
    lppom_date = fields.Date(string='LPPOM Decision')
    start = fields.Date()
    finish = fields.Date()


    @api.constrains('start','finish')
    def _check_period(self):
        for record in self:
            if record.start and record.finish:
                from_dt = datetime.strptime(record.start, "%Y-%m-%d")
                to_dt = datetime.strptime(record.finish, "%Y-%m-%d")

                if to_dt < from_dt:
                     raise ValidationError("Certificate finish date must be grater than start")
