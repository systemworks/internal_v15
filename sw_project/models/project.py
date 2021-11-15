from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Project(models.Model):
    _inherit = "project.project"
    deployment_id = fields.Many2one("project.project", string="Deployment")

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        if self._context.get('deployment_id'):
            res.deployment_id=self._context.get('deployment_id')
            if self._context.get('task_id'):
                task=self.env['project.task'].browse([self._context.get('task_id')])
                newTask=task.copy()
                newTask.name=task.name
                newTask.project_id=res.id
        return res


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
    task_code = fields.Char(string="Task Code", readonly=True)
    git_commit_id = fields.Char(string="Commit Hash", tracking=True)

    task_log_id = fields.One2many('project.task.log', 'related_task_id', string='Task Log ID')
    task_log_count = fields.Integer(
        string='Task Log Count',
        compute='_task_log_count'
    )

    deployed_indicator = fields.Boolean(string="Deployed", tracking=True)

    @api.model
    def create(self, vals):
        res = super(Task, self).create(vals)
        seq_no = self.env['ir.sequence'].next_by_code('project.task')
        res.write({
            'task_code': seq_no,
        })
        return res

    @api.onchange('parent_id')
    def on_change(self):
        if self.parent_id != False:
            self.billing_type = 'sub_task'

    @api.constrains('name')
    def _check_name_field(self):
        if len(self.name) > 50:
            raise ValidationError('Number of characters must not exceed 50')

    @api.depends('task_log_id')
    def _task_log_count(self):
        for partner in self:
            partner.task_log_count = len(partner.task_log_id)

    ##def deploy_button_action(self):
     ##   action = self.env["ir.actions.actions"]._for_xml_id("project.edit_project")
      ##  action['context'] = {'default_project_id': active_id}
       # return action

    def deploy_button_action(self):
        view = self.env.ref('project.edit_project')

        project_deployment = self.env['project.project'].sudo().search([
            ('deployment_id', '=', self.project_id.id)
        ])
        if not project_deployment:
            return {
                'name': _('Project'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.project',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'main',
                'context':{'deployment_id':self.project_id.id,'task_id':self.id, 'default_deployed_indicator':True},
            }
        else:
            newTask=self.copy()
            newTask.name=self.name
            newTask.project_id=project_deployment.id

            return {
                'name': _('Project'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.project',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'main',
                'res_id':project_deployment.id
            }

