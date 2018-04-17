from odoo import models, fields, api, exceptions



class Semester(models.Model):
    _name = 'itb.academic_semester'
    
    name = fields.Char(index=True)
    type = fields.Selection([('even','Even'),('odd','Odd'),('short','Short')])
    year = fields.Integer()
    start = fields.Date(required=True)
    finish = fields.Date(required=True)
