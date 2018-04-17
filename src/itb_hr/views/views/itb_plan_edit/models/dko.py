from odoo import models, fields, api, exceptions, tools
from odoo.osv import osv
from datetime import date
from datetime import timedelta
from datetime import datetime


# global stat_dko
global data_child
global ret_child

class Request_Dko(models.Model):
	_name = 'itb.plan_dko'
	_rec_name = 'pay_to'
	# global stat_dko

	name = fields.Char(index=True)
	reference = fields.Char()
	day = fields.Date(default=date.today() ,index=True)
	due = fields.Date(default=date.today())
	total = fields.Float(default=0)
	is_reconciled = fields.Boolean()
	note = fields.Text()
	# source_total = fields.Float(default=0, compute='_total_budget', store=True, readonly=True)
	# alocation_total = fields.Float(default=0, compute='_total_alocation', store=True, readonly=True)
	state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('paid', 'Paid')], 'Status',default='draft', required=True, readonly=True, copy=False ,index=True)
	unit_id = fields.Many2one('itb.plan_unit', ondelete='cascade', required=True, index=True)
	pay_to = fields.Many2one('res.partner', ondelete='cascade', required=True, index=True)
	dkotaken_ids = fields.One2many('itb.plan_dko_taken', 'dko_taken_id', 'Dko Taken', copy=True)
	dkoalo_ids = fields.One2many('itb.plan_dko_allocation', 'dko_alo_id', 'Dko Alocation', copy=True)
	price_id = fields.Many2one('itb.plan_price', ondelete='cascade', required=True, index=True)
	source = fields.Selection([('dm', 'Dana Masyarakat'), ('boptn', 'BOPTN')], 'Source', default='dm' ,index=True)
	tax_ids = fields.One2many('itb.plan_request_tax', 'request_id', 'Tax Request', copy=True)
	#cash_advance = fields.Boolean(default=False)
	cash_id = fields.Many2one('itb.plan_cash_advance', string='Cash Advance', index=True, ondelete='cascade')
	faktur = fields.Boolean(default=True, string='Receipt')
	date_process = fields.Date(readonly=True)
	statement_id_dko = fields.Many2one('itb.plan_bank_statement', index=True)
	rekening = fields.Float(related='statement_id_dko.available', readonly=True, store=True)
	request_id = fields.Many2one('itb.plan_request', ondelete='cascade', index=True)
	reimburse_id = fields.Many2one('itb.plan_reimburse', related='request_id.reimburse_id', readonly=True, store=True ,index=True)
	state_req = fields.Selection(related='request_id.state', readonly=True, store=True)
	t_taken = fields.Float(default=0,compute='_get_taken',store=True,readonly=True)
	
	@api.multi
	def set_confirmed_dko(self):
		st = self.env['itb.plan_dko'].search([('state','!=','confirm')])
		st.write({'state':'confirm'})

	@api.multi
	def set_validate_dko(self):
		st = self.env['itb.plan_dko'].search([('state','!=','validate')])
		st.write({'state':'validate'})
	
	@api.one
	@api.depends('dkotaken_ids')
	#@api.onchange('dkotaken_ids')
	def _get_taken(self):
		self.t_taken = 0
		if self.dkotaken_ids:
			for payment in self.dkotaken_ids:
				self.t_taken += payment.tot_taken
	# stat_dko = False

	@api.constrains('statement_id_dko')
	def cek_available_bank(self):
		for rec in self:
			if rec.total > rec.statement_id_dko.available:
				raise models.ValidationError('Available in Bank not Enough')
	
	@api.multi
	def action_payment_req_confirmed(self):
		self.state = 'confirm'

		
	@api.multi
	def action_payment_req_paid(self):
		self.state = 'paid'


	@api.multi
	def action_payment_req_validate(self):
		self.state = 'validate'
		
	@api.multi
	def action_payment_req_abort(self):
		self.state = 'draft'

	
	@api.multi
	def set_dko_lines(self):
		stats = self.ids
		pr = self.env['itb.plan_dko'].search([('id', 'in', stats)])
		unitid = list(set(pr.mapped('unit_id.id')))
		unit = unitid
		if unit:
			if len(unit) > 1 :
				raise models.ValidationError('only can select in same unit dko ' + str(len(unit)))

		priceid = list(set(pr.mapped('price_id.id')))
		price = priceid
		if price:
			if len(price) > 1:
				raise models.ValidationError('only can select in same price')

		sourceid = list(set(pr.mapped('source')))
		source = sourceid
		if source:
			if len(source) > 1:
				raise models.ValidationError('only can select in same source')
		return {
			'name': 'Send DKO to request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_dko_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_id': self.active_ids},
		}
	
	@api.multi
	def sendrequest(self):
		footer=self.env['itb.plan_dko_wizard_child'].search([])
		header=self.env['itb.plan_dko_wizard'].search([])
		footer.unlink()
		header.unlink()
		return {
			'name': 'Send DKO to request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_dko_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_id': self.ids},
		}
	
	@api.multi
	def split_price(self):
		if self.dkoalo_ids:
			
			target=self.env['itb.plan_dko_wizard_split']
			target.create({'name': 'wiz-split ' + str(self.id),})
			tgr = self.env['itb.plan_dko_wizard_split'].search([('name','=','wiz-split ' + str(self.id))],limit=1,order='id desc')
			target_child = self.env['itb.plan_dko_price_wizard_child']
			
			if tgr:
				for rec in self.dkoalo_ids:
					#raise models.ValidationError(str(rec.unit_id.id))
					target_child.create({'dko_price_wiz_id':tgr.id, 'unit_id':rec.unit_id.id,})
			
				return {
					'name': 'Split Price For STEI',
					'type': 'ir.actions.act_window',
					'res_model': 'itb.plan_dko_wizard_split',
					'view_mode': 'form',
					'view_type': 'form',
					'target': 'new',
					'context': {'parent_id': self.id},
					'res_id': tgr.id,
					'flags': {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}},
				}
		else:
			raise models.ValidationError('No Data STEI can be split')


	@api.multi
	def mismatch_price(self):
		if self.dkotaken_ids:
			target=self.env['itb.plan_dko_wizard_mismatch']
			target.create({'name': 'wiz-missmatch ' + str(self.id),})
			tgr = self.env['itb.plan_dko_wizard_mismatch'].search([('name','=','wiz-missmatch ' + str(self.id))],limit=1,order='id desc')
			target_child = self.env['itb.plan_dko_wizard_mismatch_child']
			if tgr:
				for rec in self.dkotaken_ids:
					target_child.create({'dko_missmatch_wiz_id':tgr.id, 'spending_actual_id':rec.actual_id.id,'total':rec.tot_taken})

				return {
					'name': 'Mismatch Price For ITB',
					'type': 'ir.actions.act_window',
					'res_model': 'itb.plan_dko_wizard_mismatch',
					'view_mode': 'form',
					'view_type': 'form',
					'target': 'new',
					'context': {'parent_id': self.id},
					'res_id': tgr.id,
					'flags': {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}},
				}
		else:
			raise models.ValidationError('No Data ITB can be mismatch')

class Send_to_Statement(models.TransientModel):
	_name = 'itb.plan_send_dko_statement'

	statement_id = fields.Many2one('itb.plan_bank_statement', required=True, index=True)

	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		part_id = self._context['parent_id']
		parent = self.env['itb.plan_dko'].search([('id','in',part_id)])
		line = self.env['itb.plan_bank_statement_dko_line']
		for rec in parent:
			line.create({'statement_id_dko' : self.statement_id.id, 'dko_id' : rec.id, 'amount':rec.total, })
		
class dko_line(models.Model):
	_name = 'itb.plan_bank_statement_dko_line'
	_rec_name='statement_id'

	statement_id = fields.Many2one('itb.plan_bank_statement',ondelete='cascade', index=True)
	dko_id = fields.Many2one('itb.plan_dko',ondelete='cascade', index=True)
	amount = fields.Float(default=0, required=True)
	note = fields.Char()

class Reimburse(models.Model):
	_name = 'itb.plan_reimburse'
	
	name = fields.Char()
	plan_request_ids = fields.One2many('itb.plan_request', 'reimburse_id', 'Reimburse', copy=True, ondelete='cascade')
	date_reimburse = fields.Date(default=date.today())
	state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('paid', 'Paid'), ('reconcile', 'Reconcile')], 'Status',default='draft', required=True, copy=False)#, readonly=True)
	total = fields.Float(default=0,compute='_get_total',store=True)
	note = fields.Char()
	
	@api.one
	@api.depends('plan_request_ids')
	def _get_total(self):
		for rec in self:
			rec.total = 0
			if rec.plan_request_ids:
				for payment in rec.plan_request_ids:
					rec.total += payment.total

	@api.multi
	def action_payment_req_confirmed(self):
		#self.plan_request_ids.write({'state':'confirm',})
		self.state = 'confirm'

		
	@api.multi
	def action_payment_req_paid(self):
		self.plan_request_ids.write({'state':'paid',})
		self.state = 'paid'
		rec = self.env['itb.plan_dko'].search([('reimburse_id', '=', self.id)])
		if rec:
			rec.write({'state':'paid'})


	@api.multi
	def action_payment_req_validate(self):
		self.state = 'validate'
		self.plan_request_ids.write({'state':'validate',})
		rec = self.env['itb.plan_dko'].search([('reimburse_id', '=', self.id)])
		if rec:
			rec.write({'state':'validate'})

	@api.multi
	def action_payment_req_abort(self):
		self.state = 'draft'
	
	@api.multi
	def action_payment_req_reconcile(self):
		self.state = 'reconcile'


class Dko_Wizard(models.TransientModel):
	_name = 'itb.plan_dko_wizard'

	sumber = fields.Selection([('1', 'Same unit, same Quarter'), ('2', 'All unit, same Quarter'), ('3', 'Same unit, All Quarter'),('4', 'All unit, Quarter')], 'Source', default='1')
	dko_wiz_child_ids = fields.One2many('itb.plan_dko_wizard_child', 'dko_wiz_id', 'ITB')
	
	def no(self):
		pass

	def oke(self):
		#global data_child
		#global ret_child
		#if ret_child == True:
		stat_line=True
		grp = self.env['itb.plan_group_dko'].search([])
		child_taken = self.env['itb.plan_dko_taken']
		child_alo = self.env['itb.plan_dko_allocation']

		parent_request = self.env['itb.plan_request']
		child_taken_request = self.env['itb.plan_request_line']
		child_alo_request = self.env['itb.plan_request_alocation']
		wizchild = self.env['itb.plan_dko_wizard_child'].search([('dko_wiz_id','=',self.id)])
		sp_id =list(set(wizchild.mapped('sp_act_id.id')))
		par_id=list(set(wizchild.mapped('parent_id.id')))
		for rec in wizchild:
			child_taken.create({'dko_taken_id':rec.parent_id.id, 'actual_id':rec.sp_act_id.id, 'tot_taken':rec.total,})
			actual=self.env['itb.plan_spending_actual'].search([('id','=',rec.sp_act_id.id),('state','=','confirm')])
			actual_start = actual.used
			if actual_start + rec.total <= actual.total:
				actual_now = actual_start + rec.total
			else:
				actual_now = actual.total
			actual.write({'used':actual_now,})

			actual_s = self.env['itb.plan_spending'].search([('id','=',actual.spending_id.id)])
			actual_s.write({'used':actual_now,})
		'''
			budget_start=0
			budget_now=0
			alo = self.env['itb.plan_allocation'].search([('spending_id','=',actual.spending_id.id)])
			child_alo.create({'dko_alo_id':rec.parent_id.id, 'dko_spen_id':alo.spending_id_int.id, 'total_alo':rec.total,})
			if alo:
				budget = self.env['itb.plan_spending_int'].search([('id','=',alo.spending_id_int.id)])
				budget_start = budget.used
				if budget_start + rec.total <= budget.total:
					budget_now = budget_start + rec.total
				else:
					budget_now = budget.total
				budget.write({'used':budget_now,})
		'''
		
		pr = self.env['itb.plan_dko'].search([('id','in',par_id)])
		a=0
		b=0
		if len(pr) > 0 :
			for rec in pr:
				
				ztot = rec.total
				thn = fields.Date.from_string(rec.day).year
				bln = fields.Date.from_string(rec.day).month
				date_start_current = fields.Date.from_string(str(thn) + '-' + str(bln) + '-01')
				if bln < 12:
					date_finish_current = fields.Date.from_string(str(thn) + '-' + str(bln+1) + '-01') + timedelta(days=-1)
				else:
					date_finish_current = fields.Date.from_string(str(thn+1) + '-01-01') + timedelta(days=-1)
				date_finish_quarter = date_finish_current
				date_finish_all = date_finish_current
				date_start_all = fields.Date.from_string(str(thn) + '-01-01')
				if bln in [1,2,3]:
					date_start_quarter = fields.Date.from_string(str(thn) + '-01-01')
				if bln in [4,5,6]:
					date_start_quarter = fields.Date.from_string(str(thn) + '-04-01')
				if bln in [7,8,9]:
					date_start_quarter = fields.Date.from_string(str(thn) + '-07-01')
				if bln in [10,11,12]:
					date_start_quarter = fields.Date.from_string(str(thn) + '-10-01')
				
				'''
				langk = 0
				alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('price_id.id','=',rec.price_id.id),('day', '>=', date_start_current), ('day', '<=', date_finish_current)], order= 'day asc')
				langk = 1
				if len(alo)==0:
					alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('price_id.id','=',rec.price_id.id),('day', '>=', date_start_quarter), ('day', '<=', date_finish_quarter)], order= 'day desc')
					langk = 2
					if len(alo)==0:
						alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('price_id.id','=',rec.price_id.id),('day', '>=', date_start_all), ('day', '<=', date_finish_all)], order= 'day desc')
						langk = 3
						if len(alo)==0:
							alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('day', '>=', date_start_current), ('day', '<=', date_finish_current)], order= 'day asc', limit=1)
							langk = 4
							if len(alo)==0:
								alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('day', '>=', date_start_quarter), ('day', '<=', date_finish_quarter)], order= 'day desc',limit=1)
								langk = 5
								if len(alo)==0:
									alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('day', '>=', date_start_all), ('day', '<=', date_finish_all)], order= 'day desc',limit=1)
									langk = 6
									if len(alo)==0:
										langk = 0
										raise models.ValidationError('this unit dont have spending anymore')
				'''
				alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('price_id.id','=',rec.price_id.id),('day', '>=', date_start_all), ('day', '<=', date_finish_all)], order= 'day desc')
				st1=False
				st2=False
				st3=False
				a=0
				b=0
				total_sementara=0
				dt2=[]
				#if langk in [1,2,3]:
				if len(alo)>0:
					#dat=[]
					if len(alo) == 1:
						child_alo.create({'dko_alo_id':rec.id, 'dko_spen_id':alo[0].id, 'total_alo':ztot,})
						budget_now = alo[0].used + rec.total
						alo[0].write({'used':budget_now,})
						ztot = 0
					else:
						if len(alo) > 1:
							budget = sum(alo.mapped('available'))

							#raise models.ValidationError(str(ztot) + '||' +str(pr) + '||' +str(langk) + '||' + str(alo) + '||' + str(budget))
							if budget > 0:
								while ztot > 0:
									for ret in [z for z in alo if z.id not in dt2] :
										if b == 0:
											b = ret.available
											total_sementara += ret.available

										if st1 == False :
											if b >= ztot:
												b = b - ztot
												if ztot > 0:
													child_alo.create({'dko_alo_id':rec.id, 'dko_spen_id':ret.id, 'total_alo':ztot,})
												budget_now = ret.used + ztot
												ret.write({'used':budget_now,})
												ztot=0
												st1 = True
											else:
												ztot = ztot - b
												if b > 0 :
													child_alo.create({'dko_alo_id':rec.id, 'dko_spen_id':ret.id, 'total_alo':b,})
												budget_now = ret.used + ret.available
												ret.write({'used':budget_now,})
												dt2.append (ret.id)
												st1 = False
												b=0
												if total_sementara == budget and ztot>0:
													ztot=0
													break
							else:
								child_alo.create({'dko_alo_id':rec.id, 'dko_spen_id':alo[0].id, 'total_alo':rec.total,})
								budget_now = alo[0].used + rec.total
								alo[0].write({'used':budget_now,})
								ztot = 0
				else:
					alo = self.env['itb.plan_spending_int'].search([('unit_id.id','=',rec.unit_id.id),('day', '>=', date_start_all), ('day', '<=', date_finish_all)], order= 'day desc',limit=1)
					if len(alo) > 0 :
						child_alo.create({'dko_alo_id':rec.id, 'dko_spen_id':alo[0].id, 'total_alo':rec.total,})
						budget_now = alo[0].used + rec.total
						alo[0].write({'used':budget_now,})
						ztot = 0
		
		
		#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx	
		tgl = datetime.today()
		pay = self.env['res.partner'].search([('name','=','dko')],limit=1)
		data = self.env['itb.plan_spending_actual'].search([('id', 'in', sp_id)])
		d_group = []
		dst = ''
		ch_a = self.env['itb.plan_dko'].search([('id','in',par_id)], order='unit_id,price_id,source')
		if ch_a:
			for cha in ch_a:
				if dst != str(cha.unit_id.id) + '||' + str(cha.price_id.id) + '||' + str(cha.source) :
					d_group.append({'unit_id':cha.unit_id.id,'price_id':cha.price_id.id,'source':cha.source})
					dst = str(cha.unit_id.id) + '||' + str(cha.price_id.id) + '||' + str(cha.source)

		#if data_child:
		if d_group:
			#for dat in data_child:
			for dat in d_group:
				#raise models.ValidationError(str(data_child))
				parent = self.env['itb.plan_dko'].search([('unit_id','=',dat['unit_id']),('price_id','=',dat['price_id']),('source','=',dat['source']),('state','=','confirm'),('request_id','=',False),('id','in',par_id)])
				
				if len(parent)>0:
					prt_id = list(set(parent.mapped('id')))
					jumlah = sum(parent.mapped('total'))
				#raise models.ValidationError(str(data_child)+ '||'+str(prt_id))
				parent_request.create({
					'name' : 'Request from DKO',
					'reference' : 'ref DKO',
					'day' : tgl,
					'due' : tgl,
					'total' : jumlah,
					'source_total' : jumlah,
					'alocation_total' : jumlah,
					'is_reconciled' : True,
					'note' : '',
					'state' : 'confirm',
					'unit_id' : dat['unit_id'],
					'pay_to' : pay.id,
					'price_id' : dat['price_id'],
					'source' : dat['source'],
				})
				#raise osv.except_osv(str(jumlah))
				tot_wiz=0
				req = self.env['itb.plan_request'].search([('name','=','Request from DKO'),('total','=',jumlah),('price_id','=',dat['price_id']),('unit_id','=',dat['unit_id']),('pay_to','=',pay.id),('source','=',dat['source'])],order='id desc', limit=1)
				if req:
					www=0
					tot_wiz=0
					wizchild = self.env['itb.plan_dko_taken'].search([('dko_taken_id','in',prt_id)],order='actual_id')
					ac_id = list(set(wizchild.mapped('actual_id.id')))
					if ac_id:
						for rec in ac_id:
							#xxx = wizchild.filtered(lambda x: x.sp_act_id.id==rec.sp_act_id.id)
							xxx = self.env['itb.plan_dko_taken'].search([('dko_taken_id', 'in', prt_id), ('actual_id','=',rec)])
							tot_wiz = sum(xxx.mapped('tot_taken'))
							#www = rec.sp_act_id.id
							child_taken_request.create({'request_id' : req.id, 'spending_actual_id' : rec, 'total' : tot_wiz,})

					if len(prt_id) > 0:	
						wizchildalo = self.env['itb.plan_dko_allocation'].search([('dko_alo_id','in', prt_id)])
						if len(wizchildalo) > 0 :
							alo_id = list(set(wizchildalo.mapped('dko_spen_id.id')))
							if len(alo_id) > 0:
								for uuu in alo_id:
									zdv = self.env['itb.plan_dko_allocation'].search([('dko_alo_id','in', prt_id),('dko_spen_id','=',uuu)])
									total_wiz_alo = sum(zdv.mapped('total_alo'))
									child_alo_request.create({'request_alo_id' : req.id, 'spending_id' : uuu, 'total_alo' : total_wiz_alo,})
					parent.write({'request_id':req.id,})
			
		#else:
		#	raise models.ValidationError('No Data DKO can be proses')
			#raise osv.except_osv('No Data DKO can be proses')

	#@api.model_cr
	def isi_all(self):
		global data_child
		#global ret_child
		data_child=[]
		tahun = (date.today()).year
		#parent_group = self.env['itb.plan_group_dko'].search([], order='unit_id asc' )
		parent_group = self.env['itb.plan_group_dko_request_nounit'].search([], order='price_id asc' )
		#raise models.ValidationError(str(parent_group))
		ccd=self.env['itb.plan_dko_wizard_child'].search([])
		ccd.unlink()
		self.dko_wiz_child_ids.unlink()
		un_id=''
		pri=''
		a = 0
		b = 0
		total_sementara = 0
		total_sementara1 = 0
		#raise models.ValidationError(str(parent_group))
		if parent_group:
			for rec in parent_group:
				'''
				if un_id != str(rec.unit_id.id) + '||' + str(rec.price_id.id) + '||' + str(rec.source):
					data_child.append({'unit_id':rec.unit_id.id,'price_id':rec.price_id.id,'source':rec.source,'req_id':rec.id})
					ret_child = True
					un_id = str(rec.unit_id.id) + '||' + str(rec.price_id.id) + '||' + str(rec.source)
				'''
				if pri == str(rec.price_id.id):
					break

				dt2 = []
				dt1 = []
				a = 0
				b = 0
				total_sementara = 0
				total_sementara1 = 0
				uni=''
				pri = str(rec.price_id.id)
				parent = self.env['itb.plan_dko'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source), ('request_id','=',False),('state','=','confirm'),('faktur','=',True)], order='unit_id,day,total asc')
				#if len(parent) < 1 :
				#	ret_child = False
				
				data1 = parent

				for i in [x for x in data1 if x.id not in dt1] :
					total_sumber = i.total
					month_parent = (fields.Date.from_string(i.day)).month
					year_parent = (fields.Date.from_string(i.day)).year
					if uni != i.unit_id.id:
						b=0

					uni = i.unit_id.id
					
					if month_parent in [1,2,3] : 
						quar = 'q1'
						start_quarter = fields.Date.from_string(str(year_parent) + '-01-01')
					if month_parent in [4,5,6] :
						quar = 'q2'
						start_quarter = fields.Date.from_string(str(year_parent) + '-04-01')
					if month_parent in [7,8,9] :
						quar = 'q3'
						start_quarter = fields.Date.from_string(str(year_parent) + '-07-01')
					if month_parent in [10,11,12] :
						quar = 'q4'
						start_quarter = fields.Date.from_string(str(year_parent) + '-10-01')
					start_current = fields.Date.from_string(str(year_parent) + '-' + str(month_parent) + '-01')
					if month_parent < 12 :
						finish_current = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
					else:
						finish_current = fields.Date.from_string(str(year_parent+1) + '-01-01') + timedelta(days=-1)
					finish_quarter = finish_current
					start_all = fields.Date.from_string(str(year_parent) + '-01-01')
					finish_all = finish_current
					sit=0
					act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', i.unit_id.id), ('price_id', '=', i.price_id.id), ('source', '=', i.source),('day', '>=', start_all), ('day', '<=', finish_all), ('state','=','confirm'),('available','>',0)], order='day desc')
					#if i.unit_id.id==41:
					#	raise models.ValidationError(str(act))
					st1=False
					st2=False
					st3=False
					total_parent=0
					
					if len(act)>0:
						data2 = act
						total_hasil = sum(act.mapped('available'))
						
						if a == 0 : 
							a = i.total
							total_parent=i.total

						#raise models.ValidationError(str(i.unit_id.id) + '=' + str(i.price_id.id) + '=' + str(total_hasil) + '=' + str(len(act)) + '=' + str(st1) +' => a')

						while st1 == False :
							#raise models.ValidationError(str(i.unit_id.id) + '=' + str(i.price_id.id) + '=' + str(total_hasil) + '=' + str(len(act)) + '=' + str(st1) + '=' + str(st2) + ' => a')
							if st2 == True:
								act1 = self.env['itb.plan_spending_actual'].search([('unit_id', '!=', i.unit_id.id),('price_id', '=', i.price_id.id), ('source', '=', i.source),('day', '>=', start_all), ('day', '<=', finish_all), ('state','=','confirm'),('available','>',0)], order='unit_id,day desc')
								if len(act1)>0:
									#raise models.ValidationError(str(act1) + '||*' + str(i.unit_id.id) + '||' + str(i.price_id.id) + ' ==> gg')
									data2 = act1
									total_hasil = sum(act1.mapped('available'))
									total_sementara=0
									b=0
									st1=False
									st2=False
									st3=False
								else:
									#raise models.ValidationError('==> gg1')
									st1=True
									st2=False
									st3=True
							
							for y in [z for z in data2 if z.id not in dt2] :
								
								if b == 0 :
									b = y.available
									total_sementara += y.available

								if st3 == False:
									if b >= a :
										b = b - a
										
										if a > 0:
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id,'sp_act_id':y.id,'total':a,'parent_id':i.id,'req_id':rec.id,})
										a = 0
										st1 = True
										st2 = False
										st3 = True
										dt1.append(i.id)
									else:
										a = a - b
										if b >0 :
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id, 'sp_act_id':y.id,'total':b,'parent_id':i.id,'req_id':rec.id,})
										b = 0
										st1 = False
										st3 = False
										dt2.append(y.id)
										#if i.id == 72:
										#	raise models.ValidationError(str(i.id) + '[' + str(a) + '#' + str(total_sementara) + '-' + str(total_hasil) + ']' + str(i.unit_id.id) + '=' + str(i.price_id.id) + '=' + str(total_hasil) + '=' + str(len(act)) + '=' + str(st1) + '=' + str(st2) + ' => b')
										if (total_sementara - total_hasil == 0) and a > 0:
											st2=True
								else:
									break
					else:
						act = self.env['itb.plan_spending_actual'].search([('price_id', '=', i.price_id.id), ('source', '=', i.source),('day', '>=', start_all), ('day', '<=', finish_all), ('state','=','confirm'),('available','>',0)], order='day desc')
						st1=False
						st2=False
						total_parent=0
						if len(act) > 0:
							data2 = act
							total_hasil = sum(act.mapped('available'))
							
							if a == 0 : 
								a = i.total
								total_parent=i.total

							while st1 == False :
								for y in [z for z in data2 if z.id not in dt2] :
									if b == 0 :
										b = y.available
										total_sementara1 = y.available
									
									if b >= a :
										b = b - a
										if a > 0:
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id,'sp_act_id':y.id,'total':a,'parent_id':i.id,'req_id':rec.id,})
										a = 0
										st1 = True
										dt1.append(i.id)
										if total_parent==total_sumber and a<=0:
											st1=True
									else:
										a = a - b
										if b > 0:
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id, 'sp_act_id':y.id,'total':b,'parent_id':i.id,'req_id':rec.id,})
										b = 0
										st1 = False
										dt2.append(y.id)
										if total_parent==total_sumber and a<=0:
											st1=True
										if (total_sementara1 == total_hasil) and a > 0:
											st1=True
						#else:
						#	raise models.ValidationError('this price dont have budget anymore')
		else:
			raise models.ValidationError('No Data DKO can be proses')
			#ret_child = False

		return {
			'name': 'Send DKO to request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_dko_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
			'flags': {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}},
			#'context': {'parent_id': self._context['parent_id']},
		}
	
	def isi_all1(self):
		global data_child
		global ret_child
		data_child=[]
		tahun = (date.today()).year
		parent_group = self.env['itb.plan_group_dko'].search([], order='unit_id asc' )
		#raise models.ValidationError(str(parent_group))
		self.dko_wiz_child_ids.unlink()
		dt1 = []
		dt2 = []
		un_id=''
		a = 0
		b = 0
		st1 = False
		st2 = False
		st3 = False
		pri=''
		#raise models.ValidationError(str(parent_group))
		if parent_group:
			for rec in parent_group:
				if pri == rec.price_id.id:
					break
				
				parent = self.env['itb.plan_dko'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source), ('request_id','=',False),('state','=','confirm'),('faktur','=',True)], order='unit_id asc')
				pri=rec.price_id.id
				if parent ==  False:
					raise models.ValidationError('No Data DKO can be proses')
					ret_child = False
				
				data1 = parent

				for i in [x for x in data1 if x.id not in dt1] :
					sumber = self.env['itb.plan_dko'].search([('request_id','=',False),('id','=',i.id)])
					total_sumber = sum(sumber.mapped('total'))
					month_parent = (fields.Date.from_string(i.day)).month
					year_parent = (fields.Date.from_string(i.day)).year
					if month_parent in [1,2,3] : 
						quar = 'q1'
						start_quarter = fields.Date.from_string(str(year_parent) + '-01-01')
					if month_parent in [4,5,6] :
						quar = 'q2'
						start_quarter = fields.Date.from_string(str(year_parent) + '-04-01')
					if month_parent in [7,8,9] :
						quar = 'q3'
						start_quarter = fields.Date.from_string(str(year_parent) + '-07-01')
					if month_parent in [10,11,12] :
						quar = 'q4'
						start_quarter = fields.Date.from_string(str(year_parent) + '-10-01')
					start_current = fields.Date.from_string(str(year_parent) + '-' + str(month_parent) + '-01')
					if month_parent < 12 :
						finish_current = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
					else:
						finish_current = fields.Date.from_string(str(year_parent+1) + '-01-01') + timedelta(days=-1)
					finish_quarter = finish_current
					start_all = fields.Date.from_string(str(year_parent) + '-01-01')
					finish_all = finish_current


					if self.sumber == '1': #Same unit, same Quarter
						if quar == 'q1':
							date_start = fields.Date.from_string(str(year_parent) + '-01-01')
							date_finish = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(year_parent) + '-04-01')
							date_finish = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(year_parent) + '-07-01')
							date_finish = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(year_parent) + '-10-01')
							if month_parent == 12:
								date_finish = fields.Date.from_string(str(year_parent + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)

						act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])
						
					if self.sumber == '2': #All unit, same Quarter
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
							if fields.Date.from_string(i.day).month==12:
								date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						
						act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id),('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)], order='day asc')
						if len(act)==0:
							act = self.env['itb.plan_spending_actual'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])
					
					if self.sumber == '3': #Same unit, All Quarter
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
							if fields.Date.from_string(i.day).month==12:
								date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						
						act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])
						if len(act)==0:
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							if fields.Date.from_string(i.day).month==12:
								date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
							act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])
						
					if self.sumber == '4': #All unit, All Quarter
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
							if fields.Date.from_string(i.day).month==12:
								date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id),('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)], order='day asc')
						if len(act)==0:
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							if fields.Date.from_string(i.day).month==12:
								date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
							else:
								date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
							act = self.env['itb.plan_spending_actual'].search([('unit_id', '=', rec.unit_id.id),('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)], order='day asc')
							if len(act)==0:
								if quar == 'q1':
									date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
									date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						
								if quar == 'q2':
									date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
									date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						
								if quar == 'q3':
									date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
									date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
						
								if quar == 'q4':
									date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
									if fields.Date.from_string(i.day).month==12:
										date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
									else:
										date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
								act = self.env['itb.plan_spending_actual'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])
								#raise models.ValidationError(str(len(act)) + 'b4')
								if len(act)==0:
									date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
									if fields.Date.from_string(i.day).month==12:
										date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
									else:
										date_finish = fields.Date.from_string(str(rec.thn) + '-' + str(fields.Date.from_string(i.day).month+1) + '-01') + timedelta(days=-1)
									act = self.env['itb.plan_spending_actual'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm'),('available','>',0)])

					sumber = self.env['itb.plan_dko'].search([('request_id','=',False)])
					total_sumber = sum(sumber.mapped('total'))
					total_hasil = sum(act.mapped('available'))
					#raise osv.except_osv(str(total_sumber) + '||' + str(total_hasil))
					if total_hasil >= total_sumber :
						if act :
							if un_id != str(rec.unit_id.id):
								data_child.append({'unit_id':rec.unit_id.id,'price_id':rec.price_id.id,'source':rec.source,'req_id':rec.id})
								ret_child = True
							un_id = str(rec.unit_id.id)
							data2 = act
							if a == 0 : 
								a = i.total
							
							while a > 0 :
								st1 = False
								for y in [z for z in data2 if z.id not in dt2] :
									if st2 == False:
										b = y.available

									if st1 == False:
										if b > a :
											b = b - a
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id,'sp_act_id':y.id,'total':a,'parent_id':i.id,'req_id':rec.id,})
											a = 0
											dt1.append(i.id)
											st1 = True
											st2 = True
											st3 = True
										else:
											a = a - b
											self.dko_wiz_child_ids.create({'dko_wiz_id':self.id, 'sp_act_id':y.id,'total':b,'parent_id':i.id,'req_id':rec.id,})
											b = 0
											st2 = False
											st1 = False
											dt2.append(y.id)
									else:
										break
						else:
							break
		else:
			raise models.ValidationError('No Data DKO can be proses')
			ret_child = False

		return {
			'name': 'Send DKO to request',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_dko_wizard',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
			'flags': {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}},
			#'context': {'parent_id': self._context['parent_id']},
		}
		
class Dko_Wizard_child(models.TransientModel):
	_name = 'itb.plan_dko_wizard_child'
	
	dko_wiz_id = fields.Many2one('itb.plan_dko_wizard', index=True)
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
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], related='sp_act_id.source',readonly=True,store=True)
	total = fields.Float(default=0)
	parent_id = fields.Many2one('itb.plan_dko', index=True)
	req_id = fields.Many2one('itb.plan_group_dko', index=True)


class Plan_Group_Dko(models.Model):
	_name = "itb.plan_group_dko"
	_description = "group dko"
	_auto = False
	
	unit_id =  fields.Many2one('itb.plan_unit', string='Unit', readonly=True, index=True)
	price_id = fields.Many2one('itb.plan_price',string='Price', readonly=True, index=True)
	source = fields.Char(string='source', readonly=True,index=True)
	thn = fields.Char(string='Year', readonly=True, index=True)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'itb_plan_group_dko')
		self._cr.execute("""
			CREATE OR REPLACE VIEW itb_plan_group_dko AS (
				SELECT row_number() over (order by unit_id) as id, unit_id,price_id,source,to_char(day, 'YYYY')thn
				FROM public.itb_plan_dko
				where request_id is null
				GROUP BY unit_id,price_id,source,to_char(day, 'YYYY')
			)
		""")

class Plan_Group_Dko_Request(models.Model):
	_name = "itb.plan_group_dko_request"
	_description = "group dko request"
	_auto = False


	unit_id =  fields.Many2one('itb.plan_unit', string='Unit', readonly=True)
	price_id = fields.Many2one('itb.plan_price',string='Price', readonly=True)
	source = fields.Char(string='Source', readonly=True)
	thn = fields.Char(string='Year', readonly=True)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'itb_plan_group_dko_request')
		self._cr.execute("""
			CREATE OR REPLACE VIEW itb_plan_group_dko_request AS (
				SELECT row_number() over (order by unit_id) as id, unit_id,price_id,source,to_char(day, 'YYYY')thn
				FROM public.itb_plan_dko
				where request_id is null and faktur = TRUE
				GROUP BY unit_id,price_id,source,to_char(day, 'YYYY')
			)
		""")

class Plan_Group_nounit_Dko_Request(models.Model):
	_name = "itb.plan_group_dko_request_nounit"
	_description = "group dko request no unit"
	_auto = False

	price_id = fields.Many2one('itb.plan_price',string='Price', readonly=True)
	source = fields.Char(string='Source', readonly=True)
	thn = fields.Char(string='Year', readonly=True)
	
	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'itb_plan_group_dko_request_nounit')
		self._cr.execute("""
			CREATE OR REPLACE VIEW itb_plan_group_dko_request_nounit AS (
				SELECT row_number() over (order by price_id) as id, price_id,source,to_char(day, 'YYYY')thn
				FROM public.itb_plan_dko
				where request_id is null and faktur = TRUE
				GROUP BY price_id,source,to_char(day, 'YYYY')
			)
		""")

class Cash_Advance (models.Model):
	_name = 'itb.plan_cash_advance'
	_rec_name = 'name'

	name = fields.Char()
	dko_ids = fields.One2many('itb.plan_dko', 'cash_id', string='Cash Advance Dko',index=True,copy=True, ondelete='cascade')
	request_ids = fields.One2many('itb.plan_request', 'cash_id', string='Cash Advance Request',index=True,copy=True, ondelete='cascade')
	pay_to = fields.Many2one('res.partner', string='Pay To',index=True)
	unit_id = fields.Many2one('itb.plan_unit', string='Unit', index=True)
	amount = fields.Float(default=0, string='Amount')
	date_pay = fields.Date(default=date.today(), string='Transaction Date')
	used = fields.Float(default=0, string='Used')
	note = fields.Text()
	state = fields.Selection([('open','Open'),('close','Close')], default='open' ,string='Status',required=True)

	@api.multi
	def action_payment_req_close(self):
		for rec in self:
			rec.state='close'

	@api.multi
	def action_payment_req_abort(self):
		for rec in self:
			rec.state='open'

class Plan_dko_actual(models.Model):
	_name = "itb.plan_actual_dko"
	_description = "spending actual dko"
	_auto = False

	spending_id = fields.Many2one('itb.plan_spending',index=True)
	plan_line_id = fields.Many2one('itb.plan_line',related='spending_id.plan_line_id',readonly=True, store=True ,index=True)
	name = fields.Char(related='spending_id.price_id.name', readonly=True, store=True ,index=True)
	code = fields.Char(related='spending_id.code', readonly=True, store=True)
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', store=True, index=True)
	day = fields.Date(related='spending_id.day', readonly=True, store=True ,index=True)
	standard = fields.Char(related='spending_id.standard', readonly=True, store=True)
	price = fields.Float(related='spending_id.price',default=0, readonly=True, store=True)
	volume = fields.Float(store=True, readonly=True, default=0)
	total = fields.Float(default=0)
	used = fields.Float(readonly=True, default=0)
	available = fields.Float(store=True, readonly=True,default=0)
	paid = fields.Float(readonly=True, default=0)
	percent_budget = fields.Float(store=True, readonly=True, default=0)
	active = fields.Boolean(default=True,readonly=True)
	previus_month = fields.Char(store=True, readonly=True)
	confirmation_ref = fields.Char(string="No Ref Confirmation",readonly=True)
	confirmation_date = fields.Date(string='Confirmation Date',readonly=True)
	confirmation_note = fields.Char(string='Confirmation Note',readonly=True)
	state=fields.Selection([('draft','Draft'),('confirm','FRA')], 'Status',default='draft', readonly=True, copy=False ,index=True)
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', related='spending_id.type', readonly=True, store=True, index=True)
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source', readonly=True)
	price_id = fields.Many2one('itb.plan_price',related='spending_id.price_id',index=True,store=True)
	plan_id = fields.Many2one('itb.plan',related='spending_id.plan_id',index=True,store=True)
	implementation_id = fields.Many2one('itb.plan_implementation',required=True,index=True)
	request_line_ids = fields.One2many('itb.plan_request_line', 'spending_actual_id', 'Request Line', index=True)
	user_ids = fields.Many2many('res.users')
	unit_id = fields.Many2one('itb.plan_unit',related='plan_line_id.unit_id',index=True, readonly=True, store=True)
	type_actual = fields.Selection([('1','Actual'),('2', 'Logistik')], 'Type Actual', default='1', readonly=True, store=True)
	previus_source = fields.Char(store=True, readonly=True)
	program_id = fields.Many2one('itb.plan_program', related='plan_line_id.program_id', readonly=True, store=True ,index=True)
	activity_id = fields.Many2one('itb.plan_activity', related='spending_id.plan_line_id.activity_id', readonly=True, store=True ,index=True)
	subactivity_id = fields.Many2one('itb.plan_subactivity', related='spending_id.plan_line_id.subactivity_id', readonly=True, store=True ,index=True)
	
	@api.model_cr
	def init(self):
		tahun=(date.today()).year
		tools.drop_view_if_exists(self._cr, 'itb_plan_actual_dko')
		self._cr.execute("""
			CREATE OR REPLACE VIEW itb_plan_actual_dko AS (
				SELECT id, subactivity_id, code, month, price_id, 
					logistic, confirmation_note, total, plan_id, percent_budget, 
					confirmation_ref, source, state, type, available, activity_id, 
					used, confirmation_date, previus_month, paid, standard, volume, 
					program_id, previus_source, active, day, name, spending_id, 
					unit_id, plan_line_id, implementation_id, price
				FROM itb_plan_spending_actual
				where state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
				and price_id in (select price_id from itb_plan_dko where request_id is null) 
				and source in (select source from itb_plan_dko where request_id is null)
			)
		""")

class Dko_Split_Price(models.TransientModel):
	_name = 'itb.plan_dko_wizard_split'

	name = fields.Char()
	dko_price_wiz_child_ids = fields.One2many('itb.plan_dko_price_wizard_child', 'dko_price_wiz_id', 'Unit')
	
	def no(self):
		pass

	def yes(self):
		par_id = self._context['parent_id']
		
		#child_id = self._context['child_id']
		child = self.env['itb.plan_dko_allocation'].search([('dko_alo_id','=',par_id)])
		c_id = list(set(child.mapped('unit_id.id')))
		e_id = self.env['itb.plan_unit'].search([('id','in',c_id)])
		unit_s = list(set(e_id.mapped('name')))
		s_id = list(set(child.mapped('dko_spen_id.id')))
		d_id = self.env['itb.plan_spending_int'].search([('id', 'in', s_id)])
		name_s = list(set(d_id.mapped('name')))
		parent=self.env['itb.plan_dko'].search([('id','=',par_id)])
		if parent.note:
			note_old = parent.note
			parent.write({'note':parent.note + ', Split Price - id (' + str(par_id) + ') - unit (' + str(unit_s) + ') - spending (' + str(name_s) + ')',})
		else:
			parent.write({'note':'Split Price - id (' + str(par_id) + ') - unit (' + str(unit_s) + ') - spending (' + str(name_s) + ')',})
		child.unlink()
		
		month_parent = (fields.Date.from_string(parent.day)).month
		year_parent = (fields.Date.from_string(parent.day)).year
		start_all = fields.Date.from_string(str(year_parent) + '-01-01')
		total = parent.total
		jum = len(self.dko_price_wiz_child_ids)
		if jum > 0:
			tot = total / jum
		if month_parent < 12 :
			finish_all = fields.Date.from_string(str(year_parent) + '-' + str(month_parent+1) + '-01') + timedelta(days=-1)
		else:
			finish_all = fields.Date.from_string(str(year_parent+1) + '-01-01') + timedelta(days=-1)
		if self.dko_price_wiz_child_ids:
			unit = list(set(self.dko_price_wiz_child_ids.mapped('unit_id.id')))
			if parent:
				for rec in unit:
					target = self.env['itb.plan_spending_int'].search([('price_id','=',parent.price_id.id),('unit_id','=',rec),('day', '>=', start_all), ('day', '<=', finish_all), ('available','>',0)], limit=1,order='day desc')
					if target:
						child.create({'dko_alo_id':par_id,'dko_spen_id':target.id,'total_alo':tot})
				
		
class Dko_Split_Price_child(models.TransientModel):
	_name = 'itb.plan_dko_price_wizard_child'

	dko_price_wiz_id = fields.Many2one('itb.plan_dko_wizard_split', index=True)
	unit_id = fields.Many2one('itb.plan_unit', string='Unit', index=True)

	'''
	@api.multi
	@api.onchange('unit_id')
	def filter_spending(self):
		par_id = self._context['parent_id']
		parent=self.env['itb.plan_dko'].search([('id','=',par_id)])
		res = dict()
		actual = self.env['itb.plan_spending_int'].search([('price_id','=',parent.price_id.id),('available','>',0)])
		spending_actual_ids=actual.mapped('unit_id.id')
		res['domain'] = {'unit_id': [('id', 'in', spending_actual_ids)]}
		return res
	'''

class Dko_Mismatch_Price(models.TransientModel):
	_name = 'itb.plan_dko_wizard_mismatch'

	name = fields.Char()
	dko_missmatch_wiz_ids = fields.One2many('itb.plan_dko_wizard_mismatch_child', 'dko_missmatch_wiz_id', 'spending')
	
	def no(self):
		pass

	def yes(self):
		par_id = self._context['parent_id']
		
		#child_id = self._context['child_id']
		child = self.env['itb.plan_dko_taken'].search([('dko_taken_id','=',par_id)])
		c_id = list(set(child.mapped('unit_id.id')))
		e_id = self.env['itb.plan_unit'].search([('id','in',c_id)])
		unit_s = list(set(e_id.mapped('name')))
		s_id = list(set(child.mapped('actual_id.id')))
		d_id = self.env['itb.plan_spending_actual'].search([('id', 'in', s_id)])
		name_s = list(set(d_id.mapped('name')))
		parent=self.env['itb.plan_dko'].search([('id','=',par_id)])
		if parent.note:
			note_old = parent.note
			parent.write({'note': note_old + ', Missmatch Price - id (' + str(par_id) + ') - unit (' + str(unit_s) + ') - spending (' + str(name_s) + ')',})	
		else:
			parent.write({'note':'Missmatch Price - id (' + str(par_id) + ') - unit (' + str(unit_s) + ') - spending (' + str(name_s) + ')',})
		child.unlink()
		
		if self.dko_missmatch_wiz_ids:
			if parent:
				for rec in self.dko_missmatch_wiz_ids:
					target = self.env['itb.plan_spending_actual'].search([('id','=',rec.spending_actual_id.id), ('available','>',0)], limit=1,order='day desc')
					if target:
						child.create({'dko_taken_id':par_id,'actual_id':rec.spending_actual_id.id,'tot_taken':rec.total,})

class Dko_Mismatch_Price_child(models.TransientModel):
	_name = 'itb.plan_dko_wizard_mismatch_child'

	dko_missmatch_wiz_id = fields.Many2one('itb.plan_dko_wizard_mismatch', index=True)
	spending_actual_id = fields.Many2one('itb.plan_spending_actual', string='Spending Actual', index=True)
	initiative = fields.Char(related='spending_actual_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='spending_actual_id.unit_id', readonly=True, store=True)
	price_id = fields.Many2one(related='spending_actual_id.price_id', readonly=True, store=True)
	used = fields.Float(related='spending_actual_id.used', readonly=True, store=True)
	available=fields.Float(related='spending_actual_id.available', readonly=True, store=True)
	month=fields.Selection(related='spending_actual_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='spending_actual_id.spending_id.plan_line_id.subactivity_id', readonly=True, store=True)
	total = fields.Float(default=0)

	@api.multi
	@api.onchange('spending_actual_id')
	def filter_spending(self):
		res = dict()
		actual = self.env['itb.plan_spending_actual'].search([('available','>',0)])
		spending_actual_ids=actual.mapped('id')
		res['domain'] = {'spending_actual_id': [('id', 'in', spending_actual_ids)]}
		return res