# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @staticmethod
    def _get_potential_priority():
        return  [('0', 'Never'),('1', 'Very Low'), ('2', 'Low'), ('3', 'Normal'), ('4', 'High'), ('5', ' Very High')]

    potential_microlot_priority = fields.Selection(selection="_get_potential_priority", string='Potential Microlots', default = '1')
    potential_varietals_priority = fields.Selection(selection="_get_potential_priority", string='Potential Varietals', default = '1')
    potential_volume_priority = fields.Selection(selection="_get_potential_priority", string='Potential Volume', default = '1')