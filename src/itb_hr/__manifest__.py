{ 
    'name': 'ITB Human Resource', 
    'description': 'Human Resource Management, the ITB way',
    'category': 'Employees',
    'author': 'Housny M.', 
    'depends': ['base','hr','website','itb_academic'],
    'data': [
        #'security/res.groups.csv',
        #'security/ir.model.access.csv',
        #'security/ir.rule.csv',
        'views/menu.xml',
        'views/award.xml',
        'views/duty.xml',
        'views/employee.xml',
        'views/assignment.xml',
        'views/award.xml',
        'views/education.xml',
        'views/employment.xml',
        'views/family.xml',
        'views/jabatan.xml',
        'views/membership.xml',
        'views/pangkat.xml',
        'views/project.xml',
        'views/publication.xml',
        'views/training.xml',
        'views/work.xml',
        'views/membership_rpt_view.xml',
        'views/membership_rpt.xml',
        #'views/example_webpage.xml',
        'reports/abet_cv.xml',
        'views/publication_authors.xml',
        #'reports/faculty.xml',
        #'reports/template.xml',
        #'reports/dosen.xml',
        #'reports/todo_web.xml',
        #'reports/todo_extend.xml',
        #'reports/config_data.xml',
    ], 
    'version': '0.1',
	'application':True,
	'installable': True,
	'auto_install': False, 
} 