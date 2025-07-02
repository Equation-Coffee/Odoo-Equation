# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PayrollNovelties(models.Model):
    _name = 'hr.payroll.novelty'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Novedades de Nómina'
    _rec_name = 'employee_id'

    @api.constrains('period_start', 'period_end')
    def _check_period_dates(self):
        for record in self:
            if record.period_start >= record.period_end:
                raise ValidationError(
                    "The start date must be before the end date.")

    @api.depends('employee_id')
    def _compute_company_id(self):
        for novelty in self.filtered(lambda p: p.employee_id):
            novelty.company_id = novelty.employee_id.company_id

    @api.constrains('payslip_total')
    def _check_payslip_total(self):
        for novelty in self:
            if novelty.payslip_total <= 0:
                raise ValidationError(_('Must have an amount greater than zero.'))


    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee', readonly=True,
        states={'draft': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id), '|', ('active', '=', True), ('active', '=', False)]",
        tracking=True)

    period_start = fields.Date(
        string='Period start', tracking=True, readonly=True, states={'draft': [('readonly', False)]})

    period_end = fields.Date(string='Period end', tracking=True,
                             readonly=True, states={'draft': [('readonly', False)]})

    input_type_id = fields.Many2one(
        comodel_name='hr.payslip.input.type', string='Concept', tracking=True,
        readonly=True, states={'draft': [('readonly', False)]})

    payslip_total = fields.Float(
        string='Total Payslip', tracking=True,
        readonly=True, states={'draft': [('readonly', False)]})

    note = fields.Char(
        string='Note',
        readonly=True,
        states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), (
        'accepted', 'Accepted'), ('done', 'Done'), ('cancelled', 'Cancelled')], string='State', default='draft', tracking=True)

    hr_payslip_id = fields.Many2one(
        comodel_name='hr.payslip', string='Payslip', tracking=True)

    company_id = fields.Many2one(
        'res.company', string='Company', copy=False,
        compute='_compute_company_id', store=True, readonly=False,
        default=lambda self: self.env.company,
        states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})

    country_id = fields.Many2one(
        'res.country', string='Country',
        related='company_id.country_id', readonly=True
    )

    country_code = fields.Char(related='country_id.code', depends=[
                               'country_id'], readonly=True)


    def action_comfirm(self):
        for novelty in self:
            novelty.write({'state': 'confirmed'})

    def action_approve(self):
        for novelty in self:
            novelty.write({'state': 'accepted'})

    def action_draft(self):
        for novelty in self:
            novelty.write({'state': 'draft'})