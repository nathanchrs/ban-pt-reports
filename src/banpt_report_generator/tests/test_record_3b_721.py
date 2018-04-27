# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='132', degree='s1', active=True
    ))
    prodi_ep = context.env['itb.academic_program'].create(dict(
        name='Teknik Tenaga Listrik', name_en='Electrical Power Engineering', prefix='180', degree='s1', active=True
    ))
    prodi_et = context.env['itb.academic_program'].create(dict(
        name='Teknik Telekomunikasi', name_en='Telecommunication Engineering', prefix='181', degree='s1', active=True
    ))
    prodi_sti = context.env['itb.academic_program'].create(dict(
        name='Sistem dan Teknologi Informasi', name_en='Information System and Technology', prefix='182', degree='s1', active=True
    ))
    prodi_eb = context.env['itb.academic_program'].create(dict(
        name='Teknik Biomedis', name_en='Biomedical Engineering', prefix='183', degree='s1', active=True
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Ridwan Kamal',
        nidn='014-A5A-133-C2D',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id
    ))
    dosen_el_1 = context.env['hr.employee'].create(dict(
        name='Ading Utet',
        nidn='B91-19l-ASW-980',
        birthday='1975-04-12',
        is_faculty=True,
        prodi=prodi_el.id
    ))
    dosen_ep_1 = context.env['hr.employee'].create(dict(
        name='Shawirna',
        nidn='123-5FS-13B-56D',
        birthday='1967-12-02',
        is_faculty=True,
        prodi=prodi_ep.id
    ))
    dosen_et_1 = context.env['hr.employee'].create(dict(
        name='Manor Akhmat',
        nidn='A2S-FF3F-HGE4-FS3',
        birthday='1979-04-05',
        is_faculty=True,
        prodi=prodi_et.id
    ))
    dosen_sti_1 = context.env['hr.employee'].create(dict(
        name='Mahdi AlHanif',
        nidn='QW3-FG5U-BF52-D4',
        birthday='1981-01-02',
        is_faculty=True,
        prodi=prodi_sti.id
    ))
    dosen_eb_1 = context.env['hr.employee'].create(dict(
        name='Wisnuwardhana Alhambra',
        nidn='AS1-DCGF4-SS3-12',
        birthday='1971-08-17',
        is_faculty=True,
        prodi=prodi_eb.id
    ))

    project_if_1 = context.env['itb.hr_project'].create(dict(name='if_1', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=1000000))
    project_if_2 = context.env['itb.hr_project'].create(dict(name='if_2', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=2004000))
    project_if_3 = context.env['itb.hr_project'].create(dict(name='if_3', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=3050000))
    project_if_4 = context.env['itb.hr_project'].create(dict(name='if_4', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=10000000))
    project_if_5 = context.env['itb.hr_project'].create(dict(name='if_5', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=21500000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_if_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_if_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_if_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_if_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_if_5.id))

    project_el_1 = context.env['itb.hr_project'].create(dict(name='el_1', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=1980000))
    project_el_2 = context.env['itb.hr_project'].create(dict(name='el_2', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=3290000))
    project_el_3 = context.env['itb.hr_project'].create(dict(name='el_3', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=43500000))
    project_el_4 = context.env['itb.hr_project'].create(dict(name='el_4', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=100000000))
    project_el_5 = context.env['itb.hr_project'].create(dict(name='el_5', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=55000000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_el_1.id, role='leader', project_id=project_el_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_el_1.id, role='leader', project_id=project_el_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_el_1.id, role='leader', project_id=project_el_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_el_1.id, role='leader', project_id=project_el_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_el_1.id, role='leader', project_id=project_el_5.id))

    project_ep_1 = context.env['itb.hr_project'].create(dict(name='ep_1', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=10000000))
    project_ep_2 = context.env['itb.hr_project'].create(dict(name='ep_2', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=4000900))
    project_ep_3 = context.env['itb.hr_project'].create(dict(name='ep_3', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=75050000))
    project_ep_4 = context.env['itb.hr_project'].create(dict(name='ep_4', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=20000000))
    project_ep_5 = context.env['itb.hr_project'].create(dict(name='ep_5', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=6500000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_ep_1.id, role='leader', project_id=project_ep_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_ep_1.id, role='leader', project_id=project_ep_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_ep_1.id, role='leader', project_id=project_ep_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_ep_1.id, role='leader', project_id=project_ep_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_ep_1.id, role='leader', project_id=project_ep_5.id))

    project_et_1 = context.env['itb.hr_project'].create(dict(name='et_1', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=25000000))
    project_et_2 = context.env['itb.hr_project'].create(dict(name='et_2', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=5050000))
    project_et_3 = context.env['itb.hr_project'].create(dict(name='et_3', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=3500000))
    project_et_4 = context.env['itb.hr_project'].create(dict(name='et_4', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=310000000))
    project_et_5 = context.env['itb.hr_project'].create(dict(name='et_5', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=41500000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_et_1.id, role='leader', project_id=project_et_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_et_1.id, role='leader', project_id=project_et_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_et_1.id, role='leader', project_id=project_et_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_et_1.id, role='leader', project_id=project_et_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_et_1.id, role='leader', project_id=project_et_5.id))

    project_sti_1 = context.env['itb.hr_project'].create(dict(name='sti_1', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=25000000))
    project_sti_2 = context.env['itb.hr_project'].create(dict(name='sti_2', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=5050000))
    project_sti_3 = context.env['itb.hr_project'].create(dict(name='sti_3', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=3500000))
    project_sti_4 = context.env['itb.hr_project'].create(dict(name='sti_4', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=310000000))
    project_sti_5 = context.env['itb.hr_project'].create(dict(name='sti_5', tipe='pengabdian', start='2015-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=41500000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_sti_1.id, role='leader', project_id=project_sti_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_sti_1.id, role='leader', project_id=project_sti_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_sti_1.id, role='leader', project_id=project_sti_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_sti_1.id, role='leader', project_id=project_sti_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_sti_1.id, role='leader', project_id=project_sti_5.id))

    project_eb_1 = context.env['itb.hr_project'].create(dict(name='eb_1', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=35000000))
    project_eb_2 = context.env['itb.hr_project'].create(dict(name='eb_2', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=750000))
    project_eb_3 = context.env['itb.hr_project'].create(dict(name='eb_3', tipe='pengabdian', start='2014-03-09', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=9000000))
    project_eb_4 = context.env['itb.hr_project'].create(dict(name='eb_4', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=275000000))
    project_eb_5 = context.env['itb.hr_project'].create(dict(name='eb_5', tipe='pengabdian', start='2013-03-09', state='valid', deskripsi_sispran='DES-05', reference='REF-05', nilai=34500000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_eb_1.id, role='leader', project_id=project_eb_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_eb_1.id, role='leader', project_id=project_eb_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_eb_1.id, role='leader', project_id=project_eb_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_eb_1.id, role='leader', project_id=project_eb_4.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_eb_1.id, role='leader', project_id=project_eb_5.id))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3B_721(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        prodi_1_test = report_1.record_3b_721.search([['program_studi', '=', 'Informatika']])
        self.assertEqual(prodi_1_test.program_studi, 'Informatika')
        self.assertEqual(prodi_1_test.jumlah_judul_kegiatan_masyarakat_ts_2, 2)
        self.assertEqual(prodi_1_test.jumlah_judul_kegiatan_masyarakat_ts_1, 1)
        self.assertEqual(prodi_1_test.jumlah_judul_kegiatan_masyarakat_ts, 2)
        self.assertEqual(prodi_1_test.total_dana_kegiatan_masyarakat_ts_2, (1000000 + 10000000) / 1000000)
        self.assertEqual(prodi_1_test.total_dana_kegiatan_masyarakat_ts_1, 2004000 / 1000000)
        self.assertEqual(prodi_1_test.total_dana_kegiatan_masyarakat_ts, (3050000 + 21500000) / 1000000)

        prodi_2_test = report_1.record_3b_721.search([['program_studi', '=', 'Teknik Elektro']])
        self.assertEqual(prodi_2_test.program_studi, 'Teknik Elektro')
        self.assertEqual(prodi_2_test.jumlah_judul_kegiatan_masyarakat_ts_2, 1)
        self.assertEqual(prodi_2_test.jumlah_judul_kegiatan_masyarakat_ts_1, 1)
        self.assertEqual(prodi_2_test.jumlah_judul_kegiatan_masyarakat_ts, 3)
        self.assertEqual(prodi_2_test.total_dana_kegiatan_masyarakat_ts_2, 1980000 / 1000000)
        self.assertEqual(prodi_2_test.total_dana_kegiatan_masyarakat_ts_1, 100000000 / 1000000)
        self.assertEqual(prodi_2_test.total_dana_kegiatan_masyarakat_ts, (3290000 + 43500000 + 55000000) / 1000000)

        prodi_3_test = report_1.record_3b_721.search([['program_studi', '=', 'Teknik Tenaga Listrik']])
        self.assertEqual(prodi_3_test.program_studi, 'Teknik Tenaga Listrik')
        self.assertEqual(prodi_3_test.jumlah_judul_kegiatan_masyarakat_ts_2, 3)
        self.assertEqual(prodi_3_test.jumlah_judul_kegiatan_masyarakat_ts_1, 2)
        self.assertEqual(prodi_3_test.jumlah_judul_kegiatan_masyarakat_ts, 0)
        self.assertEqual(prodi_3_test.total_dana_kegiatan_masyarakat_ts_2, (10000000 + 4000900 + 20000000) / 1000000)
        self.assertEqual(prodi_3_test.total_dana_kegiatan_masyarakat_ts_1, (75050000 + 6500000) / 1000000)
        self.assertEqual(prodi_3_test.total_dana_kegiatan_masyarakat_ts, 0 / 1000000)

        prodi_4_test = report_1.record_3b_721.search([['program_studi', '=', 'Teknik Telekomunikasi']])
        self.assertEqual(prodi_4_test.program_studi, 'Teknik Telekomunikasi')
        self.assertEqual(prodi_4_test.jumlah_judul_kegiatan_masyarakat_ts_2, 1)
        self.assertEqual(prodi_4_test.jumlah_judul_kegiatan_masyarakat_ts_1, 2)
        self.assertEqual(prodi_4_test.jumlah_judul_kegiatan_masyarakat_ts, 2)
        self.assertEqual(prodi_4_test.total_dana_kegiatan_masyarakat_ts_2, 41500000 / 1000000)
        self.assertEqual(prodi_4_test.total_dana_kegiatan_masyarakat_ts_1, (5050000 + 310000000) / 1000000)
        self.assertEqual(prodi_4_test.total_dana_kegiatan_masyarakat_ts, (25000000 + 3500000) / 1000000)

        prodi_5_test = report_1.record_3b_721.search([['program_studi', '=', 'Sistem dan Teknologi Informasi']])
        self.assertEqual(prodi_5_test.program_studi, 'Sistem dan Teknologi Informasi')
        self.assertEqual(prodi_5_test.jumlah_judul_kegiatan_masyarakat_ts_2, 0)
        self.assertEqual(prodi_5_test.jumlah_judul_kegiatan_masyarakat_ts_1, 0)
        self.assertEqual(prodi_5_test.jumlah_judul_kegiatan_masyarakat_ts, 5)
        self.assertEqual(prodi_5_test.total_dana_kegiatan_masyarakat_ts_2, 0 / 1000000)
        self.assertEqual(prodi_5_test.total_dana_kegiatan_masyarakat_ts_1, 0 / 1000000)
        self.assertEqual(prodi_5_test.total_dana_kegiatan_masyarakat_ts, (25000000 + 3500000 + 5050000 + 310000000 + 41500000) / 1000000)

        prodi_6_test = report_1.record_3b_721.search([['program_studi', '=', 'Teknik Biomedis']])
        self.assertEqual(prodi_6_test.program_studi, 'Teknik Biomedis')
        self.assertEqual(prodi_6_test.jumlah_judul_kegiatan_masyarakat_ts_2, 2)
        self.assertEqual(prodi_6_test.jumlah_judul_kegiatan_masyarakat_ts_1, 3)
        self.assertEqual(prodi_6_test.jumlah_judul_kegiatan_masyarakat_ts, 0)
        self.assertEqual(prodi_6_test.total_dana_kegiatan_masyarakat_ts_2, (34500000 + 275000000) / 1000000)
        self.assertEqual(prodi_6_test.total_dana_kegiatan_masyarakat_ts_1, (35000000 + 750000 + 9000000) / 1000000)
        self.assertEqual(prodi_6_test.total_dana_kegiatan_masyarakat_ts, 0 / 1000000)
