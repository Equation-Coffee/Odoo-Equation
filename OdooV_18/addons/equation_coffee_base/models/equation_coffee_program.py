# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EquationCoffeeProgram(models.Model):

    _name = 'equation.coffee_program'
    _description = 'Equation Coffee Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.constrains('name')
    def _constrains_name(self):
        for rec in self:
            if self.search_count([('name', '=ilike', rec.name)]) > 1:
                raise ValidationError(
                    _(f"A coffee program with this name {rec.name} already exists. Please contact your administrator."))

    name = fields.Char(string="Name", tracking=True, translate=True)
    equation_coffee_project_ids = fields.Many2many(
        comodel_name="equation.coffee_project", relation="equation_coffee_program_project_rel", column1="coffee_program_id", column2="project_id", string='Projects')
    active = fields.Boolean(string='Active', tracking=True, default=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
