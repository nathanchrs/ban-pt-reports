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
        'views/record_3a_454_views.xml',
        'views/record_3a_455_views.xml',
        'views/record_3a_461_views.xml',
        'views/record_3a_5121_views.xml',
        'views/record_3a_5122_views.xml',
        'views/record_3a_513_views.xml',
        'views/record_3a_541_views.xml',
        'views/record_3a_551_views.xml',
        'views/record_3a_6211_views.xml',
        'views/record_3a_6212_views.xml',
        'views/record_3a_622_views.xml',
        'views/record_3a_623_views.xml',
        'views/record_3a_631_views.xml',
        'views/record_3a_632_views.xml',
        'views/record_3a_633_views.xml',
        'views/record_3a_6411_views.xml',
        'views/record_3a_6412_views.xml',
        'views/record_3a_643_views.xml',
        'views/record_3a_652_views.xml',
        'views/record_3a_711_views.xml',
        'views/record_3a_712_views.xml',
        'views/record_3a_713_views.xml',
        'views/record_3a_714_views.xml',
        'views/record_3a_721_views.xml',
        'views/record_3a_731_views.xml',
        'views/record_3a_732_views.xml',
        'views/record_3b_312_views.xml',
        'views/record_3b_321_views.xml',
        'views/record_3b_411_views.xml',
        'views/record_3b_412_views.xml',
        'views/record_3b_42_views.xml',
        'views/record_3b_6111_views.xml',
        'views/record_3b_6112_views.xml',
        'views/record_3b_6113_views.xml',
        'views/record_3b_642_views.xml',
        'views/record_3b_711_views.xml',
        'views/record_3b_721_views.xml',
        'views/record_3b_731_views.xml',
        'views/record_3b_732_views.xml',

        # This line must be last (after all other view files)
        'views/banpt_report_generator.xml'
    ],

    # Data files containing optionally loaded demonstration data.
    'demo': []
}
