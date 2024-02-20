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
    receipt_document_number = fields.Char(string="Receipt Document Number")
    import_decleration_number = fields.Char(string="Custom Decleration No")
    edespatch_move_id  = fields.Many2one('stock.move', string="E-Despatch Move")
    edespatch_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Response'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], string='e-Dispatch State', default='draft', required=True)
    transport_type = fields.Selection([
        ('airtransport', 'Air Transport'),
        ('roadtransport', 'Road Transport'),
        ('railtransport', 'Rail Transport'),
        ('maritimetransport', 'Maritime Transport'),
    ], string='Transport Type',  default="roadtransport")
    edespatch_profile = fields.Selection(
        [('TEMELIRSALIYE', 'Temel İrsaliye')], 
        string='e-Despatch Profile', 
        default='TEMELIRSALIYE', 
    )
    edespatch_sender_id = fields.Many2one(
        'edespatch.sender', 
        string='e-Despatch Sender', 
        domain=[('name', '=', ['urn:mail:irsaliyegb@yenaengineering.nl'])],
    )
    edespatch_state = fields.Selection(
        [('draft', 'Draft'), 
         ('waiting', 'Waiting'), 
         ('completed', 'Completed'), 
         ('failed', 'Failed'), 
         ('rejected', 'Rejected'),
         ('different', 'E-despatch Statuses are different!')],
        string='e-Despatch State',
        #compute='_compute_edespatch_state',
        default='draft',
        store=True
    )
    edespatch_number_sequence = fields.Many2one(
        'ir.sequence', 
        string='e-Despatch Number Sequence', 
        domain=[('name', 'in', ['E-Despatch'])],
    )
    edespatch_postbox_id = fields.Many2one(
        'edespatch.postbox', 
        string='e-Despatch Postbox',
        domain=[('name', '=', ['urn:mail:irsaliyepk@gib.gov.tr'])],
    )