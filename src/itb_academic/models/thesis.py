from odoo import models, fields, api, exceptions

class Thesis(models.Model):
    _name = 'itb.academic_thesis'
     
    name = fields.Char(required=True,index=True)
    note = fields.Text(index=True)
    authors = fields.Char(compute='_get_authors',readonly=True,store=True)
    supervisors = fields.Char(compute='_get_supervisors',readonly=True,store=True)
    category = fields.Selection([('skripsi','Skripsi'),('thesis','Thesis'),('disertasi','Disertasi')],default='skripsi')
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('go','On Going'),('cancel','Cancel'),('done','Done')])
    progress = fields.Float()
    start = fields.Date()
    finish = fields.Date()
    graduation = fields.Date()
    graduation_semester = fields.Many2one('itb.academic_semester',string='Semester',compute='_get_semester',readonly=True,store=True)
    grade = fields.Selection([('a','A'),('ab','AB'),('b','B'),('bc','BC'),('c','C'),('d','D'),('e','E'),('t','T')])
    active = fields.Boolean(default=True)
    structure_id = fields.Many2one('itb.academic_structure',domain="[('parent_id','=',False)]",index=True,string='Structure')        
    author_ids = fields.One2many('itb.academic_author','thesis_id',string='Authors')
    req_supervisor_ids = fields.One2many('itb.academic_req_supervisor','thesis_id',string='Requested Supervisors')
    supervisor_ids = fields.One2many('itb.academic_supervisor','thesis_id',string='Supervisors')
    meetup_ids = fields.One2many('itb.academic_meetup','thesis_id',string='Meetups')
    defence_ids = fields.One2many('itb.academic_defence','thesis_id',string='Defence')
    progress_ids = fields.One2many('itb.academic_progress','thesis_id',string='Progress')  
    
    
    @api.depends('graduation')
    def _get_semester(self): 
        for thesis in self:
            semester = self.env['itb.academic_semester'].search([('start','<=',thesis.graduation),('finish','>=',thesis.graduation)])
            semester.ensure_one()
            thesis.graduation_semester = semester.id            

    
    @api.depends('author_ids')
    def _get_authors(self):
        for thesis in self:
            authors = ', '.join(thesis.author_ids.mapped(lambda x: x.partner_id.name + ' (' + x.partner_id.student_id + ')'))
            thesis.authors = authors


    @api.depends('supervisor_ids')
    def _get_supervisors(self):
        for thesis in self:
            supervisors = thesis.mapped('supervisor_ids.partner_id.name')
            thesis.supervisors = supervisors
        

    @api.multi
    def update_default(self):
        thesis = self.search([])
        for item in thesis:
            """
            authors = ', '.join(item.author_ids.mapped(lambda x: x.partner_id.name + ' (' + x.partner_id.student_id + ')'))
            supervisors = ', '.join(item.mapped('supervisor_ids.partner_id.name'))
            item.write({'authors':authors,'supervisors':supervisors})
            """
            semester = self.env['itb.academic_semester'].search([('start','<=',item.graduation),('finish','>=',item.graduation)])
            semester.ensure_one()
            item.write({'graduation_semester':semester.id})  



class Author(models.Model):
    _name = 'itb.academic_author'
    _rec_name = 'partner_id'
    
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    sequence = fields.Integer()
    graduation_ids = fields.Many2many('itb.academic_graduation',relation='itb_academic_graduation_author',readonly=True)


class Requested_Supervisor(models.Model):
    _name = 'itb.academic_req_supervisor'
    _rec_name = 'partner_id'
    
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    sequence = fields.Integer()
    
    
class Supervisor(models.Model):
    _name = 'itb.academic_supervisor'
    _rec_name = 'partner_id'
    _order = 'start desc'
    
    partner_id = fields.Many2one('res.partner',index=True,required=True,ondelete='cascade',string='Person')
    employee_id = fields.Many2one('hr.employee',index=True,ondelete='cascade',string='Employee')
    thesis_id = fields.Many2one('itb.academic_thesis',index=True,required=True,ondelete='cascade',string='Thesis')
    role = fields.Selection([('lead','Lead'),('assistant','Assistant')],default='lead')
    sequence = fields.Integer()
    start = fields.Date(related='thesis_id.start',string='Start',store=True)
    finish = fields.Date(related='thesis_id.finish',string='Finish',store=True)
    semester = fields.Char(related='thesis_id.graduation_semester.name',store=True)