# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - CRM',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customization crm',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'crm',
        'sales_team'
    ],
    'data': [
        'views/crm_lead_views.xml'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
