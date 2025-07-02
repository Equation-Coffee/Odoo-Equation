# -*- coding: utf-8 -*-
{
    'name': 'Reporte de Comisiones',
    'version': '18.0.0.0',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/commission_report_wizard_views.xml',
        'views/account_menus.xml',
    ],
    'application': True,
}