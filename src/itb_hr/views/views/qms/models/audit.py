from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class audit(models.Model):
    _name = 'qms.audit'
    _rec_name = 'partner_id'
    
    reference = fields.Char()
    partner_id = fields.Many2one('res.partner',domain="[('role','=','vendor')]",string='Vendor',required=True)
    date = fields.Date(required=True)
    allow_closing = fields.Boolean()
    closing_date = fields.Date()
    score = fields.Float()
    grade = fields.Char(compute='_set_grade',store=True)
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('run','Run'),('close','Close')],default='draft')
    auditor_ids = fields.Many2many('res.partner',string='Auditors', domain="[('role','=','employee')]")
    auditee_ids = fields.One2many('qms.auditee','audit_id',string='Auditees')
    capa_ids = fields.One2many('qms.capa','audit_id',string='CAPA')
    positive = fields.Text(string='Positive Points')
    special = fields.Boolean()


    @api.depends('score')
    def _set_grade(self):
        for record in self:
            if record.score < 10:
                record.grade = 'E'
            elif record.score >= 10 and record.score < 31:
                record.grade = 'D'
            elif record.score >=31 and record.score < 51:
                record.grade = 'C'
            elif record.score >=51 and record.score < 81:
                record.grade = 'B'
            elif record.score >=81:
                record.grade = 'A'
                
                
                
            
class auditee(models.Model):
    _name = 'qms.auditee'
    _rec_name = 'auditee'
    _sql_constraints = [ 
        ('auditee_uniq', 
         'UNIQUE (audit_id, auditee)', 
         'Auditee can not duplicate!')]
    
    audit_id = fields.Many2one('qms.audit',string='Audit')
    auditee = fields.Many2one('res.partner',string='Auditee',domain="[('role','=','contact')]")