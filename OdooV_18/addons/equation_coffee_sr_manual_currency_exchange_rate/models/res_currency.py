# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company=None, date=None):
        super(ResCurrency, self)._get_conversion_rate(from_currency, to_currency, company, date)
        company = company or self.env.company
        date = date or fields.Date.context_today(self)
        if from_currency == to_currency:
            return 1
        elif self._context.get('active_manual_currency_rate') and self._context.get('manual_rate') > 0:
            res = (1 / self._context.get('manual_rate'))
            return res
        elif self._context.get('source_aml_move_id', False) and self._context.get('source_aml_move_id').apply_manual_currency_exchange and self._context.get('source_aml_move_id').manual_currency_exchange_rate > 0:
            currency_rates = (from_currency + to_currency)._get_rates(company, date)
            res = currency_rates.get(to_currency.id) / (currency_rates.get(to_currency.id) / self._context.get('source_aml_move_id').manual_currency_exchange_rate)
            return res
        else:
            return from_currency.with_company(company).with_context(to_currency=to_currency.id, date=str(date)).inverse_rate

