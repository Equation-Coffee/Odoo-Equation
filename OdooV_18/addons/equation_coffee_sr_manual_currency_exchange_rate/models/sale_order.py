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


class SalesOrder(models.Model):

    _inherit = 'sale.order'

    manual_currency_exchange_rate = fields.Float(string='Exchange Rate')
    fixing_date_manual_currency_exchange_rate = fields.Date(string = 'Fixing Date', tracking=True)

    def _prepare_invoice(self):
        result = super(SalesOrder, self).with_context(active_manutal_currency=self.apply_manual_currency_exchange)._prepare_invoice()
        result.update({
            'fixing_date_manual_currency_exchange_rate':self.fixing_date_manual_currency_exchange_rate
            })
        return result
