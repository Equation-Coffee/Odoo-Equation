from odoo import models,fields, api

class SaleOrderLine(models.Model):
    _inherit='sale.order.line'

    description_sale=fields.Text(string='Descripción')

    ####Comput Fields #####

    @api.onchange('product_template_id')
    def _onchange_description_sale(self):
        if self.product_template_id:
            self.description_sale=self.product_template_id.description_sale

    def _prepare_invoice_line(self, **optional_values):
        invoice_line_vals = super()._prepare_invoice_line(**optional_values)
        invoice_line_vals['description_sale'] = self.description_sale
        invoice_line_vals['product_packaging_id'] = self.product_packaging_id.id
        return invoice_line_vals
    

