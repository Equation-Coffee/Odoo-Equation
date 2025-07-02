# -*- coding: utf-8 -*-
#
{
    'name': 'l10n co hr payroll novelties',
    'summary': 'Nómina novedades',
    'description': "novelties menu on payroll",
    'author': 'Firefly-e',
    'license': 'AGPL-3',
    'category': 'Human Resources/Localizations/Payroll',
    'version': '18.0.0.0',
    'website': "https://www.firefly-e.com",
    'support': 'info@firefly-e.com',
    'depends': [
        'hr_payroll',
        'hr_work_entry_contract_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_payroll_novelties_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': False,
}
