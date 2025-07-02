# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from typing import Sequence

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EquationCoffeeProject(models.Model):

    _name = 'equation.coffee_project'
    _description = 'Equation Coffee Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.constrains('name', 'code')
    def _constrains_name(self):
        for rec in self:
            if self.search_count([('name', '=ilike', rec.name), ('code', '=ilike', rec.code)]) > 1:
                raise ValidationError(
                    _(f"A project with this name {rec.name} and code {rec.code} already exists. Please contact its administrator."))


    @api.depends('name', 'code')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = '['+record.code+']' + ' ' + name
            res.append((record.id, name))
        return res


    name = fields.Char(string="Name", tracking=True, translate=True)
    code = fields.Char(string="Code", tracking=True, translate=True)
    sequence_id = fields.Many2one(comodel_name='ir.sequence', string = 'Sequence')
    
    active = fields.Boolean(string='Active', tracking=True, default=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
