# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, _, api

_logger = logging.getLogger(__name__)

class L10ncoExogenousFormatFieldsAccount(models.Model):
    _name = "l10n_co.exogenous_format_field_account"

    @staticmethod
    def _get_accumulated():
        return [('balance', _('Net')), (
        'credit', _('Credit')), ('debit', _('Debit')),(
        'tax_base_amount', _('Base')), ('closing_balance', _('Closing Balance'))]
    
    @api.depends('format_field_id')
    def _get_format_applies_concepts(self):
        for rec in self:
            if rec.format_field_id.source != 'journal_items' or not rec.format_field_id.format_applies_concepts:
                rec.format_applies_concepts = False
            else:
                rec.format_applies_concepts = True

    name = fields.Selection(string='Accumulated by', selection="_get_accumulated", default='balance')
    account_ids = fields.Many2many(comodel_name='account.account', string='Accounts')
    concept_id = fields.Many2one(comodel_name="l10n_co.exogenous_concept", string='Concept')
    
    format_field_id = fields.Many2one(comodel_name="l10n_co.exogenous_format_field", string='Format Field')
    format_applies_concepts = fields.Boolean(string='Apply Concepts', compute='_get_format_applies_concepts', readonly=True)