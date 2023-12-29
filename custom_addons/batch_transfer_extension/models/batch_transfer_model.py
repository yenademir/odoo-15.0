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
        'batch_customer_rel'
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
    purchase_count = fields.Integer(string='Purchases', compute='_compute_purchase_count')
    scheduled_date = fields.Date(string='Scheduled Date')
    arrival_date = fields.Date(string='Arrival Date')
    vehicle_type_id = fields.Many2one('vehicle.type', string='Araç Türü')
    airtag_url = fields.Char(string='Airtag URL', compute='_compute_airtag_url', store=True)
    transportation_code = fields.Char(string='Transportation Code')
    import_decleration_number = fields.Char(string='Custom Decleration No', inverse='_inverse_import_decleration_number', store=True)
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
            # Her bir picking kaydındaki project_transfer alanını topla
            projects = record.picking_ids.mapped('project_transfer')
            # Many2many alanına bu projelerin ID'lerini ata
            project_ids = projects.ids if projects else []
            record.project_ids = [(6, 0, project_ids)]



    def action_show_purchases(self):
        self.ensure_one()
        purchase_ids = []

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
                ('project_purchase', '=', batch.project_ids.ids)
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

    @api.onchange('edespatch_date', 'situation', 'arrival_date', 'import_decleration_number')
    def _onchange_transfer_related_fields(self):
        for batch in self:
            edespatch_dates = {'edespatch_date': batch.edespatch_date}
            arrival_dates = {'arrival_date': batch.arrival_date}
            situation = {'situation': batch.situation}
            import_decleration_number = {'import_decleration_number': batch.import_decleration_number}
            for transfer in batch.picking_ids:
                transfer.write(edespatch_dates)
                transfer.write(situation)
                transfer.write(arrival_dates)
                transfer.write(import_decleration_number)

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

    def _inverse_import_decleration_number(self):
        for batch in self:
            # Batch modelindeki import_decleration_number değeri değiştiğinde, bu değeri tüm ilişkili picking kayıtlarına yaz.
            if batch.import_decleration_number:
                batch.picking_ids.write({'import_decleration_number': batch.import_decleration_number})

    @api.depends('picking_ids.driver_ids')
    def _inverse_driver_ids(self):
        for batch in self:
            driver_ids = batch.driver_ids.ids
            batch.picking_ids.write({'driver_ids': [(6, 0, driver_ids)]})


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    project_ids = fields.Many2one('project.project', string='Projects', compute='_compute_project_transfer', store=True)

    @api.depends('picking_id.project_transfer')
    def _compute_project_transfer(self):
        for record in self:
            record.project_ids = record.picking_id.project_transfer
            
class Picking(models.Model):
    _inherit = 'stock.picking'
    edespatch_date = fields.Date(related='batch_id.edespatch_date', store=True, readonly=False)
    arrival_date = fields.Date(related="batch_id.arrival_date", string='Arrival Date')
    project_transfer = fields.Many2one("project.project", string="Project Number")
    situation = fields.Selection(
        [("to_be_planned", "To Be Planned"),
         ("on_the_way", "On The Way"),
         ("arrived", "Arrived")], string="Situation", related="batch_id.situation")