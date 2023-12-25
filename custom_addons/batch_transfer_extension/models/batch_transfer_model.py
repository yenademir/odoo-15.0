from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'
    _description = "Batch Transfer"
    _order = "name desc"

    edespatch_date = fields.Date(string="Real Departure Date")
    situation = fields.Selection(
        [("to_be_planned", "To Be Planned"),
         ("on_the_way", "On The Way"),
         ("arrived", "Arrived")], string="Situation")
    customer_ids = fields.Many2many(
        'res.partner',
        'batch_customer_rel', 
        'batch_id', 
        'partner_id',
        string='Customers'
    )
    vendor_ids = fields.Many2many(
        'res.partner',
        'batch_vendor_rel',
        'batch_id', 
        'partner_id',
        string='Vendors'
    )
    project_ids = fields.Many2many('project.project', string='Projects', compute='_compute_projects', store=True)
    transportation_code = fields.Char(string='Transportation Code')
    purchase_count = fields.Integer(string='Purchases', compute='_compute_purchase_count')
    scheduled_date = fields.Date(string='Scheduled Date')
    arrival_date = fields.Date(string='Arrival Date')
    vehicle_type_id = fields.Many2one('vehicle.type', string='Araç Türü')
    airtag_url = fields.Char(string='Airtag URL', compute='_compute_airtag_url', store=True)  
    edespatch_delivery_type = fields.Selection(
        [
            ("edespatch", "E-Despatch"),
            ("printed", "Printed")
        ],
        compute='_compute_edespatch_delivery_type',
        inverse='_inverse_edespatch_delivery_type',
        store=True,
        readonly=False
    )
    driver_ids = fields.Many2many(
        'res.partner',
        'batch_driver_rel',
        'batch_id',
        'partner_id',  
        string='Drivers',
        inverse='_inverse_driver_ids',
        store=True, 
    )

    @api.depends('picking_ids.project_transfer')
    def _compute_projects(self):
        for record in self:
            projects = record.picking_ids.mapped('project_transfer')
            record.project_ids = projects

    def action_show_purchases(self):
        self.ensure_one()
        purchase_ids = []

        # Batch transferin adı ile eşleşen purchase'ları bul
        purchases = self.env['purchase.order'].search([('project_purchase', '=', self.name)])

        for purchase in purchases:
            purchase_ids.append(purchase.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', purchase_ids)],
            'context': {'create': False},
        }

    def _compute_purchase_count(self):
        for batch in self:
            purchases = self.env['purchase.order'].search([
                ('project_purchase', '=', batch.name)
            ])
            batch.purchase_count = len(purchases)

    @api.depends('transportation_code')
    def _compute_airtag_url(self):
        base_url = "https://portal-test.yenaengineering.nl/transfers/"
        for record in self:
            if record.transportation_code:
                record.airtag_url = base_url + record.transportation_code
            else:
                record.airtag_url = False

    @api.onchange('edespatch_date', 'situation', 'arrival_date')
    def _onchange_transfer_related_fields(self):
        for batch in self:
            edespatch_dates = {'edespatch_date': batch.edespatch_date}
            arrival_dates = {'arrival_date': batch.arrival_date}
            situation = {'situation': batch.situation}
            for transfer in batch.picking_ids:
                transfer.write(edespatch_dates)
                transfer.write(situation)
                transfer.write(arrival_dates)

    @api.depends('picking_ids')
    def _compute_edespatch_delivery_type(self):
        for batch in self:
            edespatch_delivery_type = batch.edespatch_delivery_type
            if edespatch_delivery_type:
                batch.picking_ids.write({'edespatch_delivery_type': edespatch_delivery_type})
    def _inverse_edespatch_delivery_type(self):
        for batch in self:
            edespatch_delivery_type = batch.edespatch_delivery_type
            batch.picking_ids.write({'edespatch_delivery_type': edespatch_delivery_type})

    @api.depends('picking_ids.driver_ids')
    def _inverse_driver_ids(self):
        for batch in self:
            driver_ids = batch.driver_ids.ids
            batch.picking_ids.write({'driver_ids': [(6, 0, driver_ids)]})
            
class Picking(models.Model):
    _inherit = 'stock.picking'
    
    edespatch_date = fields.Date(related='batch_id.edespatch_date', store=True, readonly=False)
    arrival_date = fields.Date(related="batch_id.arrival_date", string='Arrival Date')
    project_transfer = fields.Many2many("project.project", string="Project Number")
    transportation_code = fields.Char(related="batch_id.transportation_code", string="Transportation Code")
    situation = fields.Selection(
        [("to_be_planned", "To Be Planned"),
         ("on_the_way", "On The Way"),
         ("arrived", "Arrived")], string="Situation", related="batch_id.situation")
