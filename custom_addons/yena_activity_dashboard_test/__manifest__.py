{
    'name': 'YENA Activity Dashboard',
    'version': '1.0',
    'summary': 'Shows all scheduled activities in one place.',
    'website': "https://yenaengineering.nl",
    'author': 'Emre Mataracı',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/yena_activity_dashboard_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}