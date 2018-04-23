# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_et = context.env['itb.academic_program'].create(dict(
        name='Teknik Telekomunikasi', name_en='Telecommunication Engineering', prefix='181', degree='s1', active=True
    ))
    prodi_sti = context.env['itb.academic_program'].create(dict(
        name='Sistem dan Teknologi Informasi', name_en='Information System and Technology', prefix='182', degree='s1', active=True
    ))
    prodi_eb = context.env['itb.academic_program'].create(dict(
        name='Teknik Biomedis', name_en='Biomedical Engineering', prefix='183', degree='s1', active='true'
    ))

    dosen_et_1 = context.env['hr.employee'].create(dict(
        name='Dosen ET Pertama',
        nidn='012-AAA-123-BBB',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_et.id,
        employment_type='contract'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Lektor ET',
        employee_id=dosen_et_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_et_1.id, degree='undergraduate', school='ITB', major='Teknik Telekomunikasi', certificate_signer='Budi darma'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_et_1.id, degree='graduate', school='ITB', major='Teknik Elektro', certificate_signer='Imam Ahmad'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_et_1.id, degree='doctoral', school='Kyoto University', major='Telecommunication Engineering', certificate_signer='Ando Takahashi'
    ))

    dosen_sti_1 = context.env['hr.employee'].create(dict(
        name='Dosen STI',
        nidn='912091239812',
        birthday='1985-12-31',
        is_faculty=True,
        prodi=prodi_sti.id,
        employment_type='contract'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Lektor STI',
        employee_id=dosen_sti_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_sti_1.id, degree='graduate', school='UI', major='Sistem Informasi'
    ))

    dosen_eb_1 = context.env['hr.employee'].create(dict(
        name='Dosen EB Pertama',
        nidn='2223123112',
        birthday='1980-01-01',
        is_faculty=True,
        prodi=prodi_eb.id,
        employment_type='contract'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Kaprodi EB',
        employee_id=dosen_eb_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_eb_1.id, degree='doctoral', school='SGU', major='Biomedical', certificate_signer='Arief Hidayat'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - ET',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_et.id
    ))

    report_2 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 2 - STI',
        year=2016,
        refresh_date='2016-07-05 08:00:00',
        prodi=prodi_sti.id
    ))

    report_3 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 3 - EB',
        year=2015,
        refresh_date='2015-10-05 08:00:00',
        prodi=prodi_eb.id
    ))

    return report_1, report_2, report_3

class TestRecord_3A_441(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2, report_3 = seed(self)

        report_1.refresh()
        report_2.refresh()
        report_3.refresh()

        dosen_1 = report_1.record_3a_441.search([['nidn', '=', '012-AAA-123-BBB']])
        self.assertEqual(dosen_1.nama, 'Dosen ET Pertama')
        self.assertEqual(dosen_1.nidn, '012-AAA-123-BBB')
        self.assertEqual(dosen_1.tanggal_lahir, '1970-03-22')
        self.assertEqual(dosen_1.jabatan, 'Lektor ET')
        self.assertEqual(dosen_1.sertifikasi, 'ya')
        self.assertEqual(dosen_1.gelar_s1, '')
        self.assertEqual(dosen_1.asal_pt_s1, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s1, 'Teknik Telekomunikasi')
        self.assertEqual(dosen_1.gelar_s2, '')
        self.assertEqual(dosen_1.asal_pt_s2, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s2, 'Teknik Elektro')
        self.assertEqual(dosen_1.gelar_s3, '')
        self.assertEqual(dosen_1.asal_pt_s3, 'Kyoto University')
        self.assertEqual(dosen_1.bidang_keahlian_s3, 'Telecommunication Engineering')

        dosen_2 = report_2.record_3a_441.search([['nidn', '=', '912091239812']])
        self.assertEqual(dosen_2.nama, 'Dosen STI')
        self.assertEqual(dosen_2.nidn, '912091239812')
        self.assertEqual(dosen_2.tanggal_lahir, '1985-12-31')
        self.assertEqual(dosen_2.jabatan, 'Lektor STI')
        self.assertEqual(dosen_2.sertifikasi, 'tidak')
        self.assertEqual(dosen_2.gelar_s1, '')
        self.assertEqual(dosen_2.asal_pt_s1, '')
        self.assertEqual(dosen_2.bidang_keahlian_s1, '')
        self.assertEqual(dosen_2.gelar_s2, '')
        self.assertEqual(dosen_2.asal_pt_s2, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s2, 'Sistem Informasi')
        self.assertEqual(dosen_2.gelar_s3, '')
        self.assertEqual(dosen_2.asal_pt_s3, '')
        self.assertEqual(dosen_2.bidang_keahlian_s3, '')

        dosen_3 = report_3.record_3a_441.search([['nidn', '=', '2223123112']])
        self.assertEqual(dosen_3.nama, 'Dosen EB Pertama')
        self.assertEqual(dosen_3.nidn, '2223123112')
        self.assertEqual(dosen_3.tanggal_lahir, '1980-01-01')
        self.assertEqual(dosen_3.jabatan, 'Kaprodi EB')
        self.assertEqual(dosen_3.sertifikasi, 'ya')
        self.assertEqual(dosen_3.gelar_s1, '')
        self.assertEqual(dosen_3.asal_pt_s1, '')
        self.assertEqual(dosen_3.bidang_keahlian_s1, '')
        self.assertEqual(dosen_3.gelar_s2, '')
        self.assertEqual(dosen_3.asal_pt_s2, '')
        self.assertEqual(dosen_3.bidang_keahlian_s2, '')
        self.assertEqual(dosen_3.gelar_s3, '')
        self.assertEqual(dosen_3.asal_pt_s3, 'SGU')
        self.assertEqual(dosen_3.bidang_keahlian_s3, 'Biomedical')
