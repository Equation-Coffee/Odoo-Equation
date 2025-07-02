from odoo import models, fields, api

class OfferingCategory(models.Model):
    _name="muestras.feedback"
    _description="Categorias Feedback"

    name=fields.Char(string="Feedback Option")
    order_line=fields.Many2many(
        'muestras.order.line',
        string="Order_line"
    )
    code=fields.Char(string="code")

    wizard_line=fields.Many2many(
        'muestras.wizard_sale.line',
        string="Wizard"
    )

