from odoo import models, fields, api, exceptions


class Spending_Int(models.Model):
	_name = 'itb.plan_spending_int'
	
	name = fields.Char(required=True ,index=True)
	code = fields.Char()
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', default='Jan', required=True ,index=True)
	day = fields.Date(compute='_month_day',readonly=True,store=True)
	standard = fields.Char(related='price_id.standard')
	price = fields.Float(related='price_id.amount')
	volume = fields.Float(readonly=True, compute='_sum_volume', default=1, store=True)
	total = fields.Float(default=0, string='Total')
	used = fields.Float()
	available = fields.Float(compute='_sum_available', store=True,readonly=True)
	paid = fields.Float()
	percent_budget = fields.Float(readonly=True, compute='_percent_budget_count', store=True)
	
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type',default='jasa')
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source',default='dm' ,index=True)
	#actual_ids = fields.One2many('itb.plan_spending_actual','spending_id',string='Spending Actual')
	price_id = fields.Many2one('itb.plan_price',domain="[('type','=',type)]",ondelete='cascade',required=True,index=True)
	plan_int_id = fields.Many2one('itb.plan_int',index=True)
	plan_line_id = fields.Many2one('itb.plan_line_int',ondelete='cascade',domain="[('plan_int_id','=',plan_int_id)]",required=True,index=True)
	allocation_int_ids = fields.One2many('itb.plan_allocation', 'spending_id_int', string= 'Allocation Internal')
	unit_id = fields.Many2one('itb.plan_unit',related='plan_int_id.unit_id',index=True, readonly=True, store=True)
	request_alo_ids = fields.One2many('itb.plan_request_alocation', 'spending_id', 'Request Alocation', index=True)
	logistic = fields.Boolean(string='Logistic', default=False, readonly=True, store=True)
	#request_dko_alo_ids = fields.One2many('itb.plan_dko_alocation', 'dko_spen_id', 'Request dko Alocation', copy=True, index=True)
	
	'''
	@api.one
	@api.constrains('volume')
	def _not_less_zero(self):
		if self.volume <= 0.00:
			raise exceptions.ValidationError("Volume do not less than zero.")
	'''

	@api.one
	@api.constrains('total')
	def _total_not_null(self):
		for rec in self:
			if rec.total == False:
				raise exceptions.ValidationError("Total must have a value not null.")

	
	@api.depends('month')
	def _month_day(self):
		months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
		
		for record in self:
			day_str = str(record.plan_int_id.year) + '-' + months[record.month] + '-01'
			record.day = fields.Date.from_string(day_str)			
	
	
	@api.one
	@api.depends('volume', 'price_id')
	def _sum_total(self):
		for rec in self:
			rec.total = rec.volume * rec.price_id.amount

	@api.one
	@api.depends('total', 'price_id')
	def _sum_volume(self):
		for rec in self:
			if rec.total > 0 and rec.price_id.amount > 0:
				rec.volume = rec.total / rec.price_id.amount

	#@api.one
	#@api.depends('request_alo_ids')
	#def _sum_used(self):
	#	used = [actual.used for actual in self.request_alo_ids]
	#	self.used = sum(used)

	@api.depends('total','used')
	def _sum_available(self):
		for record in self:
			record.available = record.total - record.used
	

	#@api.one
	#@api.onchange('actual_ids')
	#def _sum_used_onchange(self):
	#	used = [actual.used for actual in self.actual_ids]
	#	self.used = sum(used)

	@api.one
	@api.depends('total', 'used')
	def _percent_budget_count(self):
		for rec in self:
			if rec.total > 0:
				rec.percent_budget = (rec.used / rec.total) * 100
			else:
				rec.percent_budget = 0
			
	# def write(self, cr, uid, ids, vals, context=None):
	# 	self._sum_used()
	# 	res = super(my_class, self).write(cr, uid, ids, vals, context=context)
	# 	return res