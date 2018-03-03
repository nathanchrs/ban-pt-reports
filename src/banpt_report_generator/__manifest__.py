# -*- coding: utf-8 -*-

# Odoo module definition file for BAN-PT Report Generator.

{
    # Module metadata
    'name': "BAN-PT Report Generator",
    'version': '1.0',
    'author': "I01K01",
    'category': 'BAN-PT',
    'description': 'BAN-PT accreditation report generator for STEI ITB',

    # List of module dependencies of this module.
    'depends': ['base'],

    # Data files always loaded at installation.
    # Add all non-Python files required by this module here.
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/banpt_report_generator.xml'
    ],

    # Data files containing optionally loaded demonstration data.
    'demo': []
}
