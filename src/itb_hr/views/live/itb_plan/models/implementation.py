from odoo import models, fields, api, exceptions
from datetime import datetime


class Implementation(models.Model):
	_name = 'itb.plan_implementation'
	#_rec_name = 'quarter'
	
	
	quarter = fields.Selection([('q1','Jan-Mar'),('q2', 'Apr-Jun'),('q3','Jul-Sep'),('q4','Oct-Dec')], 'Quarter',default='q1')
	reference = fields.Char()
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')], 'Status', default='draft')
	#plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True,domain="[('state','=','validate')]")
	spending_actual_ids = fields.One2many('itb.plan_spending_actual', 'implementation_id', 'Spending Implementation Lines', copy=True)
	
	@api.multi
	def action_state_confirmed(self):
		if self.spending_actual_ids:
			for rec in self.spending_actual_ids:
				#imp= self.env['itb.plan_implementation'].search([('id','=',rec)])
				actual=self.env['itb.plan_spending_actual'].search([('id','=',rec.id)])
			#for dat in actual:
				spending=self.env['itb.plan_spending'].search([('id','=',actual.spending_id.id)])
				spending.write({'implemented' : actual.total,})

				self.state = 'confirm'
		else:
			raise models.ValidationError('Spending ids empty')
		#self.write({ 'state' : 'confirm' })
		#return True
	
	@api.multi
	def action_state_validated(self):
		self.state = 'validate'
		#self.write({ 'state' : 'validate' })
		#return True

	@api.multi
	def action_state_abort(self):
		for rec in self.spending_actual_ids:
			#imp= self.env['itb.plan_implementation'].search([('id','=',rec)])
			actual=self.env['itb.plan_spending_actual'].search([('id','=',rec.id)])
		#for rec in actual:
			spending=self.env['itb.plan_spending'].search([('id','=',actual.spending_id.id)])
			spending.write({'implemented' : 0,})
		self.state = 'draft'
		#self.write({ 'state' : 'draft' })
		#return True

	@api.multi
	def generate_spending(self):
		return {
        	'name': 'Generate Spending for Plan ITB',
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

#class Tbl_temp(models.Model):
#	_name = 'itb.plan_temp'
#	val1 = fields.Char()
#	val2 = fields.Integer()
#	val3 = fields.Integer()
#	val4 = fields.Integer()

class Wizard_Implementation(models.TransientModel):
	_name = 'itb.plan_wizard_implementasi'

	tgl = datetime.now()
	#@api.multi
	#def get_data(self):
	#	self.note = self._context['parent_obj']
	par_id=0
	year = fields.Integer(default=tgl.year, string="Year")
	quartal1 = fields.Boolean(default=True, string="Q1")
	quartal2 = fields.Boolean(default=False, string="Q2")
	quartal3 = fields.Boolean(default=False, string="Q3")
	quartal4 = fields.Boolean(default=False, string="Q4")
	#note = fields.Char(default='get_data', string="Note")

	@api.multi
	def yesd(self):
		if self.year>0:
			if self.quartal1==True:
				date_start=date(int(self.year),1,1)
				date_finish=date(int(self.year),3,1)
				spend = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish)])
			#	for rec in spend:


			if self.quartal2==True:
				date_start=datetime(int(self.year),4,1)
				date_finish=date(int(self.year),6,1)
				spend = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish)])



			if self.quartal3==True:
				date_start=datetime(int(self.year),7,1)
				date_finish=datetime(int(self.year),9,1)
				spend = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish)])

			if self.quartal4==True:
				date_start=date(int(self.year),10,1)
				date_finish=date(int(self.year),12,1)
				spend = self.env['itb.plan_spending'].search([('day','>=',date_start),('day','<=',date_finish)])


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
								
								#self.env.cr.execute("""
								#	INSERT INTO itb_plan_temp(val1,val2,val3,val4) 
								#	select  '""" + month + """', '""" + str(self._uid) + """', '""" + str(parent_id) + """', '""" 
								#	+ str(rec.id) + """'
								#	;
								#""")

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid, spending_id, write_date, 
										active, write_uid, day, plan_line_id, implementation_id,state,unit_id,price_id)
									select CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, a.id, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, a.plan_line_id, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id
									from itb_plan_spending a, itb_plan_line b 
									where a.plan_line_id = b.id and a.id = '""" + str(rec.id) + """' 
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
								
								#self.env.cr.execute("""
								#	INSERT INTO itb_plan_temp(val1,val2,val3,val4) 
								#	select  '""" + month + """', '""" + str(self._uid) + """', '""" + str(parent_id) + """', '""" 
								#	+ str(rec.id) + """'
								#	;
								#""")

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid, spending_id, write_date, 
										active, write_uid, day, plan_line_id, implementation_id,state,unit_id,price_id)
									select CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, a.id, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, a.plan_line_id, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id
									from itb_plan_spending a, itb_plan_line b 
									where a.plan_line_id = b.id and a.id = '""" + str(rec.id) + """' 
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
								
								#self.env.cr.execute("""
								#	INSERT INTO itb_plan_temp(val1,val2,val3,val4) 
								#	select  '""" + month + """', '""" + str(self._uid) + """', '""" + str(parent_id) + """', '""" 
								#	+ str(rec.id) + """'
								#	;
								#""")

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid, spending_id, write_date, 
										active, write_uid, day, plan_line_id, implementation_id,state,unit_id,price_id)
									select CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, a.id, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, a.plan_line_id, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id
									from itb_plan_spending a, itb_plan_line b 
									where a.plan_line_id = b.id and a.id = '""" + str(rec.id) + """' 
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
								
								#self.env.cr.execute("""
								#	INSERT INTO itb_plan_temp(val1,val2,val3,val4) 
								#	select  '""" + month + """', '""" + str(self._uid) + """', '""" + str(parent_id) + """', '""" 
								#	+ str(rec.id) + """'
								#	;
								#""")

								self.env.cr.execute("""
									INSERT INTO itb_plan_spending_actual(
										create_date, month, total, create_uid, plan_id, 
										percent_budget, type, available, used, paid, spending_id, write_date, 
										active, write_uid, day, plan_line_id, implementation_id,state,unit_id,price_id)
									select CURRENT_TIMESTAMP, '""" + month + """', a.total,'""" + str(self._uid) + """', a.plan_id,
										a.percent_budget, a.type, a.available, a.used, a.paid, a.id, CURRENT_TIMESTAMP,
										TRUE, '""" + str(self._uid) + """', a.day, a.plan_line_id, '""" + str(parent_id) + """','draft', 
										b.unit_id, a.price_id
									from itb_plan_spending a, itb_plan_line b 
									where a.plan_line_id = b.id and a.id = '""" + str(rec.id) + """' 
									;
								""")