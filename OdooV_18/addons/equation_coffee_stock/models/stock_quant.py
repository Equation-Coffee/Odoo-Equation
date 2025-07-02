# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_container = fields.Char(string='Lot Container', related='lot_id.lot_container')
    description_warehouse = fields.Char(string='Description Warehouse', related='lot_id.description_warehouse')
    equation_coffee_llc_project_lot = fields.Char(string='Project Lot', related='lot_id.equation_coffee_llc_project_lot')
    equation_coffee_llc_position_lot = fields.Char(string='Position Lot', related='lot_id.equation_coffee_llc_position_lot')