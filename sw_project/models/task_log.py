from odoo import api, fields, models, _
from datetime import datetime


class TaskLog(models.AbstractModel):
    _name = 'project.task.log'

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    related_task = fields.Many2one('project.task', string="Related Task", required=True)
    logged_by = fields.Many2one('res.partner',
                                string='Logged By',
                                required=True)
    logged_on = fields.Date(String="Logged On", default=fields.Date.today())
    log_source = fields.Char(string="Log Source")
    related_meeting = fields.Char(string="Related Meeting")
