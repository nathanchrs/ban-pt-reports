# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Ridwan Kamal',
        nidn='014-A5A-133-C2D',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id,
        employment_type='pns'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_1.id, degree='doctoral', school='Kyoto University', major='Cyber Security & Informatics', city='Kyoto', finish='2014-05-05'
    ))

    dosen_if_2 = context.env['hr.employee'].create(dict(
        name='Baja Lodra',
        nidn='AS9-1J3-459K-DD',
        birthday='1967-04-20',
        is_faculty=True,
        prodi=prodi_if.id,
        employment_type='pns'
    ))
    context.env['itb.hr_education'].create(dict(
        employee_id=dosen_if_2.id, degree='doctoral', school='University of Manchester', major='Computer Science', city='Manchester', finish='2015-01-01'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_452(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        project_1_test = report_1.record_3a_452.search([['nama_dosen', '=', 'Ridwan Kamal']])
        self.assertEqual(project_1_test.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(project_1_test.jenjang_pendidikan, 'doctoral')
        self.assertEqual(project_1_test.bidang_studi, 'Cyber Security & Informatics')
        self.assertEqual(project_1_test.perguruan_tinggi, 'Kyoto University')
        self.assertEqual(project_1_test.negara, 'Kyoto')
        self.assertEqual(project_1_test.tahun_pelaksanaan, '2014')

        project_2_test = report_1.record_3a_452.search([['nama_dosen', '=', 'Baja Lodra']])
        self.assertEqual(project_2_test.nama_dosen, 'Baja Lodra')
        self.assertEqual(project_2_test.jenjang_pendidikan, 'doctoral')
        self.assertEqual(project_2_test.bidang_studi, 'Computer Science')
        self.assertEqual(project_2_test.perguruan_tinggi, 'University of Manchester')
        self.assertEqual(project_2_test.negara, 'Manchester')
        self.assertEqual(project_2_test.tahun_pelaksanaan, '2015')
