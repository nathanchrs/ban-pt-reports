import random
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
    gelombang_id = fields.Many2one('tnix.posisi',string='Gelombang')
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
    active = fields.Boolean()
    kuota_ids = fields.One2many('tnix.kuota','gelombang_id',string='Kuota')


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



class Kandidat(models.Model):
    _name = 'tnix.kandidat'
    _rec_name = 'nama'

    nama = fields.Char(required=True,index=True)
    nrp = fields.Char( string='NRP')
    dikum = fields.Char()
    bidang = fields.Selection([('INTELIJEN','INTELIJEN'),('OPERASI','OPERASI'),('PERSONEL','PERSONEL'),('LOGISTIK','LOGISTIK'),('TERITORIAL','TERITORIAL'),('PERENCANAAN','PERENCANAAN')])
    sarjana_id =  fields.Many2one('tnix.kesarjanaan', string='Kesarjanaan')
    #ranking_dikum = fields.Integer(string="Ranking Dikum")
    ranking = fields.Integer(string="Ranking Diktuk",group_operator='avg')
    #ranking_diksar = fields.Integer(string="Ranking Diksar")
    pangkat = fields.Char()
    diktuk = fields.Selection([('AKMIL','AKMIL'),('SEPA','SEPA'),('SECAPA','SECAPA')],default='AKMIL')
    kelamin = fields.Selection([('L','Laki-Laki'),('P','Perempuan')],default='L')
    kecabangan_id =  fields.Many2one('tnix.kecabangan', string='Kecabangan')
    suku_id =  fields.Many2one('tnix.suku', string='Suku')
    minat = fields.Many2one('tnix.kesatuan', string='Minat')
    minat2 = fields.Many2one('tnix.kesatuan', string='Minat 2')
    panda = fields.Many2one('tnix.kesatuan', string='Panda')
    propinsi_tinggal = fields.Many2one('tnix.propinsi', string='Tempat Tinggal')
    propinsi_lahir = fields.Many2one('tnix.propinsi', string='Tempat Lahir')
    propinsi_suami = fields.Many2one('tnix.propinsi', string='Dinas Suami')
    rekomendasi1 = fields.Many2one('tnix.posisi', string='Rekomendasi 1')
    rekomendasi2 = fields.Many2one('tnix.posisi', string='Rekomendasi 2')
    rekomendasi1_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi1.kesatuan_id',store=True, string='Kesatuan Rekomendasi 1')
    rekomendasi2_kesatuan = fields.Many2one('tnix.kesatuan',related='rekomendasi2.kesatuan_id',store=True, string='Kesatuan Rekomendasi 2')
    penempatan = fields.Many2one('tnix.posisi')
    kesatuan_penempatan = fields.Many2one('tnix.kesatuan',related='penempatan.kesatuan_id',store=True)
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    umur = fields.Integer(compute='_hitung_umur',store=True,group_operator='avg')
    tanggal_sidang = fields.Date()
    tanggal_keputusan = fields.Date()
    secapa = fields.Selection([('minat','Minat'),('toa','ToA'),('return','Return')],default='minat',string='Metode Alokasi')
    status = fields.Selection([('usulan','Usulan'),('resmi','Resmi')],default='usulan')
    foto = fields.Binary("Foto", attachment=True, help="Foto kandidat, ukurannya mohon max 1024x1024px.")

    
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
        man_akmil_kopassus = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat.nama == 'KOPASSUS')
        man_akmil_kostrad = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat.nama == 'KOSTRAD')
        man_akmil_other = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        man_sepa_kopassus = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat.nama == 'KOPASSUS')
        man_sepa_kostrad = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat.nama == 'KOSTRAD')
        man_sepa_other = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        man_secapa_kopassus = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat.nama == 'KOPASSUS')
        man_secapa_kostrad = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat.nama == 'KOSTRAD')
        man_secapa_other = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        woman_akmil_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat.nama == 'KOPASSUS')
        woman_akmil_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat.nama == 'KOSTRAD')
        woman_akmil_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        woman_sepa_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat.nama == 'KOPASSUS')
        woman_sepa_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat.nama == 'KOSTRAD')
        woman_sepa_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        woman_secapa_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat.nama == 'KOPASSUS')
        woman_secapa_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat.nama == 'KOSTRAD')
        woman_secapa_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat.nama not in ['KOSTRAD','KOPASSUS'])
        penempatan = {x.kode: 0 for x in jobs}
        kopassus_job = jobs.filtered(lambda x: x.kode == 'KOPASSUS')
        kostrad_job = jobs.filtered(lambda x: x.kode == 'KOSTRAD')
        akmil_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'AKMIL' not in str(x.khusus_diktuk)).mapped('nama')
        sepa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SEPA' not in str(x.khusus_diktuk)).mapped('nama')
        secapa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SECAPA' not in str(x.khusus_diktuk)).mapped('nama')
        kopassus_dep = departments.filtered(lambda x: x.nama == 'KOPASSUS')
        kostrad_dep = departments.filtered(lambda x: x.nama == 'KOSTRAD')
        kopassus_kecabangan = kopassus_dep.khusus_kecabangan_ids if kopassus_dep.khusus_kecabangan_ids else corps
        kostrad_kecabangan = kostrad_dep.khusus_kecabangan_ids if kostrad_dep.khusus_kecabangan_ids else corps

        if man_secapa_kopassus:
            for applicant in man_secapa_kopassus:
                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
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
                                potential_job.terisi = potential_job.terisi +  1
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        potential_job.terisi = potential_job.terisi +  1
                                        break
                                else:
                                    continue
                                break
                if applicant.secapa == 'return':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
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
                                    potential_job.terisi = potential_job.terisi +  1
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
                                        potential_job.terisi = potential_job.terisi + 1
                                        break
                                else:
                                    continue
                                break


        if man_secapa_kostrad:
            for applicant in man_secapa_kostrad:
                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
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
                                potential_job.terisi = potential_job.terisi +  1
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        potential_job.terisi = potential_job.terisi +  1
                                        break
                                else:
                                    continue
                                break
                if applicant.secapa == 'return':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
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
                                    potential_job.terisi = potential_job.terisi +  1
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
                                        potential_job.terisi = potential_job.terisi + 1
                                        break
                                else:
                                    continue
                                break
        
        
        if man_secapa_other:
            for applicant in man_secapa_other:
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
                                potential_job.terisi = potential_job.terisi + 1
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
                                            potential_job.terisi = potential_job.terisi + 1    
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
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
                                potential_job.terisi = potential_job.terisi + 1
                            else:
                                if applicant.minat.kategori == 'a':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                                if applicant.minat.kategori == 'b':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                                if applicant.minat.kategori == 'c':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                if applicant.minat.kategori not in ['a','b','c']:
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.kategori)
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.sequence)
                                for dep in terdekat_dep:
                                    if dep.kategori in ['a','b','c']:
                                        kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                    else:
                                        kode = dep.nama
                                    potential_job = jobs.filtered(lambda x: x.kode == kode)
                                    if potential_job:
                                        if potential_job.bukaan:
                                            applicant.rekomendasi1 = potential_job
                                            potential_job.terisi = potential_job.terisi + 1
                                            break
                if applicant.secapa == 'return':
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
                                potential_job.terisi = potential_job.terisi + 1
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
                                            potential_job.terisi = potential_job.terisi +  1
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
                                            potential_job.terisi = potential_job.terisi + 1
                                            break
                                    else:
                                        continue
                                    break


        if woman_secapa_kopassus:
            for applicant in woman_secapa_kopassus:
                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
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
                                potential_job.terisi = potential_job.terisi +  1
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        potential_job.terisi = potential_job.terisi +  1
                                        break
                                else:
                                    continue
                                break
                if applicant.secapa == 'return':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi1 = kopassus_job
                        kopassus_job.terisi = kopassus_job.terisi + 1
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
                                    potential_job.terisi = potential_job.terisi +  1
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
                                        potential_job.terisi = potential_job.terisi + 1
                                        break
                                else:
                                    continue
                                break


        if woman_secapa_kostrad:
            for applicant in woman_secapa_kostrad:
                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
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
                                potential_job.terisi = potential_job.terisi +  1
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
                    else:
                        other_department = departments.filtered(lambda x: x.kategori == 'c')
                        if other_department:
                            for dep in other_department:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                potential_job = jobs.filtered(lambda x: x.kode == kode)
                                if potential_job:
                                    if potential_job.bukaan:
                                        applicant.rekomendasi1 = potential_job
                                        potential_job.terisi = potential_job.terisi +  1
                                        break
                                else:
                                    continue
                                break
                if applicant.secapa == 'return':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi1 = kostrad_job
                        kostrad_job.terisi = kostrad_job.terisi + 1
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
                                    potential_job.terisi = potential_job.terisi +  1
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
                                        potential_job.terisi = potential_job.terisi + 1
                                        break
                                else:
                                    continue
                                break


        if woman_secapa_other:
            for applicant in woman_secapa_other:
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
                                potential_job.terisi = potential_job.terisi + 1
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
                                            potential_job.terisi = potential_job.terisi + 1    
                    if applicant.rekomendasi1 == False:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
                        for dep in terdekat_dep:
                            if dep.kesatuan_id.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                            else:
                                kode = dep.kesatuan_dekat.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break
                if applicant.secapa == 'toa':
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
                                potential_job.terisi = potential_job.terisi + 1
                            else:
                                if applicant.minat.kategori == 'a':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                                if applicant.minat.kategori == 'b':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                                if applicant.minat.kategori == 'c':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                if applicant.minat.kategori not in ['a','b','c']:
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.kategori)
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.sequence)
                                for dep in terdekat_dep:
                                    if dep.kategori in ['a','b','c']:
                                        kode = applicant.kecabangan_id.kode + '-' + dep.nama
                                    else:
                                        kode = dep.nama
                                    potential_job = jobs.filtered(lambda x: x.kode == kode)
                                    if potential_job:
                                        if potential_job.bukaan:
                                            applicant.rekomendasi1 = potential_job
                                            potential_job.terisi = potential_job.terisi + 1
                                            break
                if applicant.secapa == 'return':
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
                                potential_job.terisi = potential_job.terisi + 1
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
                                            potential_job.terisi = potential_job.terisi +  1
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
                                            potential_job.terisi = potential_job.terisi + 1
                                            break
                                    else:
                                        continue
                                    break


        if man_akmil_kopassus:
            man_akmil_kopassus = man_akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_kopassus:
                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                    kopassus_job.terisi = kopassus_job.terisi + 1 
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1 
                                    break


        if man_akmil_kostrad:
            man_akmil_kostrad = man_akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_kostrad:
                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                    kostrad_job.terisi = kostrad_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if man_akmil_other:
            man_akmil_other = man_akmil_other.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence) 
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0:
                                applicant.rekomendasi1 = potential_job
                                potential_job.terisi = potential_job.terisi + 1
                                break


        if woman_akmil_kopassus:
            woman_akmil_kopassus = woman_akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_kopassus:
                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                    kopassus_job.terisi = kopassus_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if woman_akmil_kostrad:
            woman_akmil_kostrad = woman_akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_kostrad:
                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                    kostrad_job.terisi = kostrad_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if woman_akmil_other:
            woman_akmil_other = woman_akmil_other.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0:
                                applicant.rekomendasi1 = potential_job
                                potential_job.terisi = potential_job.terisi + 1
                                break


        if man_sepa_kopassus:
            man_sepa_kopassus = man_sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_kopassus:
                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                    kopassus_job.terisi = kopassus_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if man_sepa_kostrad:
            man_sepa_kostrad = man_sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_kostrad:
                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                    kostrad_job.terisi = kostrad_job.terisi
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if man_sepa_other:
            man_sepa_other = man_sepa_other.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0:
                                applicant.rekomendasi1 = potential_job
                                potential_job.terisi = potential_job.terisi + 1
                                break

                        
        if woman_sepa_kopassus:
            woman_sepa_kopassus = woman_sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_kopassus:
                if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi1 = kopassus_job
                    kopassus_job.terisi = kopassus_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if woman_sepa_kostrad:
            woman_sepa_kostrad = woman_sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_kostrad:
                if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi1 = kostrad_job
                    kostrad_job.terisi = kostrad_job.terisi + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi1 = potential_job
                                    potential_job.terisi = potential_job.terisi + 1
                                    break


        if woman_sepa_other:
            woman_sepa_other = woman_sepa_other.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0:
                                applicant.rekomendasi1 = potential_job
                                potential_job.terisi = potential_job.terisi + 1
                                break



    def allocate2(self):
        applicants = self.env['tnix.kandidat'].search([('status','=','usulan')])
        jobs = self.env['tnix.posisi'].search([])
        departments = self.env['tnix.kesatuan'].search([])
        corps = self.env['tnix.kecabangan'].search([])
        man_akmil_kopassus = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat2.nama == 'KOPASSUS')
        man_akmil_kostrad = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat2.nama == 'KOSTRAD')
        man_akmil_other = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'AKMIL' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        man_sepa_kopassus = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat2.nama == 'KOPASSUS')
        man_sepa_kostrad = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat2.nama == 'KOSTRAD')
        man_sepa_other = applicants.filtered(lambda x: x.kelamin =='L' and x.diktuk == 'SEPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        man_secapa_kopassus = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat2.nama == 'KOPASSUS')
        man_secapa_kostrad = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat2.nama == 'KOSTRAD')
        man_secapa_other = applicants.filtered(lambda x: x.kelamin == 'L' and x.diktuk == 'SECAPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        woman_akmil_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat2.nama == 'KOPASSUS')
        woman_akmil_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat2.nama == 'KOSTRAD')
        woman_akmil_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'AKMIL' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        woman_sepa_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat2.nama == 'KOPASSUS')
        woman_sepa_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat2.nama == 'KOSTRAD')
        woman_sepa_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SEPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        woman_secapa_kopassus = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat2.nama == 'KOPASSUS')
        woman_secapa_kostrad = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat2.nama == 'KOSTRAD')
        woman_secapa_other = applicants.filtered(lambda x: x.kelamin == 'P' and x.diktuk == 'SECAPA' and x.minat2.nama not in ['KOSTRAD','KOPASSUS'])
        penempatan = {x.kode: 0 for x in jobs}
        kopassus_job = jobs.filtered(lambda x: x.kode == 'KOPASSUS')
        kostrad_job = jobs.filtered(lambda x: x.kode == 'KOSTRAD')
        akmil_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'AKMIL' not in str(x.khusus_diktuk)).mapped('nama')
        sepa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SEPA' not in str(x.khusus_diktuk)).mapped('nama')
        secapa_forbidden = departments.filtered(lambda x: x.khusus_diktuk !=False and 'SECAPA' not in str(x.khusus_diktuk)).mapped('nama')
        kopassus_dep = departments.filtered(lambda x: x.nama == 'KOPASSUS')
        kostrad_dep = departments.filtered(lambda x: x.nama == 'KOSTRAD')
        kopassus_kecabangan = kopassus_dep.khusus_kecabangan_ids if kopassus_dep.khusus_kecabangan_ids else corps
        kostrad_kecabangan = kostrad_dep.khusus_kecabangan_ids if kostrad_dep.khusus_kecabangan_ids else corps


        if man_secapa_kopassus:
            for applicant in man_secapa_kopassus:
                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi2 = kopassus_job
                    else:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
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
                                    break
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


        if man_secapa_kostrad:
            for applicant in man_secapa_kostrad:
                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi2 = kostrad_job
                    else:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
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


        if man_secapa_other:
            for applicant in man_secapa_other:
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
                            else:
                                terdekat_dep1 = applicant.minat.terdekat_ids
                                terdekat_dep2 = applicant.minat2.terdekat_ids
                                terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                            else:
                                if applicant.minat2.kategori == 'a':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                                if applicant.minat2.kategori == 'b':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                                if applicant.minat2.kategori == 'c':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                if applicant.minat2.kategori not in ['a','b','c']:
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.kategori)
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.sequence)
                                terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
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
                                    if dep.kesatuan_id.kategori in ['a','b','c']:
                                        kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                    else:
                                        kode = dep.kesatuan_dekat.nama
                                    potential_job = jobs.filtered(lambda x: x.kode == kode)
                                    if potential_job:
                                        if potential_job.bukaan:
                                            applicant.rekomendasi2 = potential_job
                                            break


        if woman_secapa_kopassus:
            for applicant in woman_secapa_kopassus:
                if applicant.secapa == 'minat':
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
                        applicant.rekomendasi2 = kopassus_job
                    else:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                    if kopassus_job.bukaan and applicant.kecabangan_id in kopassus_kecabangan:
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
                                    break
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


        if woman_secapa_kostrad:
            for applicant in woman_secapa_kostrad:
                if applicant.secapa == 'minat':
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
                        applicant.rekomendasi2 = kostrad_job
                    else:
                        terdekat_dep1 = applicant.minat.terdekat_ids
                        terdekat_dep2 = applicant.minat2.terdekat_ids
                        terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                    if kostrad_job.bukaan and applicant.kecabangan_id in kostrad_kecabangan:
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
                                    if potential_job.bukaan and potential_job.lowong > 0:
                                        applicant.rekomendasi2 = potential_job
                                        break


        if woman_secapa_other:
            for applicant in woman_secapa_other:
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
                            else:
                                terdekat_dep1 = applicant.minat.terdekat_ids
                                terdekat_dep2 = applicant.minat2.terdekat_ids
                                terdekat_dep = terdekat_dep1 + terdekat_dep2
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
                            else:
                                if applicant.minat2.kategori == 'a':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['b','c'])
                                if applicant.minat2.kategori == 'b':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','c'])     
                                if applicant.minat2.kategori == 'c':
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                if applicant.minat2.kategori not in ['a','b','c']:
                                    terdekat_dep = departments.filtered(lambda x: x.kategori in ['a','b'])
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.kategori)
                                terdekat_dep = terdekat_dep.sorted(key=lambda x: x.sequence)
                                terdekat_dep = terdekat_dep - applicant.rekomendasi1_kesatuan
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
                                    if dep.kesatuan_id.kategori in ['a','b','c']:
                                        kode = applicant.kecabangan_id.kode + '-' + dep.kesatuan_dekat.nama
                                    else:
                                        kode = dep.kesatuan_dekat.nama
                                    potential_job = jobs.filtered(lambda x: x.kode == kode)
                                    if potential_job:
                                        if potential_job.bukaan:
                                            applicant.rekomendasi2 = potential_job
                                            break


        if man_akmil_kopassus:
            man_akmil_kopassus = man_akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_kopassus:
                if kopassus_job.bukaan and kopassus_job.lowong >= penempatan['KOPASSUS'] and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                    penempatan['KOPASSUS'] = penempatan['KOPASSUS'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if man_akmil_kostrad:
            man_akmil_kostrad = man_akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_kostrad:
                if kostrad_job.bukaan and kostrad_job.lowong >= penempatan['KOSTRAD'] and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                    penempatan['KOSTRAD'] = penempatan['KOSTRAD'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if man_akmil_other:
            man_akmil_other = man_akmil_other.sorted(key=lambda x: x.ranking)
            for applicant in man_akmil_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                other_department = other_department - applicant.rekomendasi1_kesatuan 
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0 and potential_job.lowong >= penempatan[kode]:
                                applicant.rekomendasi2 = potential_job
                                penempatan[kode] = penempatan[kode] + 1
                                break
                        

        if woman_akmil_kopassus:
            woman_akmil_kopassus = woman_akmil_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_kopassus:
                if kopassus_job.bukaan and kopassus_job.lowong >= penempatan['KOPASSUS'] and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                    penempatan['KOPASSUS'] = penempatan['KOPASSUS'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if woman_akmil_kostrad:
            woman_akmil_kostrad = woman_akmil_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_kostrad:
                if kostrad_job.bukaan and kostrad_job.lowong >= penempatan['KOSTRAD'] and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                    penempatan['KOSTRAD'] = penempatan['KOSTRAD'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if woman_akmil_other:
            woman_akmil_other = woman_akmil_other.sorted(key=lambda x: x.ranking)
            for applicant in woman_akmil_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in akmil_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                other_department = other_department - applicant.rekomendasi1_kesatuan
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0 and potential_job.lowong >= penempatan[kode]:
                                applicant.rekomendasi2 = potential_job
                                penempatan[kode] = penempatan[kode] + 1
                                break


        if man_sepa_kopassus:
            man_sepa_kopassus = man_sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_kopassus:
                if kopassus_job.bukaan and kopassus_job.lowong >= penempatan['KOPASSUS'] and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                    penempatan['KOPASSUS'] = penempatan['KOPASSUS'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if man_sepa_kostrad:
            man_sepa_kostrad = man_sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_kostrad:
                if kostrad_job.bukaan and kostrad_job.lowong >= penempatan['KOSTRAD'] and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                    penempatan['KOSTRAD'] = penempatan['KOSTRAD'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if man_sepa_other:
            man_sepa_other = man_sepa_other.sorted(key=lambda x: x.ranking)
            for applicant in man_sepa_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                other_department = other_department - applicant.rekomendasi1_kesatuan
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0 and potential_job.lowong >= penempatan[kode]:
                                applicant.rekomendasi2 = potential_job
                                penempatan[kode] = penempatan[kode] + 1
                                break

                
        if woman_sepa_kopassus:
            woman_sepa_kopassus = woman_sepa_kopassus.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_kopassus:
                if kopassus_job.bukaan and kopassus_job.lowong >= penempatan['KOPASSUS'] and applicant.kecabangan_id in kopassus_kecabangan:
                    applicant.rekomendasi2 = kopassus_job
                    penempatan['KOPASSUS'] = penempatan['KOPASSUS'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if woman_sepa_kostrad:
            woman_sepa_kostrad = woman_sepa_kostrad.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_kostrad:
                if kostrad_job.bukaan and kostrad_job.lowong >= penempatan['KOSTRAD'] and applicant.kecabangan_id in kostrad_kecabangan:
                    applicant.rekomendasi2 = kostrad_job
                    penempatan['KOSTRAD'] = penempatan['KOSTRAD'] + 1
                else:
                    other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                    other_department = other_department.sorted(key=lambda x: x.sequence)
                    other_department = other_department - applicant.rekomendasi1_kesatuan
                    if other_department:
                        for dep in other_department:
                            if dep.kategori in ['a','b','c']:
                                kode = applicant.kecabangan_id.kode + '-' + dep.nama
                            else:
                                kode = dep.nama
                            potential_job = jobs.filtered(lambda x: x.kode == kode)
                            if potential_job:
                                if potential_job.bukaan and potential_job.lowong > 0:
                                    applicant.rekomendasi2 = potential_job
                                    penempatan[kode] = penempatan[kode] + 1
                                    break


        if woman_sepa_other:
            woman_sepa_other = woman_sepa_other.sorted(key=lambda x: x.ranking)
            for applicant in woman_sepa_other:
                other_department = departments.filtered(lambda x: (len(x.khusus_kecabangan_ids) == 0 or applicant.kecabangan_id in x.khusus_kecabangan_ids) and x.nama not in ['KOPASSUS','KOSTRAD'] and x.nama not in sepa_forbidden and x.id != applicant.panda.id and applicant.propinsi_lahir not in x.propinsi_ids and applicant.propinsi_tinggal not in x.propinsi_ids  and applicant.suku_id not in x.suku_ids)
                other_department = other_department.sorted(key=lambda x: x.sequence)
                other_department = other_department - applicant.rekomendasi1_kesatuan
                if other_department:
                    potential_department = other_department
                    if applicant.sarjana_id:
                        sarjana_department = other_department.filtered(lambda x: applicant.sarjana_id in x.utama_kesarjanaan_ids)
                        if sarjana_department:
                            potential_department = sarjana_department
                    for dep in potential_department:
                        if dep.kategori in ['a','b','c']:
                            kode = applicant.kecabangan_id.kode + '-' + dep.nama
                        else:
                            kode = dep.nama
                        potential_job = jobs.filtered(lambda x: x.kode == kode)
                        if potential_job:
                            if potential_job.bukaan and potential_job.lowong > 0 and potential_job.lowong >= penempatan[kode]:
                                applicant.rekomendasi2 = potential_job
                                penempatan[kode] = penempatan[kode] + 1
                                break