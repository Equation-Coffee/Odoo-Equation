# -*- coding:utf-8 -*-

import logging

from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    def _get_noveties_by_employeed(self):
        """
            This function allows you to obtain the news that an employee has had during the month in which the payroll is being generated, in addition to verifying that said news are in an approved status.
        """
        return self.env['hr.payroll.novelty'].search([('state', '=', 'accepted'), ('period_start', '<=', self.date_to), ('period_end', '>=', self.date_from), ('employee_id', '=', self.employee_id.id)])


    def _get_vals_inputs(self, accepted_novelties):
        processed_inputs = dict()
        for novelty in accepted_novelties:
            if novelty.input_type_id.id not in processed_inputs:
                processed_inputs[novelty.input_type_id.id] = {'name': novelty.note, 'amount': novelty.payslip_total, 'input_type_id': novelty.input_type_id.id, 'hr_payroll_nolvety_ids': [novelty.id]}
            else:
                processed_inputs[novelty.input_type_id.id]['name'] = processed_inputs[novelty.input_type_id.id].get('name') + ', '+ novelty.note
                processed_inputs[novelty.input_type_id.id]['amount'] = processed_inputs[novelty.input_type_id.id].get('amount') + novelty.payslip_total
                processed_inputs[novelty.input_type_id.id].get('hr_payroll_nolvety_ids').append(novelty.id)
        return processed_inputs
    
    def _set_input_line_ids(self, accepted_novelties):
        """
            This function receives the novelties found for each employee and based on these, a list is created with the creation command to enter the inputs to the payroll.

            @params
                accepted_novelties -> Object of type hr.payroll.novelty with the novelties found for the employee.

            @return
                input_line_vals -> List with the inputs to be created for the payroll

        """
        input_line_vals = list()
        processed_inputs = self._get_vals_inputs(accepted_novelties)
        
        for processed_input in processed_inputs:
            vals = processed_inputs.get(processed_input)
            vals['hr_payroll_nolvety_ids'] = [Command.set(vals.get('hr_payroll_nolvety_ids'))]
            input_line_vals.append(Command.create(vals))
        return input_line_vals

    def _get_input_line_ids(self, accepted_novelties):
        """
            This function returns a list of the novelties to be created.

            @params
                accepted_novelties -> Object of type hr.payroll.novelty with the novelties found for the employee.

            @return
                input_line_vals -> List of commands to create the inputs

        """
        input_line_vals = self._set_input_line_ids(accepted_novelties)
        return input_line_vals
    
    def _create_or_update_input_line_ids(self, accepted_novelties):
        """
            This function allows you to create the inputs based on the novelties.
        """
        input_line_vals = self._get_input_line_ids(accepted_novelties)
            
        if input_line_vals:
            self.update({'input_line_ids': input_line_vals})

    def _call_novelties(self):
        for payslip in self:
            accepted_novelties = payslip._get_noveties_by_employeed()
            if self.input_line_ids and self.input_line_ids.filtered(lambda input: input.hr_payroll_nolvety_ids.ids):
                self.input_line_ids.filtered(lambda input: input.hr_payroll_nolvety_ids.ids).unlink()
            payslip._create_or_update_input_line_ids(accepted_novelties)


    def _get_novelties_by_input(self):
        return self.input_line_ids.filtered(lambda input: input.hr_payroll_nolvety_ids).mapped('hr_payroll_nolvety_ids')

    def _set_state_to_novelties(self, state, payslip_id):
        novelties = self._get_novelties_by_input()
        if novelties:
            novelties.write({'state': state, 'hr_payslip_id': payslip_id})

    def _set_novelties_to_done(self):
        for novelty in self:
            novelty._set_state_to_novelties('done', novelty.id)

    def compute_sheet(self):
        for payslip in self:
            payslip._call_novelties()
        return super().compute_sheet()

    def action_payslip_draft(self):
        res = super(HrPayslip, self).action_payslip_draft()
        for novelty in self:
            novelty._set_state_to_novelties('accepted', False)
        return res
    
    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()
        for novelty in self:
            novelty._set_state_to_novelties('cancelled', False)
        return res

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for payslip in self:
            payslip._set_novelties_to_done()
        return res