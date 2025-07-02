# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Electronic Invoice',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customizations Electronic Invoice',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_partner',
        'equation_coffee_stock_account',
        'equation_coffee_productor',
        'l10n_co_account_edi',
        'account'
    ],
    'data': [
        'report/report_edi_account_invoice.xml',
        'views/res_partner_views.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
