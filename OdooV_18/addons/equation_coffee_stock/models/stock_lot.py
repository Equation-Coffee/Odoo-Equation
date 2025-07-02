# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class StockLot(models.Model):

    _inherit = 'stock.lot'

    equation_coffee_harvest_year = fields.Char(string='Harvest Year')
    packing_lot=fields.Many2one('equation.coffee_lot_package',string="Empaquetado")



    def _compute_is_colombian_company(self):
        for rec in self:
            if rec.company_id and rec.company_id.country_id  and rec.company_id.country_id.id == self.env.ref('base.co').id:
                rec.is_colombian_company = True
            else:
                rec.is_colombian_company = False

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            if rec.equation_coffee_year and rec.is_it_export_coffee:
                year = rec.equation_coffee_year
                name = f'{name} - {year}'
            result.append((rec.id, name))
        return result

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string='Product template', related='product_id.product_tmpl_id', store=True)

    equation_coffee_date_production = fields.Date(
        string='Date of production', tracking=True)

    equation_coffee_sca_score_ids = fields.One2many(
        comodel_name="equation.coffee_sca_score", inverse_name="lot_id", string="SCA Score", check_company=True)

    is_it_coffee = fields.Boolean(
        string='Is it Coffee?', related="product_tmpl_id.is_it_coffee", store=True)

    is_it_export_coffee = fields.Boolean(
        string='Is it export coffee?', related="product_tmpl_id.is_it_export_coffee", store=True)

    equation_coffee_profile_id = fields.Many2one(
        comodel_name="equation.coffee_profile", string="Profile", tracking=True, check_company=True)
    equation_coffee_partner_id = fields.Many2one(
        comodel_name="res.partner", string='Producer', tracking=True, check_company=True)
    equation_coffee_data_sheet = fields.Binary(
        string='Data Sheet', attachment=True, tracking=True)
    equation_coffee_data_sheet_name = fields.Char(string='Data Sheet Name')

    equation_coffee_project_id = fields.Many2one(
        comodel_name='equation.coffee_project', string='Project', related="product_tmpl_id.equation_coffee_project_id", store=True)

    equation_coffee_varietal_id = fields.Many2one(
        comodel_name='equation.coffee_varietal', string='Varietal', related="product_tmpl_id.equation_coffee_varietal_id", store=True)

    equation_coffee_program_id = fields.Many2one(
        comodel_name='equation.coffee_program', string='Program', related="product_tmpl_id.equation_coffee_program_id", store=True)

    equation_coffee_drying_process_id = fields.Many2one(
        comodel_name='equation.coffee_drying_process', string='Drying Process', related="product_tmpl_id.equation_coffee_drying_process_id", store=True)

    equation_coffee_fermentation_process_id = fields.Many2one(
        comodel_name='equation.coffee_fermentation_process', string='Fermentation Process', related="product_tmpl_id.equation_coffee_fermentation_process_id", store=True)

    equation_coffee_year = fields.Char(string = 'Year ICO', default = '2024', size=4)

    is_colombian_company = fields.Boolean(string = 'Is Colombian company?', compute = "_compute_is_colombian_company", default = False)

    # Fields To EEUU
    equation_coffee_llc_project_lot = fields.Char(string = 'Project Lot')
    equation_coffee_llc_position_lot = fields.Char(string = 'Position Lot')
    lot_container = fields.Char(string='Lot Container')
    description_warehouse = fields.Char(string='Description Warehouse')
   