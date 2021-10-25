from odoo import api, fields, models, _


class FunctionalArea(models.Model):
    _name = "project.odoo.function"
    _description = 'Functional Area'

    name = fields.Char(string="Name")
