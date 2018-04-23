# -*- coding: utf-8 -*-

from odoo.tests import common

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
    context.env['itb.hr_award'].create(dict(
        name='award0',
        level='global',
        start='2018-01-01',
        employee_id=dosen_if_1.id
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
    context.env['itb.hr_award'].create(dict(
        name='award1',
        level='local',
        start='2018-01-01',
        employee_id=dosen_if_2.id
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
    context.env['itb.hr_award'].create(dict(
        name='award2',
        level='national',
        start='2018-01-01',
        employee_id=dosen_el_1.id
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

class TestRecord_3A_454(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2 = seed(self)

        report_1.refresh()
        report_2.refresh()

        award_1 = report_1.record_3a_454.search([['nama', '=', 'Dosen IF Pertama']])
        self.assertEqual(award_1.nama, 'Dosen IF Pertama')
        self.assertEqual(award_1.prestasi_yang_dicapai, 'award0')
        self.assertEqual(award_1.tahun_pencapaian, '2018-01-01')
        self.assertEqual(award_1.tingkat_internasional, True)
        self.assertEqual(award_1.tingkat_nasional, False)
        self.assertEqual(award_1.tingkat_lokal, False)

        award_2 = report_1.record_3a_454.search([['nama', '=', 'Dosen IF Kedua']])
        self.assertEqual(award_2.nama, 'Dosen IF Kedua')
        self.assertEqual(award_2.prestasi_yang_dicapai, 'award1')
        self.assertEqual(award_2.tahun_pencapaian, '2018-01-01')
        self.assertEqual(award_2.tingkat_internasional, False)
        self.assertEqual(award_2.tingkat_nasional, False)
        self.assertEqual(award_2.tingkat_lokal, True)

        award_3 = report_2.record_3a_454.search([['nama', '=', 'Dosen EL Pertama']])
        self.assertEqual(award_3.nama, 'Dosen EL Pertama')
        self.assertEqual(award_3.prestasi_yang_dicapai, 'award2')
        self.assertEqual(award_3.tahun_pencapaian, '2018-01-01')
        self.assertEqual(award_3.tingkat_internasional, False)
        self.assertEqual(award_3.tingkat_nasional, True)
        self.assertEqual(award_3.tingkat_lokal, False)
