from odoo import api, fields, models, _


class ChangeRequestLog(models.Model):
    _inherit = 'project.task.log'
    _name = 'project.change.request.log'
