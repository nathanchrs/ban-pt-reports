# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    employee1 = context.env['hr.employee'].create(dict(
        name='pustakawan1',
        nidn='012-AAA-123-BBB1',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pustakawan',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='undergraduate',
        employee_id=employee1.id
    ))

    employee2 = context.env['hr.employee'].create(dict(
        name='pustakawan2',
        nidn='012-AAA-123-BBB2',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pustakawan',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='graduate',
        employee_id=employee2.id
    ))

    employee3 = context.env['hr.employee'].create(dict(
        name='pustakawan3',
        nidn='012-AAA-123-BBB3',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pustakawan',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='doctoral',
        employee_id=employee3.id
    ))

    employee4 = context.env['hr.employee'].create(dict(
        name='pustakawan7',
        nidn='012-AAA-123-BBB7',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pustakawan',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='diploma',
        employee_id=employee4.id
    ))

    employee5 = context.env['hr.employee'].create(dict(
        name='pustakawan9',
        nidn='012-AAA-123-BBB9',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pustakawan',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='senior-high',
        employee_id=employee5.id
    ))

    employee6 = context.env['hr.employee'].create(dict(
        name='laboran/teknisi/analis/operator/programmer1',
        nidn='013-AAA-123-BBB1',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='laboran/teknisi/analis/operator/programmer',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='undergraduate',
        employee_id=employee6.id
    ))

    employee7 = context.env['hr.employee'].create(dict(
        name='laboran/teknisi/analis/operator/programmer2',
        nidn='013-AAA-123-BBB2',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='laboran/teknisi/analis/operator/programmer',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='graduate',
        employee_id=employee7.id
    ))

    employee8 = context.env['hr.employee'].create(dict(
        name='laboran/teknisi/analis/operator/programmer3',
        nidn='013-AAA-123-BBB3',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='laboran/teknisi/analis/operator/programmer',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='doctoral',
        employee_id=employee8.id
    ))

    employee9 = context.env['hr.employee'].create(dict(
        name='laboran/teknisi/analis/operator/programmer7',
        nidn='013-AAA-123-BBB7',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='laboran/teknisi/analis/operator/programmer',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='diploma',
        employee_id=employee9.id
    ))

    employee10 = context.env['hr.employee'].create(dict(
        name='laboran/teknisi/analis/operator/programmer9',
        nidn='013-AAA-123-BBB9',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='laboran/teknisi/analis/operator/programmer',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='senior-high',
        employee_id=employee10.id
    ))

    employee11 = context.env['hr.employee'].create(dict(
        name='tenaga administrasi1',
        nidn='014-AAA-123-BBB1',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='tenaga administrasi',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='undergraduate',
        employee_id=employee11.id
    ))

    employee12 = context.env['hr.employee'].create(dict(
        name='tenaga administrasi2',
        nidn='014-AAA-123-BBB2',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='tenaga administrasi',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='graduate',
        employee_id=employee12.id
    ))

    employee13 = context.env['hr.employee'].create(dict(
        name='tenaga administrasi3',
        nidn='014-AAA-123-BBB3',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='tenaga administrasi',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='doctoral',
        employee_id=employee13.id
    ))

    employee14 = context.env['hr.employee'].create(dict(
        name='tenaga administrasi7',
        nidn='014-AAA-123-BBB7',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='tenaga administrasi',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='diploma',
        employee_id=employee14.id
    ))

    employee15 = context.env['hr.employee'].create(dict(
        name='tenaga administrasi9',
        nidn='014-AAA-123-BBB9',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='tenaga administrasi',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='senior-high',
        employee_id=employee15.id
    ))

    employee16 = context.env['hr.employee'].create(dict(
        name='pramu1',
        nidn='015-AAA-123-BBB1',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pramu',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='undergraduate',
        employee_id=employee16.id
    ))

    employee17 = context.env['hr.employee'].create(dict(
        name='pramu2',
        nidn='015-AAA-123-BBB2',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pramu',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='graduate',
        employee_id=employee17.id
    ))

    employee18 = context.env['hr.employee'].create(dict(
        name='pramu3',
        nidn='015-AAA-123-BBB3',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pramu',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='doctoral',
        employee_id=employee18.id
    ))
    
    employee19 = context.env['hr.employee'].create(dict(
        name='pramu7',
        nidn='015-AAA-123-BBB7',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pramu',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='diploma',
        employee_id=employee19.id
    ))

    employee20 = context.env['hr.employee'].create(dict(
        name='pramu9',
        nidn='015-AAA-123-BBB9',
        birthday='1970-03-22',
        is_faculty=True,
        tendik='pramu',
        prodi=prodi_if.id
    ))
    context.env['itb.hr_education'].create(dict(
        name='education1',
        degree='senior-high',
        employee_id=employee20.id
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_461(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        ts_1 = report_1.record_3a_461.search([['jenis_tenaga_kependidikan', '=', 'Pustakawan']])
        self.assertEqual(ts_1.jenis_tenaga_kependidikan, 'Pustakawan')
        self.assertEqual(ts_1.jumlah_S3, 1)
        self.assertEqual(ts_1.jumlah_S2, 1)
        self.assertEqual(ts_1.jumlah_S1, 1)
        self.assertEqual(ts_1.jumlah_D4, 0)
        self.assertEqual(ts_1.jumlah_D3, 1)
        self.assertEqual(ts_1.jumlah_D2, 0)
        self.assertEqual(ts_1.jumlah_D1, 0)
        self.assertEqual(ts_1.jumlah_SMA_SMK, 1)
        self.assertEqual(ts_1.unit_kerja, 'UPT Perpustakaan ITB')

        ts_2 = report_1.record_3a_461.search([['jenis_tenaga_kependidikan', '=', 'Laboran/ Teknisi/ Analis/ Operator/ Programmer']])
        self.assertEqual(ts_2.jenis_tenaga_kependidikan, 'Laboran/ Teknisi/ Analis/ Operator/ Programmer')
        self.assertEqual(ts_2.jumlah_S3, 1)
        self.assertEqual(ts_2.jumlah_S2, 1)
        self.assertEqual(ts_2.jumlah_S1, 1)
        self.assertEqual(ts_2.jumlah_D4, 0)
        self.assertEqual(ts_2.jumlah_D3, 1)
        self.assertEqual(ts_2.jumlah_D2, 0)
        self.assertEqual(ts_2.jumlah_D1, 0)
        self.assertEqual(ts_2.jumlah_SMA_SMK, 1)
        self.assertEqual(ts_2.unit_kerja, 'STEI')

        ts_3 = report_1.record_3a_461.search([['jenis_tenaga_kependidikan', '=', 'Administrasi']])
        self.assertEqual(ts_3.jenis_tenaga_kependidikan, 'Administrasi')
        self.assertEqual(ts_3.jumlah_S3, 1)
        self.assertEqual(ts_3.jumlah_S2, 1)
        self.assertEqual(ts_3.jumlah_S1, 1)
        self.assertEqual(ts_3.jumlah_D4, 0)
        self.assertEqual(ts_3.jumlah_D3, 1)
        self.assertEqual(ts_3.jumlah_D2, 0)
        self.assertEqual(ts_3.jumlah_D1, 0)
        self.assertEqual(ts_3.jumlah_SMA_SMK, 1)
        self.assertEqual(ts_3.unit_kerja, 'STEI')

        ts_4 = report_1.record_3a_461.search([['jenis_tenaga_kependidikan', '=', 'Lainnya']])
        self.assertEqual(ts_4.jenis_tenaga_kependidikan, 'Lainnya')
        self.assertEqual(ts_4.jumlah_S3, 1)
        self.assertEqual(ts_4.jumlah_S2, 1)
        self.assertEqual(ts_4.jumlah_S1, 1)
        self.assertEqual(ts_4.jumlah_D4, 0)
        self.assertEqual(ts_4.jumlah_D3, 1)
        self.assertEqual(ts_4.jumlah_D2, 0)
        self.assertEqual(ts_4.jumlah_D1, 0)
        self.assertEqual(ts_4.jumlah_SMA_SMK, 1)
        self.assertEqual(ts_4.unit_kerja, 'STEI')

        ts_5 = report_1.record_3a_461.search([['jenis_tenaga_kependidikan', '=', 'Total']])
        self.assertEqual(ts_5.jenis_tenaga_kependidikan, 'Total')
        self.assertEqual(ts_5.jumlah_S3, 4)
        self.assertEqual(ts_5.jumlah_S2, 4)
        self.assertEqual(ts_5.jumlah_S1, 4)
        self.assertEqual(ts_5.jumlah_D4, 0)
        self.assertEqual(ts_5.jumlah_D3, 4)
        self.assertEqual(ts_5.jumlah_D2, 0)
        self.assertEqual(ts_5.jumlah_D1, 0)
        self.assertEqual(ts_5.jumlah_SMA_SMK, 4)
        self.assertEqual(ts_5.unit_kerja, '')
