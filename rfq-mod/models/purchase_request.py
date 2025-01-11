from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(
        string='Request Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Requesting Employee',
        required=True,
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        related='employee_id.department_id',
        store=True
    )
    request_date = fields.Date(
        string="Request Date", 
        required=True, 
        default=fields.Date.context_today
    )
    product_ids = fields.One2many(
        'purchase.request.line',
        'request_id',
        string='Products'
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rfq_created', 'RFQ Created'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    def action_create_rfq(self):
        """Create RFQ from approved purchase request."""
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_('Only approved requests can create RFQs.'))
            
        vals = {
            'origin': self.name,
            'date_order': fields.Datetime.now(),
        }
        
        rfq = self.env['purchase.order'].create(vals)
        
        for line in self.product_ids:
            self.env['purchase.order.line'].create({
                'order_id': rfq.id,
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'name': line.description or line.product_id.name,
                'date_planned': fields.Date.today(),
            })
        
        self.write({'state': 'rfq_created'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': rfq.id,
            'view_mode': 'form',
            'target': 'current',
        }

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'
    
    request_id = fields.Many2one(
        'purchase.request',
        string='Purchase Request'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0
    )
