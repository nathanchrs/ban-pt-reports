# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='182', degree='s1', active=True
    ))

    catalog_1 = context.env['itb.academic_catalog'].create(dict(
        name='Katalog 1',
        code='k01',
        credit=2,
        note='This is note',
        syllabus='This is syllabus'
    ))
    curriculum_1 = context.env['itb.academic_curriculum'].create(dict(
        name='Curriculum 1',
        program_id=prodi_if.id,
        year=2015
    ))
    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_1.id,
        catalog_id=catalog_1.id,
        semester=0,
        category='wajib'
    ))

    catalog_2 = context.env['itb.academic_catalog'].create(dict(
        name='Katalog 2',
        code='k02',
        credit=3,
        note='This is note',
        syllabus='This is syllabus'
    ))
    curriculum_2 = context.env['itb.academic_curriculum'].create(dict(
        name='Curriculum 2',
        program_id=prodi_el.id,
        year=2016
    ))
    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_2.id,
        catalog_id=catalog_2.id,
        semester=0,
        category='opsional'
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

class TestRecord_3A_5121(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2 = seed(self)

        report_1.refresh()
        report_2.refresh()

        catalog_1 = report_1.record_3a_5121.search([['jenis_mata_kuliah', '=', 'Wajib']])
        self.assertEqual(catalog_1[0].jenis_mata_kuliah, 'Wajib')
        self.assertEqual(catalog_1[0].sks, 2)
        self.assertEqual(catalog_1[0].keterangan, '')

        catalog_11 = report_1.record_3a_5121.search([['jenis_mata_kuliah', '=', 'Pilihan']])
        self.assertEqual(catalog_11[0].jenis_mata_kuliah, 'Pilihan')
        self.assertEqual(catalog_11[0].sks, 0)
        self.assertEqual(catalog_11[0].keterangan, '')

        catalog_2 = report_2.record_3a_5121.search([['jenis_mata_kuliah', '=', 'Pilihan']])
        self.assertEqual(catalog_2[1].jenis_mata_kuliah, 'Pilihan')
        self.assertEqual(catalog_2[1].sks, 3)
        self.assertEqual(catalog_2[1].keterangan, '')

        catalog_22 = report_2.record_3a_5121.search([['jenis_mata_kuliah', '=', 'Wajib']])
        self.assertEqual(catalog_22[1].jenis_mata_kuliah, 'Wajib')
        self.assertEqual(catalog_22[1].sks, 0)
        self.assertEqual(catalog_22[1].keterangan, '')
