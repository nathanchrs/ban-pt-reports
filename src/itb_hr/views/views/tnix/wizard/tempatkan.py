from odoo import models, fields, api, exceptions


class Tempatkan_Wizard(models.TransientModel):
    _name = 'tnix.tempatkan_wizard'
	
    tipe = fields.Selection([('rekomendasi1','Rekomendasi 1'),('rekomendasi2','Rekomendasi 2'),('bincab','Saran BINCAB'),('spersad','Saran SPERSAD'),('bebas','Bebas'),('seadanya','Seadanya')], default='spersad',required=True,string='Tempatkan sesuai')
    posisi_id = fields.Many2one('tnix.posisi',string='Posisi Terpilih')
    tanggal_keputusan = fields.Date(default=fields.Date.today(),string='Tanggal Keputusan')
    

    @api.multi
    def tempatkan(self):
        if not self.tipe or (self.tipe == 'bebas' and not self.posisi_id):
            raise exceptions.ValidationError('Tujuan Penempatan belum dipilih!')

        ids = self.env.context.get('active_ids',[])
        applicants = self.env['tnix.kandidat'].search(['&',('id','in',ids),('status','!=','resmi')])
        if self.tipe == 'rekomendasi1':
            for applicant in applicants:
                if applicant.rekomendasi1:
                    applicant.update({'penempatan':applicant.rekomendasi1,'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})
        elif self.tipe == 'rekomendasi2':
            for applicant in applicants:
                if applicant.rekomendasi2:
                    applicant.update({'penempatan':applicant.rekomendasi2,'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})
        elif self.tipe == 'bincab':
            for applicant in applicants:
                if applicant.rekomendasi_bincab:
                    applicant.update({'penempatan_detil':applicant.rekomendasi_bincab_detil,'penempatan':applicant.rekomendasi_bincab,'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})
        elif self.tipe == 'spersad':
            for applicant in applicants:
                if applicant.rekomendasi_spersad:
                    applicant.update({'penempatan_detil':applicant.rekomendasi_spersad_detil,'penempatan':applicant.rekomendasi_spersad,'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})        
        elif self.tipe == 'bebas':
            applicants.write({'penempatan':self.posisi_id.id,'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})
        elif self.tipe == 'seadanya':
            applicants.write({'tanggal_keputusan':self.tanggal_keputusan,'status':'resmi'})

        return{}