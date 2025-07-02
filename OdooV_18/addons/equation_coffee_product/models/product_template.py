# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_it_coffee = fields.Boolean(
        string='Is it Coffee?')

    is_it_export_coffee = fields.Boolean(
        string='Is it export coffee?')

    equation_coffee_category_id=fields.Many2many(
        'equation.coffee_category'
        ,string="Categorias Offering")

    equation_coffee_project_id = fields.Many2one(
        comodel_name='equation.coffee_project', string='Project', tracking = True)
    equation_coffee_varietal_id = fields.Many2one(
        comodel_name='equation.coffee_varietal', string='Varietal', tracking = True)
    equation_coffee_program_id = fields.Many2one(
        comodel_name='equation.coffee_program', string='Program', domain="[('equation_coffee_project_ids', '=', equation_coffee_project_id)]", tracking = True)
    equation_coffee_drying_process_id = fields.Many2one(
        comodel_name='equation.coffee_drying_process', string='Drying Process', domain="[('equation_coffee_project_ids', '=', equation_coffee_project_id)]", tracking = True)
    equation_coffee_fermentation_process_id = fields.Many2one(
        comodel_name='equation.coffee_fermentation_process', string='Fermentation Process', tracking = True)
