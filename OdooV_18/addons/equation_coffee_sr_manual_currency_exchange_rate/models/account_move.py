# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from functools import lru_cache
from contextlib import contextmanager

from odoo import models, fields, api


class AccountMove(models.Model):

    _inherit = 'account.move'

    manual_currency_exchange_rate = fields.Float(string='Exchange rate')
    fixing_date_manual_currency_exchange_rate = fields.Date(string = 'Fixing Date', tracking=True)