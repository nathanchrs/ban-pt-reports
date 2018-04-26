# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='132', degree='s1', active=True
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Ridwan Kamal',
        nidn='014-A5A-133-C2D',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id,
        employment_type='pns'
    ))

    partner_1 = context.env['res.partner'].create(dict(
        name='Partner Only', is_instructor=True
    ))

    semester_2_2015 = context.env['itb.academic_semester'].create(dict(name='2-2014/2015', type='even', year=2015, start='2015-01-01', finish='2015-05-05'))
    semester_1_2015 = context.env['itb.academic_semester'].create(dict(name='1-2014/2015', type='odd', year=2014, start='2014-09-01', finish='2014-12-12'))

    catalog_1 = context.env['itb.academic_catalog'].create(dict(code='IF9999', name='Matkul Informatika 1', credit=3))
    catalog_2 = context.env['itb.academic_catalog'].create(dict(code='IF9998', name='Matkul Informatika 2', credit=2))
    catalog_3 = context.env['itb.academic_catalog'].create(dict(code='IF9997', name='Matkul Elektro 3', credit=1))
    catalog_4 = context.env['itb.academic_catalog'].create(dict(code='IF9996', name='Matkul Elektro 4', credit=4))

    course_1 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_1.id, program_id=prodi_if.id, semester_id=semester_2_2015.id))
    course_2 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_2.id, program_id=prodi_if.id, semester_id=semester_2_2015.id))
    course_3 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_3.id, program_id=prodi_el.id, semester_id=semester_1_2015.id))
    course_4 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_4.id, program_id=prodi_el.id, semester_id=semester_1_2015.id))

    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='2-2014/2015', course_id=course_1.id, partner_id=partner_1.id, credit=course_1.catalog_id.credit))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='2-2014/2015', course_id=course_2.id, partner_id=partner_1.id, credit=course_2.catalog_id.credit))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='1-2014/2015', course_id=course_3.id, partner_id=partner_1.id, credit=course_3.catalog_id.credit))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='1-2014/2015', course_id=course_4.id, partner_id=partner_1.id, credit=course_4.catalog_id.credit))

    project_1 = context.env['itb.hr_project'].create(dict(name='test_1', tipe='penelitian', start='2014-03-09', state='valid', deskripsi_sispran='DES-01', reference='REF-01', nilai=1000000))
    project_2 = context.env['itb.hr_project'].create(dict(name='test_2', tipe='pengabdian', start='2014-03-10', state='valid', deskripsi_sispran='DES-02', reference='REF-02', nilai=1000000))
    project_3 = context.env['itb.hr_project'].create(dict(name='test_3', tipe='penelitian', start='2015-01-08', state='valid', deskripsi_sispran='DES-03', reference='REF-03', nilai=1000000))
    project_4 = context.env['itb.hr_project'].create(dict(name='test_4', tipe='pengabdian', start='2015-01-10', state='valid', deskripsi_sispran='DES-04', reference='REF-04', nilai=1000000))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_1.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_2.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_3.id))
    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_4.id))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_433(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        dosen_1_test = report_1.record_3a_433.search([['nama_dosen', '=', 'Ridwan Kamal']])
        self.assertEqual(dosen_1_test.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(dosen_1_test.sks_ps_sendiri, 5)
        self.assertEqual(dosen_1_test.sks_ps_lain_pt_sendiri, 5)
        self.assertEqual(dosen_1_test.sks_pt_lain, 0)
        self.assertEqual(dosen_1_test.sks_penelitian, 2)
        self.assertEqual(dosen_1_test.sks_pengmas, 2)
        self.assertEqual(dosen_1_test.sks_mgmt_pt_sendiri, 0)
        self.assertEqual(dosen_1_test.sks_mgmt_pt_lain, 0)
        self.assertEqual(dosen_1_test.sks_total, 14)
