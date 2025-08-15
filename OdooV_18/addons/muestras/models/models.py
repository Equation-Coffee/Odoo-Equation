# -*- coding: utf-8 -*-

from odoo import models, fields, api
import csv
import os 
import logging
from odoo.exceptions import ValidationError
import math

_logger=logging.getLogger(__name__)

class Tabla(models.Model):
    _name = 'muestras.tabla'
    _description = 'tabla'

    name = fields.Char()

class Inventario(models.Model):
    _name='muestras.inventario'
    _description = "Inventario"
    _inherit=['muestras.father','mail.thread', 'mail.activity.mixin']
    _rec_name="lote"
    
    ## FIELDS ###
    offeringCat=fields.Many2many(
        'muestras.offeringcat',
        string="Categorias Portafolio"
    )
    stock_id=fields.Many2one('stock.lot',string="Stock Lot ID")


    def write(self,vals):
        result=super(Inventario,self).write(vals)
        self.env['muestras.allproducts'].upsert_inventary(self)
        return result

    @api.model
    def create(self,vals):
        record=super(Inventario,self).create(vals)
        self.env['muestras.allproducts'].upsert_inventary(record)
        return record
    
    @api.model
    def normalize_inventary(self,product):
        # products=self.env['stock.lot'].search([])

        # for product in products:
        existing_record=self.search([
            ('stock_id','=',product.id)
        ],limit=1)
        if existing_record:
            existing_record.write({
                'name':product.name,
            })
        else:
            self.create({
                'name':product.name,
                'stock_id':product.id,
            })
            self.env.cr.commit()

  
    def button_inventory(self):
        products=self.env['stock.lot'].search([])

        for product in products:
            existing_record=self.search([
                ('stock_id','=',product.id)
            ],limit=1)
            if existing_record:
                existing_record.write({
                    'name':product.name,
                })
            else:
                self.create({
                    'name':product.name,
                    'stock_id':product.id,
                })
                self.env.cr.commit()



    
  


class Disponibles(models.Model):
    _name='muestras.disponible'
    _inherit=['muestras.father','mail.thread', 'mail.activity.mixin']
    _description="Productos disponibles"
    _rec_name="lote"


    ## Camios en las herencias del modelo padre
    equation_project=fields.Many2one('equation.coffee_project',string="Equation Project",
                default=lambda self: self.env['equation.coffee_project'].search([('name', '=', 'Equation Coffee')], limit=1),required=True
                )   
    equation_program = fields.Many2one('equation.coffee_program',string="Equation Program",tracking=True,required=True)
    equation_varietal = fields.Many2one('equation.coffee_varietal',string="Equation Varietal",tracking=True,required=True)
    equation_fermentation_process = fields.Many2one('equation.coffee_fermentation_process',string="Fermentation Process Equation",tracking=True,required=True)
    equation_process_offering = fields.Many2one('equation.coffee_process_offering',string="Equation Offering Process",tracking=True,required=True)
    equation_origin_town = fields.Many2one('equation.coffee_origin',string="Origin",tracking=True,required=True)
    equation_macroprofile = fields.Many2one('equation.coffee_macroprofile',string="Equation Macroprofile",tracking=True,required=True)
    location = fields.Char(string="Location",default="Colombia",required=True)



    #### Cambios campos de la modelo padre
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],
        string="Unidad de Medida",
        default='kg',
        required=True
        )
    

    ## FIELDS ###
    offeringCat=fields.Many2many(
        'muestras.offeringcat',
        string="Categorias Portafolio"
    )

    main_category=fields.Many2one('muestras.offeringcat',string="Categoria Principal",required=True,tracking=True)
    second_category=fields.Many2one('muestras.offeringcat',string="Categoria Secundaria")
    price_category_adjustment=fields.Float(string="Precio Adicional Spot por categoria")  ### Campo abolido
    category_margin=fields.Float(string="Category Margin",store=True,compute="_price_category_adjustment")
    category_margin_spot = fields.Float(string="Category Margin SPOT",store=True,compute="_price_category_adjustment_SPOT")
    trm=fields.Float(string="TRM",store=True,default=lambda self:self._default_price('USD/COP Exchange Rate')) ### ,compute="_compute_trm"
    price_c=fields.Float(string="Precio C",store=True,default=lambda self:self._default_price('Coffee C Price'))
    eu_us=fields.Float(string="Tasa de Conversion Euro-Dolar",store=True,default=lambda self:self._default_price('EUR/USD Exchange Rate'))
    coffee_load=fields.Float(string="Carga Estandar",store=True,default=lambda self:self._default_price('Coffee Load'))
    uml=fields.Float(string="Utilidad Microlote",store=True,default=lambda self:self._default_price('Utilidad Microlote'))
    ur=fields.Float(string="Utilidad Regional",store=True,default=lambda self:self._default_price('Utilidad Regional'))
    c_fob=fields.Float(string="Costos FOB",store=True,default=lambda self:self._default_price('FOB Cost'))
    spot_cost_us=fields.Float(string="SPOT Cost US",store=True,default=lambda self:self._default_price('SPOT Cost US'))
    spot_cost_eu=fields.Float(string="SPOT Cost EU",store=True,default=lambda self:self._default_price('SPOT Cost US'))
    us_tariffs = fields.Float(string="US Tariffs",store=True,default=lambda self:self._default_price('US Tariffs'))
    decaf_cost = fields.Float(string="Decaf Cost",store=True,default=lambda self:self._default_price('Decaf Cost'))
    price_c_dif=fields.Float(string="Precio C + Dif",store=True)
    price_fob_usa=fields.Float(string='FOB US/lb',store=True,compute="_price_fob_usa")
    price_fob_eu=fields.Float(string='FOB EU/kg',store=True,compute="_price_fob_eu")
    price_exw=fields.Float(string='EXW US/lb',store=True,compute="_price_exw")
    price_exw_kg=fields.Float(string='EXW US/kg',store=True,compute="_price_exw_kg")
    price_exw_eu=fields.Float(string="EXW EU/kg",store=True,compute="_price_exw_eu")
    price_spot_usa_tariffs=fields.Float(string="Spot US/lb with Tariffs",store=True,compute="_price_spot_usa_tariffs")
    price_spot_usa=fields.Float(string='Spot US/lb',store=True,compute="_price_spot_usa")
    price_spot_eu=fields.Float(string='SPOT EU/kg',store=True,compute="_price_spot_eu")
    price_fwb_usa=fields.Float(string='FWB USDxlb',store=True,compute="_price_fwb_usa")
    price_fwb_eu=fields.Float(string='FWB EUxkg',store=True,compute="_price_fwb_eu")
    
    price_selector=fields.Selection(        
        selection=[
            ('exc','Exlceso'),
            ('dfc','Diferencial de Compra'),
            ('pxc','Precio por Carga')
        ],
        string="Price Selector",
        default='exc',required=True,tracking=True)
    excelso_kg=fields.Float(string="Valor Kilogramo de Excelso",tracking=True)
    cost_variance=fields.Float(string="Diferncial de Compra (USD/LB)",tracking=True)
    load_price=fields.Float(string="Precio por carga",tracking=True)
    factor=fields.Float(string="Factor de Rendimiento",compute='_factor')
    availability_35kg=fields.Float(string="Disponibilidad en sacos de 35 kg",store=True,compute="_aval_35",tracking=True)
    availability_70kg=fields.Float(string="Disponibilidad en sacos de 70 kg",required=True)
    pdf_prueba = fields.Binary(string="Archivo PDF",attachment=True) 
    sample_availability=fields.Float(string="Disponibilidad de Gramos de muestras",required=True,tracking=True)

    # @api.model
    # def get_global_param(self,param_name,default):
    #     param=self.env['muestras.price'].search([("name","=",param_name)],limit=1)
    #     return param.value if param else deafult  


    @api.model
    def create(self,vals):
        if vals.get('equation_project'):
            eq = self.env['equation.coffee_project'].browse(vals['equation_project'])
            if eq.exists():
                vals['project']=eq.name
        record=super(Disponibles,self).create(vals)
        self.env['muestras.allproducts'].disponible_upsert(record)
        return record
    
    @api.depends('equation_process_offering')
    def _factor(self):
        for record in self:
            record.factor = record.equation_process_offering.efficiency_factor

    
    def _default_price(self, price_name):
        try:
            Price = self.env['muestras.price']
            # Confirmamos que el campo 'name' existe
            if not Price._fields.get('name') or not Price._fields.get('value'):
                _logger.error("Campos 'name' o 'value' no existen en muestras.price")
                return 0.0

            # Buscamos el registro correspondiente por nombre y ordenamos por fecha
            price_record = Price.search(
                [('name', '=', price_name)],
                order='date desc, create_date desc',
                limit=1
            )

            if price_record and price_record.value:
                try:
                    return float(price_record.value)
                except ValueError:
                    _logger.warning(f"Valor para '{price_name}' no convertible: {price_record.value}")
                    return 0.0
            return 0.0

        except Exception as e:
            _logger.exception(f"Error al calcular valor para '{price_name}': {e}")
            return 0.0
     
   
    @api.model
    def crear_canal_productos(self):
        canal = self.env['mail.channel'].search([('name', '=', 'Productos')], limit=1)
        if not canal:
            usuarios = self.env['res.users'].search([])
            partner_ids = [u.partner_id.id for u in usuarios if u.partner_id]
            canal = self.env['mail.channel'].create({
                'name': 'Productos',
                'channel_type': 'channel',
                'public': 'private',
                'channel_partner_ids': [(6, 0, partner_ids)]
            })
        return canal
    
   
    def write(self, vals):
        result = super(Disponibles, self).write(vals)
        self.env['muestras.allproducts'].disponible_upsert(self)
        return result


    def _send_notification_to_users(self, message):
        users = self.env['res.users'].search([])
        notifications = []
        for user in users:
            partner = user.partner_id
            if partner:
                notifications.append((
                    f'res.partner,{partner.id}',  # Canal de la notificación
                    'simple_notification',  # Tipo de la notificación
                    {
                        'type': 'simple_notification',
                        'title': 'Notificación del sistema',  # Título
                        'message': message,  # Mensaje
                        'sticky': False,  # No pegajosa
                    }
                ))

        # Enviar las notificaciones si la lista no está vacía
        if notifications:
            self.env['bus.bus']._sendmany(notifications)

    @api.depends('main_category','main_category.category_margin_spot')
    def _price_category_adjustment_SPOT(self):
        for record in self:
            record.category_margin_spot = record.main_category.category_margin_spot
    
    @api.depends('main_category','main_category.category_margin')
    def _price_category_adjustment(self):
        for record in self:
            record.category_margin=record.main_category.category_margin

    #### --------------------- Flujo Calculo de Precios --------------------------------- ######

    @api.depends('price_selector','excelso_kg','trm','price_c','cost_variance','load_price','program','factor','category_margin','is_decaf','is_premium','extra_charge_premium')
    def _price_exw(self):
        for record in self:
            if record.price_selector=='exc':
                if record.trm>0:
                    price_one= record.excelso_kg/(2.2046*record.trm)
                else:
                    price_one=0  
            else:
                if record.price_selector=='dfc':
                    price_one=record.cost_variance + record.price_c
                else:
                    if record.price_selector=='pxc':
                        if record.trm>0:
                            price_one=((record.load_price/record.coffee_load)*record.factor)/(record.trm*154.322)
                        else:
                            price_one=0
                    else:
                        price_one=0
            price_decaf = record.decaf_cost if record.is_decaf else 0.0
            price_premium = record.extra_charge_premium if record.is_premium else 0.0
            calculate_price = price_one + record.category_margin + price_decaf + price_premium
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_exw= final_price

    @api.depends('price_exw')
    def _price_exw_kg(self):
        for record in self:
            calculate_price=record.price_exw*2.2046
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_exw_kg = final_price

    @api.depends('price_exw','eu_us')
    def _price_exw_eu(self):
        for record in self:
            calculate_price = record.price_exw*2.2046/record.eu_us
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_exw_eu = final_price

    @api.depends('price_exw','category_margin_spot','spot_cost_us')
    def _price_spot_usa(self):
        for record in self:
            calculate_price = record.price_exw + record.spot_cost_us + record.category_margin_spot
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_spot_usa = final_price


    @api.depends('price_spot_usa','us_tariffs')
    def _price_spot_usa_tariffs(self):
        for record in self:
            calculate_price = record.price_spot_usa*(1+record.us_tariffs)
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_spot_usa_tariffs = final_price

    @api.depends('price_exw','spot_cost_eu','category_margin_spot','eu_us')
    def _price_spot_eu(self):
        for record in self:
            calculate_price = (record.price_exw + record.spot_cost_eu + record.category_margin_spot)*2.2046/record.eu_us 
            final_price = self.round_to_nearest_5(calculate_price)
            record.price_spot_eu = final_price 

     
    @api.depends('availability_70kg')
    def _aval_35(self):
        for record in self:
            record.availability_35kg = round(record.availability_70kg*2,2)


    @api.depends('price_selector','excelso_kg','trm','price_c','cost_variance','load_price','uml','ur','program','c_fob','factor','is_decaf','is_premium')
    def _price_fob_usa(self):
        for record in self:
            if record.price_selector=='exc':
                if record.trm>0:
                    price_one= record.excelso_kg/(2.2046*record.trm)
                else:
                    price_one=0  
            else:
                if record.price_selector=='dfc':
                    price_one=record.cost_variance + record.price_c
                else:
                    if record.price_selector=='pxc':
                        if record.trm>0:
                            price_one=((record.load_price/record.coffee_load)*record.factor)/(record.trm*154.322)
                        else:
                            price_one=0
                    else:
                        price_one=0
            
            if record.equation_program.name=="Microlot":
                price_two=(record.uml+record.c_fob)/100
            elif record.equation_program.name=='Regional':
                price_two=(record.ur+record.c_fob)/100
            else:
                price_two=0
            record.price_fob_usa=price_one + record.category_margin




    @api.depends('price_fob_usa','eu_us') ## Agregrar El 10 % arancel. Disclaimer deta,e 10 porceinto arancel
    def _price_fob_eu(self):
        for record in self:
            record.price_fob_eu=record.price_fob_usa*record.eu_us*2.2046


    
    @api.depends('main_category','main_category.category_margin_spot')
    def _price_category_adjustment_SPOT(self):
        for record in self:
            record.category_margin_spot = record.main_category.category_margin_spot
    
    @api.depends('main_category','main_category.category_margin')
    def _price_category_adjustment(self):
        for record in self:
            record.category_margin=record.main_category.category_margin
    


    @api.depends('price_fob_usa')
    def _price_fwb_usa(self):
        for record in self:
            record.price_fwb_usa=record.price_fob_usa+0.5

    @api.depends('price_fob_eu')
    def _price_fwb_eu(self):
        for record in self:
            record.price_fwb_eu=record.price_fob_eu+0.5

    @staticmethod
    def round_to_nearest_5(value):
        dec = int((value * 100) % 100)
        res = dec%5
        print(res)
        if res !=0:
            final = round((math.trunc(value* 100) / 100)+(5-res)/100,2)
        else: 
            final = math.trunc(value*100)/100 
        return final

    @api.constrains('available','price_selector','excelso_kg','load_price')
    def _check_price_selector_values(self):
        if self.available =='dis':
            if self.price_selector == 'exc':
                if self.excelso_kg<=0:
                    raise ValidationError("El valor de Excelso debe ser mayor a 0")
            elif self.price_selector == 'pxc':
                if self.load_price<=0:
                    raise ValidationError("El valor del Precio por Carga debe ser mayor a 0")

    @api.constrains('available','availability_70kg')
    def _check_availability_70kg(self):
        if self.available == 'dis':
            if self.availability_70kg<=0:
                raise ValidationError("El valor disponible en sacos de 70 kg debe ser mayor a 0") 
            
    @api.constrains('available','sample_availability')
    def _checko_sample_availability(self):
        if self.available =='dis':
            if self.sample_availability<=0:
                raise ValidationError("El valor disponible de muestra debe ser mayor a 0") 

    def action_open_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }






# class SPOTEU(models.Model):
#     _name="muestras.spoteu"
#     _description="SPOT EU Temporary"
#     _inherit=   ['muestras.father','mail.thread', 'mail.activity.mixin']
#     _rec_name="lote"
    
#     offeringCat=fields.Many2many(
#         'muestras.offeringcat',
#         string="Categorias Portafolio"
#     )

    
#     def write(self,vals):
#         result=super(SPOTEU,self).write(vals)
#         self.env['muestras.allproducts'].spotEU_data(self)
#         return result

#     @api.model
#     def create(self,vals):
#         record=super(SPOTEU,self).create(vals)
#         self.env['muestras.allproducts'].spotEU_data(record)
#         return record
    
    
   
  





class Product(models.Model):
        _name = 'muestras.product'
        _description ='Productos Disponibles'
        _rec_name='code'


        code = fields.Char(string="Código del Producto",store=True)
        project = fields.Char(string='Nombre del Proyecto', required=True)
        quantity_kg = fields.Float(string='Cantidad', default=0)
        price_usd = fields.Float(string='Precio USD/kg',required=True)
        pricelb=fields.Float(string="Precio USD/lb")
        variety = fields.Text(string='Variedad')
        program = fields.Text(string='Program')
        category = fields.Text(string = 'Categoria',required=True)
        # parameter_id = fields.Many2one('muestras.parametros','code',compute="_compute_code",store=True)
        location =fields.Char(string="Location")
        warehouse=fields.Char(string="Warehouse")
        country_origin=fields.Char(string="Country of Origin")
        lote=fields.Char(string="lote")
        internal_code=fields.Char(string="Internal Code")
        edition=fields.Char(string="edition")
        process=fields.Char(string="Proceso de Lavado")
        fprocess=fields.Char(string="Proceso de Fermentación")
        score=fields.Integer(string="Score")
        macroprofile=fields.Char(string="Perfil Sensorial")
        sca_entrega=fields.Float(string="SCA Entrega")
        sca_actual=fields.Float(string="SCA Actual")
        sku=fields.Char(string="SKU")
        condicion=fields.Char(string="Condición")

        # category = fields.Selection([
        #     ('C1', 'Categoría 1'),
        #     ('C2', 'Categoría 2'),
        #     ('C3', 'Categoría 3'),
        # ], string='Categoría')
        # region = fields.Text(string='Region',required=True)
        # region = fields.Selection([
        #     ('USA', 'Estados Unidos'),
        # ], string='Región')
        quantityUSA= fields.Float(string="Cantidad USA",groups="muestras.group_USA",store=True) 
        quantityEU= fields.Float(string = "Cantidad EU",groups="muestras.group_EU",store=True)
        quantityAsia= fields.Float(string= "Cantidad Asia",groups="muestras.group_Asia",store=True)



        

        # @api.model    
        # def dataLoad (self):
        #     file_path = '/mnt/extra-addons/muestras/data/inventarioprueba.csv'
        #     try:
        #         with open(file_path,mode='r',encoding ='utf-8') as file:
        #             reader = csv.DictReader(file)
        #             for row in reader:
        #                 record = self.create({
        #                     'project':row['project'],
        #                     'quantity_kg':float(row['quantity_kg']),
        #                     'price_usd':float(row['price_usd']),
        #                     'program':row['variety'],
        #                     'category':row['category'],
        #                     # 'region': row['region'],
        #                 })
        #                 self.env.cr.commit()
        #                 record.code = str(record.project)+str(record.category)+str(record.program)
        #                 combi = self.env['muestras.parametros'].search([
        #                     ('code','=',record.code),
        #                 ],limit=1)

        #                 if combi:
        #                     record.parameter_id = combi
        #                     return record.parameter_id
        #                 _logger.info(f"Registro creado :{record.id}")

        #         _logger.info("Datos cargados exitosamente desde prueba.csv")
        #     except FileNotFoundError:
        #         _logger.info(f"No se encontro el archivo:{file_path}")
        #     except Exception as e:
        #         _logger.info(f"Error al cargar los datos: {str(e)}")

        # @api.depends('parameter_id','parameter_id.percentAsia','parameter_id.percentEU','parameter_id.percentUSA')
        # def _compute_disp_region(self):
        #     for record in self:
        #         record.quantityAsia=record.quantity_kg*record.parameter_id.percentAsia
        #         record.quantityEU=record.quantity_kg*record.parameter_id.percentEU
        #         record.quantityUSA=record.quantity_kg*record.parameter_id.percentUSA

        @api.model
        def create(self, vals):
            record = super(Product, self).create(vals)
            self.env['muestras.allproducts'].normalize_product_data()

            return record

        def write(self, vals):
            result = super(Product, self).write(vals)
            self.env['muestras.allproducts'].normalize_product_data()

            return result

        @api.constrains('quantityUSA','quantityEU','quantityAsia')
        def _cheksum_percent(self):
            for record in self:
                    total_sum = record.quantityUSA+ record.quantityAsia + record.quantityEU
                    if total_sum !=1:
                        raise ValidationError("La suma de los campos debe ser exactamente {}. Actualmente es {:.2f}".format(self.quantity_kg, total_sum))





  

class StockLot(models.Model):
    _inherit='stock.lot'


    def write(self,vals):   
        result=super(StockLot,self).write(vals)
        for lot in self:
            if lot.company_id.id == 15:
                self.env['muestras.spoteu'].normalize_inventary(lot)
        return result

    @api.model
    def create(self,vals):
        record=super(StockLot,self).create(vals)
        if record.company_id.id == 15:
                self.env['muestras.spoteu'].normalize_inventary(record)
        return record


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def create(self, vals_list):
        records = super().create(vals_list)
        for quant in records:
            lot = quant.lot_id
            if lot and lot.company_id.id == 15:
                quant.env['muestras.spoteu'].normalize_inventary(lot)
        return records

    def write(self, vals):
        result = super().write(vals)
        processed_lots = set()
        for quant in self:
            lot = quant.lot_id
            if lot and lot.id not in processed_lots and lot.company_id.id == 15:
                quant.env['muestras.spoteu'].normalize_inventary(quant.lot_id)
                processed_lots.add(quant.lot_id.id)
        return result
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()

        for picking in self:
            if picking.picking_type_id.code == 'incoming':
                for move_line in picking.move_line_ids:
                    lot = move_line.lot_id
                    if lot:
                        _logger.info("Normalizando lote %s desde picking %s", lot.name, picking.name)
                        self.env['muestras.spoteu'].normalize_inventary(lot)
        return res        