{ 
    'name': 'ITB Planning', 
    'description': 'Planning, the ITB way',
    'category': 'Plan',
    'author': 'Housny M.', 
    'depends': ['base'],
     'data': [
        'security/itb_plan_security.xml',
        'security/ir.model.access.csv',
        'views/confirmation.xml',
        'views/evaluation.xml',
        'views/implementation.xml',
        'views/indicator.xml',
        'views/initiative.xml',
        'views/menu.xml',
        'views/plan.xml',
        'views/program.xml',
        'views/relocation.xml',
        'views/request.xml',
        'views/spending_actual.xml',
        'views/spending.xml',
        'views/target.xml',
        'views/unit.xml',
        'wizard/budget_manager_wizard.xml',
        'views/ado.xml',
        'views/pagu.xml',
        'views/allocation.xml',
        'views/plan_int.xml',
        'views/initiative_int.xml',
        'views/spending_int.xml',
        'views/target_int.xml',
        #'data/itb.plan_line.csv',
        #'security/itb.plan_spending.csv',
        #'security/itb.plan_quarter.csv',
        #'wizard/plan_itb_wizard.xml',
        #'views/dialog.xml',
    ], 
    'version': '0.1',
	'application':True,
	'installable': True,
	'auto_install': False, 
} 