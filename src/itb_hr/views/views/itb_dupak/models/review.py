from odoo import models, fields, api, exceptions


class Review(models.Model):
	_name = 'itb.dupak_review'
	
	total_score = fields.Float()
	note = fields.Text()
	employee_id = fields.Many2one('hr.employee', string="Name",required=True,index=True)
	dupak_id = fields.Many2one('itb.dupak',ondelete='cascade',required=True,index=True)



class Review_Line(models.Model):
    _name = 'itb.dupak_review_line'

    review_id = fields.Many2one('itb.dupak_review', string="Review",required=True,index=True)
    dupak_line_id = fields.Many2one('itb.dupak_line', string="DUPAK Line",required=True,index=True)
    score = fields.Float()