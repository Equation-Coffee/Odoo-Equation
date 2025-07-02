# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Reports',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customizations',
    'author': 'Equation Coffee',
    'maintainer': 'Equation IA',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'l10n_co',
        'l10n_co_account_edi'
    ],
    'data': [
        'reports/equation_coffee_reports_edi_account_invoice_report.xml',
        
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
