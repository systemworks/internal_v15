from odoo import api, fields, models, _


class InformationLog(models.Model):
    _inherit = 'project.task.log'
    _name = 'project.information.log'
