# -*- coding: utf-8 -*-
# pylint: skip-file

# Odoo module definition file for BAN-PT Report Generator.

{
    # Module metadata
    'name': "BAN-PT Report Generator",
    'version': '1.0',
    'author': "I01K01",
    'category': 'BAN-PT',
    'application': True,
    'description': 'BAN-PT accreditation report generator for STEI ITB',

    # List of module dependencies of this module.
    'depends': ['base', 'web', 'itb_academic', 'itb_hr'],

    # Data files always loaded at installation.
    # Add all non-Python files required by this module here.
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # Add view files here
        'views/report_views.xml',

        'views/Record_3A_454_views.xml',
        'views/Record_3A_455_views.xml',
        'views/Record_3A_461_views.xml',
        'views/Record_3A_622_views.xml',
        'views/Record_3A_623_views.xml',
        'views/Record_3A_631_views.xml',
        'views/dosen_views.xml',
        'views/identitas_views.xml',
        'views/pengisi_views.xml',
        'views/record_3a_311_views.xml',
        'views/record_3a_312_views.xml',
        'views/record_3a_314_views.xml',
        'views/record_3a_331_views.xml',
        'views/record_3a_431_views.xml',
        'views/record_3a_432_views.xml',
        'views/record_3a_433_views.xml',
        'views/record_3a_434_views.xml',
        'views/record_3a_435_views.xml',
        'views/record_3a_441_views.xml',
        'views/record_3a_442_views.xml',
        'views/record_3a_451_views.xml',
        'views/record_3a_452_views.xml',
        'views/record_3a_453_views.xml',
        'views/record_3a_5121_views.xml',
        'views/record_3a_5122_views.xml',
        'views/record_3a_513_views.xml',
        'views/record_3a_541_views.xml',
        'views/record_3a_551_views.xml',

        # This line must be last (after all other view files)
        'views/banpt_report_generator.xml'
    ],

    # Data files containing optionally loaded demonstration data.
    'demo': []
}
