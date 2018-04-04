from odoo import models, fields, api, exceptions
from datetime import date

class Plan(models.Model):
	_name = 'itb.plan'
	_sql_constraints = [
		('name', 'unique(name)', 'Nama rencana harus berbeda dengan yang pernah dibuat')
	]

	#name = fields.Char(required=True,compute='_name_onchange',store=True,default='Default Name Plan')
	name = fields.Char(required=True,store=True,ondelte='cascade', default='Plan STEI - 2018')# + str(date.today().year+1))
	# name_view = fields.Char(compute='_autoreload_name')
	year = fields.Integer(default=date.today().year+1, required=True)
	budget = fields.Float(compute='_compute_budget', store=True,default=0)
	percent_budget = fields.Float(readonly=True, compute='_compute_avg', store=True,default=0)
	percent_performance = fields.Float(readonly=True, compute='_compute_avg', store=True,default=0)
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated'),('archived','Archived')], 'Status',default='draft', required=True, readonly=True, copy=False)
	#unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	plan_line_ids = fields.One2many('itb.plan_line', 'plan_id', 'Initiative', copy=True)
	target_ids = fields.One2many('itb.plan_target','plan_id',string='Performance')
	spending_ids = fields.One2many('itb.plan_spending','plan_id',string='Budget')
	
	# @api.one
	# @api.depends('name')
	# @api.onchange('name')
	# def _autoreload_name(self):
	# 	self.name_view = self.name

	@api.one
	@api.constrains('year')
	def _check_year(self):
		return self.year < date.today().year

	@api.one
	@api.depends('spending_ids')
	#@api.onchange('spending_ids')
	def _compute_budget(self):
		spendings = [spending.total for spending in self.spending_ids]
		self.budget = sum(spendings)
	
	#@api.one
	#@api.depends('unit_id')
	#@api.onchange('unit_id')
	#def _name_onchange(self):
	#def _compute_name(self):
	#	if self.unit_id:
	#		self.name = 'Plan STEI - ' + str(date.today().year+1))
			# self.name_view = str(self.unit_id.name + ' ' + str(date.today().year+1))
	#	else:
	#		self.name = 'Plan STEI'
			# self.name_view = 'Default Name Plan'

	# @api.one
	# @api.depends('unit_id')
	# def _compute_name(self):
	# 	if self.unit_id:
	# 		self.name = str(self.unit_id.name + ' ' + str(date.today().year+1))
	# 	else:
	# 		self.name = 'Default Name Plan'

	@api.one
	@api.depends('plan_line_ids')
	#@api.onchange('plan_line_ids')
	def _compute_avg(self):
		count = 0
		perf_total = 0
		budg_total = 0
		for row in self.plan_line_ids.search([('plan_id', '=', self.id)]):
			count+=1
			budg_total += row.percent_budget
			perf_total += row.percent_performance
			pass
		if count > 0:
			self.percent_budget = budg_total / count
			self.percent_performance = perf_total / count
		else:
			self.percent_budget = 0
			self.percent_performance = 0
	
	# def action_state_draft(self, cr, uid, ids):
	# 	self.write(cr, uid, ids, { 'state' : 'draft' })
	# 	return True

	@api.multi
	def action_state_confirmed(self):
		self.state = 'confirm'
		#self.write({ 'state' : 'confirm' })
		#return True
	
	@api.multi
	def action_state_validated(self):
		self.state = 'validate'
		#self.write({ 'state' : 'validate' })
		#return True

	@api.multi
	def action_state_abort(self):
		self.state = 'draft'
		#self.write({ 'state' : 'draft' })
		#return True

	@api.multi
	def action_state_archived(self):
		self.state = 'archived'
		#self.write({ 'state' : 'archived' })
		#return True

class Plan_Line(models.Model):
	_name = 'itb.plan_line'
	
	name = fields.Char(required=True)
	code = fields.Char()
	barang = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	jasa = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	modal = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	pegawai = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	budget = fields.Float(default=0)
	percent_budget = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	percent_performance = fields.Float(compute='_compute_target', readonly=True, default=0, store=True)

	unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	program_id = fields.Many2one('itb.plan_program',ondelete='cascade',required=True,index=True)
	activity_id = fields.Many2one('itb.plan_activity',ondelete='cascade',domain="[('program_id','=',program_id)]",required=True,index=True)
	subactivity_id = fields.Many2one('itb.plan_subactivity',ondelete='cascade',domain="[('activity_id','=',activity_id)]",required=True,index=True)
	plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True)
	target_ids = fields.One2many('itb.plan_target','plan_line_id',string='Performance Target')
	spending_ids = fields.One2many('itb.plan_spending','plan_line_id',string='Spending')
	is_project = fields.Boolean(default=False)

	@api.one
	@api.depends('spending_ids')
	#@api.onchange('spending_ids')
	def _compute_spending(self):
		count = 0
		budg_perc_total = 0
		self.barang = 0
		self.jasa = 0
		self.modal = 0
		self.pegawai = 0
		self.budget = 0
		for row in self.spending_ids.search([('plan_line_id', '=', self.id)]):
			count += 1
			self.budget += row.total
			budg_perc_total += row.percent_budget
			if row.type == 'barang':
				self.barang += row.total
			else:
				if row.type == 'jasa':
					self.jasa += row.total
				else:
					if row.type == 'modal':
						self.modal += row.total
					else:
						if row.type == 'pegawai':
							self.pegawai += row.total
		if count > 0:
			self.percent_budget = budg_perc_total / count
		else:
			self.percent_budget = 0
	
	
	@api.one
	@api.depends('target_ids')
	#@api.onchange('target_ids')
	def _compute_target(self):
		count = 0
		perf_total = 0
		for row in self.target_ids.search([('plan_line_id', '=', self.id)]):
			count += 1
			perf_total += row.percent_performance
		if count > 0:
			self.percent_performance = perf_total / count
		else:
			self.percent_performance = 0