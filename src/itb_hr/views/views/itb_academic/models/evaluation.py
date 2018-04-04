from odoo import models, fields, api, exceptions
   

class Evaluation(models.Model):
    _name = 'itb.academic_evaluation'
    
    name = fields.Char(index=True,required=True)
    type = fields.Selection([('mid','Mid Exam'),('final','Final Exam'),('group','Group Assignment'),('personal','Personal Assignment'),('quiz','Quiz'),('exercise','Exercise')],'Evaluation Type',default='group')
    when = fields.Selection([('at','At'),('before','Before'),('after','After')],'When',default='at')
    topic_id = fields.Many2one('itb.academic_topic',index=True,required=True,string='Topic')
    catalog_id = fields.Many2one('itb.academic_catalog',index=True,required=True,string='Catalog')    
