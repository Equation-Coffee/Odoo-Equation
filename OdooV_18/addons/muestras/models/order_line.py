from odoo import models, fields, api,_
import csv
import os 
import logging
from io import BytesIO
from reportlab.pdfgen import canvas

class Order_line(models.Model):
    _name=  "muestras.order.line"
    # _inherit='analytic.mixin'
    _description="Cada uno de los registros de venta"
    _rec_names_search=['name','order_id.name']
    _order='order_id,sequence,id'
    _check_company_auto=True



    ### FIELDS ####
    order_id=fields.Many2one(comodel_name='muestras.order',string='Order Reference',ondelete='cascade',
        required=True,index=True,copy=False
        )   
    product_id=fields.Many2one(comodel_name='muestras.allproducts',string='Product',ondelete='cascade',required=True,index=True,copy=True,
        domain="[('available_status', '=', 'dis')]")
    quantity=fields.Float(string="Sample(g)",required=True)
    price=fields.Float(string="Unit Price",required=False,digits=(16,2),help="The price per unit of the product")
    booking=fields.Float(string="Reserva",required=True,default=0.0)
    subtotal=fields.Float(string="Subtotal",required=False,digits=(16,2),help="Subtotal Price",store=True)
    project = fields.Char(string='Proyecto')
    variety = fields.Text(string='Variedad')
    program = fields.Text(string='Categoria')
    category = fields.Text(string = '.')
    location =fields.Char(string="Location")
    warehouse=fields.Char(string="Warehouse")
    country_origin=fields.Char(string="Origen")
    region=fields.Char(string="Region")
    lote=fields.Char(string="Lote")
    internal_code=fields.Char(string="Cod Int")
    edition=fields.Char(string="Edition")
    process=fields.Char(string="Process")
    score=fields.Float(string="Score")
    macroprofile=fields.Char(string="Macro Pr.")
    fuente=fields.Char(string="Fuente de datos")
    state=fields.Selection(string="Order State ", related="order_id.state")
    notes=fields.Text(string="Notas Adicionales")
    farm=fields.Char(string="Finca")
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],
        string="Unidad de Medida",
        default=None,
        required=True
        )
    boolean_booking=fields.Boolean(string=" ")
    sale_check=fields.Selection(
        selection=[
            ('ns','No venta'),
            ('sl','Venta'),
        ],
        string='Venta',
        default=None
    )

    booking_change=fields.Float(string="Venta")
    feedback_selection= fields.Many2many(
        'muestras.feedback',
        string="Feedback"
    )
    feedback_notes=fields.Text(string="Notas Feedback")
    
    ### Campos para visualización en el menu de order line###
    order_name = fields.Char(related="order_id.name", string="Order Name")
    order_create_date = fields.Date(related="order_id.create_date", string="Order Date")
    salesperson_name = fields.Char(related="order_id.salesperson_header.name", string="Salesperson")
    partner_name = fields.Char(related="order_id.partner_id.name", string="Customer")


    ### Campos especificos de logica 
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line0_note', "Note"),
        ], default=False)

    sequence=fields.Integer(string='Sequence',default=10)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if  self.product_id:      
            self.price = self.product_id.price
            self.project=self.product_id.project
            self.variety=self.product_id.variety
            self.program=self.product_id.program
            self.category=self.product_id.category
            self.location=self.product_id.location
            self.warehouse=self.product_id.warehouse
            self.country_origin=self.product_id.country_origin
            self.lote=self.product_id.lote
            self.internal_code=self.product_id.internal_code
            self.edition=self.product_id.edition
            if self.product_id.disponible_id:
                self.process=self.product_id.fprocess
            else:    
                self.process=self.product_id.process 
            self.score=self.product_id.score
            self.macroprofile=self.product_id.macroprofile
            self.fuente=self.product_id.fuente
            self.region=self.product_id.region
            self.uom=self.product_id.uom
            self.farm=self.product_id.farm



    @api.onchange('booking','price')
    def _subtotal(self):
        if self.quantity:
            self.subtotal=self.price*self.booking


