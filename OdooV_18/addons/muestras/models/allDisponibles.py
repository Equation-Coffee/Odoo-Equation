from odoo import models, fields, api

class CustomModel(models.Model):
    _name = 'muestras.alldisponibles'
    _description = 'Simulate Full Join'

    _description = 'All Products by Region'
    _rec_name="product_id"

    # Relación con el producto originalM
    product_id = fields.Many2one('muestras.product',string='Parent Product',required=False)
    disponible_id = fields.Many2one('muestras.disponible',string='Parent Disponible')
    name=fields.Text(string="Product Name")
    # Región asociada al producto
    region=fields.Text(string="Region")
    # region = fields.Selection([
    #     ('usa', 'USA'),
    #     ('eu', 'Europe'),
    #     ('asia', 'Asia')
    # ], string='Region', required=True)
    # Cantidad disponible en la región
    quantity = fields.Float(string='Quantity',required=False,store=True,compute="_actualize_quantity")
    booking = fields.Float(string="Booking Quantity")
    sale = fields.Float(string="Sold Quantity")
    avalible=fields.Float(string="Avalible Quantity")
    price=fields.Float(string="Price")

    project = fields.Char(string='Nombre del Proyecto')
    variety = fields.Text(string='Variedad')
    program = fields.Text(string='Program')
    category = fields.Text(string = 'Categoria')
    location =fields.Char(string="Location")
    warehouse=fields.Char(string="Warehouse")
    country_origin=fields.Char(string="Country of Origin")
    lote=fields.Char(string="lote")
    internal_code=fields.Char(string="Internal Code")
    edition=fields.Char(string="edition")
    process=fields.Char(string="Process")
    score=fields.Integer(string="Score")
    macroprofile=fields.Char(string="Macro-profile")
    referencia_origen = fields.Reference(
        selection=[
            ('modelo.productos.region_a', 'Modelo Región A'),
            ('modelo.productos.region_b', 'Modelo Región B'),
            ('modelo.productos.region_c', 'Modelo Región C'),
        ],
        string='Referencia al Producto Original'
    )





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


    @api.depends('product_id.quantityEU')
    def _actualize_quantity(self):
        products = self.env['muestras.product'].search([])

        # Iterar sobre cada producto y crear registros normalizados
        for product in products:
            print(F'recorriendo el registro:{product}')
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
                    })
                else:

                    if product.quantityUSA and regionTemp=="United States":
                        self.create({
                            'product_id':product.id,
                            'region': "United States",
                            'quantity': product.quantityUSA,
                            'price':product.price_usd,
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
                        })
                        self.env.cr.commit()
                    # Crear un registro para el precio de Asia
                    if product.quantityAsia and regionTemp=="Asia":
                        self.create({
                            'product_id': product.id,
                            'region': 'Asia',
                            'quantity': product.quantityAsia,
                            'price':product.price_usd,
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
                        })
                        self.env.cr.commit()

    @api.model
    def disponible_upsert(self):
        products=self.env['muestras.disponible'].search([])
        regions=['United States','Europe','Asia']
        for product in products:
            for region in regions:
                print('Hola')
                existing_record=self.search([
                    ('disponible_id','=',product.id),
                    ('region','=',region)
                ],limit=1)

                if existing_record:
                    exisiting_record.write({
                        'quantity':product.quantity_kg
                    })

                else:
                    self.create({
                        'disponible_id':product_id,
                        'region':region,
                        'quantity':quantity_kg
                    })
                    self.env.cr.commit()

             
        
    @api.model
    def normalize_product_data(self):
        # Obtener todos los productos
        products = self.env['muestras.product'].search([])

        # Iterar sobre cada producto y crear registros normalizados
        for product in products:
            print(F'recorriendo el registro:{product}')
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
                    })
                else:

                    if product.quantityUSA and regionTemp=="United States":
                        self.create({
                            'product_id':product.id,
                            'region': "United States",
                            'quantity': product.quantityUSA,
                        })
                        self.env.cr.commit()
                    # Crear un registro para el precio de Europa
                    if product.quantityEU and regionTemp=="Europe":
                        print('Europa')
                        self.create({
                            'product_id': product.id,
                            'region': "Europe",
                            'quantity': product.quantityEU,
                        })
                        self.env.cr.commit()
                    # Crear un registro para el precio de Asia
                    if product.quantityAsia and regionTemp=="Asia":
                        self.create({
                            'product_id': product.id,
                            'region': 'Asia',
                            'quantity': product.quantityAsia,
                        })
                        self.env.cr.commit()

        print("Datos normalizados correctamente.")



