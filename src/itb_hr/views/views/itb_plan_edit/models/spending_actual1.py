from odoo import models, fields, api, exceptions
from datetime import date
from odoo.osv import osv


class Spending_Actual(models.Model):
	_name = 'itb.plan_spending_actual'
	
	spending_id = fields.Many2one('itb.plan_spending',ondelete='cascade',required=True,index=True)
	plan_line_id = fields.Many2one('itb.plan_line',related='spending_id.plan_line_id',readonly=True, store=True)
	name = fields.Char(related='plan_line_id.name', readonly=True, store=True)
	code = fields.Char(related='spending_id.code', readonly=True, store=True)
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', required=True,store=True, index=True)
	day = fields.Date(related='spending_id.day', readonly=True, store=True)
	standard = fields.Char(related='spending_id.standard', readonly=True, store=True)
	price = fields.Float(related='spending_id.price',default=0, readonly=True, store=True)
	volume = fields.Float(compute='_sum_volume', store=True, readonly=True, default=0)
	total = fields.Float(default=0)
	used = fields.Float(readonly=True, default=0)
	available = fields.Float(compute='_sum_available', store=True, readonly=True)
	paid = fields.Float(readonly=True, default=0)
	percent_budget = fields.Float(compute='_recalculate_percent_budget',store=True, readonly=True, default=0)
	active = fields.Boolean(default=True,readonly=True)
	previus_month = fields.Char(store=True, readonly=True)
	confirmation_ref = fields.Char(string="No Ref Confirmation",readonly=True)
	confirmation_date = fields.Date(string='Confirmation Date',readonly=True)
	confirmation_note = fields.Char(string='Confirmation Note',readonly=True)
	state=fields.Selection([('draft','Draft'),('confirm','FRA')], 'Status',default='draft', required=True, readonly=True, copy=False)
	
	
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', related='spending_id.type', readonly=True, store=True)
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source', readonly=True)
	price_id = fields.Many2one('itb.plan_price',related='spending_id.price_id',ondelete='cascade',index=True,store=True)
	
	plan_id = fields.Many2one('itb.plan',related='spending_id.plan_id',ondelete='cascade',index=True,store=True)
	implementation_id = fields.Many2one('itb.plan_implementation',ondelete='cascade',required=True,index=True)
	#confirmation_id = fields.Many2one('itb.plan_confirmation',ondelete='cascade',index=True)
	request_line_ids = fields.One2many('itb.plan_request_line', 'spending_actual_id', 'Request Line', index=True)
	user_ids = fields.Many2many('res.users')
	unit_id = fields.Many2one('itb.plan_unit',related='plan_line_id.unit_id',index=True, readonly=True, store=True)
	logistic = fields.Boolean(string='Logistic', default=False, readonly=True, store=True)
	previus_source = fields.Char(store=True, readonly=True)
	#dko_line_ids = fields.One2many('itb.plan_dko_line', 'actual_id', 'dko request', index=True, copy=True)
	#umk_line_ids = fields.One2many('itb.plan_spending_actual_umk', 'spending_actual_id', 'umk Line', index=True)
	program_id = fields.Many2one('itb.plan_program', related='plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one('itb.plan_activity', related='spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one('itb.plan_subactivity', related='spending_id.plan_line_id.subactivity_id', readonly=True, store=True)


	@api.one
	@api.depends('total', 'price_id')
	def _sum_volume(self):
		for rec in self:
			if rec.total > 0 and rec.price_id.amount > 0:
				rec.volume = rec.total / rec.price_id.amount
	
	@api.multi
	def action_state_confirmed(self):
		self.state = 'confirm'
	
	@api.multi
	def action_state_abort(self):
		self.state = 'draft'
	
	@api.one
	@api.depends('price')
	def _calculate_total(self):
		for rec in self:
			rec.total = rec.price * rec.volume

	'''
	@api.one
	def _recalculate_all_used(self):
		for rec in self:
			rec.used = sum([budget.total for budget in rec.request_line_ids])
	'''

	@api.one
	@api.depends('total','used')
	def _recalculate_percent_budget(self):
		for rec in self:
			if rec.total > 0:
				rec.percent_budget = (100 * rec.used) / rec.total
			else:
				rec.percent_budget = 0

	@api.depends('total','used')
	def _sum_available(self):
		for record in self:
			record.available = record.total - record.used
			
	@api.multi
	def set_confirmation(self):
		return {
			'name': 'Set Confirmation',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_confirmation_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.active_ids},
			}
	
	@api.multi
	def send_to_logistik(self):
		return {
			'name': 'Generate Logistik to Request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_send_logistik_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.active_ids},
			}
	
	@api.multi
	def send_to_request(self):
		return {
			'name': 'Send Spending Actual to Request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_send_request_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.active_ids},
			}
	
	@api.multi
	def set_source(self):
		return {
			'name': 'Set New source Spending Actual after FRA',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_set_source_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.active_ids},
			}

	'''
	@api.multi
	def set_to_dko(self):
		return {
			'name': 'Set Spending Actual to DKO',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_set_dko_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.active_ids},
			}
	'''

class Set_source_Wizard(models.TransientModel):
	_name = 'itb.plan_set_source_wizard'
	
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source')
	
	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		parent_id=self._context['parent_id']
		if parent_id:
			actual =  self.env['itb.plan_spending_actual'].search([('id','in',parent_id),('state','=','confirm')])
			for rec in actual:
				if rec.request_line_ids.id == False:
					raise osv.except_osv(str(rec.request_line_ids.id) + '||' + len(str(rec.request_line_ids.id)))
					cek = self.env['itb.plan_implementation'].search([('id','=',rec.implementation_id.id)])
					if cek.state == 'validate':
						ret = rec.write({
							'previus_source':rec.source,
							'source':self.source,
							})



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
				actual =  self.env['itb.plan_spending_actual'].search([('id','=',rec),('state','=','draft')])
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
	day = fields.Date(default=date.today())
	due = fields.Date(default=date.today())
	total = fields.Float(default=0)
	is_reconciled = fields.Boolean()
	note = fields.Text()
	pay_to = fields.Many2one('res.partner',required=True,index=True)

	@api.multi
	def no(self):
	    pass

	@api.multi
	def yes(self):
		parent_id=self._context['parent_id']
		if parent_id:
			actual =  self.env['itb.plan_spending_actual'].search([('id','=',rec),('state','=','confirm')])
			price = set(actual.mapped('price_id'))
			source = set(actual.mapped('source'))
			if len(price)==1 and len(source)==1:
				pass
			else:
				raise osv.except_osv('only 1 same type or source spending allowed sending to request')
				pass

class Send_Logistik(models.TransientModel):
	_name = 'itb.plan_send_logistik_wizard'

	name = fields.Char(default='Logistik', readonly=True)
	reference = fields.Char()
	#request_id = fields.Many2one('itb.plan_request', index=True)
	day = fields.Date(default=date.today())
	due = fields.Date(default=date.today())
	#total = fields.Float(default=0)
	is_reconciled = fields.Boolean()
	note = fields.Text()
	pay_to = fields.Many2one('res.partner',default='Logistik', required=True,index=True)

	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		parent_id=self._context['parent_id']
		if parent_id:
			request = self.env['itb.plan_request_line']
			req_id = request.mapped('spending_actual_id')
			if req_id:
				actual = self.env['itb.plan_spending_actual'].search([('id','in',parent_id),('state','=','confirm'),('available','>',0),('id','not in',req_id)])
			else:
				actual = self.env['itb.plan_spending_actual'].search([('id','in',parent_id),('state','=','confirm'),('available','>',0)])
			#price = set(actual.mapped('price_id'))
			
			if actual:
				
				rec_total = sum(actual.mapped('total'))
				actual.write({
					'Logistic' : True,
				})
				plan_req = self.env['itb.plan_request']
				req_line = self.env['itb.plan_request_line']
				req_alo = self.env['itb.plan_request_alocation']
				for rec in actual:
					unit=self.env['itb.plan_unit'].search([('id','=',rec.unit_id.id)])
					if unit:
						self.name = self.name + ' - (' + str(rec.price_id.id) + ') ' + str(unit.name)
					pay=self.pay_to
					price=rec.price_id
					sumber=rec.source
					
					
					ret = plan_req.create({
						'name' : self.name,# + ' - (' + str(rec.price_id.id) + ') ' + str(rec.unit_id),
						'reference' : self.reference,
						'day' : self.day,
						'due' : self.due,
						'total' : rec.total,
						'source_total' : rec.total,
						'alocation_total' : rec.total,
						'is_reconciled' : self.is_reconciled,
						'note' : self.note,
						'state' : 'validate',
						'unit_id' : rec.unit_id.id,
						'pay_to' : self.pay_to.id,
						'price_id' : rec.price_id.id,
						'source' : sumber,
					})
					req=self.env['itb.plan_request'].search([('name','=',self.name),('total','=',rec.total),('price_id','=',rec.price_id.id),('unit_id','=',rec.unit_id.id),('pay_to','=',self.pay_to.id),('source','=',rec.source)],order='id desc', limit=1)
					ret_req = req_line.create({
						'request_id' : req.id,
						'spending_actual_id' : rec.id,
						'total' : rec.total
					})
					alo = self.env['itb.plan_allocation'].search([('spending_id','=',rec.spending_id.id)],limit=1)
					if alo:
						alo_req=self.env['itb.plan_spending_int'].search([('id','=',alo.spending_id_int.id)])
						req_alo.create({
							'request_alo_id' : req.id,
							'spending_id' : alo.spending_id_int.id,
							'total_alo' : req.total
						})
