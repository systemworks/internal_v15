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
    task_code = fields.Char(string="Task Code", compute='compute_sequence_task', readonly=True)
    git_commit_id = fields.Char(string="Commit Hash")

    bug_log_id = fields.One2many('project.task.bug.log', 'related_task', string='Bug Log ID')
    bug_log_count = fields.Integer(
        string='Bug Log Count',
        compute='_bug_log_count'
    )
    change_request_log_id = fields.One2many('project.change.request.log', 'related_task', string='Change Request ID')
    change_request_log_count = fields.Integer(
        string='Change Request Count',
        compute='_change_request_log_count'
    )
    risk_log_id = fields.One2many('project.risk.log', 'related_task', string='Risk Log ID')
    risk_log_count = fields.Integer(
        string='Risk Log Count',
        compute='_risk_log_count'
    )
    decision_log_id = fields.One2many('project.decision.log', 'related_task', string='Decision Log ID')
    decision_log_count = fields.Integer(
        string='Decision Log Count',
        compute='_decision_log_count'
    )
    information_log_id = fields.One2many('project.information.log', 'related_task', string='Information Log ID')
    information_log_count = fields.Integer(
        string='Information Log Count',
        compute='_information_log_count'
    )

    def compute_sequence_task(self):
        for task in self:
            seq_no = self.env['ir.sequence'].next_by_code('project.task')
            task.write({
                'task_code': seq_no,
            })
        return True

    @api.onchange('parent_id')
    def on_change(self):
        if self.parent_id != False:
            self.billing_type = 'sub_task'

    @api.constrains('name')
    def _check_name_field(self):
        if len(self.name) > 50:
            raise ValidationError('Number of characters must not exceed 50')

    @api.depends('bug_log_id')
    def _bug_log_count(self):
        for partner in self:
            partner.bug_log_count = len(partner.bug_log_id)

    @api.depends('change_request_log_id')
    def _change_request_log_count(self):
        for partner in self:
            partner.change_request_log_count = len(partner.change_request_log_id)

    @api.depends('risk_log_id')
    def _risk_log_count(self):
        for partner in self:
            partner.risk_log_count = len(partner.risk_log_id)

    @api.depends('decision_log_id')
    def _decision_log_count(self):
        for partner in self:
            partner.decision_log_count = len(partner.decision_log_id)

    @api.depends('information_log_id')
    def _information_log_count(self):
        for partner in self:
            partner.information_log_count = len(partner.information_log_id)