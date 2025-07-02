# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Sale',
    'version': '18.0.0.0',
    'category': 'Customizations/Sales/CRM',
    'description': 'Equation Coffee customization sale',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'sale_management'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
