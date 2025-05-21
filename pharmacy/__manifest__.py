{
    'name': 'Pharmacy Management',
    'version': '1.0',
    'summary': 'Manage Pharmacy',
    'sequence': 10,
    'category': 'Healthcare',
    'depends': ['base', 'contacts', ],
    'data': [
        'security/ir.model.access.csv',
        'views/vendor_views.xml',
        'views/purchase_management.xml',
        'report/report_purchase.xml',
        'report/report_purchase_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

