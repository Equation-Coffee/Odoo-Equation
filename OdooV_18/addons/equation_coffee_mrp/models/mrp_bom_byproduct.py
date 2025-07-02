# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class MrpByProduct(models.Model):

    _inherit = 'mrp.bom.byproduct'

    cost_share = fields.Float(digits="Equation Coffee Cost Share")