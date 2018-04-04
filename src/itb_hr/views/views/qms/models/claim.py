from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class claim(models.Model):
    _name = 'qms.claim'

    type = fields.Selection([('internal','Internal'),('external','External')],default='external')
    site_id = fields.Many2one('qms.site',string='Issued By')
    internal_to = fields.Many2many('qms.unit',string='Sent To')
    external_to = fields.Many2one('res.partner',domain="[('role','=','vendor')]",string='Sent To')
    actor = fields.Char()
    external_pic = fields.Many2one('res.partner',domain="[('role','=','contact'),('parent_id','=',external_to)]",string='Attention')
    internal_pic = fields.Many2one('res.partner',domain="[('role','=','employee')]",string='Attention')
    date = fields.Date(default=fields.Date.today(),string='Reported')
    reference = fields.Char()
    urgency = fields.Selection([('very-serious','Very Serious'),('serious','Serious'),('for-attention','For Attention')],default='serious')
    effect_ids = fields.Many2many('qms.effect',string='Effect')
    name = fields.Char(required=True)
    occurance = fields.Date(required=True)
    location = fields.Char()
    request = fields.Text()
    state = fields.Selection([('open','Open'),('close','Close')],default='open')
    capa_ids = fields.One2many('qms.capa','claim_id',string='CAPA')
    

    @api.constrains('occurance')
    def _validate_occurance_date(self):
        for record in self:
            if record.date and record.occurance:
                date_dt = datetime.strptime(record.date, "%Y-%m-%d")
                occurance_dt = datetime.strptime(record.occurance, "%Y-%m-%d")

                if date_dt < occurance_dt:
                     raise ValidationError("You cant report future occurance date")



class effect(models.Model):
    _name = 'qms.effect'

    name = fields.Char()
    claim_ids = fields.Many2many('qms.claim',string='Claims')



class unit(models.Model):
    _name = 'qms.unit'

    name = fields.Char()
    claim_ids = fields.Many2many('qms.claim',string='Claims')