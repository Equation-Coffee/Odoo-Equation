# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    def _compute_is_colombian_company(self):
        for rec in self:
            if rec.company_id and rec.company_id.country_id  and rec.company_id.country_id.id == self.env.ref('base.co').id:
                rec.is_colombian_company = True
            else:
                rec.is_colombian_company = False


    @staticmethod
    def _get_equation_coffee_purchase_type():
        return [('price_in_pesos_per_kilogram', _('Price in pesos per kilogram')), (
        'differential', _('At a differential')), ('price_in_dollars_per_pound', _('Price in dollars per pound'))]

    equation_coffee_currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency', default=lambda self: self.env.ref('base.USD'))

    buy_green_coffee = fields.Boolean(
        string='Buy Green Coffee?', default=False, tracking=True)

    equation_coffee_purchase_type = fields.Selection(selection='_get_equation_coffee_purchase_type', string='Purchase Type', default='price_in_pesos_per_kilogram', tracking=True)

    contract_price_c = fields.Monetary(string = 'Contract price C', currency_field='equation_coffee_currency_id', tracking=True)
    fixing_date_contract_price_c = fields.Date(string = 'Fixing Date', tracking=True)

    price_diferential = fields.Monetary(string = 'Diferential', currency_field='equation_coffee_currency_id', tracking=True)
    fixing_date_price_diferential = fields.Date(string = 'Fixing Date', tracking=True)

    price_in_dollars_per_pound = fields.Monetary(string = 'Price in dollars per pound', currency_field='equation_coffee_currency_id', tracking=True)
    fixing_date_price_in_dollars_per_pound = fields.Date(string = 'Fixing Date', tracking=True)

    is_colombian_company = fields.Boolean(string = 'Is Colombian company?', compute = "_compute_is_colombian_company", default = False)
