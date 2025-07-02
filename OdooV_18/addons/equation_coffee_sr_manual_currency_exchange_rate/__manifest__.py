# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Exchange Rate',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customization Exchange Rate',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_purchase',
        'sr_manual_currency_exchange_rate',
        'account_accountant'
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'report/purchase_quotation_templates.xml',
        'report/purchase_order_template.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
