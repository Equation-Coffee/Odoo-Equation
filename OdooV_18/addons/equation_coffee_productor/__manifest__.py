# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Productor',
    'version': '18.0.0.0',
    'category': 'Customizations/Sales/CRM',
    'description': 'Equation Coffee customization contact productor',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'contacts'
    ],
    'data': [
        'views/res_partner_views.xml'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
