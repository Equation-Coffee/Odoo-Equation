from odoo import fields, models,api
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        for move in self:
            if move.partner_id:
                move.partner_id.last_sale = date.today()