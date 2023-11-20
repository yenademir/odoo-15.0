{
    'name': "auto_fill_sales_model",
    'version': '1.0',
    'summary': "Automatically fills certain fields upon sales.order and purchase.order",
    'author': "Alperen Alihan ER",
    'website': "https://yenaengineering.nl",
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'project', 'analytic', 'sale'],
    'data': [
        'views/print_button.xml',
    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
