# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class StockMove(models.Model):

    _inherit = 'stock.move'

    def _compute_is_colombian_company(self):
        for rec in self:
            if rec.company_id and rec.company_id.country_id  and rec.company_id.country_id.id == self.env.ref('base.co').id:
                rec.is_colombian_company = True
            else:
                rec.is_colombian_company = False

    is_it_coffee = fields.Boolean(
        string='Is it Coffee?', related="product_tmpl_id.is_it_coffee", store=True)
    
    is_it_export_coffee = fields.Boolean(
        string='Is it export coffee?', related="product_tmpl_id.is_it_export_coffee", store=True)

    is_colombian_company = fields.Boolean(string = 'Is Colombian company?', compute = "_compute_is_colombian_company", default = False)

    def get_lot_name_by_project(self):
        for sml in self.move_line_ids:
            if sml.move_id.is_it_coffee and not sml.lot_name:
                sml.lot_name = sml._get_lot_name_by_project()