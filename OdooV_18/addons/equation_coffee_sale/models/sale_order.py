# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.depends('product_id', 'product_uom')
    def _compute_price_unit(self):
        return super(SaleOrder, self)._compute_price_unit()

       