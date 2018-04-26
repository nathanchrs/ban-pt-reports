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

    publication_type = context.env['itb.hr_publication_media'].create(dict(name='International Proceeding'))

    publication_1 = context.env['itb.hr_publication'].create(dict(
        name='Publication 1',
        day='2014-10-05',
        publisher='Konferensi Anu 1',
        state='validate',
        media_id=publication_type.id
    ))

    context.env['itb.hr_publication_author'].create(dict(employee_id=dosen_if_1.id, role='author', publication_id=publication_1.id))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_453(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        publication_1_test = report_1.record_3a_453.search([['nama_dosen', '=', 'Ridwan Kamal'], ['jenis_kegiatan', '=', 'Konferensi Anu 1']])
        self.assertEqual(publication_1_test.nama_dosen, 'Ridwan Kamal')
        self.assertEqual(publication_1_test.jenis_kegiatan, 'Konferensi Anu 1')
        self.assertEqual(publication_1_test.tempat, '')
        self.assertEqual(publication_1_test.tahun, '2014')
        self.assertEqual(publication_1_test.sebagai_penyaji, 'checklist')
        self.assertFalse(publication_1_test.sebagai_peserta, '')
