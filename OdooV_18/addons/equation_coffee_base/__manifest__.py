# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EQUATION COFFEE - Base',
    'version': '18.0.0.0',
    'category': 'Customizations',
    'description': 'Equation Coffee customizations',
    'author': 'Equation Coffee',
    'maintainer': 'Firefly-e',
    'website': 'https://equationcoffee.com/',
    'depends': [
        'l10n_co'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        #Cron
        'data/get_currency_rate_usd_to_cop_ir_cron.xml',

        'data/res_partner_data.xml',
        'data/res_company_data.xml',
        'data/res_currency_data.xml',
        'data/res_country_data.xml',

        'data/res.country.state.csv',
        # 'data/res.city.csv',
        
        'data/ir_sequence_data.xml',
        'data/ir_sequence_date_range_data.xml',
        #'data/product_pricelist_data.xml',

        'data/equation_coffee_account_type_data.xml',
        'data/equation_coffee_customer_origin_data.xml',
        'data/equation_coffee_customer_program_data.xml', 


        'data/equation_coffee_project_data.xml',
        'data/equation_coffee_program_data.xml',
        'data/equation_coffee_varietal_data.xml',
        'data/equation_coffee_drying_process_data.xml', 
        'data/equation_coffee_fermentation_process_data.xml',
        'data/equation_coffee_profile_data.xml',
        'data/equation_coffee_category_data.xml',
        'data/equation_coffee_origin_data.xml',
        'data/equation_coffee_sca_data.xml',
        'data/equation_coffee_macroprofile_data.xml',
        'data/equation_coffee_process_offering_data.xml',

        'views/res_company_views.xml',

        'views/equation_coffe_account_type_views.xml',
        'views/equation_coffee_customer_origin_views.xml',
        'views/equation_coffee_project_views.xml',
        'views/equation_coffee_customer_program_views.xml',
        'views/equation_coffee_varietal_views.xml',
        'views/equation_coffee_drying_process_views.xml',
        'views/equation_coffee_fermentation_process_views.xml',
        'views/equation_coffee_program_views.xml',
        'views/equation_coffee_profile_views.xml',
        'views/equation_coffee_category_views.xml',
        'views/equation_coffee_origin_views.xml',
        'views/equation_coffee_sca_views.xml',
        'views/equation_coffee_macroprofile_views.xml',
        'views/equation_coffee_process_offering_views.xml',
        'views/equation_coffee_origin_town_views.xml',
        'views/menus.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
