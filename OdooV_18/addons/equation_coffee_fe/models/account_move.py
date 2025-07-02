from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_colombian_company = fields.Boolean(string = 'Is Colombian company?', compute = "_compute_is_colombian_company", default = False)

    def _compute_is_colombian_company(self):
        for rec in self:
            if rec.company_id and rec.company_id.country_id  and rec.company_id.country_id.id == self.env.ref('base.co').id:
                rec.is_colombian_company = True
            else:
                rec.is_colombian_company = False