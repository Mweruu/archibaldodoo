from odoo import models, fields, api

class RFQBid(models.Model):
    _name = 'rfq.bid'
    _description = 'RFQ Supplier Bid'
    
    rfq_id = fields.Many2one(
        'purchase.order',
        string='RFQ',
        required=True
    )
    bid_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], 
    string="Bid Status", default='draft'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        required=True,
        domain="[('supplier_rank', '>', 0)]"
    )
    bid_amount = fields.Monetary(
        string='Bid Amount',
        required=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id.id
    )
    bid_date = fields.Datetime(
        string='Bid Submission Date',
        default=fields.Datetime.now
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('won', 'Won'),
        ('lost', 'Lost')
    ], string='Status', default='draft')
    
    delivery_time = fields.Integer(
        string='Delivery Time (Days)'
    )
    notes = fields.Text(
        string='Additional Notes'
    )
