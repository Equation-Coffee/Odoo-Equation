# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class AccountMove(models.Model):

    _inherit = 'account.move'

    equation_coffee_qty = fields.Char(string = 'Quantity', tracking=True)
    equation_coffee_country_ori = fields.Char(string = 'Country of origin', tracking=True)

    equation_coffee_loading_port = fields.Char(string = 'Origin', tracking=True)
    equation_coffee_destination_port = fields.Char(string = 'Destination', tracking=True)
    equation_coffee_shipping_line = fields.Char(string = 'Shipping Line /  Carrier', tracking=True)
    equation_coffee_bill_lading = fields.Char(string = 'BL / AWB Number', tracking=True)
    equation_coffee_hs_code = fields.Char(string = 'HS code', tracking=True)
    equation_coffee_reference = fields.Char(string = 'Reference', tracking=True) 
