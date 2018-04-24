from odoo import models, fields, api, exceptions
from datetime import datetime

class Project(models.Model):
	_name = 'itb.hr_project'

	name = fields.Char()
	reference = fields.Char()
	start = fields.Date()
	finish = fields.Date()
	tipe = fields.Selection([('pendidikan','Pendidikan'),('penelitian','Penelitian'),('pengabdian','Pengabdian')],default='penelitian',string='Type')
	tahun = fields.Integer(compute='_get_year', store=True)
	sumber = fields.Char(string='Source')
	deskripsi_sispran = fields.Char(string='SISPRAN Note')
	deskripsi = fields.Char(string='Note')
	program = fields.Char(string='Program')
	jenis = fields.Char(string='Category')
	kk = fields.Char(string='KK')
	mitra = fields.Char()
	no_kontrak = fields.Char(string='Contract Ref')
	tgl_kontrak = fields.Char(string='Contract Date')
	nilai = fields.Float(string='Amount')
	team_ids = fields.One2many('itb.hr_project_team','project_id',string='Team')
	state = fields.Selection([('draft','Draft'),('valid','Valid')], 'Status', default='draft', required=True, readonly=True, copy=False,index=True)
	partner_id = fields.Many2one('res.partner', string='Partner')
	research_group_id = fields.Many2one('itb.hr_research_group', string='Research Group')
	
	@api.depends('start')
	def _get_year(self):
		for project in self:
			if project.start:
				year = datetime.strptime(project.start, '%Y-%m-%d').strftime('%Y')
				project.tahun = int(year)
	

class Project_Type(models.Model):
	_name = 'itb.hr_project_type'
	
	name = fields.Char()
	
	
class Project_Team(models.Model):
	_name = 'itb.hr_project_team'
	
	employee_id = fields.Many2one('hr.employee', string='Name')
	role = fields.Selection([('member','Member'),('leader','Leader')],default='member')
	project_id = fields.Many2one('itb.hr_project',ondelete='cascade',required=True,index=True)
	client = fields.Char('Client',related='project_id.mitra')
	year = fields.Integer('Year',related='project_id.tahun')
	amount = fields.Float('Amount',related='project_id.nilai')
	research_group = fields.Char(related='employee_id.research_group_id.name',string='Research Group',store=True)