from odoo import models, fields, api, exceptions, tools
from datetime import date,datetime

class Plan_Int(models.Model):
	_name = 'itb.plan_int'
	_sql_constraints = [
		('name', 'unique(name)', 'Nama rencana harus berbeda dengan yang pernah dibuat')
	]

	name = fields.Char(required=True,compute='_compute_name',store=True,default='Default Name Plan')
	# name_view = fields.Char(compute='_autoreload_name')
	year = fields.Integer(default=date.today().year+1, required=True)
	budget = fields.Float(compute='_compute_budget', store=True, default=0)
	percent_budget = fields.Float(readonly=True, compute='_compute_avg', store=True, default=0)
	percent_performance = fields.Float(readonly=True, compute='_compute_avg', store=True, default=0)
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated'),('archived','Archived')], 'Status', default='draft',required=True, readonly=True, copy=False)
	unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	plan_line_ids = fields.One2many('itb.plan_line_int', 'plan_int_id', 'Initiative', copy=True)
	target_ids = fields.One2many('itb.plan_target_int','plan_int_id',string='Performance')
	spending_ids = fields.One2many('itb.plan_spending_int','plan_int_id',string='Budget')
	
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
	def _compute_budget(self):
		spendings = [spending.total for spending in self.spending_ids]
		self.budget = sum(spendings)
	
	@api.one
	@api.depends('unit_id')
	#@api.onchange('unit_id')
	def _compute_name(self):
		if self.unit_id:
			self.name = str(self.unit_id.name + ' ' + str(date.today().year+1))
			# self.name_view = str(self.unit_id.name + ' ' + str(date.today().year+1))
		else:
			self.name = 'Default Name Plan'
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
	def _compute_avg(self):
		count = 0
		perf_total = 0
		budg_total = 0
		for row in self.plan_line_ids.search([('plan_int_id', '=', self.id)]):
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

	#@api.multi
	def tes(self):
		tgl = datetime.now()
		thn = tgl.year + 1
		tbl = self.env['itb.plan_tes'].search([])
		ret = self.env['itb.plan_tes'].create({'rec1':thn,'rec2':'Testing'})

	@api.multi
	def generate_plan_itb(self):
		return {
        	'name': 'Generate Plan ITB',
        	'type': 'ir.actions.act_window',
            'res_model': 'itb.plan_dialog',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        	}

	@api.model_cr
	def simpan(self):
		tgl = datetime.now()
		thn = tgl.year + 1

		plan = self.env['itb.plan'].search([('year','=',thn),('state','=','validate')])
		if plan:
			#raise exceptions.except_orm(('My Title'), ('My message + lorem ipsum'))
			#raise Warning(_("You are trying to delete a record that is still referenced!"))
			tb_plan = self.env['itb.plan'].search([('year','=',thn)])
    		#return super(tb_plan, self).unlink()
			ret = tb_plan.unlink()
		#else:
		self.env.cr.execute("""
			INSERT INTO itb_plan(create_uid, name, percent_budget, year, budget, write_uid,state, percent_performance, write_date, create_date)
			select """ + str(self._uid) + """,'Plan STEI - """ + str(thn) + """',0,""" + str(thn) + """
			,0,""" + str(self._uid) + """,'draft',0,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP 
			;
		""")

		plan = self.env['itb.plan'].search([('year','=',thn)])
		if plan :
			p_int = self.env['itb.plan_int'].search([('year','=',thn)])
			budget_total = 0
			for w in p_int:
				if p_int:
					p_line_int = self.env['itb.plan_line_int'].search([('plan_int_id','=',w.id)])
					for x in p_line_int:
						if x.id:
							self.env.cr.execute("""
								insert into itb_plan_line (subactivity_id, code, create_date, barang, write_uid, plan_id, 
										percent_performance, create_uid, percent_budget, pegawai, activity_id, 
										program_id, write_date, name, budget, jasa, modal,unit_id)
								SELECT a.subactivity_id, a.code,CURRENT_TIMESTAMP , a.barang, """ + str(self._uid) + """, """ + str(plan.id) + """, 
										a.percent_performance, """ + str(self._uid) + """, a.percent_budget, a.pegawai, a.activity_id, 
										a.program_id,CURRENT_TIMESTAMP, a.name, a.budget, a.jasa, a.modal,b.unit_id
								FROM public.itb_plan_line_int a, itb_plan_int b
								where a.plan_int_id=b.id and a.id='""" + str(x.id) + """'
								;
							""") 
							p_line = self.env['itb.plan_line'].search([('plan_id','=',plan.id)], order='id desc', limit=1)
							if p_line:
								self.env.cr.execute("""
										INSERT INTO itb_plan_spending(
											code, create_date, month, price_id, total, create_uid, plan_id,
											percent_budget, source, type, available, used, paid, volume,
											write_date, write_uid, day, name, plan_line_id) 
										select code, CURRENT_TIMESTAMP, month, price_id, total, """ + str(self._uid) + """,""" + str(plan.id) + """,
											percent_budget, source, type, available, used, paid, volume,
											CURRENT_TIMESTAMP, """ + str(self._uid) + """, day, name, """ + str(p_line.id) + """ 
										from itb_plan_spending_int
										where plan_line_id='""" + str(x.id) + """' and plan_int_id='""" + str(w.id) + """'
									;
								""")

								budget=self.env['itb.plan_spending_int'].search([('plan_line_id','=',x.id),('plan_int_id','=',w.id)])
								if budget:
									for rec in budget:
										p_spend = self.env['itb.plan_spending'].search([('plan_id','=',plan.id)], order='id desc', limit=1)
										budget_total = budget_total + rec.total
										self.env.cr.execute("""
												INSERT INTO itb_plan_allocation(
													create_uid, write_date, budget, write_uid, create_date, spending_id_int, 
													date_request, note, spending_id, date_created) 
												select """ + str(self._uid) + """, CURRENT_TIMESTAMP, """ + str(rec.total) + """, """ + str(self._uid) + 
													""", CURRENT_TIMESTAMP, """ + str(rec.id)  + """, CURRENT_TIMESTAMP, '', """ 
													+ str(p_spend.id) + """, CURRENT_TIMESTAMP 
											;
										""")

								self.env.cr.execute("""
										INSERT INTO itb_plan_target(
											create_uid, plan_id, indicator_id, create_date, plan, write_date, 
											actual, write_uid, plan_line_id) 
										select """ + str(self._uid) + """, """ + str(plan.id) + """, indicator_id, CURRENT_TIMESTAMP, plan, CURRENT_TIMESTAMP, 
											actual, """ + str(self._uid) + """, """ + str(p_line.id) + """ 
										from itb_plan_target_int
										where plan_line_id='""" + str(x.id) + """' and plan_int_id='""" + str(w.id) + """'
									;
								""")

			self.env.cr.execute("""
					update itb_plan
						set budget = '""" + str(budget_total) + """'
					where id='""" + str(plan.id) + """' and year='""" + str(thn) + """'
				;
			""")	


        #tools.drop_view_if_exists(self._cr, 'itb_hr_report_membership')
		#tgl = datetime.now()
		#year = tgl.year + 1
		#plan = self.env['itb.plan'].search([])
		#plan_line = self.env['itb.plan_line'].search([])
		#target = self.env['itb.plan_target'].search([])
		#spending = self.env['itb.plan_spending'].search([])
		#ret = self.env['itb.plan'].create({'name': 'Plan STEI - ' + str(year),'year' : year})
		#rec_h = self.env['itb.plan'].search([('name','=','Plan STEI - ' + str(year))])
		#dat = self.env['itb.plan_int'].search([('year','=',year)])
		#uid = request.uid

        
		

	def set_plan_itb(self):
		
		#itb.plan.write({'name': [(2,plan.name) for plan in ('Plan ITB - ' + str(rec.year))]})
		tgl = datetime.now()
		year = tgl.year + 1
		plan = self.env['itb.plan'].search([])
		plan_line = self.env['itb.plan_line'].search([])
		target = self.env['itb.plan_target'].search([])
		spending = self.env['itb.plan_spending'].search([])
		ret = self.env['itb.plan'].create({'name': 'Plan STEI - ' + str(year),'year' : year})
		rec_h = self.env['itb.plan'].search([('name','=','Plan STEI - ' + str(year))])
		dat = self.env['itb.plan_int'].search([('year','=',year),('state','=','confirm')])
		if dat:
			for rec in dat:
				if rec.name:
					rec1 = self.env['itb.plan_line_int'].search([('plan_int_id', '=', rec.id)])
					#unit = self.env['itb.plan_unit'].search([('id','=',rec.unit_id)])
					for pl in rec1:
						if pl.name:
							#activity = self.env['itb.plan_activity'].search([('name','=',pl.activity_id),('name','=',pl.program_id)])
							#subactivity = self.env['itb.plan_subactivity'].search([('name','=',pl.subactivity_id),('activity_id','=',pl.activity_id)])
							ret = self.env['itb.plan_line'].create({
										'name' : pl.name,
										'code' : pl.code,
										'unit_id' : rec.unit_id,
										'program_id' : pl.program_id,
										'activity_id' : pl.activity_id,
										'subactivity_id' : pl.subactivity_id,
										'plan_id' : rec_h.id
									})
							rec_p = self.env['itb.plan_line'].search([('plan_id','=',rec_h.id)], order='id desc', limit=1)

class Dialog(models.TransientModel):
	_name = 'itb.plan_dialog'

	yes_no = fields.Char(default='Do you want to proceedS?')
	
	@api.multi
	def isi(self):
		tgl = datetime.now()
		thn = tgl.year + 1

		plan = self.env['itb.plan'].search([('year','=',thn)])
		if plan:
			#raise exceptions.except_orm(('My Title'), ('My message + lorem ipsum'))
			#raise Warning(_("You are trying to delete a record that is still referenced!"))
			tb_plan = self.env['itb.plan'].search([('year','=',thn)])
    		#return super(tb_plan, self).unlink()
			ret = tb_plan.unlink()
		#else:
		self.env.cr.execute("""
			INSERT INTO itb_plan(create_uid, name, percent_budget, year, budget, write_uid,state, percent_performance, write_date, create_date)
			select """ + str(self._uid) + """,'Plan STEI - """ + str(thn) + """',0,""" + str(thn) + """
			,0,""" + str(self._uid) + """,'draft',0,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP 
			;
		""")

		plan = self.env['itb.plan'].search([('year','=',thn)])
		if plan :
			p_int = self.env['itb.plan_int'].search([('year','=',thn),('state','=','validate')])
			budget_total = 0
			for w in p_int:
				if p_int:
					p_line_int = self.env['itb.plan_line_int'].search([('plan_int_id','=',w.id)])
					for x in p_line_int:
						if x.id:
							self.env.cr.execute("""
								insert into itb_plan_line (subactivity_id, code, create_date, barang, write_uid, plan_id, 
										percent_performance, create_uid, percent_budget, pegawai, activity_id, 
										program_id, write_date, name, budget, jasa, modal,unit_id)
								SELECT a.subactivity_id, a.code,CURRENT_TIMESTAMP , a.barang, """ + str(self._uid) + """, """ + str(plan.id) + """, 
										a.percent_performance, """ + str(self._uid) + """, a.percent_budget, a.pegawai, a.activity_id, 
										a.program_id,CURRENT_TIMESTAMP, a.name, a.budget, a.jasa, a.modal,b.unit_id
								FROM public.itb_plan_line_int a, itb_plan_int b
								where a.plan_int_id=b.id and a.id='""" + str(x.id) + """'
								;
							""") 
							p_line = self.env['itb.plan_line'].search([('plan_id','=',plan.id)], order='id desc', limit=1)
							if p_line:
								self.env.cr.execute("""
										INSERT INTO itb_plan_spending(
											code, create_date, month, price_id, total, create_uid, plan_id,
											percent_budget, source, type, available, used, paid, volume,
											write_date, write_uid, day, name, plan_line_id) 
										select code, CURRENT_TIMESTAMP, month, price_id, total, """ + str(self._uid) + """,""" + str(plan.id) + """,
											percent_budget, source, type, available, used, paid, volume,
											CURRENT_TIMESTAMP, """ + str(self._uid) + """, day, name, """ + str(p_line.id) + """ 
										from itb_plan_spending_int
										where plan_line_id='""" + str(x.id) + """' and plan_int_id='""" + str(w.id) + """'
									;
								""")

								budget=self.env['itb.plan_spending_int'].search([('plan_line_id','=',x.id),('plan_int_id','=',w.id)])
								if budget:
									for rec in budget:
										p_spend = self.env['itb.plan_spending'].search([('plan_id','=',plan.id)], order='id desc', limit=1)
										budget_total = budget_total + rec.total
										self.env.cr.execute("""
												INSERT INTO itb_plan_allocation(
													create_uid, write_date, budget, write_uid, create_date, spending_id_int, 
													date_request, note, spending_id, date_created) 
												select """ + str(self._uid) + """, CURRENT_TIMESTAMP, """ + str(rec.total) + """, """ + str(self._uid) + 
													""", CURRENT_TIMESTAMP, """ + str(rec.id)  + """, CURRENT_TIMESTAMP, '', """ 
													+ str(p_spend.id) + """, CURRENT_TIMESTAMP 
											;
										""")

								self.env.cr.execute("""
										INSERT INTO itb_plan_target(
											create_uid, plan_id, indicator_id, create_date, plan, write_date, 
											actual, write_uid, plan_line_id) 
										select """ + str(self._uid) + """, """ + str(plan.id) + """, indicator_id, CURRENT_TIMESTAMP, plan, CURRENT_TIMESTAMP, 
											actual, """ + str(self._uid) + """, """ + str(p_line.id) + """ 
										from itb_plan_target_int
										where plan_line_id='""" + str(x.id) + """' and plan_int_id='""" + str(w.id) + """'
									;
								""")

			self.env.cr.execute("""
					update itb_plan
						set budget = '""" + str(budget_total) + """'
					where id='""" + str(plan.id) + """' and year='""" + str(thn) + """'
				;
			""")
	
	@api.multi
	def no(self):
	    pass

class Plan_Line_Int(models.Model):
	_name = 'itb.plan_line_int'
	
	name = fields.Char(required=True)
	code = fields.Char()
	barang = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	jasa = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	modal = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	pegawai = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	budget = fields.Float(default=0)
	percent_budget = fields.Float(compute='_compute_spending', readonly=True, default=0, store=True)
	percent_performance = fields.Float(compute='_compute_target', readonly=True, default=0, store=True)

	program_id = fields.Many2one('itb.plan_program',ondelete='cascade',required=True,index=True)
	activity_id = fields.Many2one('itb.plan_activity',ondelete='cascade',domain="[('program_id','=',program_id)]",required=True,index=True)
	subactivity_id = fields.Many2one('itb.plan_subactivity',ondelete='cascade',domain="[('activity_id','=',activity_id)]",required=True,index=True)
	plan_int_id = fields.Many2one('itb.plan_int',ondelete='cascade',required=True,index=True)
	target_ids = fields.One2many('itb.plan_target_int','plan_line_id',string='Performance Target')
	spending_ids = fields.One2many('itb.plan_spending_int','plan_line_id',string='Spending')

	@api.one
	@api.depends('spending_ids')
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