from odoo import models, fields

class PackagingPreparation(models.Model):
    _name = 'packaging.preparation'
    _description = 'Packaging Preparation'

    name = fields.Char('Description')
    batch_id = fields.Many2one('stock.picking.batch', string='Batch Reference')


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    packaging_preparation_ids = fields.One2many(
        comodel_name='packaging.preparation',
        inverse_name='batch_id',
        string='Packaging Preparations'
    )

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking'

    edespatch_delivery_type = fields.Selection(
        [
            ("edespatch", "E-Despatch"),
            ("printed", "Printed")
        ],
        store=True,
        readonly=False
    )