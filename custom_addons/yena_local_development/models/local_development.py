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
    edespatch_delivery_type = fields.Selection([
        ('printed', 'Printed'),
        ('edespatch', 'E-Despatch')
    ], string='E-Despatch Delivery Type')

    driver_ids = fields.Many2many(
        'res.partner',
        'stock_picking_driver_rel',
        'batch_id',
        'partner_id',  
        string='Drivers',
        store=True, 
    )
    edespatch_date = fields.Datetime(string="Real Departure Date")
    receipt_document_number = fields.Char(string="Receipt Document Number")
    import_decleration_number = fields.Char(string="Import Decleration Number")
    edespatch_move_id  = fields.Many2one('stock.move', string="E-Despatch Move")