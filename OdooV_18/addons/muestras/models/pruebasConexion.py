from odoo import models, fields, api
import requests
import logging
from odoo.exceptions import ValidationError
from odoo import _
_logger = logging.getLogger(__name__)

class Prueba(models.Model):
    _name = "muestras.prueba"
    _description = "Inventario Proyectos ATLAS"
    _inherit=['muestras.father','mail.thread','mail.activity.mixin']
    _rec_name="lote"


    # --- Temporeales--- Tanr pontro arregle ele problema de las acrualizaicones se soluciona --- 
    project = fields.Char(string='Project', required=True, default="",compute=None)
    variety = fields.Text(string='Variety',compute=None)
    program = fields.Text(string='Program',compute=None)
    fprocess = fields.Char(string="Fermentation Process",compute=None)
    town = fields.Char(string="Origin",compute=None)
    mcp = fields.Char(string="Macroprofile",compute=None)
    process = fields.Char(string="Drying Process",compute=None)

    ### General Info ###
    available=fields.Selection(
        selection=[
            ('dis','Disponible'),
            ('nodis','No Disponible'),
        ],
        string="Availability",default='dis',required=True,compute='no_disp',store=True,readonly=False,tracking=True)
    offeringCat = fields.Many2many('muestras.offeringcat',string="Portafolio Categories")    
    dis_temporarly_button = fields.Boolean(string="Availability Temporarly Button",default=True)
    update_mode=fields.Selection(
        selection=[
            ('odoo','Created and Updated in Odoo'),
            ('atlas','Created and Updated from Atlas')
        ],string="Update Mode",default='atlas',required=True)

    ### Inventory ###
    peso_neto = fields.Float(string="Initial Quantity",required=False)
    peso_salida = fields.Float(string="Output Weight",required=False)
    quantityUSA = fields.Float(string="USA Quantity",store=True,tracking=True) 
    quantityEU = fields.Float(string ="EU Quantity",store=True,tracking=True)
    quantityAsia = fields.Float(string="Asia Quantity",store=True,tracking=True)
    needsRegionUpdate = fields.Boolean(string="Needs Region Update")
    update_boolean = fields.Boolean(string="Updated All Products")

    ### Price ###
    price_us = fields.Float(string="Price US/kg",required=False,tracking=True)
    pricelb = fields.Float(string="USD/lb",required=False,tracking=True)

    ### API ###
    last_execution_date = fields.Datetime(string="Last Execution",required=False)
    entry_id = fields.Char(string="Entry ID",required=False)


    ### Methods ###
    @api.model
    def default_model(self,fields):
        res=super(Prueba,self).default_get(fields)
        self._atlas()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Prueba, self).create(vals_list)
        for record in records:
            if record.needsRegionUpdate == False:
                self.env['muestras.allproducts'].normalize_product_data(record)
        return records


    def write(self, vals):
        if self.env.context.get('skip_normalization'):
            return super(Prueba, self).write(vals)
        result = super(Prueba, self).write(vals)
        if self.needsRegionUpdate == False:
            self.env['muestras.allproducts'].normalize_product_data(self)
            if self.available=='dis':
                self.with_context(skip_normalization=True).write({'update_boolean': True})
        return result
    
    @api.constrains('quantityUSA','quantityEU','quantityAsia')
    def _cheksum_percent(self):
        for record in self:
                total_sum = record.quantityUSA + record.quantityAsia + record.quantityEU
                if record.quantity_kg!=0:
                    if total_sum !=record.quantity_kg:      
                        raise ValidationError(_(
                            "Lot %(lote)s: For the product, the sum of the fields must be exactly %(expected).2f. "
                            "It is currently %(actual).2f."
                        ) % {
                            'lote': record.lote,
                            'expected': record.quantity_kg,
                            'actual': total_sum
                        })  
                


    @api.onchange('quantity_kg','quantityUSA','quantityEU','quantityAsia','available')
    def _needsRegionUpdate(self):
        for record in self:
            total_sum = record.quantityUSA + record.quantityAsia + record.quantityEU
            if record.quantity_kg!=0 and record.available=='dis':
                if total_sum!=record.quantity_kg:
                    record.needsRegionUpdate = True
                else : record.needsRegionUpdate = False 
            elif record.available =='nodis':
                record.needsRegionUpdate = False               
    

    @api.depends('quantity_kg')             
    def no_disp(self):
        for record in self:
            if record.quantity_kg==0:
                record.available='nodis'


    def update(self):   
        self._atlas()

    @api.model
    def atlas(self):
        urlToken = 'https://www.atlas-grano.com/api/token/'
        urlConnection = 'https://www.atlas-grano.com/api/inventory/consolidated/'
        _logger.info("Iniciando carga de datos desde la API externa")

        payloadToken = {
            "username": "api_user",
            "password": "D9cn82M>dSCoP7/)Ur^&8"
        }

        try:
            # Solicitar el token
            response = requests.post(urlToken, json=payloadToken)
            if response.status_code == 200:
                access = response.json().get("access")
                _logger.info("Token obtenido correctamente: %s", access)

                # Configurar el encabezado con el token
                headerConnection = {"Authorization": f"Bearer {access}"}
                importData = requests.get(urlConnection, headers=headerConnection)  
                if importData.status_code == 200:
                    _logger.info("Conexión exitosa a la API de Atlas")
                    datos = importData.json()
                    lotes = [item['lote'] for item in datos]
                    products=self.env['muestras.prueba'].search([('quantity_kg','!=',0)])

                    for prod in products:
                        if prod.lote not in lotes and prod.update_mode == 'atlas'and prod.available=='dis':
                            prod.available='nodis'
                            prod.peso_neto=0
                            prod.quantity_kg=0
                            prod.quantityUSA=0
                            prod.quantityEU=0
                            prod.quantityAsia=0
                            prod.needsRegionUpdate=False
                    for item in datos:
                        country_map = {'COL':"Colombia",'PAN':"Panama",'MEX':"Mexico"}
                        country_name = country_map.get(item.get('country_code'),' ')
                        existing_record=self.search([
                            ('lote','=',item.get('lote'))
                        ],limit=1)
                        equation_project = self.env['equation.coffee_project'].search([('name','=',item.get("project_name"))])
                        equation_program = self.env['equation.coffee_program'].search([('name','=',item.get("programa"))])
                        equation_varietal = self.env['equation.coffee_varietal'].with_context(lang='en_CO').search([('name','=',item.get("variedad"))])
                        if not existing_record:
                            record = self.create({
                                'lote': item.get("lote") or 'Sin Lote',
                                'peso_neto': item.get("total_entradas") or 0.0,
                                'quantity_kg': item.get("inventario_actual") or 0.0,
                                'peso_salida': item.get("total_salidas") or 0.0,
                                'project': item.get("project_name") or 'Desconocido',
                                'equation_project': equation_project.id or None,
                                'equation_program': equation_program.id or None,
                                'equation_varietal':equation_varietal.id or None,
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
                                'available':'dis',
                                'update_mode':'atlas',
                                'needsRegionUpdate':True,

                            })
                        if existing_record:
                            if item.get('quantity_kg') == existing_record.quantityUSA + existing_record.quantityEU + existing_record.quantityAsia:
                                needsUpdate = False
                            else : needsUpdate = True
                            if existing_record.update_mode =='odoo':
                                continue
                            existing_record.write({
                                'sca_actual':item.get("sca_score") or 0.0,
                                'lote': item.get("lote") or 'Sin Lote',
                                'peso_neto': item.get("total_entradas") or 0.0,
                                'quantity_kg': item.get("inventario_actual") or 0.0,
                                'peso_salida': item.get("total_salidas") or 0.0,
                                'project': item.get("project_name") or 'Desconocido',
                                'equation_project': equation_project.id or None,
                                'equation_program': equation_program.id or None,
                                'equation_varietal':equation_varietal.id or None,
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
                                'available':'dis',
                                'needsRegionUpdate':needsUpdate,
                            })
                        self.env.cr.commit()
                        _logger.info("Registro creado para lote: %s", item.get("lote_number"))
                    self.write({'last_execution_date': fields.Datetime.now()})
                else:
                    error_message = f"Error en la conexión con Atlas Grano: código de estado {importData.status_code}"
                    _logger.error(error_message)
            else:
                error_message = f"No se pudo obtener el token: código de estado {response.status_code}"
                _logger.error(error_message)
        except requests.exceptions.RequestException as e:
            error_message = f"Error en la conexión con la API externa: {e}"
            _logger.error(error_message)
        return {"mensaje": "Actualización completada con éxito"}


class PruebaLog(models.Model):
    _name = "muestras.pruebalog"
    _description = "Log de ejecuciones de la función de conexión con Atlas"

    execution_date = fields.Datetime(string="Fecha de Ejecución", required=True)
    status = fields.Selection([('Success', 'Success'), ('Error', 'Error'), ('Exception', 'Exception')], string="Estado", required=True)
    details = fields.Text(string="Detalles")




