from odoo import models, fields, api, _
from odoo.exceptions import UserError

class BidSelectionWizard(models.TransientModel):
    _name = 'bid.selection.wizard'
    _description = 'Wizard to select winning bid'

    # Reference to the purchase order (RFQ)
    rfq_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        required=True,
        ondelete='cascade',
        readonly=True
    )

    # Bids to choose from
    bid_ids = fields.Many2many(
        'rfq.bid',
        string='Bids',
        domain="[('rfq_id', '=', rfq_id)]",
        required=True
    )

    # Selected winning bid
    winning_bid_id = fields.Many2one(
        'rfq.bid',
        string='Winning Bid',
        required=True
    )

    def action_confirm_winner(self):
        """Confirms the winning bid and updates the purchase order"""
        if not self.winning_bid_id:
            raise UserError(_('Please select a winning bid.'))

        # Update the purchase order with the winning bid
        self.rfq_id.write({'winning_bid_id': self.winning_bid_id.id})

        # Optionally: You can perform additional actions here, such as creating the purchase order
        self.create_purchase_order()

        # Inform the user
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.rfq_id.id,
            'target': 'current',
        }

    def create_purchase_order(self):
        """Creates the actual purchase order from the selected bid"""
        order_values = {
            'partner_id': self.winning_bid_id.vendor_id.id,  # Vendor of the winning bid
            'order_line': [(0, 0, {
                'product_id': self.winning_bid_id.product_id.id,
                'price_unit': self.winning_bid_id.price,
                'product_uom': self.winning_bid_id.product_uom.id,
                'product_qty': self.winning_bid_id.product_qty,
            })],
            # Additional fields based on your use case (e.g., currency, payment terms, etc.)
        }
        order = self.env['purchase.order'].create(order_values)
        return order.id
