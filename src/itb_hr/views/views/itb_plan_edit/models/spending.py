from odoo import models, fields, api, exceptions


class Spending(models.Model):
	_name = 'itb.plan_spending'
	
	name = fields.Char(required=True, index=True)
	code = fields.Char()
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month', required=True ,index=True)
	day = fields.Date(compute='_month_day',readonly=True, store=True)
	volume = fields.Float(readonly=True, compute='_sum_volume', default=1, store=True)
	total = fields.Float(default=0, string='Total')
	#total = fields.Float(readonly=True, compute='_sum_volume', store=True)
	used = fields.Float(compute='_sum_used',store=True)
	available = fields.Float(compute='_sum_available', store=True, readonly=True)
	paid = fields.Float()
	implemented = fields.Float()
	percent_budget = fields.Float(readonly=True, compute='_percent_budget_count', store=True)
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type',default='jasa')
	source = fields.Selection([('dm','Dana Masyarakat'),('boptn', 'BOPTN')], 'Source',default='dm' ,index=True)
	actual_ids = fields.One2many('itb.plan_spending_actual','spending_id',string='Spending Actual')
	allocation_ids = fields.One2many('itb.plan_allocation', 'spending_id', string= 'Allocation')
	#actual_ids = fields.Many2one('itb.plan_spending_actual','implementation_id', ondelete='cascade', string='Spending Actual')
	logistic = fields.Boolean(string='Logistic', default=False, readonly=True, store=True)
	
	price_id = fields.Many2one('itb.plan_price',domain="[('type','=',type)]",ondelete='cascade',required=True,index=True)
	plan_id = fields.Many2one('itb.plan',index=True)
	plan_line_id = fields.Many2one('itb.plan_line',ondelete='cascade',domain="[('plan_id','=',plan_id)]",required=True,index=True)
	
	standard = fields.Char(related='price_id.standard', readonly=True, store=True)
	price = fields.Float(related='price_id.amount', readonly=True, store=True)
	unit_id = fields.Many2one(related='plan_line_id.unit_id', readonly=True, store=True, index=True)
	program_id = fields.Many2one(related='plan_line_id.program_id', readonly=True, store=True, index=True)
	activity_id = fields.Many2one(related='plan_line_id.activity_id', readonly=True, store=True, index=True)
	subactivity_id = fields.Many2one(related='plan_line_id.subactivity_id', readonly=True, store=True, index=True)

	#@api.one
	#@api.constrains('volume')
	#def _not_less_zero(self):
	#	if self.volume <= 0.00:
	#		raise exceptions.ValidationError("Volume do not less than zero.")
	
	@api.one
	@api.constrains('total')
	def _total_not_null(self):
		if self.total == False :
			raise exceptions.ValidationError("Total must have a value not null.")

	
	@api.depends('month')
	def _month_day(self):
		months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
		
		for record in self:
			day_str = str(record.plan_id.year) + '-' + months[record.month] + '-01'
			record.day = fields.Date.from_string(day_str)			
	
	
	@api.one
	@api.depends('total', 'price_id')
	def _sum_volume(self):
		if self.total > 0 and self.price_id.amount > 0:
			self.volume = self.total / self.price_id.amount
	@api.one
	@api.depends('volume', 'price_id')
	def _sum_total(self):
		self.total = self.volume * self.price_id.amount

	@api.one
	@api.depends('actual_ids')
	def _sum_used(self):
		used = [actual.used for actual in self.actual_ids]
		self.used = sum(used)

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
		if self.total > 0:
			self.percent_budget = (self.used / self.total) * 100
		else:
			self.percent_budget = 0
			
	# def write(self, cr, uid, ids, vals, context=None):
	# 	self._sum_used()
	# 	res = super(my_class, self).write(cr, uid, ids, vals, context=context)
	# 	return res