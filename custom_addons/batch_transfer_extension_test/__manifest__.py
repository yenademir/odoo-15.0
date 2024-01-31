{
    'name': 'Batch Transfer Extension',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Extends Batch Transfer with additional fields',
    'author': 'Emre Mataracı',
    'website': 'www.yenaengineering.nl',
    'depends': ['stock', 'project', 'purchase', 'contacts', 'yena_local_development'],
    'data': [
        'views/batch_transfer_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
