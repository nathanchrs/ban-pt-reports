# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='132', degree='s1', active=True
    ))
    prodi_ep = context.env['itb.academic_program'].create(dict(
        name='Teknik Tenaga Listrik', name_en='Electrical Power Engineering', prefix='180', degree='s1', active='true'
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Dosen IF Pertama',
        nidn='012-AAA-123-BBB',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id,
        employment_type='itb'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Lektor IF',
        employee_id=dosen_if_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='undergraduate', school='ITB', major='Teknik Informatika', certificate_signer='Budi darma'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='graduate', school='ITB', major='Informatika', certificate_signer='Imam Ahmad'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='doctoral', school='UCLA', major='Computer Science', certificate_signer='Prabawa'
    ))

    dosen_if_2 = context.env['hr.employee'].create(dict(
        name='Faiz Haznitrama',
        nidn='912091239812',
        birthday='1985-12-31',
        is_faculty=True,
        prodi=prodi_if.id,
        employment_type='pns'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Lektor Senior',
        employee_id=dosen_if_2.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_2.id, degree='undergraduate', school='UI', major='Matematika'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_2.id, degree='graduate', school='UI', major='Statistika'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_2.id, degree='doctoral', school='UI', major='Matematika'
    ))

    dosen_el_1 = context.env['hr.employee'].create(dict(
        name='Dosen EL Pertama',
        nidn='2223123112',
        birthday='1980-01-01',
        is_faculty=True,
        prodi=prodi_el.id,
        employment_type='itb'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Kaprodi',
        employee_id=dosen_el_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_el_1.id, degree='doctoral', school='ITS', major='Elektro', certificate_signer='Arief Hidayat'
    ))

    dosen_ep_1 = context.env['hr.employee'].create(dict(
        name='Dosen EP Pertama',
        nidn='3209187659883',
        birthday='1969-01-16',
        is_faculty=True,
        prodi=prodi_ep.id,
        employment_type='pns'
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Wakil Dekan Bidang Sumberdaya',
        employee_id=dosen_ep_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_ep_1.id, degree='graduate', school='UGM', major='Tenaga Pembangkit Listrik'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    report_2 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 2 - EL',
        year=2016,
        refresh_date='2016-07-05 08:00:00',
        prodi=prodi_el.id
    ))

    report_3 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 3 - EP',
        year=2015,
        refresh_date='2015-10-05 08:00:00',
        prodi=prodi_ep.id
    ))

    return report_1, report_2, report_3

class TestRecord_3A_431(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2, report_3 = seed(self)

        report_1.refresh()
        report_2.refresh()
        report_3.refresh()

        dosen_1 = report_1.record_3a_431.search([['nidn', '=', '012-AAA-123-BBB']])
        self.assertEqual(dosen_1.nama, 'Dosen IF Pertama')
        self.assertEqual(dosen_1.nidn, '012-AAA-123-BBB')
        self.assertEqual(dosen_1.tanggal_lahir, '1970-03-22')
        self.assertEqual(dosen_1.jabatan, 'Lektor IF')
        self.assertEqual(dosen_1.sertifikasi, 'ya')
        self.assertEqual(dosen_1.gelar_s1, '')
        self.assertEqual(dosen_1.asal_pt_s1, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s1, 'Teknik Informatika')
        self.assertEqual(dosen_1.gelar_s2, '')
        self.assertEqual(dosen_1.asal_pt_s2, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s2, 'Informatika')
        self.assertEqual(dosen_1.gelar_s3, '')
        self.assertEqual(dosen_1.asal_pt_s3, 'UCLA')
        self.assertEqual(dosen_1.bidang_keahlian_s3, 'Computer Science')

        dosen_2 = report_1.record_3a_431.search([['nidn', '=', '912091239812']])
        self.assertEqual(dosen_2.nama, 'Faiz Haznitrama')
        self.assertEqual(dosen_2.nidn, '912091239812')
        self.assertEqual(dosen_2.tanggal_lahir, '1985-12-31')
        self.assertEqual(dosen_2.jabatan, 'Lektor Senior')
        self.assertEqual(dosen_2.sertifikasi, 'tidak')
        self.assertEqual(dosen_2.gelar_s1, '')
        self.assertEqual(dosen_2.asal_pt_s1, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s1, 'Matematika')
        self.assertEqual(dosen_2.gelar_s2, '')
        self.assertEqual(dosen_2.asal_pt_s2, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s2, 'Statistika')
        self.assertEqual(dosen_2.gelar_s3, '')
        self.assertEqual(dosen_2.asal_pt_s3, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s3, 'Matematika')

        dosen_3 = report_2.record_3a_431.search([['nidn', '=', '2223123112']])
        self.assertEqual(dosen_3.nama, 'Dosen EL Pertama')
        self.assertEqual(dosen_3.nidn, '2223123112')
        self.assertEqual(dosen_3.tanggal_lahir, '1980-01-01')
        self.assertEqual(dosen_3.jabatan, 'Kaprodi')
        self.assertEqual(dosen_3.sertifikasi, 'ya')
        self.assertEqual(dosen_3.gelar_s1, '')
        self.assertEqual(dosen_3.asal_pt_s1, '')
        self.assertEqual(dosen_3.bidang_keahlian_s1, '')
        self.assertEqual(dosen_3.gelar_s2, '')
        self.assertEqual(dosen_3.asal_pt_s2, '')
        self.assertEqual(dosen_3.bidang_keahlian_s2, '')
        self.assertEqual(dosen_3.gelar_s3, '')
        self.assertEqual(dosen_3.asal_pt_s3, 'ITS')
        self.assertEqual(dosen_3.bidang_keahlian_s3, 'Elektro')

        dosen_4 = report_3.record_3a_431.search([['nidn', '=', '3209187659883']])
        self.assertEqual(dosen_4.nama, 'Dosen EP Pertama')
        self.assertEqual(dosen_4.nidn, '3209187659883')
        self.assertEqual(dosen_4.tanggal_lahir, '1969-01-16')
        self.assertEqual(dosen_4.jabatan, 'Wakil Dekan Bidang Sumberdaya')
        self.assertEqual(dosen_4.sertifikasi, 'tidak')
        self.assertEqual(dosen_4.gelar_s1, '')
        self.assertEqual(dosen_4.asal_pt_s1, '')
        self.assertEqual(dosen_4.bidang_keahlian_s1, '')
        self.assertEqual(dosen_4.gelar_s2, '')
        self.assertEqual(dosen_4.asal_pt_s2, 'UGM')
        self.assertEqual(dosen_4.bidang_keahlian_s2, 'Tenaga Pembangkit Listrik')
        self.assertEqual(dosen_4.gelar_s3, '')
        self.assertEqual(dosen_4.asal_pt_s3, '')
        self.assertEqual(dosen_4.bidang_keahlian_s3, '')
