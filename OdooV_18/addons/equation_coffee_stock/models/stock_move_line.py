# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'
    
    @api.depends('lot_id')
    def _compute_get_data(self):
         for rec in self:
             if rec.lot_id:
                if rec.lot_id.equation_coffee_llc_project_lot:
                     rec.equation_coffee_llc_project_lot = rec.lot_id.equation_coffee_llc_project_lot
                if rec.lot_id.equation_coffee_llc_position_lot:
                     rec.equation_coffee_llc_position_lot = rec.lot_id.equation_coffee_llc_position_lot
                if rec.lot_id.lot_container:
                     rec.lot_container = rec.lot_id.lot_container
                if rec.lot_id.description_warehouse:
                     rec.description_warehouse = rec.lot_id.description_warehouse
                
        

    def _compute_is_colombian_company(self):
        for rec in self:
            if rec.company_id and rec.company_id.country_id  and rec.company_id.country_id.id == self.env.ref('base.co').id:
                rec.is_colombian_company = True
            else:
                rec.is_colombian_company = False
                
                
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string='Product template', related='product_id.product_tmpl_id', store=True)

    is_it_coffee = fields.Boolean(
        string='Is it Coffee?', related="product_tmpl_id.is_it_coffee", store=True)

    is_it_export_coffee = fields.Boolean(
        string='Is it export coffee?', related="product_tmpl_id.is_it_export_coffee", store=True)

    equation_coffee_date_production = fields.Date(string='Date of production')

    equation_coffee_profile_id = fields.Many2one(
        comodel_name="equation.coffee_profile", string="Profile", check_company=True)

    equation_coffee_partner_id = fields.Many2one(
        comodel_name="res.partner", string='Producer', check_company=True)

    is_colombian_company = fields.Boolean(string = 'Is Colombian company?', compute = "_compute_is_colombian_company", default = False)
    # Fields To EEUU
    equation_coffee_llc_project_lot = fields.Char(string = 'Project Lot', compute="_compute_get_data", store=True)
    equation_coffee_llc_position_lot = fields.Char(string = 'Position Lot', compute="_compute_get_data", store=True)
    lot_container = fields.Char(string='Lot Container',compute="_compute_get_data", store=True)
    description_warehouse = fields.Char(string='Description Warehouse',compute="_compute_get_data", store=True)
   

    def _get_lot_name_by_project(self):
        sequence_code = self.product_tmpl_id.equation_coffee_project_id.sequence_id.code
        return self.env['ir.sequence'].with_company(self.product_tmpl_id.equation_coffee_project_id.company_id).next_by_code(sequence_code)

    def _get_value_production_lot(self):
        res = super()._get_value_production_lot()
        if self.is_it_coffee:

            coffee_profile = self.equation_coffee_profile_id

            if coffee_profile:
                res.update({
                    'equation_coffee_profile_id': self.equation_coffee_profile_id.id
                })          

            if not self.is_colombian_company:
                res.update({
                    'equation_coffee_llc_project_lot': self.equation_coffee_llc_project_lot,
                    'equation_coffee_llc_position_lot': self.equation_coffee_llc_position_lot,
                    'lot_container' : self.lot_container,
                    'description_warehouse' : self.description_warehouse,
                    
                })   

            res.update({
                'equation_coffee_date_production': self.equation_coffee_date_production,
                'equation_coffee_partner_id': self.equation_coffee_partner_id.id
            })
        return res
