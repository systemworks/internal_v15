from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Project(models.Model):
    _inherit = "project.project"




class Task(models.Model):
    _inherit = "project.task"

    billing_type = fields.Selection([
        ('parent', 'Parent'),
        ('sub_task', 'Sub-Task'), ], string="Billing Type")
    task_type_id = fields.Many2one('project.task.subtype', string="Task Type")
    related_module = fields.Many2one('project.odoo.module', string="Related Module")
    functional_area = fields.Many2one('project.odoo.function', string="Functional Area")
    billing_status = fields.Selection([
        ('to bill', 'To Bill'),
        ('billed', 'Billed')], string="Billing Status")


    @api.onchange('parent_id')
    def on_change(self):
        if self.parent_id != False:
            self.billing_type = 'sub_task'

    @api.constrains('name')
    def _check_name_field(self):
        if len(self.name) > 50:
            raise ValidationError('Number of characters must not exceed 50')