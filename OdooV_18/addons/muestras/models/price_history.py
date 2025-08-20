from odoo import models, fields, api
from datetime import date

class Price(models.Model):
    _name = "muestras.price_history"
    _description = "Precios Productos Disponibles"

    price_id = fields.Many2one('muestras.price',string="Price Indicator")
    name = fields.Char(string="Price Indicator")
    value = fields.Float(string="Value")
    execution_time = fields.Datetime(string="Execution Time")


# zjXLSp_3Z5pDxzFkqiYf
    