from odoo import models, fields, api, exceptions

class Meetup(models.Model):
    _name = 'itb.academic_meetup'
    _rec_name = 'thesis_id'
    
    day = fields.Date()
    location = fields.Char()
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    discussion_ids = fields.One2many('itb.academic_discussion','meetup_id',string='Discussions')
     
     
class Discussion(models.Model):
    _name = 'itb.academic_discussion' 
    _rec_name = 'structure_id'
    
    meetup_id = fields.Many2one('itb.academic_meetup',index=True,required=True,ondelete='cascade',string='Meetup')        
    structure_id = fields.Many2one('itb.academic_structure',index=True,required=True,string='Deliverable')        
    progress = fields.Float()
    note = fields.Text()


class Progress(models.Model):
    _name = 'itb.academic_progress'
    _rec_name = 'structure_id'

    structure_id = fields.Many2one('itb.academic_structure',index=True,required=True,string='Deliverable')        
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    progress = fields.Float()