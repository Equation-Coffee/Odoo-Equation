# -*- coding: utf-8 -*-
{
    'name': "Modulo de Muestras",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Juan Pablo Vallejo Montañez - Departamento de Inteligencia Artificial",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventario',
    'version': '18.0.0.0',
    'installable': True,
    'auto-install': False,
    'application' : True,
    'license' : 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','web','stock','uom','equation_coffee_base'],

    'images': ['muestras/static/description/icon.png'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/sequences.xml',
        'views/muestras_atlas_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/offering_history_views.xml',
        'views/muestras_spoteu_views.xml',
        'views/muestras_order_lines_views.xml',
        'views/muestras_order_lines_release_views.xml',
        'views/muestras_order_views.xml',
        'views/muestras_wizard_sale_views.xml',
        'views/muestras_wizard_extend_due_date_views.xml',
        'views/muestras_extension_reason_views.xml',
        'views/muestras_order_extension_views.xml', 
        'views/muestras_price_views.xml',
        'views/muestras_menus.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'data/rules.xml',
        'reports/muestras_report_view.xml',
        'reports/muestras_report_template.xml',
        'reports/offering_wizard_report.xml',
        'data/muestras_price_data.xml',
        'views/crm.xml',

        # 'views/assets.xml',
    
    ],
    'demo': [
        'demo/demo.xml',
    ],

    # 'post_init_hook':'post_init_hook',

   'assets': {
        'web.assets_backend': [
            '/muestras/static/src/css/custom_styles.css',
            # '/muestras/static/src/js/custom_tree_button.js',
            '/muestras/static/src/js/sale_tree_extend.js',
            '/muestras/static/src/xml/wizard_button_offering.xml',
            '/muestras/static/src/xml/atlas_update_button.xml',
            '/muestras/static/src/img/offering_background.png',
            # '/muestras/static/src/js/autocomplete.js',
            # '/muestras/static/equationlogo.png',  # Asegúrate de que tenga la extensión .xml
            # '/muestras/static/src/css/offering.css',
            # '/muestras/static/src/css/css_report.xml',

        ],

        'web.assets_qweb': [  # Si es para el reporte QWeb
            '/muestras/static/src/css/offering.css',  # Ruta del archivo CSS
        ],
    },
}
