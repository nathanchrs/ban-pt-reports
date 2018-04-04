from odoo import models, fields, api, exceptions


class Secapa_Wizard(models.TransientModel):
    _name = 'tnix.secapa_wizard'
	
    secapa = fields.Selection([('minat','Minat'),('toa','ToA'),('return','Return')],default='minat',string='Metode Alokasi')
    

    @api.multi
    def alokasi(self):
        if not self.secapa:
            raise exceptions.ValidationError('Metode alokasi SECAPA belum dipilih')

        ids = self.env.context.get('active_ids',[])
        applicants = self.env['tnix.kandidat'].search(['&',('id','in',ids),('status','!=','resmi'),('diktuk','=','SECAPA')])
        if self.secapa:
            applicants.write({'secapa':self.secapa})
        return{}