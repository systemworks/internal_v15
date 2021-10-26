from odoo import api, fields, models, _


class RiskLog(models.Model):
    _inherit = 'project.task.log'
    _name = 'project.risk.log'
