from odoo import models, fields, api, exceptions
from odoo.osv import osv
from datetime import date
from datetime import timedelta
from datetime import datetime

stat = False
stat_line = False
stat_dko = False
stat_line_dko = False

class Request(models.Model):
	_name = 'itb.plan_request'
	_rec_name = 'pay_to'
	
	global stat

	name = fields.Char(index=True)
	reference = fields.Char()
	day = fields.Date(default=date.today() ,index=True)
	due = fields.Date(default=date.today())
	total = fields.Float(default=0)
	is_reconciled = fields.Boolean()
	note = fields.Text()
	source_total = fields.Float(default=0, compute='_total_budget', store=True, readonly=True)
	alocation_total = fields.Float(default=0, compute='_total_alocation', store=True, readonly=True)
	cash_id = fields.Many2one('itb.plan_cash_advance', string='Cash Advance', index=True, ondelete='cascade')

	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated'),('paid','Paid')], 'Status', default='draft',required=True, readonly=True, copy=False ,index=True)
	unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	pay_to = fields.Many2one('res.partner',ondelete='cascade',required=True,index=True)
	request_line_ids = fields.One2many('itb.plan_request_line','request_id', 'Request Line', copy=True)
	request_alocation_ids = fields.One2many('itb.plan_request_alocation', 'request_alo_id', 'Request Alocation', copy=True)
	price_id = fields.Many2one('itb.plan_price',ondelete='cascade',required=True,index=True)
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source',default='dm' ,index=True)
	tax_line_ids = fields.One2many('itb.plan_request_tax', 'request_id', 'Tax Request', copy=True)
	reimburse_id = fields.Many2one('itb.plan_reimburse', ondelete='cascade', index=True)
	
	stat=True

	'''
	@api.multi
	def create(self, vals):
		stat=False
		return super(Request, self).create(vals)
	'''
	@api.multi
	def set_confirm_request(self):
		budget_start=0
		budget_now = 0
		request_draft = self.env['itb.plan_request'].search([('state','!=','confirm')])
		for rec in request_draft:
			lines = self.env['itb.plan_request_line'].search([('request_id','=',rec.id)])
			for rec2 in lines:
				budget = self.env['itb.plan_spending_actual'].search([('id','=',rec2.spending_actual_id.id),('state','=','confirm')])
				budget_start = budget.used
				if budget_start + rec2.total <= budget.total:
					budget_now = budget_start + rec2.total
				else:
					budget_now = budget.total
				budget.write({'used':budget_now,})

				budget_s = self.env['itb.plan_spending'].search([('id','=',rec2.spending_actual_id.spending_id.id)])
				budget_s.write({'used':budget_now,})
			
			budget_start=0
			budget_now = 0
			lines2 = self.env['itb.plan_request_alocation'].search([('request_alo_id','=',rec.id)])
			for rec2 in lines2:
				budget = self.env['itb.plan_spending_int'].search([('id','=',rec2.spending_id.id)])
				budget_start = budget.used
				if budget_start + rec2.total_alo <= budget.total:
					budget_now = budget_start + rec2.total_alo
				else:
					budget_now = budget.total
				budget.write({'used':budget_now,})
		request_draft.write({'state':'confirm'})

	@api.multi
	def set_all_draft(self):
		request_draft = self.env['itb.plan_request'].search([('state','!=','draft')])
		request_draft.write({'state':'draft'})

	@api.multi
	def set_paid_request(self):
		budget_start=0
		budget_now = 0
		request_draft = self.env['itb.plan_request'].search([('state','!=','paid')])
		for rec in request_draft:
			lines = self.env['itb.plan_request_line'].search([('request_id','=',rec.id)])
			for rec2 in lines:
				budget = self.env['itb.plan_spending_actual'].search([('id','=',rec2.spending_actual_id.id),('state','=','confirm')])
				budget_start = budget.used
				if budget_start + rec2.total <= budget.total:
					budget_now = budget_start + rec2.total
				else:
					budget_now = budget.total
				budget.write({'paid':budget_now,})

				budget_s = self.env['itb.plan_spending'].search([('id','=',rec2.spending_actual_id.spending_id.id)])
				budget_s.write({'paid':budget_now,})
			
			budget_start=0
			budget_now = 0
			lines2 = self.env['itb.plan_request_alocation'].search([('request_alo_id','=',rec.id)])
			for rec2 in lines2:
				budget = self.env['itb.plan_spending_int'].search([('id','=',rec2.spending_id.id)])
				budget_start = budget.used
				if budget_start + rec2.total_alo <= budget.total:
					budget_now = budget_start + rec2.total_alo
				else:
					budget_now = budget.total
				budget.write({'paid':budget_now,})
		request_draft.write({'state':'paid'})

	@api.multi
	def action_payment_req_confirmed(self):
		budget_start=0
		budget_now = 0
		for rec in self.request_line_ids:
			budget = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			budget_start = budget.used
			if budget_start + rec.total <= budget.total:
				budget_now = budget_start + rec.total
			else:
				budget_now = budget.total
			budget.write({'used':budget_now,})

			budget_s = self.env['itb.plan_spending'].search([('id','=',rec.spending_actual_id.spending_id.id)])
			budget_s.write({'used':budget_now,})
		
		budget_start=0
		budget_now = 0
		for rec in self.request_alocation_ids:
			budget = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			budget_start = budget.used
			if budget_start + rec.total_alo <= budget.total:
				budget_now = budget_start + rec.total_alo
			else:
				budget_now = budget.total
			budget.write({'used':budget_now,})
		self.state = 'confirm'

	@api.multi
	def action_payment_req_paid(self):
		paid_start=0
		paid_now = 0
		for rec in self.request_line_ids:
			paid = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			paid_start = paid.paid
			if paid_start + rec.total <= paid.total:
				paid_now = paid_start + rec.total
			else:
				paid_now = paid.total
			paid.write({'paid':paid_now,})

			paid_s = self.env['itb.plan_spending'].search([('id','=',rec.spending_actual_id.spending_id.id)])
			paid_s.write({'paid':paid_now,})
		
		paid_start=0
		paid_now = 0
		for rec in self.request_alocation_ids:
			paid = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			paid_start = paid.paid
			if paid_start + rec.total_alo <= paid.total:
				paid_now = paid_start + rec.total_alo
			else:
				paid_now = paid.total
			paid.write({'paid':paid_now,})
		self.state = 'paid'

	@api.multi
	def action_payment_req_validate(self):
		self.state = 'validate'

	@api.multi
	def action_payment_req_abort(self):
		budget_start=0
		budget_now = 0
		for rec in self.request_line_ids:
			budget = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id),('state','=','confirm')])
			if budget.used>0:
				budget_start = budget.used
				if budget_start - rec.total > 0:
					budget_now = budget_start - rec.total
				else:
					budget_now = 0
				budget.write({'used':budget_now,})

			budget_s = self.env['itb.plan_spending'].search([('id','=',rec.spending_actual_id.spending_id.id)])
			budget_s.write({'used':budget_now,})

		budget_start=0
		budget_now = 0
		for rec in self.request_alocation_ids:
			budget = self.env['itb.plan_spending_int'].search([('id','=',rec.spending_id.id)])
			if budget.used>0:
				budget_start = budget.used
				if budget_start - rec.total_alo > 0:
					budget_now = budget_start - rec.total_alo
				else:
					budget_now=0
				budget.write({'used':budget_now,})
		self.state = 'draft'

	
	@api.multi
	def isi_request(self):
		global stat
		global stat_line
		stat=True
		if self.state=='draft':
			if self.request_line_ids:
				self.request_line_ids.unlink()
				
			ls_kk=['KK Elektronika','KK Informatika','KK Rekayasa Perangkat Lunak dan Pengetahuan','KK Sistem Kendali dan Komputer','KK Teknik Biomedika','KK Teknik Ketenagalistrikan','KK Teknik Komputer','KK Teknik Telekomunikasi','KK Teknologi Informasi']
			kk = self.env['itb.plan_unit'].search([('name','in',ls_kk)])
			kk_id = kk.mapped('id')
			
			if self.unit_id.id in kk_id:
				spending = self.env['itb.plan_spending'].search([('price_id','=',self.price_id.id),('unit_id','=',self.unit_id.id)])
			else:
				spending = self.env['itb.plan_spending'].search([('price_id','=',self.price_id.id),('unit_id','not in',kk_id)])
			
			spen_id = spending.mapped('id')
			actual = self.env['itb.plan_spending_actual'].search([('spending_id','in', spen_id),('state','=','confirm'),('source','=',self.source),('available','>',0)])
			tot_source=sum(actual.mapped('total'))
			self.write({'source_total':tot_source,})
			req_mod = self.env['itb.plan_request_line']
			alo_mod = self.env['itb.plan_request_alocation']
			stat_line = True
			if actual:
				for rec in actual:
					self.request_line_ids.create({
						'request_id' : self.id,
						'spending_actual_id' : rec.id,
						'total' : rec.total,
					})
			stat_line = False
			if self.request_alocation_ids:
				self.request_alocation_ids.unlink()
			
			alo = self.env['itb.plan_spending_int'].search([('unit_id','=',self.unit_id.id),('price_id','=',self.price_id.id),('available','>',0)])
			
			tot_alo=sum(alo.mapped('total'))
			self.write({'alocation_total':tot_alo,})
			if alo:
				for rec in alo:
					
					self.request_alocation_ids.create({
						'request_alo_id' : self.id,
						'spending_id' : rec.id,
						'total_alo' : rec.total,
					})
		#self.request_line_ids.write({'status':False,})
		stat=False

	@api.multi
	def generate_taken(self):
		global stat
		stat=True
		return {
			'name': 'Recomended Taken for Request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_wizard_taken',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj' : self.id},
			}
		stat = False
		
	@api.one
	@api.depends('request_line_ids')
	def _total_budget(self):
		self.source_total = 0
		if self.request_line_ids:
			for payment in self.request_line_ids:
				self.source_total += payment.total
	
	@api.one
	@api.depends('request_alocation_ids')
	def _total_alocation(self):
		self.alocation_total = 0
		if self.request_alocation_ids:
			for payment in self.request_alocation_ids:
				self.alocation_total += payment.total_alo

	@api.constrains('total')
	def _check_below_zero(self):
		global stat
		if stat == False:
			if self.total < 0.01:
				raise models.ValidationError('Total payment is below or equal zero.')

	@api.constrains('source_total')
	def _check_total_source(self):
		global stat
		if stat == False:
			if self.request_line_ids:
				if self.source_total>0:
					if self.total != self.source_total:
						raise models.ValidationError('total taken must have same value with Total payment')

	@api.constrains('alocation_total')
	def _check_total_alocation(self):
		global stat
		if stat == False :
			if self.request_alocation_ids:
				if self.alocation_total>0:
					if self.total != self.alocation_total:
						raise models.ValidationError('total alocation must have same value with Total payment')

	@api.multi
	def _tes(self):
		stats = len(self.id)
		raise osv.except_osv(str(stats))

	'''
	@api.multi
	def unlink(self):
		stats = self.ids
		#for rec in stats:
		if stats:
			record = self.env['itb.plan_request'].search([('id','in',stats)])
			#dat =  self.env['itb.plan_request'].search([('id','not in',stats)]).mapped('id')
			dat = list(set(record.mapped('state')))
			wwe = ', '.join(str(stats))
			if len(dat) == 1:
				if dat[0] == 'draft':
					return super(Request, self).unlink()				
				else:
					raise models.ValidationError('Error1, only state draft can be delete' + dat[0])	
			else:
				raise models.ValidationError('Error3, only state draft can be delete ' + wwe)
		#return super(Request, self).unlink()
	'''
	
	'''
	@api.multi
	def write(self):
		global stat
		stat = False
		return super(Request, self).write()
	
	@api.multi
	def create(self):
		global stat
		stat = False
		return super(Request, self).create()
	'''
class Wizard_Find_Request_child(models.TransientModel):
	_name = 'itb.plan_wizard_find_child'
	
	wiz_find_id = fields.Many2one('itb.plan_wizard_taken', index=True)
	sp_act_id = fields.Many2one('itb.plan_spending_actual', index=True)
	initiative = fields.Char(related='sp_act_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='sp_act_id.unit_id', readonly=True, store=True)
	used = fields.Float(default=0, related='sp_act_id.used', readonly=True, store=True)
	available = fields.Float(default=0, related='sp_act_id.available', readonly=True, store=True)
	month = fields.Selection(related='sp_act_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='sp_act_id.spending_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='sp_act_id.spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='sp_act_id.spending_id.plan_line_id.subactivity_id', readonly=True,store=True)
	spending_id = fields.Many2one(related='sp_act_id.spending_id', readonly=True,store=True)
	price_id = fields.Many2one(related='sp_act_id.price_id', readonly=True,store=True)
	total = fields.Float(default=0)
	parent_id = fields.Char()

class Wizard_Taken(models.TransientModel):
	_name = 'itb.plan_wizard_taken'

	global data_child
	global ret_child
	opr = fields.Boolean(default=True, string="Delete Existing taken and alocation")
	#unit = fields.Boolean(default=True, string="Same Unit")
	#quartal1 = fields.Boolean(default=True, string="Q1")
	#quartal2 = fields.Boolean(default=False, string="Q2")
	#quartal3 = fields.Boolean(default=False, string="Q3")
	#quartal4 = fields.Boolean(default=False, string="Q4")
	sumber = fields.Selection([('1', 'Same unit, same Quarter'), ('2', 'All unit, same Quater'), ('3', 'Same unit, All Quater'),('4', 'All unit, Quater')], 'Source', default='1')
	wiz_find_child_ids = fields.One2many('itb.plan_wizard_find_child', 'wiz_find_id', 'Wizard Child')
	parent_id=fields.Char()
	total = fields.Float(default=0)

	def no(self):
		pass

	def oke(self):
		parent_id=self._context['parent_obj']
		chil = self.env['itb.plan_wizard_find_child'].search([('wiz_find_id','=', self.id),('total','>',0)])
		parent = self.env['itb.plan_request'].search([('id','=',parent_id)])
		if chil :
			tot = sum(chil.mapped('total'))
			if self.total == tot:
				parent.write({'alocation_total':self.total,})
				parent.write({'source_total':self.total,})
				child_taken=self.env['itb.plan_request_line']
				child_alo=self.env['itb.plan_request_alocation']
				for rec in chil:
					child_taken.create({
						'request_id' : parent_id,
						'spending_actual_id':rec.sp_act_id.id,
						'total' : rec.total,
						})
					#self.env['itb.plan_request_line'].create({'request_id' : rec.parent_id.id, 'spending_actual_id' : rec.sp_act_id.id, 'total' : rec.total,})
					alo = self.env['itb.plan_allocation'].search([('spending_id','=',rec.spending_id.id)],limit=1)
					if alo:
						#self.env['itb.plan_request_alocation'].create({'request_alo_id' : rec.parent_id.id, 'spending_id' : alo.spending_id_int.id, 'total_alo' : rec.total,})
						child_alo.create({
							'request_alo_id' : parent_id,
							'spending_id' : alo.spending_id_int.id,
							'total_alo' : rec.total,
							})
			else:
				raise osv.except_osv('Total Request no equal with total Taken')
			
	def isi_all(self):
		parent_id=self._context['parent_obj']
		self.wiz_find_child_ids.unlink()
		parent = self.env['itb.plan_request'].search([('id','=',parent_id)])
		self.write({'parent_id':parent_id, 'total':parent.total,})
		tang = fields.Date.from_string(parent.day)
		dt_start = fields.Date.from_string(str(tang.year) + '-01-01')
		dt_finish = fields.Date.from_string(str(tang.year) + '-04-01') + timedelta(days=-1)
		if (tang >= dt_start and tang <= dt_finish) :
			quar = 'q1'

		dt_start = fields.Date.from_string(str(tang.year) + '-04-01')
		dt_finish = fields.Date.from_string(str(tang.year) + '-07-01') + timedelta(days=-1)
		if (tang >= dt_start and tang <= dt_finish) :
			quar='q2'

		dt_start = fields.Date.from_string(str(tang.year) + '-07-01')
		dt_finish = fields.Date.from_string(str(tang.year) + '-10-01') + timedelta(days=-1)
		if (tang >= dt_start and tang <= dt_finish) :
			quar='q3'

		dt_start = fields.Date.from_string(str(tang.year) + '-10-01')
		dt_finish = fields.Date.from_string(str(int(tang.year) + 1) + '-01-01') + timedelta(days=-1)
		if (tang >= dt_start and tang <= dt_finish) :
			quar='q4'
			
		if self.sumber == '1':
			if quar == 'q1':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-04-01') + timedelta(days=-1)
	
			if quar == 'q2':
				date_start = fields.Date.from_string(str(tang.year) + '-04-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-07-01') + timedelta(days=-1)
	
			if quar == 'q3':
				date_start = fields.Date.from_string(str(tang.year) + '-07-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-10-01') + timedelta(days=-1)
	
			if quar == 'q4':
				date_start = fields.Date.from_string(str(tang.year) + '-10-01')
				date_finish = fields.Date.from_string(str(int(tang.year) + 1) + '-01-01') + timedelta(days=-1)

			act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', parent.unit_id.id), ('price_id', '=', parent.price_id.id), ('source', '=', parent.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state', '=', 'confirm')])
			#tes='a'
		if self.sumber == '2':
			if quar == 'q1':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-04-01') + timedelta(days=-1)
	
			if quar == 'q2':
				date_start = fields.Date.from_string(str(tang.year) + '-04-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-07-01') + timedelta(days=-1)
	
			if quar == 'q3':
				date_start = fields.Date.from_string(str(tang.year) + '-07-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-10-01') + timedelta(days=-1)
	
			if quar == 'q4':
				date_start = fields.Date.from_string(str(tang.year) + '-10-01')
				date_finish = fields.Date.from_string(str(int(tang.year) + 1) + '-01-01') + timedelta(days=-1)
	
			act = self.env['itb.plan_spending_actual'].search([('price_id', '=', parent.price_id.id), ('source', '=', parent.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state', '=', 'confirm')])
			#tes='b'
		if self.sumber == '3':
			if quar == 'q1':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-04-01') + timedelta(days=-1)
	
			if quar == 'q2':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-07-01') + timedelta(days=-1)
	
			if quar == 'q3':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-10-01') + timedelta(days=-1)
	
			if quar == 'q4':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(int(tang.year) + 1) + '-01-01') + timedelta(days=-1)
	
			act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', parent.unit_id.id), ('price_id', '=', parent.price_id.id), ('source', '=', parent.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state', '=', 'confirm')])
			#tes='c'
		if self.sumber == '4':
			if quar == 'q1':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-04-01') + timedelta(days=-1)
	
			if quar == 'q2':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-07-01') + timedelta(days=-1)
	
			if quar == 'q3':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(tang.year) + '-10-01') + timedelta(days=-1)
	
			if quar == 'q4':
				date_start = fields.Date.from_string(str(tang.year) + '-01-01')
				date_finish = fields.Date.from_string(str(int(tang.year) + 1) + '-01-01') + timedelta(days=-1)
	
			act = self.env['itb.plan_spending_actual'].search([('price_id', '=', parent.price_id.id), ('source', '=', parent.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state', '=', 'confirm')])
		
		if act :
			for rec in act:
				self.wiz_find_child_ids.create({'wiz_find_id':self.id,'sp_act_id':rec.id,'total':0,'parent_id':parent_id,})
		
		return {
			'name': 'Send DKO to request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_wizard_taken',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
			'context': {'parent_obj': self._context['parent_obj']},
			'flags': {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}},
		}

	
class Request_Line(models.Model):
	_name = 'itb.plan_request_line'

	global stat_line
	request_id = fields.Many2one('itb.plan_request',ondelete='cascade',required=True,index=True)
	spending_actual_id = fields.Many2one('itb.plan_spending_actual',ondelete='cascade',required=True,index=True)
	initiative = fields.Char(related='spending_actual_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='spending_actual_id.unit_id', readonly=True, store=True)
	used = fields.Float(related='spending_actual_id.used', readonly=True, store=True)
	available=fields.Float(related='spending_actual_id.available', readonly=True, store=True)
	month=fields.Selection(related='spending_actual_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.subactivity_id', readonly=True, store=True)
	total = fields.Float(default=0)
	stat_line = False

	'''
	@api.multi
	def create(self, vals):
		stat_line=True
		return super(Request_Line, self).create(vals)
	'''
	
	def _available_budget(self):
		budget = self.env['itb.plan_spending_actual'].browse(self.spending_actual_id.id)
		return float(self.spending_actual_id.id)
	
	@api.multi
	@api.onchange('spending_actual_id')
	def filter_spending(self):
		res = dict()
		ls_kk=['KK Elektronika','KK Informatika','KK Rekayasa Perangkat Lunak dan Pengetahuan','KK Sistem Kendali dan Komputer','KK Teknik Biomedika','KK Teknik Ketenagalistrikan','KK Teknik Komputer','KK Teknik Telekomunikasi','KK Teknologi Informasi']
		kk = self.env['itb.plan_unit'].search([('name','in',ls_kk)])
		kk_id = kk.mapped('id')
		#if self.request_id.unit_id.id in kk_id:
		#	spending = self.env['itb.plan_spending'].search([('price_id','=',self.request_id.price_id.id),('unit_id','=',request_id.unit_id.id)])
		#else:
		#	spending = self.env['itb.plan_spending'].search([('price_id','=',self.request_id.price_id.id),('unit_id','not in',kk_id)])
		#spen_id = spending.mapped('id')
		
		if self.request_id.unit_id.id in kk_id:
			actual = self.env['itb.plan_spending_actual'].search([('unit_id.id','=', request_id.unit_id.id),('price_id.id','=',self.request_id.price_id.id),('state','=','confirm'),('source','=',self.request_id.source),('available','>',0)])
		else:
			actual = self.env['itb.plan_spending_actual'].search([('unit_id.id','not in', kk_id),('price_id.id','=',self.request_id.price_id.id),('state','=','confirm'),('source','=',self.request_id.source),('available','>',0)])
		#actual = self.env['itb.plan_spending_actual'].search([('spending_id','in', spen_id),('state','=','confirm'),('source','=',self.request_id.source),('available','>',0)])
		spending_actual_ids=actual.mapped('id')
		res['domain'] = {'spending_actual_id': [('id', 'in', spending_actual_ids)]}
		return res
	
	@api.constrains('total')
	def _check_below_zero(self):
		if self.total < 0.01:
			raise models.ValidationError('Total taken is below or equal zero.')
	
	@api.constrains('total')
	def _check_total(self):
		global stat_line
		if stat_line == True :
			if self.total > (self.available):
				raise models.ValidationError('Total taken is over then available.')
	

class Request_Alocation(models.Model):
	_name = 'itb.plan_request_alocation'

	request_alo_id = fields.Many2one('itb.plan_request',ondelete='cascade',required=True,index=True)
	spending_id = fields.Many2one('itb.plan_spending_int',ondelete='cascade',required=True,index=True)
	initiative_alo = fields.Char(related='spending_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='spending_id.unit_id', readonly=True, store=True)
	#type_alo = fields.Selection(related='spending_id.type')
	used_alo = fields.Float(related='spending_id.used', readonly=True, store=True)
	available_alo = fields.Float(related='spending_id.available', readonly=True,store=True)
	month=fields.Selection(related='spending_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='spending_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='spending_id.plan_line_id.subactivity_id', readonly=True, store=True)
	total_alo = fields.Float(default=0)
	
	
	def _available_budget(self):
		budget = self.env['itb.plan_spending_int'].browse(self.spending_id.id)
		return float(self.spending_id.id)
	
	@api.multi
	@api.onchange('spending_id')
	def filter_spending_id(self):
		res = dict()
		spending = self.env['itb.plan_spending_int'].search([('unit_id','=',self.request_alo_id.unit_id.id),('price_id','=',self.request_alo_id.price_id.id),('available','>',0)])
		spending_ids=spending.mapped('id')
		res['domain'] = {'spending_id': [('id', 'in', spending_ids)]}
		return res

	@api.constrains('total_alo')
	def _check_below_zero(self):
		if self.total_alo < 0.01:
			raise models.ValidationError('Total Alocation is below or equal zero.')
	

class Request_Tax(models.Model):
	_name = 'itb.plan_request_tax'

	request_id = fields.Many2one('itb.plan_request',ondelete='cascade',index=True)
	tax_id = fields.Many2one('itb.plan_tax',ondelete='cascade',required=True,index=True)
	tax_percent = fields.Float(related='tax_id.percent', readonly=True, store=True)
	note = fields.Char()
	amount = fields.Float(default=0, required=True)
	dko_id = fields.Many2one('itb.plan_dko',ondelete='cascade',index=True)
	
	@api.multi
	@api.onchange('tax_id')
	def filter_tax_id(self):
		for rec in self:
			if rec.amount==0:
				if rec.request_id:
					rec.amount = rec.request_id.total * (rec.tax_percent/100)
				elif rec.dko_id:
					rec.amount = rec.dko_id.total * (rec.tax_percent/100)
		
	@api.constrains('amount')
	def _check_below_zero(self):
		for rec in self:
			if rec.amount < 0.01:
				raise models.ValidationError('Amount tax is below or equal zero.')

class Bank(models.Model):
	_name = 'itb.plan_bank'

	name = fields.Char('Bank', required=True, index=True)
	no_rek = fields.Char('No Rekening', required=True)
	note = fields.Char()

class Statement_line(models.Model):
	_name = 'itb.plan_bank_statement_line'
	_rec_name='statement_id'

	type = fields.Selection([('reimburse','Reimburse'),('saldoawal', 'Saldo Awal')], 'Type',default='reimburse')
	statement_id = fields.Many2one('itb.plan_bank_statement',ondelete='cascade', index=True)
	reimburse_id = fields.Many2one('itb.plan_reimburse',ondelete='cascade', index=True)
	amount = fields.Float(default=0, required=True)
	note=fields.Char()

	@api.multi
	@api.onchange('reimburse_id')
	def filter_reimburse(self):
		for rec in self:
			if rec.type == 'reimburse':
				reim = self.env['itb.plan_reimburse'].search([('id','=', self.reimburse_id.id)])
				if reim:
					total=0
					for rec in reim.plan_request_ids:
						total += rec.total
					self.amount=total

class Statement(models.Model):
	_name = 'itb.plan_bank_statement'
	_rec_name='bank'

	#bank_id = fields.Many2one('itb.plan_bank',ondelete='cascade',required=True,index=True)
	bank = fields.Char(string='Bank',required=True,index=True)
	date_in = fields.Date(default=date.today())
	reference = fields.Char()
	amount = fields.Float(compute='_total_amount',default=0, store=True, readonly=True)
	used = fields.Float(compute='_total_used',default=0, store=True, readonly=True)
	available = fields.Float(compute='_total_available', default=0, store=True, readonly=True)
	note=fields.Char()
	request_dko_ids = fields.One2many('itb.plan_dko', 'statement_id_dko', 'Statement', copy=True, domain=([('state_req','in',[False,'confirm','validate'])]))
	reimburse_ids = fields.One2many('itb.plan_bank_statement_line', 'statement_id', 'Statement', copy=True)

	#@api.one
	@api.depends('request_dko_ids')
	def _total_used(self):
		for record in self:
			record.used = 0
			if record.request_dko_ids:
				for payment in record.request_dko_ids:
					record.used += payment.total
	
	@api.depends('reimburse_ids')
	def _total_amount(self):
		for record in self:
			record.amount = 0
			if record.reimburse_ids:
				for payment in record.reimburse_ids:
					record.amount += payment.amount
	
	@api.depends('amount','used')
	def _total_available(self):
		for record in self:
			record.available = record.amount - record.used
	
class Tax(models.Model):
	_name = 'itb.plan_tax'

	name = fields.Char('Tax', required=True, index=True)
	percent = fields.Float('percent tax', required=True)
	note = fields.Char()

class Send_to_reimburse(models.TransientModel):
	_name = 'itb.plan_send_reimburse'
	existing = fields.Boolean(default=False)
	reimburse_id = fields.Many2one('itb.plan_reimburse', string='Reimburse')

	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		part_id = self._context['parent_id']
		parent = self.env['itb.plan_request'].search([('id','in',part_id)])
		
		reim = self.env['itb.plan_reimburse']
		tgl=date.today()
		if self.existing == False:
			nama = 'Reimburse - (' + str(tgl.year) + '-' + str(tgl.month) + '-' + str(tgl.day) + ')'
			reim.create({'name':nama, 'date_reimburse' : tgl, 'state' : 'draft',})
			reimburse = self.env['itb.plan_reimburse'].search([('name','=', nama),('date_reimburse','=',tgl),('state','=','draft')],order='id desc', limit=1)
			reim_id = reimburse.id
		else :
			reim_id = self.reimburse_id.id
		
		
		if reim_id:
			#raise osv.except_osv(str(reim_id))
			parent.write({'reimburse_id':reim_id, 'is_reconciled':True,})
		else:
			raise osv.except_osv('Not Valid Data Reimbuse Not Selected')
		