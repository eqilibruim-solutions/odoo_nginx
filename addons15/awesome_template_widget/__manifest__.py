# -*- coding: utf-8 -*-
{
    'name': "awesome_template_widget",

    'summary': """
        awesome template widget, usefull widget to show image, color, url, html, and many other custom content in list, it is a advace field for list""",

    'description': """
        awesome template widget, usefull widget to show image, url, and many other custom content in list view and form view
    """,

    'author': "awesome odoo",
    'website': "https://www.funenc.com",
    'live_test_url': "https://www.funenc.com",

    'category': 'application/widget',
    'version': '15.0.0.1',
    'license': 'OPL-1',
    'images': ['static/description/banner.png',
               'static/description/screen_shot.png'],

    'depends': ['base'],

    'data': [],

    'assets': {
        'web.assets_backend': [
            'awesome_template_widget/static/js/template_widget.js',
            'awesome_template_widget/static/js/basic_render.js',
        ],

        'web.assets_qweb': []
    }
}
