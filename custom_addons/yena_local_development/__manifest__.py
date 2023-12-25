{
    'name': "Local Development",
    'version': '15.0.1',
    'summary': "Synchronization of local server to live server",
    'author': "Emre MATARACI",
    'website': "https://yenaengineering.nl",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'sale',
        'purchase',
        'project',
        'contacts',
        'stock',
        'account',
    ],
     'data': [
         'views/local_view.xml',
     ],
    'installable': True,
    'auto_install': False,
}
