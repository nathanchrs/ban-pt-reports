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

    partner_1 = context.env['res.partner'].create(dict(
        name='Partner Only', is_instructor=True
    ))

    semester_2_2015 = context.env['itb.academic_semester'].create(dict(name='2-2014/2015', type='even', year=2015, start='2015-01-01', finish='2015-05-05'))
    semester_1_2015 = context.env['itb.academic_semester'].create(dict(name='1-2014/2015', type='odd', year=2014, start='2014-09-01', finish='2014-12-12'))

    catalog_1 = context.env['itb.academic_catalog'].create(dict(code='IF9999', name='Matkul Informatika 1', credit=3))
    catalog_2 = context.env['itb.academic_catalog'].create(dict(code='IF9998', name='Matkul Informatika 2', credit=2))
    catalog_3 = context.env['itb.academic_catalog'].create(dict(code='IF9997', name='Matkul Informatika 3', credit=1))
    catalog_4 = context.env['itb.academic_catalog'].create(dict(code='IF9996', name='Matkul Informatika 4', credit=4))

    course_1 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_1.id, program_id=prodi_if.id, semester_id=semester_2_2015.id))
    course_2 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_2.id, program_id=prodi_if.id, semester_id=semester_2_2015.id))
    course_3 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_3.id, program_id=prodi_if.id, semester_id=semester_1_2015.id))
    course_4 = context.env['itb.academic_course'].create(dict(catalog_id=catalog_4.id, program_id=prodi_if.id, semester_id=semester_1_2015.id))

    group_1 = context.env['itb.academic_group'].create(dict(name='Group 1', course_id=course_1.id))

    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='2-2014/2015', course_id=course_1.id, partner_id=partner_1.id))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='2-2014/2015', course_id=course_2.id, partner_id=partner_1.id))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='1-2014/2015', course_id=course_3.id, partner_id=partner_1.id))
    context.env['itb.academic_instructor'].create(dict(employee_id=dosen_if_1.id, semester='1-2014/2015', course_id=course_4.id, partner_id=partner_1.id))

    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_1.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_1.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-11 06:25:33.966', finish='2015-03-11 06:25:33.966', course_id=course_1.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-12 06:25:34.966', finish='2015-03-12 06:25:34.966', course_id=course_1.id, group_id=group_1.id))

    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_2.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_2.id, group_id=group_1.id))

    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_3.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_3.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_3.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_3.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_3.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_3.id, group_id=group_1.id))

    context.env['itb.academic_lecture'].create(dict(start='2015-03-09 06:25:31.966', finish='2015-03-09 06:25:31.966', course_id=course_4.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_4.id, group_id=group_1.id))
    context.env['itb.academic_lecture'].create(dict(start='2015-03-10 06:25:32.966', finish='2015-03-10 06:25:32.966', course_id=course_4.id, group_id=group_1.id))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_434(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        matkul_1 = report_1.record_3a_434.search([['nama_dosen', '=', 'Ridwan Kamal'], ['kode_matkul', '=', 'IF9999']])
        self.assertEqual(matkul_1.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(matkul_1.kode_matkul, 'IF9999')
        self.assertEqual(matkul_1.nama_matkul, 'Matkul Informatika 1')
        self.assertEqual(matkul_1.jumlah_sks_matkul, 3)
        self.assertEqual(matkul_1.jumlah_pertemuan_terencana_matkul, 30)
        self.assertEqual(matkul_1.jumlah_pertemuan_terlaksana_matkul, 4)

        matkul_2 = report_1.record_3a_434.search([['nama_dosen', '=', 'Ridwan Kamal'], ['kode_matkul', '=', 'IF9998']])
        self.assertEqual(matkul_2.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(matkul_2.kode_matkul, 'IF9998')
        self.assertEqual(matkul_2.nama_matkul, 'Matkul Informatika 2')
        self.assertEqual(matkul_2.jumlah_sks_matkul, 2)
        self.assertEqual(matkul_2.jumlah_pertemuan_terencana_matkul, 15)
        self.assertEqual(matkul_2.jumlah_pertemuan_terlaksana_matkul, 2)

        matkul_3 = report_1.record_3a_434.search([['nama_dosen', '=', 'Ridwan Kamal'], ['kode_matkul', '=', 'IF9997']])
        self.assertEqual(matkul_3.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(matkul_3.kode_matkul, 'IF9997')
        self.assertEqual(matkul_3.nama_matkul, 'Matkul Informatika 3')
        self.assertEqual(matkul_3.jumlah_sks_matkul, 1)
        self.assertEqual(matkul_3.jumlah_pertemuan_terencana_matkul, 15)
        self.assertEqual(matkul_3.jumlah_pertemuan_terlaksana_matkul, 6)

        matkul_4 = report_1.record_3a_434.search([['nama_dosen', '=', 'Ridwan Kamal'], ['kode_matkul', '=', 'IF9996']])
        self.assertEqual(matkul_4.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(matkul_4.kode_matkul, 'IF9996')
        self.assertEqual(matkul_4.nama_matkul, 'Matkul Informatika 4')
        self.assertEqual(matkul_4.jumlah_sks_matkul, 4)
        self.assertEqual(matkul_4.jumlah_pertemuan_terencana_matkul, 30)
        self.assertEqual(matkul_4.jumlah_pertemuan_terlaksana_matkul, 3)
