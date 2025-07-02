# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.depends('name', 'product_id')
    def _compute_other_description(self):
        for line in self:
            if not line.name or line.display_type:
                line.other_description = line.name
                continue
                
            country_code = self.env.company.country_id.code
            line.other_description = line.name
            product_name = ""
            if line.product_id:
                product_name = line.product_id.display_name
                
            if country_code != 'CO'  and product_name in line.name:
                line.other_description = line.name.replace(line.product_id.display_name, "")

    other_description = fields.Text(string='Otro Nombre', compute="_compute_other_description", help="Other description of the product")

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        country_code = self.env.company.country_id.code
        if country_code == 'CO':
            return res
        if res.get('name', False):
            res['name'] = self.env['account.move.line']._get_journal_items_full_name(self.other_description, False)
        return res
