# -*- coding: utf-8 -*-

from odoo import models, fields, api
import csv
import os 
import logging
from odoo.exceptions import ValidationError
import math

_logger=logging.getLogger(__name__)


class SPOTEU(models.Model):
    _name="muestras.spoteu"
    _description="SPOT EU Temporary"
    _inherit=   ['muestras.father','mail.thread', 'mail.activity.mixin']
    _rec_name="lote"
    

    #--- Campos Adicionales al Product Father
    offeringCat=fields.Many2many(
        'muestras.offeringcat',
        string="Categorias Portafolio"
    )
    stock_id=fields.Many2one('stock.lot',string="Stock Lot ID")
    default_code=fields.Char(string='Reference')

    def write(self,vals):
        result=super(SPOTEU,self).write(vals)
        self.env['muestras.allproducts'].upsert_inventary(self)
        return result

    @api.model
    def create(self,vals):
        record=super(SPOTEU,self).create(vals)
        self.env['muestras.allproducts'].upsert_inventary(record)
        return record
    
    @api.model
    def normalize_inventary(self,product):
        existing_record=self.search([
            ('stock_id','=',product.id)
        ],limit=1)
        if existing_record:
            if product.product_qty==0:
                dis = 'nodis'
            else:
                dis ='dis'
            existing_record.write({
                'available':dis,
                'quantity_kg':product.product_qty,
            })
        else:
            if product.company_id.id == 15:
                self.create({
                    'name':product.product_id.name,
                    'lote':product.name,
                    'stock_id':product.id,
                    'equation_project':product.equation_coffee_project_id.id,
                    'equation_program':product.equation_coffee_program_id.id,
                    'equation_varietal':product.equation_coffee_varietal_id.id,
                    'equation_fermentation_process':product.equation_coffee_fermentation_process_id.id,
                    'equation_drying_process':product.equation_coffee_drying_process_id.id,
                    'location':'Europe',
                    'default_code':product.product_id.default_code,
                    'quantity_kg':product.product_qty, 
                    'uom':'kg',
                    'available':'dis',
                })
            self.env.cr.commit()

        
    def update_button(self):
        products=self.env['stock.lot'].search([('company_id', '=', 15)])
        for product in products:
            if  product.is_it_coffee==True:
                existing_record=self.search([('stock_id','=',product.id)],limit=1)
                if existing_record:
                    available = 'nodis' if product.product_qty == 0 else 'dis'
                    existing_record.write({
                        'available':available,
                        'quantity_kg':product.product_qty,
                    })
                else:
                    if product.product_qty!=0:
                        self.create({
                            'name':product.product_id.name,
                            'lote':product.name,
                            'stock_id':product.id,
                            'equation_project':product.equation_coffee_project_id.id,
                            'equation_program':product.equation_coffee_program_id.id,
                            'equation_varietal':product.equation_coffee_varietal_id.id,
                            'equation_fermentation_process':product.equation_coffee_fermentation_process_id.id,
                            'equation_drying_process':product.equation_coffee_drying_process_id.id,
                            'location':'Europe',
                            'default_code':product.product_id.default_code,
                            'quantity_kg':product.product_qty, 
                            'uom':'kg',
                            'available':'dis',
                        })
                    self.env.cr.commit()



    
    def write(self,vals):
        result=super(SPOTEU,self).write(vals)
        self.env['muestras.allproducts'].spotEU_data(self)
        return result

    @api.model
    def create(self,vals):
        record=super(SPOTEU,self).create(vals)
        self.env['muestras.allproducts'].spotEU_data(record)
        return record
    
    
   