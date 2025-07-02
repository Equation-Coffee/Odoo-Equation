# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Account',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customizations Account',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'account',
        'equation_coffee_base'
    ],
    'data': ['views/account_move_views.xml',
    'reports/report_invoice_document.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
