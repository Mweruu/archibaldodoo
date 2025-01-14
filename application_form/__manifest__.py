{
    'name': 'Application Form',
    'version': '1.0',
    'depends': ['base', 'mail'],  # Ensure the purchase module is installed
    'author': 'odoo',
    'description': """
    """,
    'data': [
        'views/application_view.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
