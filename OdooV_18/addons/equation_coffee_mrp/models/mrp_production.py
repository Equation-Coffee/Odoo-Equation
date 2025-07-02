# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.tools import float_round
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class MRPProduction(models.Model):
    
    _inherit = 'mrp.production'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.depends('bom_id', 'move_raw_ids', 'move_raw_ids.quantity', 'move_raw_ids.product_uom_qty')
    def _compute_bom_price(self):
        self.ensure_one()
        if not self.bom_id or not self.product_id or not self.move_raw_ids:
            self.equation_bom_price = 0

        total = 0
        for move in self.move_raw_ids:
            if self.state == 'draft':
                total += move.product_id.uom_id._compute_price(move.product_id.standard_price, move.product_uom) * move.product_uom_qty
            else:
                total += move.product_id.uom_id._compute_price(move.product_id.standard_price, move.product_uom) * move.quantity

        self.equation_bom_price = total

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self._default_currency_id())
    equation_bom_price = fields.Monetary(string = 'Cost components', compute = "_compute_bom_price", currency_field='currency_id')