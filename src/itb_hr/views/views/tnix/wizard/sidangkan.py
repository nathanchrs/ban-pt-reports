from odoo import models, fields, api, exceptions


class Sidangkan_Wizard(models.TransientModel):
    _name = 'tnix.sidangkan_wizard'
	
    tanggal_sidang = fields.Date(default=fields.Date.today(),string='Tanggal Sidang')
    

    @api.multi
    def sidangkan(self):
        if not self.tanggal_sidang:
            raise exceptions.ValidationError('Tanggal sidang belum dipilih!')

        ids = self.env.context.get('active_ids',[])
        applicants = self.env['tnix.kandidat'].search(['&',('id','in',ids),('status','!=','resmi')])
        if self.tanggal_sidang:
            applicants.write({'tanggal_sidang':self.tanggal_sidang,'status':'sidang'})
        return{}