# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning

_logger = logging.getLogger(__name__)

class L10ncoExogenousContactFieldLine(models.Model):
    _name = "l10n_co.exogenous_contact_field_line"
    _description = "Template for configuring Odoo fields with exogenous ones"

    field_odoo_id = fields.Many2one(comodel_name='ir.model.fields', string='Odoo Field')
    field_odoo_internal_id = fields.Many2one(comodel_name='ir.model.fields', string='Odoo relational field', domain="[('model', '=', relation), ('ttype', 'not in', ('many2one' , 'one2many', 'many2many'))]")
    field_format_id = fields.Many2one(comodel_name='l10n_co.exogenous_format_field', string='Field Format')
    contact_field_id = fields.Many2one(comodel_name='l10n_co.exogenous_contact_field', string='Contact Field')

    ttype = fields.Selection(related='field_odoo_id.ttype', readonly=True)
    relation = fields.Char(related='field_odoo_id.relation', readonly=True)
