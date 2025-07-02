from odoo import api, fields, models, _

class ResPartnerPurchaseHistory(models.Model):
    _name='res.partner_purchase_history'
    _description='Historico de compras por cliente'
    

    partner=fields.Many2one('res.partner',string="Customer")
    city=fields.Char(string="City")
    country=fields.Char(string="Country")

    date=fields.Date(string="Date")

    project=fields.Char(string="Project")
    program=fields.Char(string="Program")
    category=fields.Char(string="Category")
    varietal=fields.Char(string="Variety")
    process=fields.Char(string="Process")

    sales_person=fields.Char(string="Commercial")
    commercial_region=fields.Char(string="Commercial Region")
    sale_type=fields.Char(string="Sale Type")
    quantity_lb=fields.Float(string="LB")
    quantity_kg=fields.Float(string="KG")
    price_lb_usd=fields.Float(string="Price x LB USD")
    total_purchase=fields.Float(string="Total Purchase")
    edition=fields.Char(string="Edition")
    warehouse=fields.Char(string="Bodega")

