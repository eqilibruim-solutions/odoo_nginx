# -*- coding: utf-8 -*-
{
    'name': "stock_mod",

    'summary': """
        Modelo de agregracion para principal stock""",

    'description': """
        Bexsoluciones modulo complementario de stock
    """,

    'author': "SimonT",
    'website': "https://bexsoluciones.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
