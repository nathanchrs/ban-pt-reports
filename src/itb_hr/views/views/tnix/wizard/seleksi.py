from odoo import models, fields, api, exceptions


class Seleksi_Wizard(models.TransientModel):
    _name = 'tnix.seleksi_wizard'
	
    kesatuan = fields.Selection([('KOPASSUS','KOPASSUS'),('KOSTRAD','KOSTRAD')], default='KOPASSUS',required=True)
    catatan = fields.Text(required=True)
    

    @api.multi
    def seleksi(self):
        if not self.kesatuan:
            raise exceptions.ValidationError('Kesatuan hasil seleksi belum dipilih!')

        ids = self.env.context.get('active_ids',[])
        applicants = self.env['tnix.kandidat'].search(['&',('id','in',ids),('status','!=','resmi')])
        if self.kesatuan == 'KOPASSUS':
            for applicant in applicants:                
                catatan = applicant.catatan if applicant.catatan else ''
                catatan = catatan + '; ' + self.catatan
                applicant.update({'catatan':catatan,'kopassus':True})
        if self.kesatuan == 'KOSTRAD':
            for applicant in applicants:                
                catatan = applicant.catatan if applicant.catatan else ''
                catatan = catatan + '; ' + self.catatan
                applicant.update({'catatan':catatan,'kostrad':True})
        return{}
