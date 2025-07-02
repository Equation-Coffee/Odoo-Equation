# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EquationCoffeeVarietal(models.Model):

    _name = 'equation.coffee_sca'
    _description = 'Equation Coffee SCA Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.constrains('name')
    def _constrains_name(self):
        for rec in self:
            if self.search_count([('name', '=ilike', rec.name)]) > 1:
                raise ValidationError(
                    _(f"A score with this name {rec.name} already exists. Please contact your administrator."))

    name = fields.Char(string="Score", tracking=True, translate=True)
    active = fields.Boolean(string='Active', tracking=True, default=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
