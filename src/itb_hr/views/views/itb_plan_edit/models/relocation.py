from odoo import models, fields, api, exceptions

class Relocation(models.Model):
	_name = 'itb.plan_relocation'
	
	name = fields.Char()
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type',default='jasa')
	price_id = fields.Many2one('itb.plan_price',domain="[('type','=',type)]",ondelete='cascade',required=True,index=True)
	notes = fields.Text()
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')], 'Status', default='draft',required=True, readonly=True, copy=False)
	relocation_line_ids = fields.One2many('itb.plan_relocation_line','relocation_id')

	@api.one
	@api.constrains('relocation_amount')
	def _check_amount(self):
		return self.relocation_amount <= self.available_source

	@api.one
	@api.depends('relocation_amount')
	def _get_tobeamount(self):
		self.to_be_amount = self.available_destination + self.relocation_amount

	def action_state_confirmed(self):
		self.write({ 'state' : 'confirm' })
		return True

	def action_state_validated(self):
		self.write({ 'state' : 'validate' })
		return True

	def action_state_abort(self):
		self.write({ 'state' : 'draft' })
		return True

class RelocationLine(models.Model):
	_name = 'itb.plan_relocation_line'
	
	relocation_id = fields.Many2one('itb.plan_relocation')
	source_id = fields.Many2one('itb.plan_spending_actual',required=True)
	available_source = fields.Float(related='source_id.available',default=0,readonly=True)
	relocation_amount = fields.Float(default=0)
	destination_id = fields.Many2one('itb.plan_spending_actual',required=True)
	available_destination = fields.Float(related='destination_id.available',default=0,readonly=True)
	to_be_amount = fields.Float(readonly=True)