# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning

_logger = logging.getLogger(__name__)

class L10ncoExogenousContactField(models.Model):
    _name = "l10n_co.exogenous_contact_field"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Template for contact field mapping for exogenous reporting"
    _rec_name = 'company_id'
    
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)

    field_line_ids = fields.One2many(comodel_name='l10n_co.exogenous_contact_field_line', inverse_name='contact_field_id', string='Fields')
