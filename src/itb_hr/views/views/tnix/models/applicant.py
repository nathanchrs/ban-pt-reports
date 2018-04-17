import random
import operator
from odoo import models, fields, api, exceptions
from datetime import datetime


class Posisi(models.Model):
    _name = 'tnix.posisi'
    _rec_name = 'nama'

    nama = fields.Char(compute='_get_nama_kode',store=True,index=True)
    kode = fields.Char(compute='_get_nama_kode',store=True,index=True)
    kesatuan_id = fields.Many2one('tnix.kesatuan', string='Kesatuan',required=True)
    kecabangan_id = fields.Many2one('tnix.kecabangan', string='Kecabangan')
    kuota = fields.Integer()
    terisi = fields.Integer(compute='_get_terisi',store=True)
    lowong = fields.Integer(compute='_get_lowong',store=True)
    bukaan = fields.Boolean(default=True)
    penempatan_ids = fields.One2many('tnix.kandidat','penempatan',string='Penempatan')
    rekomendasi1_ids = fields.One2many('tnix.kandidat','rekomendasi1',string='Rekomendasi1')
    rekomendasi2_ids = fields.One2many('tnix.kandidat','rekomendasi2',string='Rekomendasi2')

    _sql_constraints = [('kode_unique','UNIQUE(kode)',"kode posisi harus unik"),('nama_unique','UNIQUE(nama)',"nama posisi harus unik")]

    @api.constrains('kuota')
    def _check_kuota(self):
        for job in self:
            if job.kuota < 0:
                raise exceptions.ValidationError('Angka kuota tidak boleh negatif')

    '''
    @api.constrains('lowong')
    def _check_lowong(self):
        for job in self:
            if job.lowong < 0:
                raise exceptions.ValidationError('Angka Lowong tidak boleh negatif')
    '''

    @api.depends('kesatuan_id','kecabangan_id')
    def _get_nama_kode(self):
        for job in self:
            if job.kesatuan_id.kategori in ['a','b','c']:
                job.nama = job.kecabangan_id.nama + '-' + job.kesatuan_id.nama
                job.kode = job.kecabangan_id.kode + '-' + job.kesatuan_id.nama
            else:
                job.nama = job.kesatuan_id.nama
                job.kode = job.kesatuan_id.nama

    @api.depends('terisi','kuota')
    def _get_lowong(self):
        for job in self:
            job.lowong = job.kuota - job.terisi

    @api.depends('penempatan_ids')
    def _get_terisi(self):
        for job in self:
            job.terisi = len(job.penempatan_ids.filtered(lambda x: x.status == 'resmi'))


class Kuota(models.Model):
    _name = 'tnix.kuota'
    _rec_name = 'posisi_id'

    posisi_id = fields.Many2one('tnix.posisi',string='Posisi')
    jumlah = fields.Integer()


class Kecabangan(models.Model):
    _name = 'tnix.kecabangan'
    _rec_name = 'nama'

    nama = fields.Char()
    kode = fields.Char()
    kesatuan_ids = fields.Many2many('tnix.kesatuan',string='Alokasi Khusus Kesatuan')


class Gelombang(models.Model):
    _name = 'tnix.gelombang'
    _rec_name = 'nama'

    nama = fields.Char(required=True)
    aktif = fields.Boolean()

    @api.constrains('aktif')
    def _check_aktif(self):
        actives = self.env['tnix.gelombang'].search_count([('aktif','=',True)])
        if actives > 1:
            raise exceptions.ValidationError('Hanya 1 gelombang yang bisa aktif.Non-aktifkan sisanya')


class Kesatuan(models.Model):
    _name = 'tnix.kesatuan'
    _rec_name = 'nama'

    nama = fields.Char()
    kategori = fields.Selection([('a','Pool A'),('b','Pool B'),('c','Pool C'),('special','Pool Khusus'),('balakpus','Balakpus')],default='a')
    sequence = fields.Integer()
    lokasi = fields.Char()
    posisi_ids = fields.One2many('tnix.posisi','kesatuan_id',string='Posisi')
    propinsi_ids = fields.One2many('tnix.propinsi','kesatuan_id',string='Wilayah')
    terdekat_ids = fields.One2many('tnix.terdekat','kesatuan_id',string='Terdekat')
    suku_ids = fields.Many2many('tnix.suku',string='Suku Asli')
    khusus_diktuk = fields.Char(string='Hanya untuk Diktuk')
    khusus_kecabangan_ids = fields.Many2many('tnix.kecabangan',string='Hanya untuk Kecabangan')
    utama_kesarjanaan_ids = fields.Many2many('tnix.kesarjanaan',string='Diutamakan untuk Kesarjanaan')


class Kesarjanaan(models.Model):
    _name = 'tnix.kesarjanaan'

    name = fields.Char()
    kesatuan_ids = fields.Many2many('tnix.kesatuan',string='Alokasi Utama Kesatuan')



class Suku(models.Model):
    _name = 'tnix.suku'
    _rec_name = 'nama'

    nama = fields.Char()
    kesatuan_ids = fields.Many2many('tnix.kesatuan',string='Kesatuan Terkait')



class Terdekat(models.Model):
    _name = 'tnix.terdekat'
    _rec_name = 'kesatuan_dekat'

    kesatuan_id =  fields.Many2one('tnix.kesatuan',string='Kesatuan')
    kesatuan_dekat =  fields.Many2one('tnix.kesatuan', string='Terdekat')
    sequence = fields.Integer()



class Propinsi(models.Model):
    _name = 'tnix.propinsi'
    _rec_name = 'nama'

    nama = fields.Char()
    kesatuan_id =  fields.Many2one('tnix.kesatuan',string='Kesatuan')



class Kopassus(models.Model):
    _name = 'tnix.kopassus'
    _rec_name = 'nrp'

    nrp = fields.Char(string='NRP',required=True)
    catatan = fields.Text()

    @api.model
    def create(self, vals):
        if 'nrp' in vals and vals['nrp']:
            applicant = self.env['tnix.kandidat'].search([('nrp','=',vals['nrp'])])
            if applicant:
                new_record = super(Kopassus, self).create(vals)
                catatan = applicant.catatan if applicant.catatan else ''
                catatan = catatan + '; ' + vals['catatan']
                applicant.update({'catatan':catatan,'kopassus':True})
                return new_record



class Kostrad(models.Model):
    _name = 'tnix.kostrad'
    _rec_name = 'nrp'

    nrp = fields.Char(string='NRP',required=True)
    catatan = fields.Text()

    @api.model
    def create(self, vals):
        if 'nrp' in vals and vals['nrp']:
            applicant = self.env['tnix.kandidat'].search([('nrp','=',vals['nrp'])])
            if applicant:
                new_record = super(Kostrad, self).create(vals)
                catatan = applicant.catatan if applicant.catatan else ''
                catatan = catatan + '; ' + vals['catatan']
                applicant.update({'catatan':catatan,'kostrad':True})
                return new_record



class Bincab(models.Model):
    _name = 'tnix.bincab'
    _rec_name = 'nrp'

    nrp = fields.Char(string='NRP',required=True)
    rekomendasi_bincab_detil = fields.Char(string='Detil')
    rekomendasi_bincab = fields.Many2one('tnix.posisi', string='Rekomendasi',required=True)

    @api.model
    def create(self, vals):
        if 'nrp' in vals and vals['nrp']:
            applicant = self.env['tnix.kandidat'].search([('nrp','=',vals['nrp'])])
            if applicant:
                new_record = super(Bincab, self).create(vals)
                applicant.update({'rekomendasi_bincab_detil':vals['rekomendasi_bincab_detil'],'rekomendasi_bincab':vals['rekomendasi_bincab']})
                return new_record



class Kandidat(models.Model):
    _name = 'tnix.kandidat'
    _rec_name = 'nama'

    def _get_gelombang(self):
        gelombang = self.env['tnix.gelombang'].search([('aktif','=',True)])
        return gelombang


    nama = fields.Char(required=True,index=True)
    nrp = fields.Char( string='NRP')
    dikum = fields.Char()
    bidang = fields.Selection([('INTELIJEN','INTELIJEN'),('OPERASI','OPERASI'),('PERSONEL','PERSONEL'),('LOGISTIK','LOGISTIK'),('TERITORIAL','TERITORIAL'),('PERENCANAAN','PERENCANAAN')])
    sarjana_id =  fields.Many2one('tnix.kesarjanaan', string='Kesarjanaan')
    ranking = fields.Integer(string="Ranking Diktuk",group_operator='avg')
    ranking_sarcab = fields.Integer(string="Ranking SARCAB",group_operator='avg')
    pangkat = fields.Char()
    diktuk = fields.Selection([('AKMIL','AKMIL'),('SEPA','SEPA'),('SECAPA','SECAPA')],default='AKMIL')
    kelamin = fields.Selection([('L','Laki-Laki'),('P','Perempuan')],default='L')
    kecabangan_id =  fields.Many2one('tnix.kecabangan', string='Kecabangan')
    suku_id =  fields.Many2one('tnix.suku', string='Suku')
    panda = fields.Many2one('tnix.kesatuan', string='Panda')
    propinsi_tinggal = fields.Many2one('tnix.propinsi', string='Tempat Tinggal')
    propinsi_lahir = fields.Many2one('tnix.propinsi', string='Tempat Lahir')
    propinsi_suami = fields.Many2one('tnix.propinsi', string='Dinas Suami')
    kopassus = fields.Boolean(string='Diterima Kopassus')
    kostrad = fields.Boolean(string='Diterima Kostrad')
    minat_detil = fields.Char(string='Detil Minat 1')
    minat2_detil = fields.Char(string='Detil Minat 2')
    minat = fields.Many2one('tnix.kesatuan', string='Minat 1')
    minat2 = fields.Many2one('tnix.kesatuan', string='Minat 2')
    rekomendasi1 = fields.Many2one('tnix.posisi', string='Rekomendasi 1',readonly=True)
    rekomendasi2 = fields.Many2one('tnix.posisi', string='Rekomendasi 2',readonly=True)
    rekomendasi_bincab = fields.Many2one('tnix.posisi', string='Rek. BINCAB')
    rekomendasi_spersad = fields.Many2one('tnix.posisi', string='Rek. SPERSAD')
    rekomendasi_bincab_detil = fields.Char(string='Detil Rek. BINCAB')
    rekomendasi_spersad_detil = fields.Char(string='Detil Rek. SPERSAD')
    tipe = fields.Selection([('rekomendasi1','Rekomendasi 1'),('rekomendasi2','Rekomendasi 2'),('bincab','Saran BINCAB'),('spersad','Saran SPERSAD'),('bebas','Bebas')],string='Tempatkan sesuai')
    penempatan = fields.Many2one('tnix.posisi')
    penempatan_detil = fields.Char(string='Detil Penempatan')
    rekomendasi1_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi1.kesatuan_id',store=True, string='Kesatuan Rekomendasi 1')
    rekomendasi2_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi2.kesatuan_id',store=True, string='Kesatuan Rekomendasi 2')
    rekomendasi_bincab_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi_bincab.kesatuan_id',store=True, string='Kesatuan Rekomendasi BINCAB')
    rekomendasi_spersad_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi_spersad.kesatuan_id',store=True, string='Kesatuan Rekomendasi SPERSAD')
    penempatan_kesatuan = fields.Many2one('tnix.kesatuan',related='penempatan.kesatuan_id',store=True, string='Kesatuan Penempatan')
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    umur = fields.Integer(compute='_hitung_umur',store=True,group_operator='avg')
    tanggal_sidang = fields.Date()
    tanggal_keputusan = fields.Date()
    secapa = fields.Selection([('minat','Minat'),('toa','ToA'),('return','Return')],default='minat',string='Metode Alokasi')
    status = fields.Selection([('usulan','Usulan'),('resmi','Resmi')],default='usulan')
    foto = fields.Binary("Foto", attachment=True, help="Foto kandidat, ukurannya mohon max 1024x1024px.")
    catatan = fields.Text()
    gelombang_id = fields.Many2one('tnix.gelombang',string='Gelombang',default=_get_gelombang,store=True,index=True)

    _sql_constraints = [('nrp_unique','UNIQUE(nrp)',"kode NRP harus unik")]


    @api.onchange('tipe')
    def tempatkan(self):
        self.ensure_one()
        if self.tipe:
            if self.tipe == 'rekomendasi1':
                self.update({'penempatan':self.rekomendasi1})
            if self.tipe == 'rekomendasi2':
                self.update({'penempatan':self.rekomendasi2})
            if self.tipe == 'bincab':
                self.update({'penempatan':self.rekomendasi_bincab,'penempatan_detil':self.rekomendasi_bincab_detil})
            if self.tipe == 'spersad':
                self.update({'penempatan':self.rekomendasi_spersad,'penempatan_detil':self.rekomendasi_spersad_detil})


    @api.multi
    @api.depends('tanggal_lahir')
    def _hitung_umur(self):
        self.ensure_one()
        self.umur = 0
        if self.tanggal_lahir != False:
            format = '%Y-%m-%d %H:%M:%S'
            format_date = '%Y-%m-%d'
            converted_birthdate_year = datetime.strptime(self.tanggal_lahir,format_date).year
            converted_today_year = datetime.strptime(fields.Datetime.now(),format).date().year
            if (converted_today_year - converted_birthdate_year) > 0:
                self.umur = converted_today_year - converted_birthdate_year


    def set_draft(self):
        self.ensure_one()
        self.status = 'usulan'
    
    
    def print_bahan_sidang(self):
        applicants = self.env['tnix.kandidat'].search([('status','=','sidang')])
        if applicants:
            ids = []
            context = dict(active_ids=ids, active_model=self._name)
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'tnix.report_bahan_sidang_template',
                'context': context,
            }

        
    def empty(self):
        applicants = self.env['tnix.kandidat'].search([('status','=','usulan')])
        applicants.write({'rekomendasi1':False,'rekomendasi2':False,'penempatan':False})
        jobs = self.env['tnix.posisi'].search([])
        jobs.write({'terisi':0})
    

    def allocate(self):
        self.empty()
        self.allocate1()
        self.allocate2()
    
    
    def allocate1(self):
        applicants = self.env['tnix.kandidat'].search([('status','=','usulan')])
        jobs = self.env['tnix.posisi'].search([])
        departments = self.env['tnix.kesatuan'].search([])
        corps = self.env['tnix.kecabangan'].search([])
        akmil_kopassus = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat.nama == 'KOPASSUS')
        akmil_kostrad = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat.nama == 'KOSTRAD')
        akmil_other = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        sepa_kopassus = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat.nama == 'KOPASSUS')
        sepa_kostrad = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat.nama == 'KOSTRAD')
        sepa_other = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        secapa_kopassus = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat.nama == 'KOPASSUS')
        secapa_kostrad = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat.nama == 'KOSTRAD')
        secapa_other = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        akmil_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'AKMIL' not in str(x.khusus_diktuk)).mapped('nama')
        sepa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SEPA' not in str(x.khusus_diktuk)).mapped('nama')
        secapa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SECAPA' not in str(x.khusus_diktuk)).mapped('nama')
        kopassus_job = jobs.filtered(lambda x: x.kode == 'KOPASSUS')
        kostrad_job = jobs.filtered(lambda x: x.kode == 'KOSTRAD')
        kopassus_dep = departments.filtered(lambda x: x.nama == 'KOPASSUS')
        kostrad_dep = departments.filtered(lambda x: x.nama == 'KOSTRAD')
        kopassus_kecabangan = kopassus_dep.khusus_kecabangan_ids if kopassus_dep.khusus_kecabangan_ids else corps
        kostrad_kecabangan = kostrad_dep.khusus_kecabangan_ids if kostrad_dep.khusus_kecabangan_ids else corps
        rekomendasi_akmil = {x.id: 0 for x in departments}
        rekomendasi_sepa = {x.id: 0 for x in departments}

        if secapa_kopassus:
            for applicant in secapa_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                    else:
                        other_department = applicant.minat2
                        if other_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                        else:
                            kode = other_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                    if applicant.rekomendasi1 == False:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    break
                if applicant.secapa == 'toa':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job                        
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        break
                if applicant.secapa == 'return':
                    if applicant.panda.nama == 'KOPASSUS' and kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                    else:
                        other_department = applicant.panda
                        if other_department:
                            if other_department.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                            else:
                                kode = other_department.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                        if applicant.rekomendasi1 == False:
                            terdekat_dep = applicant.panda.terdekat_ids 
                            for dep in terdekat_dep:
                                if dep.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        
                                        break


        if secapa_kostrad:
            for applicant in secapa_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    
                    continue

                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        
                    else:
                        other_department = applicant.minat2
                        if other_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                        else:
                            kode = other_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                                
                    if applicant.rekomendasi1 == False:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    
                                    break
                if applicant.secapa == 'toa':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        break
                if applicant.secapa == 'return':
                    if applicant.panda.nama == 'KOSTRAD' and kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                    else:
                        other_department = applicant.panda
                        if other_department:
                            if other_department.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                            else:
                                kode = other_department.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                        if applicant.rekomendasi1 == False:
                            terdekat_dep = applicant.panda.terdekat_ids 
                            for dep in terdekat_dep:
                                if dep.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        
                                        break
        
        
        if secapa_other:
            for applicant in secapa_other:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if applicant.secapa == 'minat':
                    if applicant.minat:
                        potential_department = applicant.minat
                        if potential_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + potential_department.nama
                        else:
                            kode = potential_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                            else:
                                if applicant.minat2:
                                    if applicant.minat2.kategori in ['a','b','c']:
                                        kode2 = applicant.kecabangan_id.kode + '-' + applicant.minat2.nama
                                    else:
                                        kode2 = applicant.minat2.nama
                                    potential_job = jobs.filtered(lambda x: x.kode == kode2)
                                    if potential_job:
                                        if potential_job.bukaan:
                                            applicant.rekomendasi1 = potential_job
                    if applicant.rekomendasi1 == False:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    break
                if applicant.secapa == 'toa':
                    if applicant.minat:
                        if applicant.minat.kategori == 'a':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                        if applicant.minat.kategori == 'b':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                        if applicant.minat.kategori == 'c':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                        if applicant.minat.kategori not in ['a','b','c']:
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                        terdekat_dep = terdekat_dep.sorted(key=lambda x: (x.kategori,x.sequence))
                        for dep in terdekat_dep:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    break
                if applicant.secapa == 'return':
                    if applicant.panda:
                        potential_department = applicant.panda
                        if potential_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + potential_department.nama
                        else:
                            kode = potential_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                        if applicant.rekomendasi1 == False:
                            terdekat_dep = applicant.panda.terdekat_ids 
                            for dep in terdekat_dep:
                                if dep.kesatuan_id.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        break


        if akmil_kopassus:
            akmil_kopassus = akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in akmil_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                        recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                        for key, value in recap_akmil:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                                rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                                break


        if akmil_kostrad:
            akmil_kostrad = akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in akmil_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                        recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                        for key, value in recap_akmil:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                                rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                                break


        if akmil_other:
            akmil_other = akmil_other.sorted(key=lambda x: (x.ranking,x.kecabangan_id))
            for applicant in akmil_other:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                if other_department:
                    other_department = other_department.sorted(key=lambda x: x.sequence) 
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            other_department = sarjana_department
                    recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                    recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                    for key, value in recap_akmil:
                        dep = departments.filtered(lambda x: x.id == key)
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job and potential_job.bukaan:
                            applicant.rekomendasi1 = potential_job
                            rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                            break


        if sepa_kopassus:
            sepa_kopassus = sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in sepa_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                        recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                        for key, value in recap_sepa:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job
                                rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                                break


        if sepa_kostrad:
            sepa_kostrad = sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in sepa_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                        recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                        for key, value in recap_sepa:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi1 = potential_job                                
                                rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                                break


        if sepa_other:
            sepa_other = sepa_other.sorted(key=lambda x: (x.ranking,x.kecabangan_id))
            for applicant in sepa_other:
                if applicant.kopassus:
                    applicant.rekomendasi1 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi1 = kostrad_job
                    continue

                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                if other_department:
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                    recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                    for key, value in recap_sepa:
                        dep = departments.filtered(lambda x: x.id == key)
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job and potential_job.bukaan:
                            applicant.rekomendasi1 = potential_job
                            rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                            break



    def allocate2(self):
        applicants = self.env['tnix.kandidat'].search([('status','=','usulan')])
        jobs = self.env['tnix.posisi'].search([])
        departments = self.env['tnix.kesatuan'].search([])
        corps = self.env['tnix.kecabangan'].search([])
        akmil_kopassus = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat2.nama == 'KOPASSUS')
        akmil_kostrad = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat2.nama == 'KOSTRAD')
        akmil_other = applicants.filtered(lambda x: x.diktuk == 'AKMIL' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        sepa_kopassus = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat2.nama == 'KOPASSUS')
        sepa_kostrad = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat2.nama == 'KOSTRAD')
        sepa_other = applicants.filtered(lambda x: x.diktuk == 'SEPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        secapa_kopassus = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat2.nama == 'KOPASSUS')
        secapa_kostrad = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat2.nama == 'KOSTRAD')
        secapa_other = applicants.filtered(lambda x: x.diktuk == 'SECAPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        akmil_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'AKMIL' not in str(x.khusus_diktuk)).mapped('nama')
        sepa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SEPA' not in str(x.khusus_diktuk)).mapped('nama')
        secapa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SECAPA' not in str(x.khusus_diktuk)).mapped('nama')
        kopassus_job = jobs.filtered(lambda x: x.kode == 'KOPASSUS')
        kostrad_job = jobs.filtered(lambda x: x.kode == 'KOSTRAD')
        kopassus_dep = departments.filtered(lambda x: x.nama == 'KOPASSUS')
        kostrad_dep = departments.filtered(lambda x: x.nama == 'KOSTRAD')
        kopassus_kecabangan = kopassus_dep.khusus_kecabangan_ids if kopassus_dep.khusus_kecabangan_ids else corps
        kostrad_kecabangan = kostrad_dep.khusus_kecabangan_ids if kostrad_dep.khusus_kecabangan_ids else corps
        rekomendasi_akmil = {x.id: 0 for x in departments}
        rekomendasi_sepa = {x.id: 0 for x in departments}

        if secapa_kopassus:
            for applicant in secapa_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi2 = kopassus_job
                    else:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job        
                                    break
                if applicant.secapa == 'toa':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi2 = kopassus_job
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi2 = potential_job
                                        break
                if applicant.secapa == 'return':
                    if applicant.panda.nama == 'KOPASSUS' and kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi2 = kopassus_job
                    else:
                        other_department = applicant.panda
                        if other_department:
                            if other_department.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                            else:
                                kode = other_department.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job
                                    
                        if applicant.rekomendasi2 == False:
                            terdekat_dep = applicant.panda.terdekat_ids 
                            terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                            for dep in terdekat_dep:
                                if dep.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi2 = potential_job
                                        break


        if secapa_kostrad:
            for applicant in secapa_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi2 = kostrad_job
                    if applicant.rekomendasi2 == False:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job
                                    break
                if applicant.secapa == 'toa':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi2 = kostrad_job
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        other_department = other_department - applicant.rekomendasi1_kesatuan
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi2 = potential_job
                                        break
                if applicant.secapa == 'return':
                    if applicant.panda.nama == 'KOSTRAD' and kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi2 = kostrad_job
                    else:
                        other_department = applicant.panda
                        if other_department:
                            if other_department.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + other_department.nama
                            else:
                                kode = other_department.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job
                        if applicant.rekomendasi2 == False:
                            terdekat_dep = applicant.panda.terdekat_ids 
                            terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                            for dep in terdekat_dep:
                                if dep.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi2 = potential_job
                                        break
        
        
        if secapa_other:
            for applicant in secapa_other:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if applicant.secapa == 'minat':
                    if applicant.minat2:
                        potential_department = applicant.minat2
                        if potential_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + potential_department.nama
                        else:
                            kode = potential_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                    if applicant.rekomendasi2 == False:
                        terdekat_dep = applicant.minat.terdekat_ids + applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job
                                    break
                if applicant.secapa == 'toa':
                    if applicant.minat:
                        if applicant.minat.kategori == 'a':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                        if applicant.minat.kategori == 'b':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                        if applicant.minat.kategori == 'c':
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                        if applicant.minat.kategori not in ['a','b','c']:
                            terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                        terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
                        terdekat_dep = terdekat_dep.sorted(key=lambda x: (x.kategori,x.sequence))
                        for dep in terdekat_dep:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi2 = potential_job
                                    break
                if applicant.secapa == 'return':
                    if applicant.panda:
                        potential_department = applicant.panda
                        if potential_department.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + potential_department.nama
                        else:
                            kode = potential_department.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                        if applicant.rekomendasi2 == False:
                            terdekat_dep = applicant.panda.terdekat_ids
                            terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan 
                            for dep in terdekat_dep:
                                if dep.kesatuan_id.kategori in ['a','b','c']:
                                    kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                else:
                                    kode = dep.kesatuan_dekat.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi2 = potential_job
                                        break


        if akmil_kopassus:
            akmil_kopassus = akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in akmil_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        other_department = other_department.sorted(key=lambda x: x.sequence)
                        recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                        recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                        for key, value in recap_akmil:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                                rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                                break


        if akmil_kostrad:
            akmil_kostrad = akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in akmil_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        other_department = other_department.sorted(key=lambda x: x.sequence)
                        recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                        recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                        for key, value in recap_akmil:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                                rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                                break


        if akmil_other:
            akmil_other = akmil_other.sorted(key=lambda x: (x.ranking,x.kecabangan_id))
            for applicant in akmil_other:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department - applicant.rekomendasi1_kesatuan
                if other_department:
                    other_department = other_department.sorted(key=lambda x: x.sequence) 
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            other_department = sarjana_department
                    recap_akmil = {x:rekomendasi_akmil[x] for x in other_department.ids}
                    recap_akmil = sorted(recap_akmil.items(), key=operator.itemgetter(1))
                    for key, value in recap_akmil:
                        dep = departments.filtered(lambda x: x.id == key)
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job and potential_job.bukaan:
                            applicant.rekomendasi2 = potential_job
                            rekomendasi_akmil[potential_job.kesatuan_id.id] = rekomendasi_akmil[potential_job.kesatuan_id.id] + 1
                            break


        if sepa_kopassus:
            sepa_kopassus = sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in sepa_kopassus:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        other_department = other_department.sorted(key=lambda x: x.sequence)
                        recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                        recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                        for key, value in recap_sepa:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                                rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                                break


        if sepa_kostrad:
            sepa_kostrad = sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in sepa_kostrad:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        other_department = other_department.sorted(key=lambda x: x.sequence)
                        recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                        recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                        for key, value in recap_sepa:
                            dep = departments.filtered(lambda x: x.id == key)
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job and potential_job.bukaan:
                                applicant.rekomendasi2 = potential_job
                                rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                                break


        if sepa_other:
            sepa_other = sepa_other.sorted(key=lambda x: (x.ranking,x.kecabangan_id))
            for applicant in sepa_other:
                if applicant.kopassus:
                    applicant.rekomendasi2 = kopassus_job
                    continue

                if applicant.kostrad and not applicant.kopassus:
                    applicant.rekomendasi2 = kostrad_job
                    continue

                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department - applicant.rekomendasi1_kesatuan
                if other_department:
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    recap_sepa = {x:rekomendasi_sepa[x] for x in other_department.ids}
                    recap_sepa = sorted(recap_sepa.items(), key=operator.itemgetter(1))
                    for key, value in recap_sepa:
                        dep = departments.filtered(lambda x: x.id == key)
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job and potential_job.bukaan:
                            applicant.rekomendasi2 = potential_job
                            rekomendasi_sepa[potential_job.kesatuan_id.id] = rekomendasi_sepa[potential_job.kesatuan_id.id] + 1
                            break