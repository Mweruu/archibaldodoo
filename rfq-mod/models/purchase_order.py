from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Multiple vendors support (Requirement 1)
    vendor_ids = fields.Many2many(
        'res.partner',
        string='Vendor',
        domain="[('supplier_rank', '>', 0)]"
    )
    
    # Bids relation (Requirement 2)
    bid_ids = fields.One2many(
        'rfq.bid',
        'rfq_id',
        string='Supplier Bids'
    )
    
    # Winning bid (Requirement 3)
    winning_bid_id = fields.Many2one(
        'rfq.bid',
        string='Winning Bid',
        readonly=True
    )
    
    def action_select_winner(self):
        """Select the winning bid and create a purchase order."""
        if not self.bid_ids:
            raise UserError(_('No bids received yet.'))

        # Open wizard to select winning bid
        return {
            'name': _('Select Winning Bid'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bid.selection.wizard',
            'target': 'new',
            'context': {'default_rfq_id': self.id}
        }
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

        # Inform the user
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.rfq_id.id,
            'target': 'current',
        }

    