# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning

_logger = logging.getLogger(__name__)

class L10ncoExogenousConcept(models.Model):
    _name = "l10n_co.exogenous_concept"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Template for the creation of exogenous information concepts"
    _rec_name = 'code'

    def name_get(self):
        result = []
        for rec in self:
            concept_name = rec.name
            if len(concept_name) > 100:
                concept_name = concept_name[0:100] + '...'
            name = f'[{rec.code}] {concept_name}'
            result.append((rec.id, name))
        return result

    name = fields.Text(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True, size=4)
    format_id = fields.Many2one(comodel_name='l10n_co.exogenous_format', string='Format', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
    report_with_informan_nit = fields.Boolean(string="Report with the informant\'s nit?", default=False)