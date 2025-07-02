# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EquationCoffeeSCAScore(models.Model):

    _name = 'equation.coffee_sca_score'
    _description = 'Equation Coffee SCA Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "lot_id"

    date = fields.Date(string="Date", tracking=True)
    score = fields.Float(string='Score', tracking=True)
    lot_id = fields.Many2one(comodel_name="stock.lot", string='Lot', check_company=True)

    product_id = fields.Many2one(comodel_name="product.product",
                                 string='Product', related="lot_id.product_id", store=True)
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string='Product template', related='product_id.product_tmpl_id', store=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
