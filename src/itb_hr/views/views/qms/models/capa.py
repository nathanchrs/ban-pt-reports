from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class capa(models.Model):
    _name = 'qms.capa'
    _STATES = [
    ('draft', 'Draft'),
    ('analysis', 'Analysis'),
    ('pending', 'Action Plan'),
    ('open', 'In Progress'),
    ('done', 'Closed'),
    ('cancel', 'Cancelled'),]
    
    name = fields.Char(required=True)
    problem = fields.Text()
    problem_date = fields.Date(string='Occurance')
    problem_by = fields.Many2one('res.partner',domain="[('role','in',['contact','employee'])]",string='Reported By')
    cause = fields.Text()
    action = fields.Text()
    action_date = fields.Date()
    action_by = fields.Many2one('res.partner',domain="[('role','in',['contact','employee'])]",string='Responsible')
    close = fields.Boolean()
    verified = fields.Boolean()
    verification = fields.Text()
    verified_by = fields.Many2one('res.partner',string='Verified By',domain="[('role','=','employee')]")
    state = fields.Selection(_STATES,'State',readonly=True,default="draft")
    source = fields.Char()
    audit_id = fields.Many2one('qms.audit',string='Related Audit')
    claim_id = fields.Many2one('qms.claim',string='Related Claim')
    assesment_id = fields.Many2one('qms.assesment',string='Related Assesment')
    committee_id = fields.Many2one('qms.committee',string='Related Committee')


    @api.model
    def create(self, vals):
        if 'claim_id' in vals and vals['claim_id']:            
            vals['source'] = 'claim'
            claim = self.env['qms.claim'].browse([vals['claim_id']])
            vals['problem_date'] = str(claim.occurance)
        
        if 'audit_id' in vals and vals['audit_id']:
            vals['source'] = 'audit'
            audit = self.env['qms.audit'].browse([vals['audit_id']])
            vals['problem_date'] = str(audit.date)

        if 'assesment_id' in vals and vals['assesment_id']:
            vals['source'] = 'assesment'
            assesment = self.env['qms.assesment'].browse([vals['assesment_id']])
            vals['problem_date'] = str(assesment.date)

        if 'committee_id' in vals and vals['committee_id']:
            vals['source'] = 'committee'
            committee = self.env['qms.committee'].browse([vals['committee_id']])
            vals['problem_date'] = str(committee.date)

        new_record = super(capa, self).create(vals)
        return new_record


    @api.constrains('action_date')
    def _validate_action_date(self):
        for record in self:
            if record.problem_date and record.action_date:
                action_dt = datetime.strptime(record.action_date, "%Y-%m-%d")
                problem_dt = datetime.strptime(record.problem_date, "%Y-%m-%d")

                if action_dt < problem_dt:
                     raise ValidationError("Action can not happen before problem")
