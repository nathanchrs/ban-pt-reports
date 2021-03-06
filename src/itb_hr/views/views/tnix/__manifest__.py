{ 
    'name': 'TNI Career', 
    'description': 'Career Placement,the TNI way.Extended version.',
    'category': 'Human Resources',
    'author': 'Odoonesia (info@odoonesia.com)', 
    'depends': ['base'],
    'data': [
        'data/tnix.suku.csv',
        'data/tnix.kecabangan.csv',
        'data/tnix.kesatuan.csv',
        'data/tnix.propinsi.csv',
        'data/tnix.terdekat.csv',
        'data/tnix.posisi.csv',
        'views/tnix.xml',
        'views/menu.xml',
        'views/custom_view.xml',
        'wizard/tempatkan.xml',
        'wizard/seleksi.xml',
        'wizard/secapa.xml',
        'reports/kandidat.xml',
        'reports/sidang.xml',
            ],
    'qweb':['static/src/xml/custom_template.xml',],
    'css': ['static/src/css/styles.css'], 
    'version': '0.1',
	'application':True,
	'installable': True,
	'auto_install': False, 
} 