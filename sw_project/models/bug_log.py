from odoo import api, fields, models, _


class TaskBugLog(models.Model):
    _inherit = 'project.task.log'
    _name = 'project.task.bug.log'
