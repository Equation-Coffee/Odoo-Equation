# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - MRP',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customization Mrp',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'purchase_mrp',
        'mrp_account'
    ],
    'data': [
        'data/decimal_precision_equation_coffee_cost_share_data.xml',
        'views/mrp_production_views.xml'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
