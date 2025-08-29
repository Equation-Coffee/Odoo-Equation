# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Contact',
    'version': '18.0.0.0',
    'category': 'Customizations/Sales/CRM',
    'description': 'Equation Coffee customization contact',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_base',
        'contacts',
        'account',
        'muestras',
    ],
    'data': [
        'report/report_invoice_template.xml',
        'views/res_partner_views.xml',
        'views/res_partner_account_priority.xml',
        'security/ir.model.access.csv'
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True,

    'assets': {
        'web.assets_backend': [
            'equation_coffee_partner/static/src/js/autocomplete.js',
            # 'equation_coffee_partner/static/src/xml/simple_autocomplete_char.xml',

        ],
        'web.assets_qweb':[
            'equation_coffee_partner/static/src/xml/simple_autocomplete_char.xml',
        ],
},
    
}
