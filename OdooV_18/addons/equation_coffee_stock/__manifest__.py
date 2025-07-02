# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Stock',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customization stock',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'equation_coffee_product',
        'equation_coffee_productor'
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'data/stock_warehouse_data.xml',
        'data/stock_location_data.xml',

        'report/report_deliveryslip_template.xml',
        'report/stock_report_delivery_has_serial_move_line.xml',
        
        'views/stock_quant_views.xml',
        'views/equation_coffee_sca_score_views.xml',
	    'views/equation.coffee_lot_package_view.xml',
        'views/stock_lot_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_move_views.xml',
        'views/menus.xml'


    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
