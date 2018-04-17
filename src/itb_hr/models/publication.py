from odoo import models, fields, api, exceptions,workflow
from lxml import etree

class Publication(models.Model):
	_name = 'itb.hr_publication'
	_inherit = ['ir.needaction_mixin']
	
	name = fields.Char()
	day = fields.Date(string='Date')
	authors = fields.Char()
	authors_count = fields.Integer(default=1)
	publisher = fields.Char()
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('review','Reviewed'),('validate','Validated')], 'Status', default='draft', required=True, readonly=True, copy=False)
	media_id =  fields.Many2one('itb.hr_publication_media', string='Type')
	category_id = fields.Many2one('itb.hr_publication_category', string='Category')
	max_score = fields.Float('Max. Score',related='category_id.score')
	scopus = fields.Char()
	url_web = fields.Char()
	area = fields.Char(compute='_get_area',store=True)
	author_ids = fields.One2many('itb.hr_publication_author','publication_id',string='Authors')
	review_ids = fields.One2many('itb.hr_publication_review','publication_id',string='Reviews')
	
	@api.constrains('author_ids')
	def _check_author(self):
		for publication in self:
			authors = publication.author_ids.filtered(lambda x: x.role == 'author')    
			if len(authors) > 1:
				raise models.ValidationError('only 1 person allowed in author role')
	
	@api.constrains('authors_count')
	def _check_author_count(self):
		for publication in self:    
			if not (publication.authors_count > 0):
				raise models.ValidationError('Author Counts must have value')

	@api.multi
	def update_authors_count(self):
		hr_publication = self.search([])

		for pub in hr_publication:
			if pub.author_ids:
				pub.authors_count=len(pub.author_ids)
			#else:
			#	pub.authors_count=1
	
	def get_weight(self):
		authors=self.env['itb.hr_publication_author'].search([])
		for record in authors:
			if record.role=='co-author':
				if record.publication_id.authors_count > 1:
					record.weight = 0.4/(record.publication_id.authors_count-1)
				else:
					record.weight = 0
			else:
				record.weight = 0.6
		
		

	def _get_area(self):
		for pub in self:
			area = pub.mapped('author_ids.employee_id.research_group_id.name')
			pub.area = '; '.join(area)

	@api.multi
	def update_area(self):
		pubs = self.search([])

		for pub in pubs:
			area = pub.mapped('author_ids.employee_id.research_group_id.name')
			area_txt = ''
			for dumb in area:
				area_txt = dumb
				break

			pub.write({'area':area_txt})

	@api.model
	def _needaction_domain_get(self):
		return [('state', '=', 'validate')]
	
	
	@api.constrains('author_ids','review_ids')
	def check_author_not_reviewer(self):
		authors = self.mapped('author_ids.employee_id.id')
		reviewers = self.mapped('review_ids.employee_id.id') 
		
		if not set(authors).isdisjoint(reviewers):
			raise exceptions.ValidationError("Author can not be an reviewer at the same time for particular publication")
	
	
	def check_review_complete(self):
		score = self.mapped('review_ids.score')
		note = self.mapped('review_ids.note')
		
		if 0 not in score and False not in note:
			return True
		else:
			return False

			
class Publication_Media(models.Model):
	_name = 'itb.hr_publication_media'
	
	name = fields.Char()
	

class Publication_Category(models.Model):
	_name = 'itb.hr_publication_category'
	
	name = fields.Char()
	score = fields.Float()


class Publication_Author(models.Model):
	_name = 'itb.hr_publication_author'
	_rec_name = 'employee_id'
	
	#sequence = fields.Integer()
	day = fields.Date(string='Published',related='publication_id.day', store=True)
	publisher = fields.Char(related='publication_id.publisher', store=True)
	media = fields.Char(related='publication_id.media_id.name', store=True)
	scopus = fields.Char(related='publication_id.scopus', store=True)
	score = fields.Float()
	weight=fields.Float(compute='get_weight', store=True)
	role = fields.Selection([('author','Author'),('co-author','Co-Author')], 'Role', default='co-author')
	employee_id = fields.Many2one('hr.employee', string="Name")
	publication_id = fields.Many2one('itb.hr_publication',ondelete='cascade',required=True,index=True)
	research_group = fields.Char(related='employee_id.research_group_id.name',string='Research Group',store=True)
	
	@api.depends('role','publication_id')
	def get_weight(self):
		for record in self:
			if record.role=='co-author':
				if record.publication_id.authors_count > 1:
					record.weight = 0.4/(record.publication_id.authors_count-1)
				else:
					record.weight = 0
			else:
				record.weight = 0.6


class Publication_Review(models.Model):
	_name = 'itb.hr_publication_review'
	
	score = fields.Float()
	note = fields.Text()
	employee_id = fields.Many2one('hr.employee', string="Name")
	publication_id = fields.Many2one('itb.hr_publication',ondelete='cascade',required=True,index=True)