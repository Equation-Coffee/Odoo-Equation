# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.onchange('equation_coffee_purchase_type', 'buy_green_coffee')
    def _onchange_equation_coffee_currency_id(self):
        for order in self:
            if order.buy_green_coffee and order.company_id and order.company_id.country_id and order.company_id.country_id.id == self.env.ref('base.co').id:
                order.currency_id = self.env.ref('base.COP')
            else:
                order.currency_id = self.env.user.company_id.currency_id.id

    manual_currency_exchange_rate = fields.Float(string='Exchange rate')
    
    fixing_date_manual_currency_exchange_rate = fields.Date(
        string='Fixing Date', tracking=True)

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        if self.company_id.country_id.id == self.env.ref('base.co').id:
            res.update({
                'fixing_date_manual_currency_exchange_rate': self.fixing_date_manual_currency_exchange_rate
            })
        return res

    @api.onchange('company_id', 'currency_id', 'buy_green_coffee', 'equation_coffee_purchase_type')
    def onchange_currency_id(self):
        if self.company_id or self.currency_id:
            if self.company_id.currency_id != self.currency_id:
                self.active_manual_currency_rate = True
            else:
                self.active_manual_currency_rate = False
        elif self.buy_green_coffee and self.equation_coffee_purchase_type != 'price_in_pesos_per_kilogram' and self.company_id.country_id.id == self.env.ref('base.co').id:
            self.active_manual_currency_rate = True
        else:
            self.active_manual_currency_rate = False
