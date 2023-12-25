from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    incoterm = fields.Many2one(
        'account.incoterms', 
        string='Incoterm', 
        help='International Commercial Terms are a series of pre-defined commercial terms used in international transactions.'
    )

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    document_number = fields.Char(
        string='Document Number', 
    )
    arrival_date = fields.Date(
        string='Arrival Date',
    )