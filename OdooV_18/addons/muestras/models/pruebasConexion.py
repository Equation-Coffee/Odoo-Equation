from odoo import models, fields, api
import requests
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class Prueba(models.Model):
    _name = "muestras.prueba"
    _description = "Inventario Proyectos ATLAS"
    _inherit="muestras.father"
    _rec_name="lote"


    # --- Temporeales--- Tanr pontro arregle ele problema de las acrualizaicones se soluciona --- 
    project = fields.Char(string='Proyecto', required=True, default="",compute=None)
    variety = fields.Text(string='Variedad',compute=None)
    program = fields.Text(string='Categoria',compute=None)
    fprocess=fields.Char(string="Proceso de Fermentación",compute=None)
    town=fields.Char(string="Region de Origen",compute=None)
    mcp=fields.Char(string="Macro-Perfil",compute=None)
    process=fields.Char(string="Proceso",compute=None) ## Proceso de lavado

    peso_neto = fields.Float(string="Cantidad Inicial",required=False)
    peso_salida = fields.Float(string="Peso  salida",required=False)
    price_usd=fields.Float(string="Precio por Kilo",required=False)
    pricelb=fields.Float(string="USD/lb",required=False)
    last_execution_date = fields.Datetime(string="Última Ejecución",required=False)
    entry_id=fields.Char(string="Entry ID",required=False)
    score=fields.Integer(string="SCA")
    macroprofile=fields.Char(string="Perfil Sensorial")
    mcp=fields.Char(string="Macro-Perfil")
    sca_entrega=fields.Float(string="SCA Entrega")
    sca_actual=fields.Float(string="SCA Actual")
    sku=fields.Char(string="SKU")
    condicion=fields.Char(string="Condición")
    quantityUSA= fields.Float(string="Cantidad USA",store=True) 
    quantityEU= fields.Float(string ="Cantidad EU",store=True)
    quantityAsia= fields.Float(string="Cantidad Asia",store=True)
    producer=fields.Char(string="Productor")
    freshness=fields.Integer(string="Frescura")
    farm=fields.Char(string="Finca")
    edition=fields.Char(string="Edicion")
    altitude=fields.Float(string="Altitud")
    offeringCat=fields.Many2many(
        'muestras.offeringcat',
        string="Categorias Portafolio"
    )
    uom=fields.Selection(
        selection=[
            ('kg','Kilogramos'),
            ('lb','Libras'),
        ],
        string="Unidad de Medida",
        default=None,
        required=True
        )
    available=fields.Selection(
        selection=[
            ('dis','Disponible'),
            ('nodis','No Disponible'),
        ],
        string="Disponibilidad",
        default='dis',
        required=True,compute='no_disp',store=True,readonly=False
    )
    date_create=fields.Date(string="Fecha de Creación")
    dis_temporarly_button = fields.Boolean(string="Disponible_temporary_Value",default=True)

    @api.model
    def default_model(self,fields):
        res=super(Prueba,self).default_get(fields)

        self._atlas()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        # Crear el registro normalmente
        records = super(Prueba, self).create(vals_list)

        # Llamar al método upsert en el modelo relacionado
        for record in records:
            self.env['muestras.allproducts'].normalize_product_data(record)

        return records

    def write(self, vals):
        # Actualizar el registro normalmentes
        result = super(Prueba, self).write(vals)

        # Llamar al método upsert en el modelo relacionado
        self.env['muestras.allproducts'].normalize_product_data(self)

        return result
    
    @api.constrains('quantityUSA','quantityEU','quantityAsia')
    def _cheksum_percent(self):
        for record in self:
                total_sum = record.quantityUSA + record.quantityAsia + record.quantityEU
                if record.quantity_kg!=0:
                    if total_sum !=record.quantity_kg:
                        raise ValidationError(
                            "Lote {}: Para el producto, la suma de los campos debe ser exactamente {}. Actualmente es {:.2f}".format(
                                record.lote, record.quantity_kg, total_sum
                            )
                        )
                    
    @api.depends('quantity_kg')
    def no_disp(self):
        for record in self:
            if record.quantity_kg==0:
                record.available='nodis'


    def update(self):   
        self._atlas()

    @api.model
    def _atlas(self):
        print('JAJAJAJAJAAJAJAJAJAJAJAJA')
        urlToken = 'https://www.atlas-grano.com/api/token/'
        urlConnection = 'https://www.atlas-grano.com/api/inventory/consolidated/'
        _logger.info("Iniciando carga de datos desde la API externa")

        # Datos de autenticación
        payloadToken = {
            "username": "api_user",
            "password": "D9cn82M>dSCoP7/)Ur^&8"
        }

        try:
            # Solicitar el token
            response = requests.post(urlToken, json=payloadToken)
            if response.status_code == 200:
                data = response.json()
                access = data.get("access")
                _logger.info("Token obtenido correctamente: %s", access)

                # Configurar el encabezado con el token
                headerConnection = {
                    "Authorization": f"Bearer {access}"
                }

                # Realizar la solicitud de datos
                importData = requests.get(urlConnection, headers=headerConnection)
                if importData.status_code == 200:
                    _logger.info("Conexión exitosa a la API de Atlas")
                    datos = importData.json()
                    print('kakakakakaka')
                    lotes = [item['lote'] for item in datos]
                    print(lotes)
                    products=self.env['muestras.prueba'].search([('quantity_kg','!=',0)])

                    for prod in products:
                        if prod.lote not in lotes:
                            print('No esta',prod.lote)
                            prod.available='nodis'
                            prod.peso_neto=0
                            prod.quantity_kg=0
                            prod.quantityUSA=0
                            prod.quantityEU=0
                            prod.quantityAsia=0

                    


                    # Crear registros en Odoo
                    for item in datos:
                        
                        if item.get('country_code')=='COL':
                            country_name="Colombia"
                        if item.get('country_code')=='PAN':
                            country_name="Panama"
                        if item.get('country_code')=='MEX':
                            country_name="Mexico"
                        existing_record=self.search([
                            ('lote','=',item.get('lote'))
                        ],limit=1)

                        if not existing_record:
                            record = self.create({
                                'lote': item.get("lote") or 'Sin Lote',
                                'peso_neto': item.get("total_entradas") or 0.0,
                                'quantity_kg': item.get("inventario_actual") or 0.0,
                                'peso_salida': item.get("total_salidas") or 0.0,
                                'project': item.get("project_name") or 'Desconocido',
                                'program': item.get("programa") or 'Desconocido',
                                'variety': item.get("variedad") or 'Desconocido',
                                'entry_id': item.get("entry_id") or  0,
                                'price_usd': item.get("precio_kilo"),
                                'location' : country_name,
                                'country_origin':country_name,
                                'warehouse' : item.get("bodega"),
                                'edition' :item.get('edicion_lote'),
                                'process':item.get("proceso"),
                                'score':item.get("sca_score"),
                                'sca_actual':item.get("sca_score"),
                                'macroprofile':item.get("macro_perfil"),
                                'uom':'kg',
                                'producer':item.get("productor"),
                                'freshness':item.get("frescura"),
                                'farm':item.get("finca_terroir"),
                                'altitude':float(item.get("altitud") or 0) if str(item.get("altitud")).replace('.', '', 1).isdigit() else 0,
                                'available':'dis'

                            })

                        if existing_record:
                            existing_record.write({
                                
                                'sca_actual':item.get("sca_score") or 0.0,
                                'lote': item.get("lote") or 'Sin Lote',
                                'peso_neto': item.get("total_entradas") or 0.0,
                                'quantity_kg': item.get("inventario_actual") or 0.0,
                                'peso_salida': item.get("total_salidas") or 0.0,
                                'project': item.get("project_name") or 'Desconocido',
                                'program': item.get("programa") or 'Desconocido',
                                'variety': item.get("variedad") or 'Desconocido',
                                'entry_id': item.get("entry_id") or  0,
                                'price_usd': item.get("precio_kilo"),
                                'location' : country_name,
                                'country_origin':country_name,
                                'warehouse' : item.get("bodega"),
                                'edition' :item.get('edicion_lote'),
                                'process':item.get("proceso"),
                                'score':item.get("sca_score"),
                                # 'sca_actual':item.get("sca_score"),
                                'macroprofile':item.get("macro_perfil"),
                                'uom':'kg',
                                'producer':item.get("productor"),
                                'freshness':item.get("frescura"),
                                'farm':item.get("finca_terroir"),
                                'altitude':float(item.get("altitud") or 0) if str(item.get("altitud")).replace('.', '', 1).isdigit() else 0,
                                'available':'dis'

                            })


                        self.env.cr.commit()
                        _logger.info("Registro creado para lote: %s", item.get("lote_number"))
                        

                    # Actualizar el campo de última ejecución
                    self.write({'last_execution_date': fields.Datetime.now()})

                else:
                    error_message = f"Error en la conexión con Atlas Grano: código de estado {importData.status_code}"
                    _logger.error(error_message)
            else:
                error_message = f"No se pudo obtener el token: código de estado {response.status_code}"
                _logger.error(error_message)
                # self.env.user.notify_info(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"Error en la conexión con la API externa: {e}"
            _logger.error(error_message)
            # self.env.user.notify_info(error_message)


# Modelo de log para registrar las ejecuciones
class PruebaLog(models.Model):
    _name = "muestras.pruebalog"
    _description = "Log de ejecuciones de la función de conexión con Atlas"

    execution_date = fields.Datetime(string="Fecha de Ejecución", required=True)
    status = fields.Selection([('Success', 'Success'), ('Error', 'Error'), ('Exception', 'Exception')], string="Estado", required=True)
    details = fields.Text(string="Detalles")


class Conexion(models.Model):
    _name="muestras.conexion"
    _description="conexion triple hpta"

    lote = fields.Text(string="Número de Lote")
    peso_neto = fields.Float(string="Peso Neto",required=False)
    peso_disponible = fields.Float(string="Peso Disponible",required=False)
    peso_salida = fields.Float(string="Peso  salida",required=False)
    proyecto = fields.Char(string="Proyecto",required=False)
    programa = fields.Char(string="Programa",required=False)
    variedad = fields.Char(string="Variedad",required=False)
    last_execution_date = fields.Datetime(string="Última Ejecución",required=False)
    entry_id=fields.Char(string="Entry ID",required=False)


    # @api.model
    # def default_get(self,fields):
    #     res=super(Prueba,self).default_get(fields)
    #     if self.env.context.get('execute_function_on_load'):
    #         self._atlas()



    @api.model
    def _atlas(self):
        print('JAJAJAJAJAAJAJAJAJAJAJAJA')
        urlToken = 'https://www.atlas-grano.com/api/token/'
        urlConnection = 'https://www.atlas-grano.com/api/inventory/consolidated/'
        _logger.info("Iniciando carga de datos desde la API externa")

        # Datos de autenticación
        payloadToken = {
            "username": "api_user",
            "password": "D9cn82M>dSCoP7/)Ur^&8"
        }

        try:
            # Solicitar el token
            response = requests.post(urlToken, json=payloadToken)
            if response.status_code == 200:
                data = response.json()
                access = data.get("access")
                _logger.info("Token obtenido correctamente: %s", access)

                # Configurar el encabezado con el token
                headerConnection = {
                    "Authorization": f"Bearer {access}"
                }

                # Realizar la solicitud de datos
                importData = requests.get(urlConnection, headers=headerConnection)
                if importData.status_code == 200:
                    _logger.info("Conexión exitosa a la API de Atlas")
                    datos = importData.json()
                    print('kakakakakaka')
                    print(datos)
                    print('mmmm')

                    # Crear registros en Odoo
                    for item in datos:
                        # print(item.get('lote'))
                        # print(type(item.get('lote')))
                        record = self.create({
                            'lote': item.get("lote") or 'Sin Lote',
                            'peso_neto': item.get("total_entradas") or 0.0,
                            'peso_disponible': item.get("inventario_actual") or 0.0,
                            'peso_salida': item.get("total_salidas") or 0.0,
                            'proyecto': item.get("project_name") or 'Desconocido',
                            'programa': item.get("programa") or 'Desconocido',
                            'variedad': item.get("variedad") or 'Desconocido',
                            'entry_id': item.get("entry_id") or  0,
                        })

                        self.env.cr.commit()
                        _logger.info("Registro creado para lote: %s", item.get("lote_number"))

                    # Actualizar el campo de última ejecución
                    self.write({'last_execution_date': fields.Datetime.now()})

                    # Crear un registro en el modelo de log
                    self.env['muestras.pruebalog'].create({
                        'execution_date': fields.Datetime.now(),
                        'status': 'Success'
                    })

                    # # Notificación al usuario
                    # self.env.user.notify_info("Conexión exitosa y datos cargados correctamente")
                else:
                    error_message = f"Error en la conexión con Atlas Grano: código de estado {importData.status_code}"
                    _logger.error(error_message)
                    # self.env.user.notify_info(error_message)

                    # Registrar error en el modelo de log
                    self.env['muestras.pruebalog'].create({
                        'execution_date': fields.Datetime.now(),
                        'status': 'Error',
                        'details': error_message
                    })
            else:
                error_message = f"No se pudo obtener el token: código de estado {response.status_code}"
                _logger.error(error_message)
                # self.env.user.notify_info(error_message)

                # Registrar error en el modelo de log
                self.env['muestras.pruebalog'].create({
                    'execution_date': fields.Datetime.now(),
                    'status': 'Error',
                    'details': error_message
                })
        except requests.exceptions.RequestException as e:
            error_message = f"Error en la conexión con la API externa: {e}"
            _logger.error(error_message)
            # self.env.user.notify_info(error_message)

            # Registrar error en el modelo de log
            self.env['muestras.pruebalog'].create({
                'execution_date': fields.Datetime.now(),
                'status': 'Exception',
                'details': str(e)
            })


