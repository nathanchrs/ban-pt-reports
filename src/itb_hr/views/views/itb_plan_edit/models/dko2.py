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
	state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('paid', 'Paid'), ('reconcile', 'Reconcile')], 'Status',default='draft', required=True, readonly=True, copy=False)
	total = fields.Float(default=0,compute='_get_total',store=True)
	note = fields.Char()
	
	@api.one
	@api.depends('plan_request_ids')
	def _get_total(self):
		for rec in self:
			rec.total = 0
			if rec.plan_request_ids:
				for payment in rec.plan_request_ids:
					record.total += payment.total

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

	sumber = fields.Selection([('1', 'Same unit, same Quarter'), ('2', 'All unit, same Quater'), ('3', 'Same unit, All Quater'),('4', 'All unit, Quater')], 'Source', default='1')
	dko_wiz_child_ids = fields.One2many('itb.plan_dko_wizard_child', 'dko_wiz_id', 'Wizard Child')
	
	def no(self):
		pass

	def oke(self):
		global data_child
		global ret_child
		if ret_child == True:
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
			thn = (date.today()).year
			for rec in par_id:
				pr = self.env['itb.plan_dko'].search([('id','=',rec)])
				raise osv.except_osv(str(pr))
				thn = fields.Date.from_string(pr.day).year
				bln = fields.Date.from_string(pr.day).month
				bulan = []
				if bln in [1,2,3]:
					quarter = 1
				if bln in [4,5,6]:
					quarter = 2
				if bln in [7,8,9]:
					quarter = 3
				if bln in [10,11,12]:
					quarter = 4

				if quarter == 1:
					bulan = [1,2,3]
				if quarter == 2:
					bulan = [4,5,6]
				if quarter == 3:
					bulan = [7,8,9]
				if quarter == 4:
					bulan = [10,11,12]
				alo = self.env['itb.plan_spending_int'].search([('unit_id','=',pr.unit_id.id)], order= 'day desc')
				alo1 = alo.filtered(lambda x: fields.Date.from_string(x.day).year == thn)
				alo2 = alo1.filtered(lambda x: x.price_id.id == pr.price_id.id and fields.Date.from_string(x.day).month == bln)
				if alo2:
					if sum(alo2.mapped('available')) >= pr.total:
						zxy=0
						sr=False
						for rech in alo2:
							if zxy==0 :
								zxy = rech.available
								ztot = rech.available
							else:
								if (zxy + rech.available) < pr.total:
									zxy += rech.available
									ztot = rech.available
								else:
									ztot = pr.total - zxy
									sr=True
							if sr==False:
								child_alo.create({'dko_alo_id':rec, 'dko_spen_id':rech.id, 'total_alo':ztot,})
					else:
						alo2 = alo1.filtered(lambda x: x.price_id.id == pr.price_id.id and fields.Date.from_string(x.day).month in bulan)
						if sum(alo2.mapped('available')) >= pr.total:
							zxy=0
							sr=False
							for rech in alo1:
								if zxy==0 :
									zxy = rech.available
									ztot = rech.available
								else:
									if (zxy + rech.available) < pr.total:
										zxy += rech.available
										ztot = rech.available
									else:
										ztot = pr.total - zxy
										sr=True
								if sr==False:
									child_alo.create({'dko_alo_id':rec, 'dko_spen_id':rech.id, 'total_alo':ztot,})
						else:
							alo2 = alo1.filtered(lambda x: x.price_id.id == pr.price_id.id and fields.Date.from_string(x.day).month <= bln)
							zxy=0
							sr=False
							for rech in alo1:
								if zxy==0 :
									zxy = rech.available
									ztot = rech.available
								else:
									if (zxy + rech.available) < pr.total:
										zxy += rech.available
										ztot = rech.available
									else:
										ztot = pr.total - zxy
										sr=True
								if sr==False:
									child_alo.create({'dko_alo_id':rec, 'dko_spen_id':rech.id, 'total_alo':ztot,})			
				else:
					alo2 = alo1.filtered(lambda x: x.price_id.id == pr.price_id.id and fields.Date.from_string(x.day).month <= bln)
					if alo2:
						zxy=0
						sr=False
						for rech in alo1:
							if zxy==0 :
								zxy = rech.available
								ztot = rech.available
							else:
								if (zxy + rech.available) < pr.total:
									zxy += rech.available
									ztot = rech.available
								else:
									ztot = pr.total - zxy
									sr=True
							if sr==False:
								child_alo.create({'dko_alo_id':rec, 'dko_spen_id':rech.id, 'total_alo':ztot,})
					else:
						alo2 = alo1.filtered(lambda x: fields.Date.from_string(x.day).month <= bln)
						if alo2:
							child_alo.create({'dko_alo_id':rec, 'dko_spen_id':alo2[0].id, 'total_alo':pr.total,})
			
				budget_start=0
				budget_now=0
				#child_alo.create({'dko_alo_id':rec.parent_id.id, 'dko_spen_id':alo.spending_id_int.id, 'total_alo':rec.total,})
				bud = self.env['itb.plan_dko_allocation'].search([('dko_alo_id','in',par_id)])
				for ss in bud:
					budget = self.env['itb.plan_spending_int'].search([('id','=',ss.dko_spen_id.id)])
					budget_start = budget.used
					if budget_start + ss.total_alo <= budget.total:
						budget_now = budget_start + ss.total_alo
					else:
						budget_now = budget.total
					budget.write({'used':budget_now,})
			
			tgl = datetime.today()
			pay = self.env['res.partner'].search([('name','=','dko')],limit=1)
			data = self.env['itb.plan_spending_actual'].search([('id', 'in', sp_id)])
			
			if data_child:
				for dat in data_child:
					parent = self.env['itb.plan_dko'].search([('unit_id','=',dat['unit_id']),('price_id','=',dat['price_id']),('source','=',dat['source']),('state','=','confirm')])
					jumlah = sum(parent.mapped('total'))
					
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
						wizchild = self.env['itb.plan_dko_wizard_child'].search([('dko_wiz_id','=',self.id),('req_id','=',dat['req_id'])])
						for rec in wizchild:
							if www != rec.sp_act_id.id:
								xxx = wizchild.filtered(lambda x: x.sp_act_id.id==rec.sp_act_id.id)
								tot_wiz = sum(xxx.mapped('total'))
								www = rec.sp_act_id.id
								child_taken_request.create({'request_id' : req.id, 'spending_actual_id' : rec.sp_act_id.id, 'total' : tot_wiz,})
								alo = self.env['itb.plan_allocation'].search([('spending_id','=', rec.spending_id.id)],limit=1)
								if alo:
									child_alo_request.create({'request_alo_id' : req.id, 'spending_id' : alo.spending_id_int.id, 'total_alo' : tot_wiz,})
						parent.write({'request_id':req.id,})
		else:
			raise osv.except_osv('No Data DKO can be proses')

	#@api.model_cr
	def isi_all(self):
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
		if parent_group:
			for rec in parent_group:
				parent = self.env['itb.plan_dko'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source), ('request_id','=',False),('state','=','confirm'),('faktur','=',True)], order='unit_id asc')
				if parent ==  False:
					raise osv.except_osv('No Data DKO can be proses')
					ret_child = False
				#raise models.ValidationError(str(parent))
				data1 = parent
				
				for i in [x for x in data1 if x.id not in dt1] : 
					dt_start = fields.Date.from_string(str(rec.thn) + '-01-01')
					dt_finish = fields.Date.from_string(str(rec.thn) + '-04-01') + timedelta(days=-1)
					if (fields.Date.from_string(i.day) >= dt_start and fields.Date.from_string(i.day) <= dt_finish) :
						quar = 'q1'

					dt_start = fields.Date.from_string(str(rec.thn) + '-04-01')
					dt_finish = fields.Date.from_string(str(rec.thn) + '-07-01') + timedelta(days=-1)
					if (fields.Date.from_string(i.day) >= dt_start and fields.Date.from_string(i.day) <= dt_finish) :
						quar='q2'

					dt_start = fields.Date.from_string(str(rec.thn) + '-07-01')
					dt_finish = fields.Date.from_string(str(rec.thn) + '-10-01') + timedelta(days=-1)
					if (fields.Date.from_string(i.day) >= dt_start and fields.Date.from_string(i.day) <= dt_finish) :
						quar='q3'

					dt_start = fields.Date.from_string(str(rec.thn) + '-10-01')
					dt_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
					if (fields.Date.from_string(i.day) >= dt_start and fields.Date.from_string(i.day) <= dt_finish) :
						quar='q4'

					#raise models.ValidationError(str(parent) + '||' + quar)
					
					if self.sumber == '1':
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-04-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-07-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-10-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
							date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
			
						tools.drop_view_if_exists(self._cr, 'itb_plan_actual_dko')
						self._cr.execute("""
							CREATE OR REPLACE VIEW itb_plan_actual_dko AS (
								SELECT id, subactivity_id, code, month, price_id, 
									type_actual, confirmation_note, total, plan_id, percent_budget, 
									confirmation_ref, source, state, type, available, activity_id, 
									used, confirmation_date, previus_month, paid, standard, volume, 
									program_id, previus_source, active, day, name, spending_id, 
									unit_id, plan_line_id, implementation_id, price
								FROM itb_plan_spending_actual
								where available > 0 and state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
									and unit_id = """ + str(rec.unit_id.id) + """ 
									and price_id = """ + str(rec.price_id.id) + """ 
									and source = '""" + rec.source + """' 
									and (day between '""" + date_start.strftime('%Y-%m-%d') + """' and '""" + date_finish.strftime('%Y-%m-%d') + """')
									and	unit_id in (select unit_id from itb_plan_dko where request_id is null) 
									and price_id in (select price_id from itb_plan_dko where request_id is null) 
									and source in (select source from itb_plan_dko where request_id is null)
								order by unit_id,id
							)
						""")
						
						act = self.env['itb.plan_actual_dko'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm')])
						#tes='a'
					if self.sumber == '2':
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-04-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-04-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-07-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-07-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-10-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-10-01')
							date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
				
						tools.drop_view_if_exists(self._cr, 'itb_plan_actual_dko')
						self._cr.execute("""
							CREATE OR REPLACE VIEW itb_plan_actual_dko AS (
								SELECT id, subactivity_id, code, month, price_id, 
									type_actual, confirmation_note, total, plan_id, percent_budget, 
									confirmation_ref, source, state, type, available, activity_id, 
									used, confirmation_date, previus_month, paid, standard, volume, 
									program_id, previus_source, active, day, name, spending_id, 
									unit_id, plan_line_id, implementation_id, price
								FROM itb_plan_spending_actual
								where available > 0 and state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
									and price_id = """ + str(rec.price_id.id) + """ 
									and source = '""" + rec.source + """' 
									and (day between '""" + date_start.strftime('%Y-%m-%d') + """' and '""" + date_finish.strftime('%Y-%m-%d') + """') 
									and	unit_id in (select unit_id from itb_plan_dko where request_id is null) 
									and price_id in (select price_id from itb_plan_dko where request_id is null) 
									and source in (select source from itb_plan_dko where request_id is null)
								order by unit_id,id
							)
						""")

						act = self.env['itb.plan_actual_dko'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm')])
						#tes='b'
					if self.sumber == '3':
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-04-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-07-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-10-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
						
						tools.drop_view_if_exists(self._cr, 'itb_plan_actual_dko')
						self._cr.execute("""
							CREATE OR REPLACE VIEW itb_plan_actual_dko AS (
								SELECT id, subactivity_id, code, month, price_id, 
									type_actual, confirmation_note, total, plan_id, percent_budget, 
									confirmation_ref, source, state, type, available, activity_id, 
									used, confirmation_date, previus_month, paid, standard, volume, 
									program_id, previus_source, active, day, name, spending_id, 
									unit_id, plan_line_id, implementation_id, price
								FROM itb_plan_spending_actual
								where available > 0 and state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
									and unit_id = """ + str(rec.unit_id.id) + """ 
									and price_id = """ + str(rec.price_id.id) + """ 
									and source = '""" + rec.source + """' 
									and (day between '""" + date_start.strftime('%Y-%m-%d') + """' and '""" + date_finish.strftime('%Y-%m-%d') + """') 
									and	unit_id in (select unit_id from itb_plan_dko where request_id is null) 
									and price_id in (select price_id from itb_plan_dko where request_id is null) 
									and source in (select source from itb_plan_dko where request_id is null)
								order by unit_id,id
							)
						""")

						act = self.env['itb.plan_actual_dko'].search([('unit_id', '=', rec.unit_id.id), ('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm')])
						
					if self.sumber == '4':
						if quar == 'q1':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-04-01') + timedelta(days=-1)
				
						if quar == 'q2':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-07-01') + timedelta(days=-1)
				
						if quar == 'q3':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(rec.thn) + '-10-01') + timedelta(days=-1)
				
						if quar == 'q4':
							date_start = fields.Date.from_string(str(rec.thn) + '-01-01')
							date_finish = fields.Date.from_string(str(int(rec.thn) + 1) + '-01-01') + timedelta(days=-1)
				
						tools.drop_view_if_exists(self._cr, 'itb_plan_actual_dko')
						self._cr.execute("""
							CREATE OR REPLACE VIEW itb_plan_actual_dko AS (
								SELECT id, subactivity_id, code, month, price_id, 
									type_actual, confirmation_note, total, plan_id, percent_budget, 
									confirmation_ref, source, state, type, available, activity_id, 
									used, confirmation_date, previus_month, paid, standard, volume, 
									program_id, previus_source, active, day, name, spending_id, 
									unit_id, plan_line_id, implementation_id, price
								FROM itb_plan_spending_actual
								where available > 0 and state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
									and price_id = """ + str(rec.price_id.id) + """ 
									and source = '""" + rec.source + """' 
									and (day between '""" + date_start.strftime('%Y-%m-%d') + """' and '""" + date_finish.strftime('%Y-%m-%d') + """') 
									and	unit_id in (select unit_id from itb_plan_dko where request_id is null) 
									and price_id in (select price_id from itb_plan_dko where request_id is null) 
									and source in (select source from itb_plan_dko where request_id is null)
								order by unit_id,id
							)
						""")

						act = self.env['itb.plan_actual_dko'].search([('price_id', '=', rec.price_id.id), ('source', '=', rec.source),('day', '>=', date_start), ('day', '<=', date_finish), ('state','=','confirm')])
					
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
						raise osv.except_osv('Total Source bigger then total simulate ' + str(total_sumber) + '||' + str(total_hasil))
		else:
			raise osv.except_osv('No Data DKO can be proses')
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
					type_actual, confirmation_note, total, plan_id, percent_budget, 
					confirmation_ref, source, state, type, available, activity_id, 
					used, confirmation_date, previus_month, paid, standard, volume, 
					program_id, previus_source, active, day, name, spending_id, 
					unit_id, plan_line_id, implementation_id, price
				FROM itb_plan_spending_actual
				where state = 'confirm' and EXTRACT(YEAR FROM day) =""" + str(tahun) + """ 
				and	unit_id in (select unit_id from itb_plan_dko where request_id is null) 
				and price_id in (select price_id from itb_plan_dko where request_id is null) 
				and source in (select source from itb_plan_dko where request_id is null)
			)
		""")