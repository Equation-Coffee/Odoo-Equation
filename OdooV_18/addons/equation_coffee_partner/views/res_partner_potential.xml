# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EquationCoffeeOrigin(models.Model):

    _name = 'equation.coffee_origin'
    _description = 'Equation Coffee Origin Region'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.constrains('name')
    def _constrains_name(self):
        for rec in self:
            if self.search_count([('name', '=ilike', rec.name)]) > 1:
                raise ValidationError(
                    _(f"An origin with this name {rec.name} already exists. Please contact your administrator."))

    name = fields.Char(string="Name", tracking=True, translate=True)
    active = fields.Boolean(string='Active', tracking=True, default=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
    wizard_offering = fields.Many2many('muestras.offering_pdf_wizard', string="Offering")