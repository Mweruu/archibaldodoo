from odoo import models, fields, api
from datetime import datetime

class Application(models.Model):
    _name = 'application'
    _description = "Application"
    _inherit = 'mail.thread'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('cancel', 'Cancelled')],
        default='draft', tracking=True)
    name = fields.Char('Name')
    surname = fields.Char('Surname')
    dob = fields.Date(default=datetime.now())
    country = fields.Char('Country')
    location = fields.Char('Location')
    picture =fields.Binary('Image')

    def action_confirm(self):
        for record in self:
            record.state = 'confirm'
