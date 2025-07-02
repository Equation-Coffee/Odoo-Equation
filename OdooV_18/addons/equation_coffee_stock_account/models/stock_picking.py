# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):

    _inherit = 'stock.picking'
    
    equation_coffee_harvest_year = fields.Char(string="Harvest Year")
    packaging_lots = fields.Many2one('x_empaque',string="Packaging")

    is_colombian_company = fields.Boolean(
        string='Is Colombian Company?',
        compute='_compute_is_colombian_company',
        store=True
    )


    def _prepare_new_lot_vals(self):
        self.ensure_one()
        vals = super()._prepare_new_lot_vals()

        vals.update({
            'equation_coffee_partner_id':self.equation_coffee_partner_id.id,
            'equation_coffee_harvest_year':self.equation_coffee_harvest_year,
            'x_empaquetadom':self.packaging_lots.id,
            
        })

        return vals

    @api.depends('company_id')
    def _compute_is_colombian_company(self):
        colombian_country_id = self.env.ref('base.co').id
        for rec in self:
            rec.is_colombian_company = rec.company_id.country_id.id == colombian_country_id


    @api.constrains('equation_coffee_gross_weight')
    def _constrains_equation_coffee_gross_weight(self):
        for rec in self:
            if rec.equation_coffee_gross_weight < 0:
                raise ValidationError(
                    _("Gross weight should be greater than zero"))


    @api.constrains('equation_coffee_net_weight')
    def _constrains_equation_coffee_net_weight(self):
        for rec in self:
            if rec.equation_coffee_net_weight < 0:
                raise ValidationError(
                    _("Net weight should be greater than zero"))



    equation_coffee_qty = fields.Char(string='Quantity')
    equation_coffee_loading_port = fields.Char(string='Origin')
    equation_coffee_destination_port = fields.Char(
        string='Destination')
    equation_coffee_shipping_line = fields.Char(string='Shipping Line / Carrier')
    equation_coffee_bill_lading = fields.Char(string='Bill of lading')
    equation_coffee_hs_code = fields.Char(string='HS code')
    equation_coffee_reference = fields.Char(string='Reference')
    equation_coffee_vessel = fields.Char(string='Vessel', tracking=True)
    equation_coffee_bl_number = fields.Char(string='BL / AWB Number', tracking=True)
    additional_instructions = fields.Char(string='Additional Instructions', tracking=True)

    equation_coffee_gross_weight = fields.Float(
        string='Gross Weight', tracking=True)
    equation_coffee_gross_weight_uom_id = fields.Many2one(comodel_name='uom.uom', string='Uom Gross Weight', tracking=True, domain=lambda self: [
                                                          ('categoty_id', '=', self.env.ref('uom.product_uom_categ_kgm').id)],
                                                          default=lambda self: self.env.ref('uom.product_uom_kgm'))
    equation_coffee_net_weight = fields.Float(
        string='Net Weight', tracking=True)
    equation_coffee_net_weight_uom_id = fields.Many2one(comodel_name='uom.uom', string='Uom Net Weight', tracking=True, domain=lambda self: [
                                                        ('categoty_id', '=', self.env.ref('uom.product_uom_categ_kgm').id)],
                                                        default=lambda self: self.env.ref('uom.product_uom_kgm'))

    def get_values_from_invoices(self):

        for rec in self:

            if rec.move_ids_without_package:

                invoices = rec.mapped('move_ids_without_package').mapped(
                    'sale_line_id').mapped('invoice_lines').mapped('move_id')
               
                if invoices:

                    invoice = invoices.sorted(lambda inv: inv.id, reverse = True)[0]

                    if invoice.equation_coffee_qty:
                        rec.equation_coffee_qty = invoice.equation_coffee_qty

                    if invoice.equation_coffee_loading_port:
                        rec.equation_coffee_loading_port = invoice.equation_coffee_loading_port

                    if invoice.equation_coffee_destination_port:
                        rec.equation_coffee_destination_port = invoice.equation_coffee_destination_port

                    if invoice.equation_coffee_shipping_line:
                        rec.equation_coffee_shipping_line = invoice.equation_coffee_shipping_line

                    if invoice.equation_coffee_bill_lading:
                        rec.equation_coffee_bill_lading = invoice.equation_coffee_bill_lading

                    if invoice.equation_coffee_hs_code:
                        rec.equation_coffee_hs_code = invoice.equation_coffee_hs_code

                    if invoice.equation_coffee_reference:
                        rec.equation_coffee_reference = invoice.equation_coffee_reference
