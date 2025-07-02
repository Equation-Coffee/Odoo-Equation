from odoo import fields, models,api

class AccountIncoterms(models.Model):
    _inherit = 'account.move.line'

    description_sale=fields.Text(string="Etiqueta")
    packaging_lots = fields.Many2one('x_empaque',string="Packaging")
    product_packaging_id = fields.Many2one('product.packaging',string="Embalaje")

    @api.onchange('product_id')
    def _onchange_description_sale(self):
        if self.product_id:
            self.description_sale=self.product_id.product_tmpl_id.description_sale
