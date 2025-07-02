from odoo import models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def action_open_commission_report_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Informe de Comisiones',
            'res_model': 'commission.report.wizard',
            'view_mode': 'form',
            'target': 'new',
        }