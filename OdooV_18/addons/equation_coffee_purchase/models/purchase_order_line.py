import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'


    product_packaging = fields.Selection([],string="Empaque")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            lots=self.env['stock.lot'].search([('product_id','=',self.product_id.id)])
            packagings=list(set(lots.mapped('packing_lot')))
            self._fields['product_packaging'].selection=[(str(p),p) for p in packagings]
            self.product_packaging=False
        else:
            self._fields['product_packaging'].selection=[]


