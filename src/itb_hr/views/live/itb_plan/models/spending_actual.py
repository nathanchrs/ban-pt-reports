from odoo import models, fields, api, exceptions
from datetime import date
from odoo.osv import osv


class Spending_Actual(models.Model):
	_name = 'itb.plan_spending_actual'
	
	name = fields.Char(related='spending_id.name')
	code = fields.Char(related='spending_id.code', readonly=True)
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', required=True,store=True)
	day = fields.Date(related='spending_id.day',store=True)
	standard = fields.Char(related='spending_id.standard',readonly=True)
	price = fields.Float(related='spending_id.price',default=0)
	volume = fields.Float(compute='_sum_volume', store=True, readonly=True, default=0)
	total = fields.Float(default=0)
	used = fields.Float(readonly=True,default=0)
	available = fields.Float(compute='_sum_available', store=True,readonly=True)
	paid = fields.Float(readonly=True,default=0)
	percent_budget = fields.Float(compute='_recalculate_percent_budget',store=True,readonly=True,default=0)
	active = fields.Boolean(default=True,readonly=True)
	previus_month = fields.Char(store=True, readonly=True)
	confirmation_ref = fields.Char(string="No Ref Confirmation",readonly=True)
	confirmation_date = fields.Date(string='Confirmation Date',readonly=True)
	confirmation_note = fields.Char(string='Confirmation Note',readonly=True)
	state=fields.Selection([('draft','Draft'),('confirm','FRA')], 'Status',default='draft', required=True, readonly=True, copy=False)
	
	spending_id = fields.Many2one('itb.plan_spending',ondelete='cascade',required=True,index=True)
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', related='spending_id.type', readonly=True, store=True)
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source', related='spending_id.source', readonly=True)
	price_id = fields.Many2one('itb.plan_price',related='spending_id.price_id',ondelete='cascade',required=True,index=True,store=True)
	plan_line_id = fields.Many2one('itb.plan_line',related='spending_id.plan_line_id',ondelete='cascade',index=True, readonly=True, store=True)
	plan_id = fields.Many2one('itb.plan',related='spending_id.plan_id',ondelete='cascade',index=True,store=True)
	implementation_id = fields.Many2one('itb.plan_implementation',ondelete='cascade',required=True,index=True)
	#confirmation_id = fields.Many2one('itb.plan_confirmation',ondelete='cascade',index=True)
	request_line_ids = fields.One2many('itb.plan_request_line', 'spending_actual_id', 'Request Line', index=True)
	user_ids = fields.Many2many('res.users')
	unit_id = fields.Many2one('itb.plan_unit',related='plan_line_id.unit_id',index=True, readonly=True, store=True)

	@api.one
	@api.depends('total', 'price_id')
	def _sum_volume(self):
		if self.total > 0 and self.price_id.amount > 0:
			self.volume = self.total / self.price_id.amount
	
	@api.multi
	def action_state_confirmed(self):
		self.state = 'confirm'
	
	@api.multi
	def action_state_abort(self):
		self.state = 'draft'
	
	@api.one
	@api.depends('price')
	def _calculate_total(self):
		self.total = self.price * self.volume

	# @api.one
	# @api.depends('payment_budget_ids')
	# @api.onchange('payment_budget_ids')
	# def _recalculate_used(self):
	# 	self.used = sum([budget.used for budget in self.payment_budget_ids])
		# self.used = 0
		# for payment_budget in self.payment_budget_ids:
		# 	pay_ment = self.env['itb.plan_payment'].browse(payment_budget.payment_id)
		# 	if pay_ment.search([('state','<>','draft')]):
		# 		self.used += payment_budget.total
			# if pay_ment.state != 'draft':
			# 	self.used += payment_budget.total
		# self.used = sum([payment.total for payment in self.payment_budget_ids])
	
	#@api.multi
	#def write(self, vals):
	#	old = self.env['itb.plan_spending_actual'].search([('id','=',self.id)])
	#	res = super(itb.plan_spending_actual, self).write(vals)
	#	return res

	@api.one
	def _recalculate_all_used(self):
		self.used = sum([budget.used for budget in self.request_line_ids])

	@api.one
	@api.depends('total','used')
	def _recalculate_percent_budget(self):
		if self.total > 0:
			self.percent_budget = 100*self.used / self.total
		else:
			self.percent_budget = 0

	@api.depends('total','used')
	def _sum_available(self):
		for record in self:
			record.available = record.total - record.used
			
	# def write(self, cr, uid, ids, vals, context=None):
	# 	self.spending_id._sum_used()
	# 	res = super(my_class, self).write(cr, uid, ids, vals, context=context)
	# 	return res
	@api.multi
	def set_confirmation(self):
		return {
        	'name': 'Generate Spending for Plan ITB',
        	'type': 'ir.actions.act_window',
            'res_model': 'itb.plan_confirmation_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
			#'res_id': self.id,
			#'context': context,
			'context': {'parent_obj': self.active_ids},
        	}

class Confirmation_Wizard(models.TransientModel):
	_name = 'itb.plan_confirmation_wizard'
	
	confirmation_ref = fields.Char(string="No Ref Confirmation")
	confirmation_date = fields.Date(default=date.today(), string='Confirmation Date')
	confirmation_note = fields.Char(string='Confirmation Note')
	state=fields.Selection([('draft','Draft'),('confirm','Confirmed')], 'Status',default='draft', required=True,)
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', required=True)

	@api.multi
	def no(self):
	    pass

	@api.multi
	def yes(self):
		parent_id=self._context['parent_id']
		dic = {'Jan':'1', 'Feb':'1', 'Mar':'1', 'Apr':'2', 'May':'2', 'Jun':'2', 'Jul':'3', 'Aug':'3', 'Sep':'3', 'Oct':'4', 'Nov':'4', 'Dec':'4'}
		if parent_id:
			for rec in parent_id:
				old_month=''
				new_month=''
				actual =  self.env['itb.plan_spending_actual'].search([('id','=',rec)])
				cek = self.env['itb.plan_implementation'].search([('id','=',actual.implementation_id.id)])
				if actual.month:
					old_month = dic[actual.month]
				if self.month:
					new_month = dic[self.month]
				if old_month > new_month:
					raise osv.except_osv('only can select confirmation month newest or same then actual month')
				if cek.state == 'validate':
					ret = actual.write({
						'confirmation_ref':self.confirmation_ref,
						'confirmation_date':self.confirmation_date,
						'confirmation_note':self.confirmation_note,
						'state':self.state,
						'month':self.month,
						'previus_month':actual.month,
						})

class Send_Request(models.TransientModel):
	_name = 'itb.plan_send_request_wizard'

	name = fields.Char()
	reference = fields.Char()
	request_id = fields.Many2one('itb.plan_request', index=True)
	day = fields.Date()
	due = fields.Date()
	total = fields.Float(default=0)
	is_reconciled = fields.Boolean()
	note = fields.Text()
	unit_id = fields.Many2one('itb.plan_unit',required=True,index=True)
	pay_to = fields.Many2one('res.partner',required=True,index=True)
	price_id = fields.Many2one('itb.plan_price',ondelete='cascade',required=True,index=True)
	from_request=fields.Boolean(default=False)

	@api.multi
	def no(self):
	    pass

	@api.multi
	def yes(self):
		parent_id=self._context['parent_id']
		if parent_id:
			actual = self.env['itb.plan_spending_actual'].search([('id','in',parent_id)])
			price = set(actual.mapped('price_id'))
			if len(price) > 1:
				#raise Warning(_("only 1 same type spending allowed sending to request"))
				#raise exceptions.except_orm(_('only 1 same type spending allowed sending to request'), _('My message + lorem ipsum'))
				raise osv.except_osv('only 1 same type spending allowed sending to request')
				pass
				#raise osv.except_osv((Error Condition), (Error Description))
			else:
				pass
		#		if actual:
				
		#		actual =  self.env['itb.plan_spending_actual'].search([('id','in',rec)])
		#		ret = actual.write({
		#			'confirmation_ref':self.confirmation_ref,
		#			'confirmation_date':self.confirmation_date,
		#			'confirmation_note':self.confirmation_note,
		#			'state':self.state,
		#			})