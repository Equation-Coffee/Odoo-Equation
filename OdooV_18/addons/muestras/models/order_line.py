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
    ### Order Info ###
    order_id=fields.Many2one(comodel_name='muestras.order',string='Order Reference',ondelete='cascade',
        required=True,index=True,copy=False
        )   
    notes=fields.Text(string="Additional Notes")
    quantity=fields.Float(string="Sample(g)",required=True,default=150.0)
    price=fields.Float(string="Unit Price",required=False,digits=(16,2),help="The price per unit of the product")
    booking=fields.Float(string="Booking",required=True,default=0.0)
    subtotal=fields.Float(string="Subtotal",required=False,digits=(16,2),help="Subtotal Price",store=True)
    line_state=fields.Selection(
        selection=[
            ('draft','Draft'),
            ('active','Active Sample'),
            ('declined','Declined Sample'),
            ('sold','Sold Sample'),
        ],string="Line State",default='draft')

    ### Product ###
    product_id=fields.Many2one(comodel_name='muestras.allproducts',string='Product',ondelete='cascade',required=True,index=True,copy=True,
        domain="[('available_status', '=', 'dis')]")
    project = fields.Char(string='Project')
    variety = fields.Text(string='Variety')
    program = fields.Text(string='Program') 
    category = fields.Text(string = '.')
    location =fields.Char(string="Location")
    warehouse=fields.Char(string="Warehouse")
    country_origin=fields.Char(string="Origin")
    region=fields.Char(string="Region")
    lote=fields.Char(string="Lot")
    internal_code=fields.Char(string="Cod Int")
    edition=fields.Char(string="Edition")
    process=fields.Char(string="Process")
    score=fields.Float(string="Score")
    macroprofile=fields.Char(string="Macroprofile")
    fuente=fields.Char(string="Data Origin")
    state=fields.Selection(string="Order State ", related="order_id.state")
    farm=fields.Char(string="Farm")
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],string="Unit of Measurement",default=None,required=True)
    boolean_booking=fields.Boolean(string=" ")
    sale_check=fields.Selection(
        selection=[
            ('ns','No venta'),
            ('sl','Venta'),
        ],string='Sale',default=None)

    booking_change=fields.Float(string="Sale Change")
    feedback_selection= fields.Many2many('muestras.feedback',string="Feedback")
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
            ('line_note', "Note"),
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
            if self.product_id.product_id:
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
        

    def sell_lot(self):
        return self.open_wizard_sale(action_type='sale',sale_check='sl')

    def release_lot(self):
        return self.open_wizard_sale(action_type='release',sale_check='ns')
        # product = self.product_id
        # product.write({
        #     'disponible':product.disponible + self.booking,
        #     'booking':product.booking - self.booking
        # })
        # self.line_state = 'declined'
        # order_states = self.states()
        # order = self.order_id
        # if 'declined' in order_states and len(order_states)==1:
        #     order.write({
        #         'state':'cancelb'
        #     })
        # elif 'declined' in order_states and len(order_states)>1:
        #     order.write({
        #         'state':'partial_rejection'
        #     })

        print('hola')

    def open_wizard_sale(self,action_type,sale_check):
        return{
            'type':'ir.actions.act_window',
            'res_model' : 'muestras.wizard_sale',
            'name':'Confirm Sample Order/Lot Sale',
            'view_mode':'form',
            'target':'new',
            'context':{
                'active_id':self.id,    
                'active_model':'muestras.order.line',
                'action_type':action_type,
                'sale_check':sale_check,
                'default_sale_check':sale_check,
            }
        }
    
    def states (self):
        lines = self.env['muestras.order.line'].search([('order_id','=',self.order_id.id)])
        states=[]
        for line in lines :
            if line.line_state not in states: states.append(self.line_state)
        return states
