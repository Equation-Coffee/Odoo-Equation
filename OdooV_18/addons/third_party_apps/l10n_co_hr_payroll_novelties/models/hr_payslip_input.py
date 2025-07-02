# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrPayslipInput(models.Model):

    _inherit = 'hr.payslip.input'

    hr_payroll_novelty_id = fields.Many2one(
        comodel_name='hr.payroll.novelty', string='Novelty')

    hr_payroll_nolvety_ids = fields.Many2many(comodel_name="hr.payroll.novelty",
                                                   relation="hr_payslip_input_hr_payroll_novelty_rel", column1="input_id", column2="novelty_id", string="Novelties")