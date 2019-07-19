# -*- coding: utf-8 -*-
{
    'name': "Mi",

    'summary': """
        This is Mi App""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Rajkumar",
    'website': "http://www.sodexis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts'],

    # always loaded
    'data': [
        'data/report.paperformat.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'wizard/test_report.xml',
        'views/sale_view.xml',
        'views/service_view.xml',
        'views/news_feed.xml',
        'report/report_order_action.xml',
        'report/report_head_foot.xml',
        'report/report_order_template.xml',
        'report/customer_order_template_report.xml',
        'views/about_view.xml',
    ]
}