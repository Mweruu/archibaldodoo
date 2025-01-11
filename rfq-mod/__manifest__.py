{
    'name': 'RFQ Customization for Multiple Vendors',
    'version': '1.0',
    'depends': ['base', 'purchase', 'mail', 'hr'],  # Ensure the purchase module is installed
    'author': 'odoo',
    'description': """
        This module extends the Purchases app to provide:
        - Multiple vendors for RFQs.
        - Bids management for RFQs.
        - Selection of winning bids and automatic PO creation.
        - A purchase-request system for employees.
    """,
    'data': [
        # Add forms, views, and menus for all custom models
        'views/purchase_order_view.xml',
        'views/bid.xml',
        'views/bid_selection_wizard_view.xml',
        'views/purchase_request_view.xml',
        # Security rules (optional but recommended)
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
