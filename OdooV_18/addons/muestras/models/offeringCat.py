from odoo import models, fields, api

class OfferingCategory(models.Model):
    _name="muestras.offeringcat"
    _description="Categorias Offering"

    name=fields.Char(string="Category Name")
    price_spot_adjustment=fields.Float(string="Precio Adicional SPOT")   ### Campo a borrar
    category_margin=fields.Float(string="Category Margin")
    category_margin_spot=fields.Float(string="Category Margin SPOT")
    disponible=fields.Many2many(
        'muestras.disponible',
        string="Modelos"
    )
    code=fields.Char(string="code")

    spot_eu=fields.Many2many(
        'muestras.spoteu',
        string="SPOT_EU"
    )

    inventario=fields.Many2many(
        'muestras.inventario',
        string="Inventario"
    )

        
    allproducts=fields.Many2many(
        'muestras.allproducts',
        string="All products"
    )

    atlas=fields.Many2many(
        'muestras.prueba',
        string="Atlas"
    )

    wizard_offering=fields.Many2many(
        'muestras.offering_pdf_wizard',
        string="Offering"
    )