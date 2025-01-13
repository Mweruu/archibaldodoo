from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    partner_ids = fields.Many2many(
        'res.partner',
        string='Vendors',
        required=True,
        states=READONLY_STATES,
        change_default=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="You can select multiple vendors by their Name, TIN, Email, or Internal Reference."
    )
