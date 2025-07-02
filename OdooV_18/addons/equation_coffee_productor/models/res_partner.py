# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'


    is_it_a_producer = fields.Boolean(string = 'Is productor?', default = False, tracking=True)
    
    equation_coffee_productor_farm = fields.Char(string = 'Farm', tracking=True)
    equation_coffee_productor_elevation = fields.Char(string = "Elevation (meters above sea level)", tracking=True)

    equation_coffee_productor_project_ids = fields.Many2many(comodel_name="equation.coffee_project",
                                                   relation="res_partner_equation_coffee_productor_project_rel", column1="partner_id", column2="equation_coffee_project_id", string="Projects")
    equation_coffee_productor_varietal_ids = fields.Many2many(comodel_name="equation.coffee_varietal",
                                                   relation="res_partner_equation_coffee_productor_varietal_rel", column1="partner_id", column2="equation_coffee_varietal_id", string="Varietals")
    equation_coffee_cropster = fields.Binary(
        string='Cropster', attachment=True, tracking=True)
    equation_coffee_cropster_name = fields.Char(string='Cropster Name')
