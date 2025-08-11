from odoo import models,fields,api, _
import csv
import os
import logging
from odoo.exceptions import ValidationError

class SampleFather(models.Model):
    _name='muestras.father'
    _description="Modelo padre menú de muestras"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name='lote'

    ### General Informatin ###
    name = fields.Char(string="Name")
    sku=fields.Char(string="SKU")
    lote = fields.Char(string="Lot")
    internal_code = fields.Char(string="Internal Code")
    code = fields.Char(string="Product Code")    
    project = fields.Char(string="Project", required=True, default="",compute="_project")
    program = fields.Text(string='Program',compute="_program")
    category = fields.Text(string ='__',required=False,default="")
    variety = fields.Text(string='Variety',compute="_varietal")
    process = fields.Char(string="Drying Process",compute="_process") ## Drying Process
    fprocess = fields.Char(string="Fermentation Process",compute="_fprocess")
    town = fields.Char(string="Origin Town",compute="_origin_town")
    date_create=fields.Date(string="Creation Date")
    available = fields.Selection(
        selection = [
            ('dis','Disponible'),
            ('nodis','No Disponible'),
        ],
        string="Availability",default=None,required=True
    )
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)

    ### Equation Info ###
    equation_project = fields.Many2one('equation.coffee_project',string="Equation Project",tracking=True)
    equation_program = fields.Many2one('equation.coffee_program',string="Equation Program",tracking=True)
    equation_varietal = fields.Many2one('equation.coffee_varietal',string="Equation Varietal",tracking=True)
    equation_drying_process = fields.Many2one('equation.coffee_drying_process',string="Drying Process Equation",tracking=True)
    equation_fermentation_process = fields.Many2one('equation.coffee_fermentation_process',string="Fermentation Process Equation",tracking=True)
    equation_origin_town = fields.Many2one('equation.coffee_origin',string="Origin",tracking=True)
    equation_sca_score = fields.Many2one('equation.coffee_sca',string="SCA Score",tracking=True)
    equation_macroprofile = fields.Many2one('equation.coffee_macroprofile',string="Equation Macroprofile",tracking=True)
    equation_process_offering = fields.Many2one('equation.coffee_process_offering',string="Equation Offering Process",tracking=True)

    ### Technical Info ###
    score = fields.Integer(string="SCA")
    sca_entrega = fields.Float(string="First SCA")
    sca_actual = fields.Float(string="Actual SCA")
    edition = fields.Char(string="Edition")
    macroprofile = fields.Char(string="Sensory Profile")
    mcp = fields.Char(string="Macro-Perfil",compute="_mcp")
    freshness = fields.Integer(string="Freshness")
    altitude = fields.Float(string="Altitude")
    condicion = fields.Char(string="Condition")
    is_decaf = fields.Boolean(string="Is Decaffeinated?")
    is_premium = fields.Boolean(string="Is Premium?")
    extra_charge_premium = fields.Float(String="Aditional Cost for Premium Coffees")
    packing_type = fields.Selection(
        selection = [
            ('bg','Bolsa'),
            ('sg','Saco'),
        ],        
        string ="Packaging",default=None)
    packing_weight = fields.Selection(
        selection = [
            ('3k','3 Kilos'),
            ('5k','5 Kilos',)
        ],
        string ="Packaging weight",default=None
    )

    ### Inventory ###
    country_origin = fields.Char(string="Country")
    location = fields.Char(string="Location")
    warehouse = fields.Char(string="Warehouse")
    farm = fields.Char(string="Farm")
    producer = fields.Char(string="Productor")
    supplier = fields.Char(string="Supplier")
    region = fields.Char(string="Region")
    quantity_kg = fields.Float(string='Quantity', default=0)
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],
        string="Unit of Measurement",default=None,required=True
        )

    ### Price ###
    price_usd = fields.Float(string='USD/kg',required=True,default="")
    pricelb=fields.Float(string="USD/lb")



    ### METHODS ###

    ### Equation Parametrization Methods ###
    @api.depends('equation_project')
    def _project(self):
        for record in self:
            record.project=record.equation_project.name

    @api.depends('equation_program')
    def _program(self):
        for record in self:
            record.program=record.equation_program.name

    @api.depends('equation_varietal')
    def _varietal(self):
        for record in self:
            record.variety=record.equation_varietal.name

    @api.depends('equation_fermentation_process')
    def _fprocess(self):
        for record in self:
            record.fprocess=record.equation_fermentation_process.name

    @api.depends('equation_drying_process')
    def _process(self):
        for record in self:
            record.process=record.equation_drying_process.name

    @api.depends('equation_origin_town')
    def _origin_town(self):
        for record in self:
            record.town=record.equation_origin_town.name    
    
    @api.depends('equation_sca_score')
    def _sca(self):
        for record in self:
            record.sca_actual=record.equation_sca_score.name

    @api.depends('equation_macroprofile')
    def _mcp(self):
        for record in self:
            record.mcp=record.equation_macroprofile.name

    





