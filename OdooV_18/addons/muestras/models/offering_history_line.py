from odoo import models, fields,api, _
import csv
import os
import logging
from io import BytesIO
from reportlab.pdfgen import canvas


class OfferingLine(models.Model):
    _name = "muestras.offering_history_line"
    _description = "Offering Lines History"
    

    offering_id = fields.Many2one(comodel_name="muestras.offering_history",
        ondelete='cascade',
        required=True,
        index=True,
        copy=False
        )
    
    code = fields.Char(string="Code")
    equation_main_category=fields.Many2one('muestras.offeringcat',string="Main Category")
    equation_origin=fields.Many2one('equation.coffee_origin',string="Origin")
    equation_process_offering=fields.Many2one('equation.coffee_fermentation_process',string="Equation Process Offering")
    equation_varietal=fields.Many2one('equation.coffee_varietal',string="Varietal")
    sca=fields.Float(string="SCA",store=True)
    equation_macroprofile=fields.Many2one('equation.coffee_macroprofile',string="Macroprofile")
    price_fob_usa=fields.Char(string="FOB US/lb")
    price_spot_usa=fields.Char(string="Spot USxlb")
    price_spot_usa_tariffs=fields.Char(string="Spot US/lb")
    price_fwb_usa=fields.Char(string="FWB USD/Lb")
    price_fob_eu=fields.Char(string="FOB EUxkg")
    price_spot_eu=fields.Char(string="Spot EUxkg")
    price_fwb_eu=fields.Char(string="FWB EUxkg")
    price_exw=fields.Char(string="EXW US/lb")
    price_exw_eu=fields.Char(string="EXW EU/kg")
    price_exw_kg=fields.Char(string="EXW US/kg")
    aval_35 = fields.Float(string="Availability in 35 kg ")


