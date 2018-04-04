from odoo import  models, fields, api, exceptions

class Participant_Group_Wizard(models.TransientModel):
    _name = 'itb.academic_participant_group_wizard'

    group_ids = fields.Many2many('itb.academic_group',relation="participant_group_wizard_rel")
    
    
    @api.multi
    def subscribe(self):
        if not(self.group_ids):
            raise exceptions.ValidationError('No Group selected!')
        
        ids = self.env.context.get('active_ids',[])
        participants = self.env['itb.academic_participant'].search([('id','in',ids)])
        for participant in participants:
            participant.group_ids |= self.group_ids
        
        return {}