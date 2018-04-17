from odoo import models, fields, api, exceptions
from odoo.osv import osv

class Request(models.Model):
	_name = 'itb.plan_request'
	_rec_name = 'pay_to'
	
	name = fields.Char()
	reference = fields.Char()
	day = fields.Date()
	due = fields.Date()
	total = fields.Float(default=0)
	#is_advance = fields.Boolean()
	is_reconciled = fields.Boolean()
	note = fields.Text()
	#type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', default='jasa', required=True)
	source_total = fields.Float(default=0, compute='_total_budget', store=True, readonly=True)
	alocation_total = fields.Float(default=0, compute='_total_alocation', store=True, readonly=True)

	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated'),('paid','Paid')], 'Status', default='draft',required=True, readonly=True, copy=False)
	unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	#plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True,domain="[('state','=','validate')]")
	pay_to = fields.Many2one('res.partner',ondelete='cascade',required=True,index=True)
	request_line_ids = fields.One2many('itb.plan_request_line', 'request_id', 'Request Line', copy=True)
	request_alocation_ids = fields.One2many('itb.plan_request_alocation', 'request_alo_id', 'Request Alocation', copy=True)
	price_id = fields.Many2one('itb.plan_price',ondelete='cascade',required=True,index=True)
	
	@api.multi
	def action_payment_req_confirmed(self):
		budget_start=0
		budget_now = 0
		for rec in self.request_line_ids:
			budget = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			budget_start = budget.used
			budget_now = budget_start + rec.total
			budget.write({'used':budget_now,})
		
		budget_start=0
		budget_now = 0
		for rec in self.request_alocation_ids:
			budget = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			budget_start = budget.used
			budget_now = budget_start + rec.total_alo
			budget.write({'used':budget_now,})
		self.state = 'confirm'

	@api.multi
	def action_payment_req_paid(self):
		paid_start=0
		paid_now = 0
		for rec in self.request_line_ids:
			paid = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			paid_start = paid.paid
			paid_now = paid_start + rec.total
			paid.write({'paid':paid_now,})
		
		paid_start=0
		paid_now = 0
		for rec in self.request_alocation_ids:
			paid = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			paid_start = paid.paid
			paid_now = paid_start + rec.total_alo
			paid.write({'paid':paid_now,})
		self.state = 'paid'

	@api.multi
	def action_payment_req_validate(self):
		self.state = 'validate'

	# def action_payment_req_abort(self, cr, uid, ids):
	@api.multi
	def action_payment_req_abort(self):
		budget_start=0
		budget_now = 0
		for rec in self.request_line_ids:
			budget = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			budget_start = budget.used
			budget_now = budget_start - rec.total
			budget.write({'used':budget_now,})

		budget_start=0
		budget_now = 0
		for rec in self.request_alocation_ids:
			budget = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			budget_start = budget.used
			budget_now = budget_start - rec.total_alo
			budget.write({'used':budget_now,})
		self.state = 'draft'

	# def _trigger_recalculate(self,cr,uid,ids):
	# 	for spending in env['itb.plan_spending_actual']:
	# 		spending._recalculate_used()

	@api.one
	@api.depends('request_line_ids')
	def _total_budget(self):
		self.source_total = 0
		for payment in self.request_line_ids:
			self.source_total += payment.total
	
	@api.one
	@api.depends('request_alocation_ids')
	def _total_alocation(self):
		self.alocation_total = 0
		for payment in self.request_alocation_ids:
			self.alocation_total += payment.total_alo

	@api.constrains('total')
	def _check_below_zero(self):
		if self.total < 0.01:
			raise models.ValidationError('Total payment is below or equal zero.')

	@api.constrains('source_total')
	def _check_total_source(self):
		if self.total != self.source_total:
			raise models.ValidationError('total source must have same value with Total payment')

	@api.constrains('alocation_total')
	def _check_total_alocation(self):
		if self.total != self.alocation_total:
			raise models.ValidationError('total alocation must have same value with Total payment')
	
	'''
	_constraints = [
		(_check_below_zero,'Total payment is below or equal zero.',['total']),
		(_check_used,'Total Alocation is below then total Request.',['total']),
		(_check_total_below,'Total payment budget is below than sum of payment budget line.',['total']),
		#(_check_total_equal,'Total payment is not equal with sum of payment budget.',['total'])
	]
	'''

class Request_Line(models.Model):
	_name = 'itb.plan_request_line'

	request_id = fields.Many2one('itb.plan_request',ondelete='cascade',required=True,index=True)
	spending_actual_id = fields.Many2one('itb.plan_spending_actual',ondelete='cascade',required=True,index=True)
	initiative = fields.Char(related='spending_actual_id.plan_line_id.name')
	unit_id = fields.Many2one(related='spending_actual_id.unit_id')
	#type = fields.Selection(related='spending_actual_id.type')
	used = fields.Float(related='spending_actual_id.used')
	available=fields.Float(related='spending_actual_id.available')
	#month=fields.Char(related='spending_actual_id.month')
	
	def _available_budget(self):
		budget = self.env['itb.plan_spending_actual'].browse(self.spending_actual_id.id)
		return float(self.spending_actual_id.id)
		
	# total_original = fields.Float(related='spending_actual_id.total')
	total = fields.Float(default=0)

	@api.multi
	@api.onchange('spending_actual_id')
	def filter_spending_actual_id(self):
		res = dict()
		spending = self.env['itb.plan_spending'].search([('price_id','=',self.request_id.price_id.id)])
		spen_id = spending.mapped('id')
		actual = self.env['itb.plan_spending_actual'].search([('spending_id','in', spen_id),('state','=','confirm')])
		spending_actual_ids=actual.mapped('id')
		res['domain'] = {'spending_actual_id': [('id', 'in', spending_actual_ids)]}
		return res

	#def _check_type(self):
	#	for budget in self.browse():
	#		for budgets in budget.request_id.request_line_ids:
	#			if budget.request_id.type != budgets.type:
	#				return False
	#	return True

	@api.constrains('total')
	def _check_below_zero(self):
		if self.total < 0.01:
			raise models.ValidationError('Total source is below or equal zero.')

	@api.constrains('total')
	def _check_total(self):
		if self.total > (self.available):
			raise models.ValidationError('Total source is over then available.')

	# @api.one
	# @api.onchange('used')
	# def _onchange_used(self):
	# 	for spending in self.env['itb.plan_spending_actual'].browse([self.spending_actual_id]):
	# 		spending._recalculate_all_used()

	'''
	_constraints = [
		(_check_below_zero,'Total payment budget is below or equal zero.',['total']),
		(_check_total,'Total payment budget is over than usable budget.',['total']),
		#(_check_type,'There is one and more payment budget type not equal with payment type.',['spending_actual_id'])
	]
	'''

class Request_Alocation(models.Model):
	_name = 'itb.plan_request_alocation'

	request_alo_id = fields.Many2one('itb.plan_request',ondelete='cascade',required=True,index=True)
	spending_id = fields.Many2one('itb.plan_spending_int',ondelete='cascade',required=True,index=True)
	initiative_alo = fields.Char(related='spending_id.plan_line_id.name')
	unit_id = fields.Many2one(related='spending_id.unit_id')
	#type_alo = fields.Selection(related='spending_id.type')
	used_alo = fields.Float(related='spending_id.used')
	available_alo = fields.Float(related='spending_id.available')
	#month=fields.Selection(related='spending_id.month')
	
	def _available_budget(self):
		budget = self.env['itb.plan_spending_int'].browse(self.spending_id.id)
		return float(self.spending_id.id)
		
	# total_original = fields.Float(related='spending_actual_id.total')
	total_alo = fields.Float(default=0)

	@api.multi
	@api.onchange('spending_id')
	def filter_spending_id(self):
		res = dict()
		spending = self.env['itb.plan_spending_int'].search([('unit_id','=',self.request_alo_id.unit_id.id),('price_id','=',self.request_alo_id.price_id.id)])
		spending_ids=spending.mapped('id')
		res['domain'] = {'spending_id': [('id', 'in', spending_ids)]}
		return res

	#def _check_type(self):
	#	for budget in self.browse():
	#		for budgets in budget.request_alo_id.request_alocation_ids:
	#			if budget.request_alo_id.type != budgets.type:
	#				return False
	#	return True

	@api.constrains('total_alo')
	def _check_below_zero(self):
		if self.total_alo < 0.01:
			raise models.ValidationError('Total Alocation is below or equal zero.')

	'''
	@api.constrains('total_alo')
	def _check_total(self):
		if self.total_alo > self.available_alo:
			raise models.ValidationError('Total Alocation is over then available')
	'''

	# @api.one
	# @api.onchange('used')
	# def _onchange_used(self):
	# 	for spending in self.env['itb.plan_spending_actual'].browse([self.spending_actual_id]):
	# 		spending._recalculate_all_used()

	'''
	_constraints = [
		(_check_below_zero,'Total payment budget is below or equal zero.',['total_alo']),
		(_check_total,'Total payment budget is over than usable budget.',['total_alo']),
		#(_check_type,'There is one and more payment budget type not equal with payment type.',['spending_id']),
		#(_check_used,'Total spending is over than total budget.',['total_alo']),
	]
	'''