from odoo import models, fields, api, exceptions, osv
from datetime import datetime


class Implementation(models.Model):
	_name = 'itb.plan_implementation'
	_rec_name = 'reference'
	
	
	quarter = fields.Selection([('q1','Jan-Mar'),('q2', 'Apr-Jun'),('q3','Jul-Sep'),('q4','Oct-Dec')], 'Quarter',default='q1')
	reference = fields.Char()
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')], 'Status', default='draft')
	#plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True,domain="[('state','=','validate')]")
	spending_actual_ids = fields.One2many('itb.plan_spending_actual', 'implementation_id', 'Spending Implementation Lines', copy=True)
	
	@api.multi
	def action_state_confirmed(self):
		if self.spending_actual_ids:
			for rec in self.spending_actual_ids:
				actual=self.env['itb.plan_spending_actual'].search([('id','=',rec.id)])
				spending=self.env['itb.plan_spending'].search([('id','=',actual.spending_id.id)])
				spending.write({'implemented' : actual.total,})

				self.state = 'confirm'
		else:
			raise models.ValidationError('Spending ids empty')
	
	@api.multi
	def action_state_validated(self):
		self.state = 'validate'

	@api.multi
	def action_state_abort(self):
		for rec in self.spending_actual_ids:
			actual=self.env['itb.plan_spending_actual'].search([('id','=',rec.id)])
			spending=self.env['itb.plan_spending'].search([('id','=',actual.spending_id.id)])
			spending.write({'implemented' : 0,})
		self.state = 'draft'

	@api.multi
	@api.constrains('quarter')
	def generate_spending(self):
		tgl = datetime.now() 
		dat = []
		cek = self.env['itb.plan_implementation'].search([('quarter','=',self.quarter)])
		for rec in cek:
			dat.append((fields.Date.from_string(rec.create_date)).year)
		thn=list(set(dat))
		#if len(cek)>1:
		#	if thn[0] == tgl.year:
		#		raise models.ValidationError('Implementation for selected quarter in this year already exist')
			
		return {
			'name': 'Find Budget for Implementation',
			'type': 'ir.actions.act_window',
			'res_model': 'itb.plan_wizard_implementasi',
			'view_mode': 'form',
			'view_type': 'form',
			'target': 'new',
			'context': {'parent_obj': self.id},
			}

	#@api.onchange('plan_id')
	@api.depends('plan_id')
	def load_spending_items(self):
		spendings = self.env['itb.plan_spending'].search([('plan_id','=',self.plan_id)])
		implementation_lines = []
		
		for s in spendings:
			implementation_lines.append((0,0,{'name':s.name,'plan_line_id':s.plan_line_id,'type':s.type,'source':s.source,'month':s.month,'price':s.price}))

 		val = {'spending_actual_ids':implementation_lines}
		#self.spending_actual_ids = implementation_lines
		return {'value':val}

class Wizard_Implementation(models.TransientModel):
	_name = 'itb.plan_wizard_implementasi'

	tgl = datetime.now()
	par_id=0
	year = fields.Integer(default=tgl.year, string="Year")
	quartal1 = fields.Boolean(default=True, string="Q1")
	quartal2 = fields.Boolean(default=False, string="Q2")
	quartal3 = fields.Boolean(default=False, string="Q3")
	quartal4 = fields.Boolean(default=False, string="Q4")

	@api.multi
	def no(self):
		pass

	@api.multi
	def yes(self):
		plan=self.env['itb.plan'].search([('year','=',self.year),('state','=','validate')])
		plan_id=plan.mapped('id')
		imp = self.env['itb.plan_implementation'].search([], order='id desc', limit=1)
		if imp.id:
			if self.year>0:
				if self.quartal1 == True:
					parent = self.env['itb.plan_implementation'].search([('id','=',self._context['parent_obj'])])
					parent_q =''
					parent_id=''
					if parent:
						parent_q = parent.quarter
						parent_id = parent.id
						
						date_start=fields.Date.from_string(str(self.year) + '-01-01')
						date_finish=fields.Date.from_string(str(self.year) + '-03-01')
						sp = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish),('plan_id','in',plan_id)])
						if sp:
							for rec in sp:
								if parent_q == 'q2':
									month='Apr'
								elif parent_q == 'q3':	
									month='Jul'
								elif parent_q == 'q4':
									month='Okt'
								else:
									month=rec.month

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										spending_id,plan_line_id,name,create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid,write_date, 
										active, write_uid, day, implementation_id,state,unit_id,price_id, 
										source, confirmation_note, volume, type_actual,program_id,
										activity_id,subactivity_id,code,price,standard)
									select a.id, b.id, left(a.name,150), CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id,a.source,'',a.volume,1,a.program_id,a.activity_id,a.subactivity_id,
										a.code,a.price,a.standard
									from itb_plan_spending a, itb_plan_line b
									where a.plan_line_id = b.id and a.id not in (select spending_id from itb_plan_spending_actual) and a.id = '""" + str(rec.id) + """' 
									;
								""")

				if self.quartal2 == True:
					parent = self.env['itb.plan_implementation'].search([('id','=',self._context['parent_obj'])])
					parent_q =''
					parent_id=''
					if parent:
						parent_q = parent.quarter
						parent_id = parent.id
						
						date_start=fields.Date.from_string(str(self.year) + '-04-01')
						date_finish=fields.Date.from_string(str(self.year) + '-06-01')
						sp = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish),('plan_id','in',plan_id)])
						if sp:
							for rec in sp:
								if parent_q == 'q1':
									month='Jan'
								elif parent_q == 'q3':	
									month='Jul'
								elif parent_q == 'q4':
									month='Okt'
								else:
									month=rec.month

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										spending_id,plan_line_id,name,create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid,write_date, 
										active, write_uid, day, implementation_id,state,unit_id,price_id, 
										source, confirmation_note, volume, type_actual,program_id,
										activity_id,subactivity_id,code,price,standard)
									select a.id, b.id, left(a.name,150), CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id,a.source,'',a.volume,1,a.program_id,a.activity_id,a.subactivity_id,
										a.code,a.price,a.standard
									from itb_plan_spending a, itb_plan_line b
									where a.plan_line_id = b.id and a.id not in (select spending_id from itb_plan_spending_actual) and a.id = '""" + str(rec.id) + """' 
									;
								""")

				if self.quartal3 == True:
					parent = self.env['itb.plan_implementation'].search([('id','=',self._context['parent_obj'])])
					parent_q =''
					parent_id=''
					if parent:
						parent_q = parent.quarter
						parent_id = parent.id
						
						date_start=fields.Date.from_string(str(self.year) + '-07-01')
						date_finish=fields.Date.from_string(str(self.year) + '-09-01')
						sp = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish),('plan_id','in',plan_id)])
						if sp:
							for rec in sp:
								if parent_q == 'q1':
									month='Jan'
								elif parent_q == 'q2':	
									month='Apr'
								elif parent_q == 'q4':
									month='Okt'
								else:
									month=rec.month

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										spending_id,plan_line_id,name,create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid,write_date, 
										active, write_uid, day, implementation_id,state,unit_id,price_id, 
										source, confirmation_note, volume, type_actual,program_id,
										activity_id,subactivity_id,code,price,standard)
									select a.id, b.id, left(a.name,150), CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id,a.source,'',a.volume,1,a.program_id,a.activity_id,a.subactivity_id,
										a.code,a.price,a.standard
									from itb_plan_spending a, itb_plan_line b
									where a.plan_line_id = b.id and a.id not in (select spending_id from itb_plan_spending_actual) and a.id = '""" + str(rec.id) + """' 
									;
								""")

				if self.quartal4 == True:
					parent = self.env['itb.plan_implementation'].search([('id','=',self._context['parent_obj'])])
					parent_q =''
					parent_id=''
					if parent:
						parent_q = parent.quarter
						parent_id = parent.id
						
						date_start=fields.Date.from_string(str(self.year) + '-10-01')
						date_finish=fields.Date.from_string(str(self.year) + '-12-01')
						sp = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish),('plan_id','in',plan_id)])
						if sp:
							for rec in sp:
								if parent_q == 'q1':
									month='Jan'
								elif parent_q == 'q2':	
									month='Apr'
								elif parent_q == 'q3':
									month='Jul'
								else:
									month=rec.month

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										spending_id,plan_line_id,name,create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid,write_date, 
										active, write_uid, day, implementation_id,state,unit_id,price_id, 
										source, confirmation_note, volume, type_actual,program_id,
										activity_id,subactivity_id,code,price,standard)
									select a.id, b.id, left(a.name,150), CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id,a.source,'',a.volume,1,a.program_id,a.activity_id,a.subactivity_id,
										a.code,a.price,a.standard
									from itb_plan_spending a, itb_plan_line b
									where a.plan_line_id = b.id and a.id not in (select spending_id from itb_plan_spending_actual) and a.id = '""" + str(rec.id) + """' 
									;
								""")
