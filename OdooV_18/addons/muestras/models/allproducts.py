from odoo import models, fields, api

class AllProducts(models.Model):
    _name = 'muestras.allproducts'
    _description = 'All Products by Region'
    _inherit = ['mail.thread']
    _rec_name="lote"
    _domain = "[('available_status', '=', 'dis')]"

    # Relación con el producto originalM
    product_id = fields.Many2one('muestras.prueba',string='Parent Product',required=False)
    disponible_id=fields.Many2one('muestras.disponible',string='Parent Disponible',required=False,ondelete='cascade')
    spotEU_id=fields.Many2one('muestras.spoteu',string='Parent SpotEU',required=False,ondelete='cascade')
    inventary_id=fields.Many2one('muestras.inventario',string='Parent Inventario',required=False,ondelete='cascade')
    name=fields.Text(string="Product Name", readonly=True)
    offeringCat=fields.Many2many(
        'muestras.offeringcat',
        string="Categorias Portafolio"
    )

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

    # Región asociada al producto
    region=fields.Text(string="Region", readonly=True)
    # Cantidad disponible en la región
    quantity = fields.Float(string='Cantidad Total',required=False,store=True, readonly=True)
    total_quantity=fields.Float(string='Cantidad Total Lote', readonly=True)
    booking = fields.Float(string="Reservado", readonly=True)
    sale = fields.Float(string="Vendido", readonly=True)
    avalible=fields.Float(string="Cantidad Disponible", readonly=True)
    price=fields.Float(string="USD/kg", readonly=True)
    pricelb=fields.Float(string="USD/lb", readonly=True)
    # quantity_init=fields.FloaT(string=)
    date_create=fields.Date(string="Fecha de Creación")

    project = fields.Char(string='Proyecto', readonly=True)
    variety = fields.Text(string='Variedad', readonly=True)
    program = fields.Text(string='Categoria', readonly=True)
    category = fields.Text(string = '___', readonly=True)
    location =fields.Char(string="Ubicación", readonly=True)
    warehouse=fields.Char(string="Bodega", readonly=True)
    country_origin=fields.Char(string="Origen", readonly=True)
    location=fields.Char(string="Ubicación", readonly=True)
    lote=fields.Char(string="Lote", readonly=True)
    internal_code=fields.Char(string="Código Interno", readonly=True)
    edition=fields.Char(string="edition", readonly=True)
    process=fields.Char(string="Proceso de Lavado", readonly=True)
    fprocess=fields.Char(string="Proceso de Fermentado", readonly=True)
    score=fields.Integer(string="SCA", readonly=True)
    macroprofile=fields.Char(string="Perfil Sensorial", readonly=True)
    mcp=fields.Char(string="Macro-Perfil", readonly=True)
    freshness=fields.Integer(string="Frescura")
    farm=fields.Char(string="Finca")
    altitude=fields.Float(string="Altitud")
    fuente=fields.Char(string="Campo", readonly=True)
    sca_entrega=fields.Float(string="SCA Entrega", readonly=True)
    sca_actual=fields.Float(string="SCA Actual", readonly=True)
    sku=fields.Char(string="SKU", readonly=True)
    condicion=fields.Char(string="Condición", readonly=True)
    disp_inventario=fields.Selection(
        selection=[
            ('dis',"Producto Disponible"),
            ('inv',"Producto en Inventario"),
        ],string="Cat. Iventario")
    
    available_status=fields.Selection(
        selection=[
            ('dis','Disponible'),
            ('nodis','No Disponible'),
        ],
        string="Disponibilidad",
        default='nodis',
        required=True
    )



    disponible=fields.Float(string="Disponible",compute="_avalible", readonly=True,store=True)
    date_create=fields.Date(string="Fecha de Creación")
    # wight_uom_id=fields.Float(string="unit")
    # weight_uom_category_id = fields.Float(string="hola")
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],
        string="Unidad de Medida",
        default=None,
        required=True
        )
    producer=fields.Char(string="Productor")


    @api.depends('booking','quantity','sale')
    def _avalible(self):
        for record in self:
            record.disponible=record.quantity-record.booking-record.sale



    # @api.model
    # def copy_data_from_products(self):
    #     print("Iniciando creación de registro...")
    #     try:
    #         record=self.create({
    #             'product_id': 1,  # ID ficticio
    #             'region': "Argentina",  # Región fija
    #             'quantity':100.0,  # Cantidad fija
    #         })
    #         self.env.cr.commit()
    #         print(f"Registro creado correctamente.:{record}")
    #         return record
    #     except Exception as e:
    #         print(f"Error en el self.create():{e}")

    #         # env['muestras.allproducts'].copy_data_from_products()


    @api.depends('product_id.quantityUSA','product_id.quantityEU','product_id.quantityAsia')
    def _actualize_quantity(self):
        products = self.env['muestras.product'].search([])

        # Iterar sobre cada producto y crear registros normalizados
        for product in products:
            # print(F'recorriendo el registro:{product}')
            regions={
                'United States':product.quantityUSA,
                'Europe':product.quantityEU,
                'Asia':product.quantityAsia,
             }

            for regionTemp,quantityTemp in regions.items():
                # Crear un registro para el precio de USA
                existing_record =self.search([
                    ('product_id','=',product.id),
                    ('region','=',regionTemp)
                ],limit=1)
                
                if existing_record:
                    print(f"match:{self.product_id}")
                    existing_record.write({
                        'quantity':quantityTemp,
                        'available_status':product.available,
                        
                    })
                else:

                    if product.quantityUSA and regionTemp=="United States":
                        self.create({
                            'product_id':product.id,
                            'region': "United States",
                            'quantity': product.quantityUSA,
                            'price':product.price_usd,
                            'equation_project':product.equation_project.id,
                            'project':product.project,
                            'variety':product.variety,
                            'program':product.program,
                            'category':product.category,
                            'location':product.location,
                            'warehouse':product.warehouse,
                            'country_origin':product.country_origin,
                            'lote':product.lote,
                            'internal_code':product.internal_code,
                            'edition':product.edition,
                            'process':product.process,
                            'score':product.score,
                            'macroprofile':product.macroprofile,
                            'fprocess':product.fprocess,
                            'sca_entrega':product.sca_entrega,
                            'sca_actual':product.sca_actual,
                            'sku':product.sku,
                            'condicion':product.condicion,
                            'pricelb':product.pricelb,
                            'offeringCat':product.offeringCat,
                            'date_create':product.date_create,
                            'available_status':product.available,
                        })
                        self.env.cr.commit()
                    # Crear un registro para el precio de Europa
                    if product.quantityEU and regionTemp=="Europe":
                        print('Europa')
                        self.create({
                            'product_id': product.id,
                            'region': "Europe",
                            'quantity': product.quantityEU,
                            'price':product.price_usd,
                            'equation_project':product.equation_project.id,
                            'project':product.project,
                            'variety':product.variety,
                            'program':product.program,
                            'category':product.category,
                            'location':product.location,
                            'warehouse':product.warehouse,
                            'country_origin':product.country_origin,
                            'lote':product.lote,
                            'internal_code':product.internal_code,
                            'edition':product.edition,
                            'process':product.process,
                            'score':product.score,
                            'macroprofile':product.macroprofile,
                            'fprocess':product.fprocess,
                            'sca_entrega':product.sca_entrega,
                            'sca_actual':product.sca_actual,
                            'sku':product.sku,
                            'condicion':product.condicion,
                            'pricelb':product.pricelb,
                            'offeringCat':product.offeringCat,
                            'available_status':product.available,

                        })
                        self.env.cr.commit()
                    # Crear un registro para el precio de Asia
                    if product.quantityAsia and regionTemp=="Asia":
                        self.create({
                            'product_id': product.id,
                            'region': 'Asia',
                            'quantity': product.quantityAsia,
                            'price':product.price_usd,
                            'equation_project':product.equation_project.id,
                            'project':product.project,
                            'variety':product.variety,
                            'program':product.program,
                            'category':product.category,
                            'location':product.location,
                            'warehouse':product.warehouse,
                            'country_origin':product.country_origin,
                            'lote':product.lote,
                            'internal_code':product.internal_code,
                            'edition':product.edition,
                            'process':product.process,
                            'score':product.score,
                            'macroprofile':product.macroprofile,
                            'fprocess':product.fprocess,
                            'sca_entrega':product.sca_entrega,
                            'sca_actual':product.sca_actual,
                            'sku':product.sku,
                            'condicion':product.condicion,
                            'pricelb':product.pricelb,
                            'offeringCat':product.offeringCat,
                            'available_status':product.available,
                        })
                        self.env.cr.commit()

    @api.model
    def disponible_upsert(self,product):
        # products=self.env['muestras.disponible'].search([])
        region='All Regions'
        # for product in products:
        print('Hola')
        existing_record=self.search([
            ('disponible_id','=',product.id)
        ],limit=1)

        if existing_record:
            existing_record.write({
                'quantity':product.quantity_kg,
                'region':region,
                'fuente':'Disponibles',
                'equation_project':product.equation_project.id,
                'project':product.project,
                'variety':product.variety,
                'program':product.program,
                'category':product.category,
                'location':product.location,
                'warehouse':product.warehouse,
                'country_origin':product.country_origin,
                'lote':product.lote,
                'internal_code':product.internal_code,
                'edition':product.main_category.name,
                'process':product.process,
                'score':product.score,
                'macroprofile':product.macroprofile,
                'pricelb': product.price_usd,
                'fprocess':product.fprocess,
                'sca_entrega':product.sca_entrega,
                'sca_actual':product.sca_actual,
                'sku':product.sku,
                'condicion':product.condicion,
                'pricelb':product.pricelb,
                'offeringCat':product.offeringCat,
                'total_quantity':product.quantity_kg,
                'disp_inventario':'dis',
                'date_create':product.date_create,
                'uom':product.uom,
                'producer':product.producer,
                'available_status':product.available,
            })
        else:
            if product.quantity_kg:
                self.create({
                    'disponible_id':product.id,
                    'region':region,
                    'quantity':product.quantity_kg,
                    'fuente':'Disponibles',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':product.location,
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.main_category.name,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'pricelb': product.price_usd,
                    'fprocess':product.fprocess,
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'dis',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,
                })
                self.env.cr.commit()

             
        
    @api.model
    def spotEU_data(self,product):
        # products=self.env['muestras.spoteu'].search([])
        # for product in products:
        existing_record=self.search([
            ('spotEU_id','=',product.id)
        ],limit=1)
        if existing_record:
            existing_record.write({
                'quantity':product.quantity_kg,
                'region':'Europe',
                'fuente':'SPOT EU Temporary',
                'equation_project':product.equation_project.id,
                'project':product.project,
                'variety':product.variety,
                'program':product.program,
                'category':product.category,
                'location':"Europe",
                'warehouse':product.warehouse,
                'country_origin':product.country_origin,
                'lote':product.lote,
                'internal_code':product.internal_code,
                'edition':product.edition,
                'process':product.process,
                'score':product.score,
                'macroprofile':product.macroprofile,
                'price':product.price_usd,  
                'fprocess':product.fprocess,
                'sca_entrega':product.sca_entrega,
                'sca_actual':product.sca_actual,
                'sku':product.sku,
                'condicion':product.condicion,
                'pricelb':product.pricelb,
                'offeringCat':product.offeringCat,
                'total_quantity':product.quantity_kg,
                'disp_inventario':'inv',
                'date_create':product.date_create,
                'uom':product.uom,
                'producer':product.producer,
                'available_status':product.available,
            })
        else:
            if product.quantity_kg:
                self.create({
                    'spotEU_id':product.id,
                    'region':'Europe',
                    'quantity':product.quantity_kg,
                    'fuente':'Disponibles',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':"Europe",
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.edition,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'price':product.price_usd,  
                    'fprocess':product.fprocess,
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'inv',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,
                })
                self.env.cr.commit()


    @api.model
    def normalize_product_data(self,products):

        # products = self.env['muestras.prueba'].search([])
        for product in products:
            exist_product=self.search([
                ('product_id','=',product.id)
            ],limit=1)
            print(F'recorriendo el registro:{exist_product}')
            regions={
                'United States':product.quantityUSA,
                'Europe':product.quantityEU,
                'Asia':product.quantityAsia,
                }

            for regionTemp,quantityTemp in regions.items():
                # Crear un registro para el precio de USA
                existing_record=self.search([
                    ('product_id','=',product.id),
                    ('region','=',regionTemp)
                ],limit=1)
                
                if existing_record:
                    print(f"match:{self.product_id}")
                    existing_record.write({
                        'quantity':quantityTemp,
                        'variety':product.variety,
                        'program':product.program,
                        'category':product.category,
                        'location':product.location,
                        'warehouse':product.warehouse,
                        'country_origin':product.country_origin,
                        'lote':product.lote,
                        'internal_code':product.internal_code,
                        'edition':product.edition,
                        'process':product.process,
                        'score':product.score,
                        'macroprofile':product.macroprofile,
                        'price':product.price_usd,
                        'fprocess':product.fprocess,
                        'sca_entrega':product.sca_entrega,
                        'sca_actual':product.sca_actual,
                        'sku':product.sku,
                        'condicion':product.condicion,
                        'pricelb':product.pricelb,
                        'offeringCat':product.offeringCat,
                        'total_quantity':product.quantity_kg,
                        'disp_inventario':'inv',
                        'date_create':product.date_create,
                        'uom':product.uom,
                        'producer':product.producer,
                        'freshness':product.freshness,
                        'farm':product.farm,
                        'altitude':product.altitude,
                        'available_status':product.available,
                        'date_create':product.date_create,
                        'equation_project':product.equation_project.id,
                    })
                else:
                    if quantityTemp:
                        self.create({
                            'product_id':product.id,
                            'region': regionTemp,
                            'quantity': quantityTemp,
                            'disponible':quantityTemp,
                            'fuente':'Proyectos',
                            'project':product.project,
                            'variety':product.variety,
                            'program':product.program,
                            'category':product.category,
                            'location':product.location,
                            'warehouse':product.warehouse,
                            'country_origin':product.country_origin,
                            'lote':product.lote,
                            'internal_code':product.internal_code,
                            'edition':product.edition,
                            'process':product.process,
                            'score':product.score,
                            'macroprofile':product.macroprofile,
                            'price':product.price_usd,
                            'fprocess':product.fprocess,
                            'sca_entrega':product.sca_entrega,
                            'sca_actual':product.sca_actual,
                            'sku':product.sku,
                            'condicion':product.condicion,
                            'pricelb':product.pricelb,
                            'offeringCat':product.offeringCat,
                            'total_quantity':product.quantity_kg,
                            'disp_inventario':'inv',
                            'date_create':product.date_create,
                            'uom':product.uom,
                            'producer':product.producer,
                            'freshness':product.freshness,
                            'farm':product.farm,
                            'altitude':product.altitude,
                            'available_status':product.available,
                            'date_create':product.date_create,
                            'equation_project':product.equation_project.id,
        
                        })
                        self.env.cr.commit()

                        

            # print("Datos normalizados correctamente.")

    @api.model
    def upsert_inventary(self,product):
        print("hola")
        # products=self.env['muestras.inventario'].search([])
        # for product in products:
        existing_record=self.search([
            ('inventary_id','=',product.id)
        ],limit=1)
        if existing_record:
            print(product.name)
            existing_record.write({
                'quantity':product.quantity_kg,
                'region':product.region,
                'fuente':'Inventario SPOT',
                'equation_project':product.equation_project.id,
                'project':product.project,
                'variety':product.variety,
                'program':product.program,
                'category':product.category,
                'location':"USA",
                'warehouse':product.warehouse,
                'country_origin':product.country_origin,
                'lote':product.lote,
                'internal_code':product.internal_code,
                'edition':product.edition,
                'process':product.process,
                'score':product.score,
                'macroprofile':product.macroprofile,
                'price':product.price_usd, 
                'fprocess':product.fprocess,
                'sca_entrega':product.sca_entrega,
                'sca_actual':product.sca_actual,
                'sku':product.sku,
                'condicion':product.condicion,
                'pricelb':product.pricelb,
                'offeringCat':product.offeringCat,
                'total_quantity':product.quantity_kg,
                'disp_inventario':'inv',
                'date_create':product.date_create,
                'uom':product.uom,
                'producer':product.producer,
                'available_status':product.available,
            })
        else:
            if product.quantity_kg:
                self.create({
                    'inventary_id':product.id,
                    'region':product.region,
                    'quantity':product.quantity_kg,
                    'fuente':'Inventario SPOT',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':"USA",
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.edition,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'price':product.price_usd,
                    'fprocess':product.fprocess,
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'inv',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,
        
                })
            self.env.cr.commit()


    ####### BUTTTONS #############

  
    def disponible_button(self):
        products=self.env['muestras.disponible'].search([])
        region='All Regions'
        for product in products:
            # for region in regions:
            print('Hola')
            existing_record=self.search([
                ('disponible_id','=',product.id)
            ],limit=1)

            if existing_record:
                existing_record.write({
                    'quantity':product.quantity_kg,
                    'region':region,
                    'fuente':'Disponibles',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':product.location,
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.main_category.name,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'pricelb': product.price_usd, 
                    'fprocess':product.fprocess,
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,  
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'dis',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,
        })

            else:
                if product.quantity_kg:
                    self.create({
                        'disponible_id':product.id,
                        'region':region,
                        'quantity':product.quantity_kg,
                        'fuente':'Disponibles',
                        'equation_project':product.equation_project.id,
                        'project':product.project,
                        'variety':product.variety,
                        'program':product.program,
                        'category':product.category,
                        'location':product.location,
                        'warehouse':product.warehouse,
                        'country_origin':product.country_origin,
                        'lote':product.lote,
                        'internal_code':product.internal_code,
                        'edition':product.main_category.name,
                        'process':product.process,
                        'score':product.score,
                        'macroprofile':product.macroprofile,
                        'pricelb': product.price_usd,
                        'fprocess':product.fprocess,
                        'sca_entrega':product.sca_entrega,
                        'sca_actual':product.sca_actual,
                        'sku':product.sku,
                        'condicion':product.condicion,
                        'pricelb':product.pricelb,
                        'offeringCat':product.offeringCat,
                        'total_quantity':product.quantity_kg,
                        'disp_inventario':'dis',
                        'date_create':product.date_create,
                        'uom':product.uom,
                        'producer':product.producer,
                        'available_status':product.available,
        
                    })
                    self.env.cr.commit()

    


    def spotEU_button(self):
        products=self.env['muestras.spoteu'].search([])
        for product in products:
            existing_record=self.search([
                ('spotEU_id','=',product.id)
            ],limit=1)
            if existing_record:
                existing_record.write({
                    'quantity':product.quantity_kg,
                    'region':'Europe',
                    'fuente':'SPOT EU Temporary',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':"Europe",
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.edition,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'price':product.price_usd,    
                    'fprocess':product.fprocess, 
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'inv',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,

                })
            else:
                if product.quantity_kg:
                    self.create({
                        'spotEU_id':product.id,
                        'region':'Europe',
                        'quantity':product.quantity_kg,
                        'fuente':'Disponibles',
                        'equation_project':product.equation_project.id,
                        'project':product.project,
                        'variety':product.variety,
                        'program':product.program,
                        'category':product.category,
                        'location':"Europe",
                        'warehouse':product.warehouse,
                        'country_origin':product.country_origin,
                        'lote':product.lote,
                        'internal_code':product.internal_code,
                        'edition':product.edition,
                        'process':product.process,
                        'score':product.score,
                        'macroprofile':product.macroprofile,
                        'price':product.price_usd,  
                        'fprocess':product.fprocess,
                        'sca_entrega':product.sca_entrega,
                        'sca_actual':product.sca_actual,
                        'sku':product.sku,
                        'condicion':product.condicion,
                        'pricelb':product.pricelb,
                        'offeringCat':product.offeringCat,
                        'total_quantity':product.quantity_kg,
                        'disp_inventario':'inv',
                        'date_create':product.date_create,
                        'uom':product.uom,
                        'producer':product.producer,
                        'available_status':product.available,
                    })
                    self.env.cr.commit()

    
    def inventary_button(self):
        print("hola")
        products=self.env['muestras.inventario'].search([])
        for product in products:
            existing_record=self.search([
                ('inventary_id','=',product.id)
            ],limit=1)
            if existing_record:
                print(product.name)
                existing_record.write({
                    'quantity':product.quantity_kg,
                    'region':product.region,
                    'fuente':'Inventario SPOT',
                    'equation_project':product.equation_project.id,
                    'project':product.project,
                    'variety':product.variety,
                    'program':product.program,
                    'category':product.category,
                    'location':"USA",
                    'warehouse':product.warehouse,
                    'country_origin':product.country_origin,
                    'lote':product.lote,
                    'internal_code':product.internal_code,
                    'edition':product.edition,
                    'process':product.process,
                    'score':product.score,
                    'macroprofile':product.macroprofile,
                    'price':product.price_usd, 
                    'fprocess':product.fprocess,
                    'sca_entrega':product.sca_entrega,
                    'sca_actual':product.sca_actual,
                    'sku':product.sku,
                    'condicion':product.condicion,
                    'pricelb':product.pricelb,
                    'offeringCat':product.offeringCat,
                    'total_quantity':product.quantity_kg,
                    'disp_inventario':'inv',
                    'date_create':product.date_create,
                    'uom':product.uom,
                    'producer':product.producer,
                    'available_status':product.available,
                })
            else:
                if product.quantity_kg:
                    self.create({
                        'inventary_id':product.id,
                        'region':product.region,
                        'quantity':product.quantity_kg,
                        'fuente':'Inventario SPOT',
                        'equation_project':product.equation_project.id,
                        'project':product.project,
                        'variety':product.variety,
                        'program':product.program,
                        'category':product.category,
                        'location':"USA",
                        'warehouse':product.warehouse,
                        'country_origin':product.country_origin,
                        'lote':product.lote,
                        'internal_code':product.internal_code,
                        'edition':product.edition,
                        'process':product.process,
                        'score':product.score,
                        'macroprofile':product.macroprofile,
                        'price':product.price_usd,
                        'fprocess':product.fprocess,
                        'sca_entrega':product.sca_entrega,
                        'sca_actual':product.sca_actual,
                        'sku':product.sku,
                        'condicion':product.condicion,
                        'pricelb':product.pricelb,
                        'offeringCat':product.offeringCat,
                        'total_quantity':product.quantity_kg,
                        'disp_inventario':'inv',
                        'date_create':product.date_create,
                        'uom':product.uom,
                        'producer':product.producer,
                        'available_status':product.available,
        
                })
            self.env.cr.commit()





class TestModel(models.Model):
    _name = 'muestras.testmodel'
    _description = 'Test Model'

    name = fields.Text(string="Name")
    value = fields.Float(string="Value")

    @api.model
    def funckkn(self):
        print("Iniciando creación de registro")
        try:
            record=self.create({
                'name':"prueba3",
                'value':2.0,
            })
            self.env.cr.commit()
            print(f"Registro creado:{record}")
            return record
        except Exception as e:
            print(f"Error en el self.create():{e}")
    



