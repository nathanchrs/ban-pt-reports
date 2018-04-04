from odoo import models, fields, api, exceptions

class Research_Group(models.Model):
	_name = 'itb.hr_research_group'
	
	name = fields.Char()



class Employee(models.Model):
	_inherit = 'hr.employee'
	
	pre_title = fields.Char()
	post_title = fields.Char()
	employment_type = fields.Selection([('itb','ITB'),('pns','PNS'),('cpns','CPNS'),('contract','Contract'),('outsource','Outsource'),('assistant','Assistant Academic')])
	nip_old = fields.Char()
	nip_new = fields.Char()
	nidn = fields.Char()
	nik = fields.Char()
	birthplace = fields.Char()
	finger_id = fields.Char()
	employee_card = fields.Char()
	pns_start = fields.Date()
	cpns_start = fields.Date()
	is_faculty = fields.Boolean()
	is_student = fields.Boolean()
	tendik = fields.Selection([('pustakawan','Pustakwan'),('laboran/teknisi/analis/operator/programmer','Laboran/Teknisi/Analis/Operator/Programmer'),('tenaga administrasi','Tenaga Administrasi'),('pramu','Pramu')])
	last_edu = fields.Char(compute='_compute_degree',store=True, string='Pendidikan terakhir')
	is_self = fields.Boolean(default=False)
	prodi = fields.Many2one('itb.academic_program', string='Prodi')
	last_jabatan = fields.Char(compute='_compute_last_jabatan',store=True, string='Jabatan terakhir')
	last_pangkat = fields.Char(compute='_compute_last_pangkat',store=True, string='Pangkat terakhir')
	npwp = fields.Char()
	
	research_group_id = fields.Many2one('itb.hr_research_group', string="Research Group")
	education_ids = fields.One2many('itb.hr_education','employee_id',string='Educations')
	work_ids = fields.One2many('itb.hr_work','employee_id',string='Works')
	assignment_ids = fields.One2many('itb.hr_assignment','employee_id',string='Assignment')
	project_ids = fields.One2many('itb.hr_project_team','employee_id',string='Project')
	training_ids = fields.One2many('itb.hr_training','employee_id',string='Trainings')
	award_ids = fields.One2many('itb.hr_award','employee_id',string='Awards')
	membership_ids = fields.One2many('itb.hr_membership','employee_id',string='Membership')
	family_ids = fields.One2many('itb.hr_family','employee_id',string='Family')
	pangkat_ids = fields.One2many('itb.hr_pangkat','employee_id',string='Pangkat')
	jabatan_ids = fields.One2many('itb.hr_jabatan','employee_id',string='Jabatan')
	publication_ids = fields.One2many('itb.hr_publication_author','employee_id',string='Publication')
	employment_ids = fields.One2many('itb.hr_employment','employee_id',string='Employment')
	duty_ids = fields.One2many('itb.hr_duty_employee','employee_id',string='Duty')

	@api.depends('education_ids')
	def _compute_degree(self):
	   for record in self:
	      if record.education_ids:
	         item = record.education_ids.sorted(key=lambda r: r.finish)[-1]
	         dict_edu = {'kindergarten': 'TK', 'elementary': 'SD', 'junior-high': 'SMP', 'senior-high': 'SMA/SMK', 'diploma': 'D3', 'undergraduate': 'S1', 'graduate': 'S2', 'doctoral': 'S3', 'post-doc': 'post-doc'}
	         record.last_edu = dict_edu[item.degree]

	@api.depends('pangkat_ids')
	def _compute_last_pangkat(self):
	   for record in self:
	      if record.pangkat_ids:
	         item = record.pangkat_ids.sorted(key=lambda r: r.start)[-1]
	         record.last_pangkat = item.pangkat

	@api.depends('jabatan_ids')
	def _compute_last_jabatan(self):
	   for record in self:
	      if record.jabatan_ids:
	         item = record.jabatan_ids.sorted(key=lambda r: r.start)[-1]
	         record.last_jabatan = item.jabatan
	
	@api.multi
	def update_jabatan(self):
		employee = self.search([])

		for emp in employee:
			if emp.jabatan_ids:
				item = emp.jabatan_ids.sorted(key=lambda r: r.start)[-1]
				emp.last_jabatan=item.jabatan

	@api.multi
	def update_pangkat(self):
		employee = self.search([])

		for emp in employee:
			if emp.pangkat_ids:
				item = emp.pangkat_ids.sorted(key=lambda r: r.start)[-1]
				emp.last_pangkat=item.pangkat
	
	@api.multi
	def update_pendidikan(self):
		employee = self.search([])

		for emp in employee:
			if emp.education_ids:
				item = emp.education_ids.sorted(key=lambda r: r.finish)[-1]
				dict_edu = {'kindergarten': 'TK', 'elementary': 'SD', 'junior-high': 'SMP', 'senior-high': 'SMA/SMK', 'diploma': 'D3', 'undergraduate': 'S1', 'graduate': 'S2', 'doctoral': 'S3', 'post-doc': 'post-doc'}
				emp.last_edu=dict_edu[item.degree]