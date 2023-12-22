from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    incoterm = fields.Many2one(
        'account.incoterms', 
        string='Incoterm', 
        help='International Commercial Terms are a series of pre-defined commercial terms used in international transactions.'
    )
