from odoo import models, fields, api, exceptions
from datetime import date
from odoo.osv import osv
from datetime import datetime
#from datetime import monthdelta
from dateutil.relativedelta import relativedelta

class Spending_Actual(models.Model):
	_name = 'itb.plan_spending_actual'
	
	spending_id = fields.Many2one('itb.plan_spending',ondelete='cascade',required=True,index=True)
	plan_line_id = fields.Many2one('itb.plan_line',related='spending_id.plan_line_id',readonly=True, store=True ,index=True)
	name = fields.Char(related='spending_id.price_id.name', readonly=True, store=True ,index=True)
	code = fields.Char(related='spending_id.code', store=True)#, readonly=True)
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', required=True,store=True, index=True)
	day = fields.Date(related='spending_id.day', store=True ,index=True)#, readonly=True)
	standard = fields.Char(related='spending_id.standard', readonly=True, store=True)
	price = fields.Float(related='spending_id.price',default=0, readonly=True, store=True)
	volume = fields.Float(compute='_sum_volume', store=True, readonly=True, default=0)
	total = fields.Float(default=0)
	used = fields.Float(readonly=True, default=0)
	available = fields.Float(compute='_sum_available', store=True, readonly=True)
	paid = fields.Float(readonly=True, default=0)
	percent_budget = fields.Float(compute='_recalculate_percent_budget',store=True, readonly=True, default=0)
	active = fields.Boolean(default=True)#,readonly=True)
	previus_month = fields.Char(store=True)#, readonly=True)
	confirmation_ref = fields.Char(string="No Fra Reference")#,readonly=True)
	confirmation_date = fields.Date(string='Fra Date')#,readonly=True)
	confirmation_note = fields.Char(string='Fra Note')#,readonly=True)
	state=fields.Selection([('draft','Draft'),('confirm','FRA')], 'Status',default='draft', required=True, copy=False ,index=True)#, readonly=True)
	
	
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', related='spending_id.type', readonly=True, store=True, index=True)
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source')#, readonly=True)
	price_id = fields.Many2one('itb.plan_price',related='spending_id.price_id',ondelete='cascade',index=True,store=True)
	
	plan_id = fields.Many2one('itb.plan',related='spending_id.plan_id',ondelete='cascade',index=True,store=True)
	implementation_id = fields.Many2one('itb.plan_implementation',ondelete='cascade',required=True,index=True)
	#confirmation_id = fields.Many2one('itb.plan_confirmation',ondelete='cascade',index=True)
	request_line_ids = fields.One2many('itb.plan_request_line', 'spending_actual_id', 'Request Line', index=True)
	user_ids = fields.Many2many('res.users')
	unit_id = fields.Many2one('itb.plan_unit',related='plan_line_id.unit_id',index=True, readonly=True, store=True)
	logistic = fields.Boolean(string='Logistic', default=False, store=True)#, readonly=True)
	previus_source = fields.Char(store=True, readonly=True)
	#dko_line_ids = fields.One2many('itb.plan_dko_line', 'actual_id', 'dko request', index=True, copy=True)
	#umk_line_ids = fields.One2many('itb.plan_spending_actual_umk', 'spending_actual_id', 'umk Line', index=True)
	program_id = fields.Many2one('itb.plan_program', related='plan_line_id.program_id', readonly=True, store=True ,index=True)
	activity_id = fields.Many2one('itb.plan_activity', related='spending_id.plan_line_id.activity_id', readonly=True, store=True ,index=True)
	subactivity_id = fields.Many2one('itb.plan_subactivity', related='spending_id.plan_line_id.subactivity_id', readonly=True, store=True ,index=True)
	year=fields.Float(default=0)


	@api.multi
	def set_confirmed_actual(self):
		st = self.env['itb.plan_spending_actual'].search([('state','!=','confirm')])
		st.write({'state':'confirm'})

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
	def set_confirmation(self, cr, uid, ids, context=None):
		sumber = self.env['itb.plan_bulan_confirmatihon'].search([])
		if sumber:
			sumber.unlink()
		sumber = self.env['itb.plan_bulan_confirmation']
		dic = {'Jan':'1', 'Feb':'1', 'Mar':'1', 'Apr':'2', 'May':'2', 'Jun':'2', 'Jul':'3', 'Aug':'3', 'Sep':'3', 'Oct':'4', 'Nov':'4', 'Dec':'4'}
		dic2 = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
		dt = {'1':'1', '2':'1', '3':'1', '4':'2', '5':'2', '6':'2', '7':'3', '8':'3', '9':'3', '10':'4', '11':'4', '12':'4'}
		dt2 = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, '11':11, '12':12}
		active_ids = self._context.get('active_ids')
		act = self.env['itb.plan_spending_actual'].search([('id','in',active_ids),('state','=','draft')])
		active=act.mapped('id')
		bulan = list(set(act.mapped('month')))
		bln = []
		bl=[]
		tgl = date.today()
		
		for rec in bulan:
			if rec in ['Jan','Feb','Mar']:
				bln.append('q1')
			if rec in ['Apr','May','Jun']:
				bln.append('q2')
			if rec in ['Jul','Aug','Sep']:
				bln.append('q3')
			if rec in ['Oct','Nov','Dec']:
				bln.append('q4')

		bul = list(set(bln))
		#raise models.ValidationError(str(len(bul))+' || '+str(bln)+' || '+str(bulan))
		if len(bul)>1:
			raise models.ValidationError('confirmation only can be proses in same quarter only')
		
		buln = dt[str(tgl.month)]
		bb=tgl.month
		cc=[]
		for rec in bulan:
			bl.append(dic[rec])
			cc.append(dic2[rec])

		dd=max(cc)
		if int(buln) >= int(bl[0]):
			if int(buln) > int(bl[0]):
				if int(bl[0])==1:
					bulan = ['Jan','Feb','Mar']
				if int(bl[0])==2:
					bulan = ['Apr','May','Jun']
				if int(bl[0])==3:
					bulan = ['Jul','Aug','Sep']
				if int(bl[0])==4:
					bulan = ['Oct','Nov','Dec']
			elif int(buln) == int(bl[0]):
				if int(bl[0])==1:
					if dd==1:
						bulan = ['Jan']
					if dd==2:
						bulan = ['Jan','Feb']
					if dd==3:
						bulan = ['Jan','Feb','Mar']
				if int(bl[0])==2:
					if dd==4:
						bulan = ['Apr']
					if dd==5:
						bulan = ['Apr','May']
					if dd==6:
						bulan = ['Apr','May','Jun']
				if int(bl[0])==3:
					if dd==7:
						bulan = ['Jul']
					if dd==8:
						bulan = ['Jul','Aug']
					if dd==9:
						bulan = ['Jul','Aug','Sep']
				if int(bl[0])==4:
					if dd==10:
						bulan = ['Oct']
					if dd==11:
						bulan = ['Oct','Nov']
					if dd==12:
						bulan = ['Oct','Nov','Dec']

			for rec in bulan:
				sumber.create({'bulan':rec,})
		else:
			raise models.ValidationError('confirmation in over quarter not allowed')

		return {
			'name': 'Set Confirmation',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_confirmation_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': active},
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
	
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source', default='dm')
	
	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		if self.source in ['dm','boptn']:
			parent_id=self._context['parent_id']
			act =  self.env['itb.plan_spending_actual'].search([('id','in',parent_id),('state','=','confirm')])
			if act:
				for rec in act:
					cek = self.env['itb.plan_implementation'].search([('id','=',rec.implementation_id.id)])
					tes = len(rec.request_line_ids)
					if tes == 0:
						if cek.state == 'validate':
							ret = rec.write({
								'previus_source':rec.source,
								'source':self.source,
								})
class Bulan_Confirmation(models.TransientModel):
	_name = 'itb.plan_bulan_confirmation'
	_rec_name = 'bulan'

	bulan = fields.Char()

class Confirmation_Wizard(models.TransientModel):
	_name = 'itb.plan_confirmation_wizard'
	
	confirmation_ref = fields.Char(string="No Fra Reference", required=True)
	confirmation_date = fields.Date(default=date.today(), string='Fra Date')
	confirmation_note = fields.Char(string='Fra Note')
	state=fields.Selection([('draft','Draft'),('confirm','Confirmed')], default='confirm' ,string='Status',required=True)
	#month = fields.Many2one('itb.plan_bulan_confirmation', required=True, string='Month')
	month = fields.Many2one('itb.plan_bulan_confirmation', string='Month')
	
	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		parent_id = self._context['parent_obj']
		dic = {'Jan':'1', 'Feb':'1', 'Mar':'1', 'Apr':'2', 'May':'2', 'Jun':'2', 'Jul':'3', 'Aug':'3', 'Sep':'3', 'Oct':'4', 'Nov':'4', 'Dec':'4'}
		dic2 = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
		dt = {'1':'1', '2':'1', '3':'1', '4':'2', '5':'2', '6':'2', '7':'3', '8':'3', '9':'3', '10':'4', '11':'4', '12':'4'}
		dt2 = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
		if parent_id:
			for rec in parent_id:
				old_month=''
				new_month=''
				actual =  self.env['itb.plan_spending_actual'].search([('id','=',rec),('state','=','draft')])
				cek = self.env['itb.plan_implementation'].search([('id','=',actual.implementation_id.id)])
				if actual.month:
					old_month = dic[actual.month]
				if self.month:
					new_month = dic[self.month.bulan]
				if old_month > new_month:
					raise osv.except_osv('only can select confirmation month newest or same then actual month')
				if cek.state == 'validate':
					for rec in actual:
						hr = fields.Date.from_string(rec.day)
						mon = hr.month
						mon2 = int(dic2[self.month.bulan])
						if mon2>mon:
							sel = mon2-mon
						else:
							sel = mon-mon2
						tgl = hr + relativedelta(months=sel)
						ret = rec.write({
							'confirmation_ref':self.confirmation_ref,
							'confirmation_date':self.confirmation_date,
							'confirmation_note':self.confirmation_note,
							'state':self.state,
							'month':self.month.bulan,
							'day':tgl,
							'previus_month':rec.month,
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
	reference = fields.Char(required=True)
	#request_id = fields.Many2one('itb.plan_request', index=True)
	day = fields.Date(default=date.today())
	due = fields.Date(default=date.today())
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
			actual = self.env['itb.plan_spending_actual'].search([('id','in',parent_id),('state','=','confirm'),('available','>',0),('logistic','=',False)])
			if actual:
				rec_total = sum(actual.mapped('total'))
				actual.write({
					'logistic' : True,
				})
				plan_req = self.env['itb.plan_request']
				req_line = self.env['itb.plan_request_line']
				req_alo = self.env['itb.plan_request_alocation']
				for rec in actual:
					unit=self.env['itb.plan_unit'].search([('id','=',rec.unit_id.id)])
					#if unit:
					#	self.name = self.name + ' - (' + str(rec.price_id.id) + ') ' + str(unit.name)
					self.name = 'Logistik : ' + self.reference
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
						'is_reconciled' : False,
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