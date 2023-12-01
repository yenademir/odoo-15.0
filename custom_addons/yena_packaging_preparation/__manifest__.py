{
    'name': "YENA Packaging Preparation",
    'version': '15.1.0',
    'summary': "Easy preparation of transfer documents",
    'author': "Alperen Alihan ER",
    'website': "https://yenaengineering.nl",
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['product', 'stock', 'barcodes', 'digest', 'purchase', 'base', 'account', 'delivery'],
    'data': [
        'views/packaging_preparation.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
