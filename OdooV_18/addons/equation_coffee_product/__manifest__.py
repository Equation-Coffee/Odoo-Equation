# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Product',
    'version': '18.0.1.0.2',
    'category': 'Customizations',
    'description': 'Equation Coffee customization product',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'stock',
        'product'
    ],
    'data': [
        'views/product_template_views.xml'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
