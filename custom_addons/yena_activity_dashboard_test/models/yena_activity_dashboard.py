from odoo import api, fields, models

class ScheduledActivityReport(models.Model):
    _name = 'scheduled.activity.report'
    _description = 'Scheduled Activity Report'

    name = fields.Char('Activity Summary')
    due_date = fields.Date('Due Date')
    user_id = fields.Many2one('res.users', 'Responsible')
    note = fields.Html('Notes')

    @api.model
    def get_scheduled_activities(self):
        activities = self.env['mail.activity'].search([('date_deadline', '<=', fields.Date.today())])
        for activity in activities:
            self.create({
                'name': activity.summary,
                'due_date': activity.date_deadline,
                'user_id': activity.user_id.id,
                'note': activity.note,
            })

