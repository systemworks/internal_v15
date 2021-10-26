from odoo import api, fields, models, _


class DecisionLog(models.Model):
    _inherit = 'project.task.log'
    _name = 'project.decision.log'
