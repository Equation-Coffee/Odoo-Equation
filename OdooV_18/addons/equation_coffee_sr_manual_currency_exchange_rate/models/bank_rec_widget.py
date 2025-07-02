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

from odoo import _, api, fields, models, tools, Command


class BankRecWidget(models.Model):

    _inherit = 'bank.rec.widget'

    def _lines_widget_recompute_exchange_diff(self):
        self.ensure_one()
        self._ensure_loaded_lines()

        line_ids_commands = []

        # Clean the existing lines.
        for exchange_diff in self.line_ids.filtered(lambda x: x.flag == 'exchange_diff'):
            line_ids_commands.append(Command.unlink(exchange_diff.id))

        new_amls = self.line_ids.filtered(lambda x: x.flag == 'new_aml')
        for new_aml in new_amls:
            # Compute the balance of the line using the rate/currency coming from the bank transaction.
            amounts_in_st_curr = self.st_line_id._prepare_counterpart_amounts_using_st_line_rate(
                new_aml.currency_id,
                new_aml.balance,
                new_aml.amount_currency,
            )
            balance = amounts_in_st_curr['balance']
            if new_aml.currency_id == self.company_currency_id and self.transaction_currency_id != self.company_currency_id:
                # The reconciliation will be expressed using the rate of the statement line.
                balance = new_aml.balance
            elif new_aml.currency_id != self.company_currency_id and self.transaction_currency_id == self.company_currency_id:
                # The reconciliation will be expressed using the foreign currency of the aml to cover the Mexican
                # case.

                # Change by Firefly Sortware Consulting
                # What this change does is that if the source movement sets the manual rate then 
                # it passes it through context so that it takes that rate into account when converting the currency. 
                currency = new_aml.currency_id
                if new_aml.source_aml_move_id and new_aml.source_aml_move_id.apply_manual_currency_exchange and new_aml.source_aml_move_id.active_manual_currency_rate:
                    currency = new_aml.currency_id.with_context(source_aml_move_id = new_aml.source_aml_move_id)
                balance = currency._convert(new_aml.amount_currency, self.transaction_currency_id, self.company_id, self.st_line_id.date)
            # Compute the exchange difference balance.
            exchange_diff_balance = balance - new_aml.balance
            if self.company_currency_id.is_zero(exchange_diff_balance):
                continue

            expense_exchange_account = self.company_id.expense_currency_exchange_account_id
            income_exchange_account = self.company_id.income_currency_exchange_account_id

            if exchange_diff_balance > 0.0:
                account = expense_exchange_account
            else:
                account = income_exchange_account

            line_ids_commands.append(Command.create({
                'flag': 'exchange_diff',
                'source_aml_id': new_aml.source_aml_id.id,

                'account_id': account.id,
                'date': new_aml.date,
                'name': _("Exchange Difference: %s", new_aml.name),
                'partner_id': new_aml.partner_id.id,
                'currency_id': new_aml.currency_id.id,
                'amount_currency': exchange_diff_balance if new_aml.currency_id == self.company_currency_id else 0.0,
                'balance': exchange_diff_balance,
            }))

        if line_ids_commands:
            self.line_ids = line_ids_commands

            # Reorder to put each exchange line right after the corresponding new_aml.
            new_lines = self.env['bank.rec.widget.line']
            for line in self.line_ids:
                if line.flag == 'exchange_diff':
                    continue

                new_lines |= line
                if line.flag == 'new_aml':
                    exchange_diff = self.line_ids\
                        .filtered(lambda x: x.flag == 'exchange_diff' and x.source_aml_id == line.source_aml_id)
                    new_lines |= exchange_diff
            self.line_ids = new_lines