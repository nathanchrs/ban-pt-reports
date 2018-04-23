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

class TestRecord_3A_5122(common.TransactionCase):
    def test_refresh(self):
        report_1, report_2 = seed(self)

        report_1.refresh()
        report_2.refresh()

        catalog_1 = report_1.record_3a_5122.search([['kode_mk', '=', 'k01']])
        self.assertEqual(catalog_1.smt, '0')
        self.assertEqual(catalog_1.kode_mk, 'k01')
        self.assertEqual(catalog_1.nama_mk, 'Katalog 1')
        self.assertEqual(catalog_1.bobot_sks, 2)
        self.assertEqual(catalog_1.sks_mk_dalam_kurikulum_inti, '')
        self.assertEqual(catalog_1.sks_mk_dalam_kurikulum_institusional, '')
        self.assertEqual(catalog_1.bobot_tugas, '')
        self.assertEqual(catalog_1.kelengkapan_deskripsi, 'v')
        self.assertEqual(catalog_1.kelengkapan_silabus, 'v')
        self.assertEqual(catalog_1.kelengkapan_sap, '')
        self.assertEqual(catalog_1.unit_penyelenggara, 'Teknik Informatika')

        catalog_2 = report_2.record_3a_5122.search([['kode_mk', '=', 'k02']])
        self.assertEqual(catalog_2.smt, '0')
        self.assertEqual(catalog_2.kode_mk, 'k02')
        self.assertEqual(catalog_2.nama_mk, 'Katalog 2')
        self.assertEqual(catalog_2.bobot_sks, 3)
        self.assertEqual(catalog_2.sks_mk_dalam_kurikulum_inti, '')
        self.assertEqual(catalog_2.sks_mk_dalam_kurikulum_institusional, '')
        self.assertEqual(catalog_2.bobot_tugas, '')
        self.assertEqual(catalog_2.kelengkapan_deskripsi, 'v')
        self.assertEqual(catalog_2.kelengkapan_silabus, 'v')
        self.assertEqual(catalog_2.kelengkapan_sap, '')
        self.assertEqual(catalog_2.unit_penyelenggara, 'Teknik Elektro')
