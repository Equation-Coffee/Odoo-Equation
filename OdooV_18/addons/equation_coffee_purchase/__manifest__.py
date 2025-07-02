# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Purchase',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customization purchase',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base'
    ],
    'data': [
        'views/purchase_order_views.xml',
        'report/purchase_quotation_templates.xml',
        'report/purchase_order_template.xml',


    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
