# -*- coding: utf-8 -*-

from odoo.tests import common
from . import testutils

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='182', degree='s1', active=True
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Dosen IF Pertama',
        nidn='012-AAA-123-BBB',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Dosen',
        employee_id=dosen_if_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='undergraduate', school='ITB', major='Teknik Informatika'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='graduate', school='ITB', major='Informatika'
    ))

    dosen_if_2 = context.env['hr.employee'].create(dict(
        name='Dosen IF Kedua',
        nidn='912091239812',
        birthday='1985-12-31',
        is_faculty=True,
        prodi=prodi_if.id
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Dosen 2',
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
        prodi=prodi_el.id
    ))
    context.env['itb.hr_jabatan'].create(dict(
        jabatan='Kaprodi',
        employee_id=dosen_el_1.id
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_el_1.id, degree='doctoral', school='ITS', major='Elektro'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    report_2 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 2',
        year=2016,
        refresh_date='2016-07-05 08:00:00',
        prodi=prodi_el.id
    ))

    return report_1, report_2

class TestDosen(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2 = seed(self)

        report_1.refresh()
        report_2.refresh()

        dosen_1 = report_1.dosen.search([['nidn', '=', '012-AAA-123-BBB']])
        self.assertEqual(dosen_1.nama, 'Dosen IF Pertama')
        self.assertEqual(dosen_1.nidn, '012-AAA-123-BBB')
        self.assertEqual(dosen_1.tanggal_lahir, '1970-03-22')
        self.assertEqual(dosen_1.jabatan, 'Dosen')
        self.assertEqual(dosen_1.gelar_s1, '')
        self.assertEqual(dosen_1.asal_pt_s1, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s1, 'Teknik Informatika')
        self.assertEqual(dosen_1.gelar_s2, '')
        self.assertEqual(dosen_1.asal_pt_s2, 'ITB')
        self.assertEqual(dosen_1.bidang_keahlian_s2, 'Informatika')
        self.assertEqual(dosen_1.gelar_s3, '')
        self.assertEqual(dosen_1.asal_pt_s3, '')
        self.assertEqual(dosen_1.bidang_keahlian_s3, '')

        dosen_2 = report_1.dosen.search([['nidn', '=', '912091239812']])
        self.assertEqual(dosen_2.nama, 'Dosen IF Kedua')
        self.assertEqual(dosen_2.nidn, '912091239812')
        self.assertEqual(dosen_2.tanggal_lahir, '1985-12-31')
        self.assertEqual(dosen_2.jabatan, 'Dosen 2')
        self.assertEqual(dosen_2.gelar_s1, '')
        self.assertEqual(dosen_2.asal_pt_s1, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s1, 'Matematika')
        self.assertEqual(dosen_2.gelar_s2, '')
        self.assertEqual(dosen_2.asal_pt_s2, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s2, 'Statistika')
        self.assertEqual(dosen_2.gelar_s3, '')
        self.assertEqual(dosen_2.asal_pt_s3, 'UI')
        self.assertEqual(dosen_2.bidang_keahlian_s3, 'Matematika')

        dosen_3 = report_2.dosen.search([['nidn', '=', '2223123112']])
        self.assertEqual(dosen_3.nama, 'Dosen EL Pertama')
        self.assertEqual(dosen_3.nidn, '2223123112')
        self.assertEqual(dosen_3.tanggal_lahir, '1980-01-01')
        self.assertEqual(dosen_3.jabatan, 'Kaprodi')
        self.assertEqual(dosen_3.gelar_s1, '')
        self.assertEqual(dosen_3.asal_pt_s1, '')
        self.assertEqual(dosen_3.bidang_keahlian_s1, '')
        self.assertEqual(dosen_3.gelar_s2, '')
        self.assertEqual(dosen_3.asal_pt_s2, '')
        self.assertEqual(dosen_3.bidang_keahlian_s2, '')
        self.assertEqual(dosen_3.gelar_s3, '')
        self.assertEqual(dosen_3.asal_pt_s3, 'ITS')
        self.assertEqual(dosen_3.bidang_keahlian_s3, 'Elektro')
