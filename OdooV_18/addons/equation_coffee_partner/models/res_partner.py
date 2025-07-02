# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'


    equation_coffee_comercial_name = fields.Char(string = "Comercial name", tracking=True)
    equation_coffee_account_type_id = fields.Many2one(
        'equation.coffee_account_type', string="Account Type", tracking=True)
    equation_coffee_region = fields.Selection(
        selection=[('north_america', 'North America'), ('asia', 'Asia'), ('australia',
                                                                         'Australia'), ('europe', 'Europe'), ('middle_east', 'Middle East'), ('south_america', 'South America')],
        string="Region", tracking=True)
    equation_coffee_customer_origin_id = fields.Many2one(
        'equation.coffee_customer_origin', string="How did they come to us? (Story & Background)", tracking=True)
    equation_coffee_customer_context = fields.Text(
        string="History/customer context (how much do we know about our customers?)", tracking=True)
    equation_coffee_personal_information = fields.Text(
        string="Personal information", tracking=True)
    equation_coffee_project_ids = fields.Many2many(comodel_name="equation.coffee_project",
                                                   relation="res_partner_equation_coffee_project_rel", column1="partner_id", column2="equation_coffee_project_id", string="What projects do they buy?")
    equation_coffee_customer_program_ids = fields.Many2many(comodel_name="equation.coffee_customer_program",
                                                   relation="res_partner_equation_coffee_customer_program_rel", column1="partner_id", column2="equation_coffee_customer_program_id", string="Coffee Programs")

    foreign_id_number = fields.Char(string='Foreign ID Number', tracking=True)
    purchase_history=fields.One2many(string="Purchase History",comodel_name='res.partner_purchase_history',
        inverse_name='partner',copy=True,auto_join=True
    )
    offering_history=fields.One2many(string="Offering History",comodel_name='muestras.offering_history',
        inverse_name='partner',copy=True,auto_join=True)