# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Stock Account',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customizations Stock Account',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'sale_stock',
        'equation_coffee_account',
        'equation_coffee_stock'
    ],
    'data': [
        'report/report_deliveryslip_template.xml',
        'report/report_invoice_template.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
