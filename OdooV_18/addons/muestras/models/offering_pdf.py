from odoo import models, fields, api,_
import csv
import os 
import logging
from io import BytesIO
from reportlab.pdfgen import canvas
from odoo.exceptions import ValidationError
import base64
import requests
import json



_logger = logging.getLogger(__name__)

class OfferingPDF(models.TransientModel):
    _name='muestras.offering_pdf_wizard'
    _description='Pestaña Emergente para revisar generar el pdf'


# --- Related Fields ---
    field_ids = fields.Many2many(
        'ir.model.fields', 
        string="Campos a Incluir", 
        domain=[('model', '=', 'muestras.disponible')],
        help="Selecciona los campos a mostrar en el informe."
    )   

    state = fields.Selection(
        selection=[
            ('draft',"Draft"),
            ('pdf',"PDF Generated"),
        ],
        string="Status",
        readonly=True,copy=False,index=True,
        default='draft'
    )

    line_id=fields.One2many('muestras.offering_pdf_wizard_line','wizard_id',string="Lineas")
    sequence = fields.Char(string="Consecutivo", readonly=True, default="/")


    # --- Temporales sin seccion ---
    trm = fields.Float(string="USD/COP Exchange Rate")
    price_c = fields.Float(string="Coffee C Price")



    # --- Custmer and Offering info ---
    distribution_type = fields.Selection([
        ('ind', 'Individual'),
        ('mas', 'Masive'),
        ], string="Offer Type",default='ind')
    partner_id=fields.Many2one(comodel_name="res.partner",string="Customer")
    salesperson_header=fields.Many2one(comodel_name="res.users",string="Main Salesperson",required=True,
        domain=lambda self:self._get_salesperson_header_domain())
    salesperson=fields.Many2one(string="Salesperson ",comodel_name="res.users",readonly=True,
        default=lambda self: self.env.user)
    expiration_date=fields.Date(string="Expiration Date",required=True)
    create_date = fields.Date(string = "Creation Date",index=True,readonly=True,default=None)

    pdf_file= fields.Binary(String="PDf")
    pdf_filename= fields.Char(string="Nombre del PDF")
    diff_price = fields.Float(string="Differencial Price",required=True,default=None)
    

    # --- Booleans --- # 
    sku_boolean=fields.Boolean(string='SKU')
    variety_boolean=fields.Boolean(string='Variety')
    fprocess_boolean=fields.Boolean(string='Process')
    origin_boolean=fields.Boolean(string='Origin')
    main_category_boolean=fields.Boolean(string="Main Category")
    second_category_boolean=fields.Boolean(string="Second Category") 
    sca_boolean=fields.Boolean(string='SCA')
    macroprofile_boolean=fields.Boolean(string="Macroprofile")
    sensory_profile_boolean=fields.Boolean(string="Sensory Profile")
    availability_35kg_boolean=fields.Boolean(string="Availability in 35 kg")
    availability_70kg_boolean=fields.Boolean(string="Availability in 70 kg")    
    exw_boolean=fields.Boolean(string="EXW Price US/lb")
    exw_kg_boolean=fields.Boolean(string="EXW Price US/kg")
    exw_eu_boolean=fields.Boolean(string="EXW Price EU/kg")
    spot_usa_boolean=fields.Boolean(string="SPOT Price USD/lb")
    spot_usa_tariffs_boolean = fields.Boolean(string="SPOT Price US/lb (Tariffs)")
    spot_eu_boolean=fields.Boolean(string="SPOT Price EU/kg")   
    fob_usa_boolean=fields.Boolean(string="FOB Price US/lb")
    fob_eu_boolean=fields.Boolean(string="FOB Price EU/kg")
    fwb_usa_boolean=fields.Boolean(string="FWB Price US/lb")
    fwb_eu_boolean=fields.Boolean(string="FWB Price EU/kg")




    main_category_selection=fields.Many2many('muestras.offeringcat',string="Filters for Main Category")
    second_category_selection=fields.Selection(selection=[('default', 'Default')],string="Filters for Second Category")
    origin_selection = fields.Many2many('equation.coffee_origin',string="Filters for Origin")
    fprocess_selection=fields.Many2many('equation.coffee_fermentation_process',relation='ecfp_muestras_offering_pdf_wizard_rel',string="Filters for Fermentation Process")
    variety_selection=fields.Many2many('equation.coffee_varietal',string="Filters for Varietal")
    macp_selection=fields.Many2many('equation.coffee_macroprofile',string="Filters for Macroprofile")
    process_offering_selection=fields.Many2many('equation.coffee_process_offering',relation='ecp_muestras_offering_pdf_wizard_rel',column1='wizard',column2='process',string="Filters for Process")
    number_registers=fields.Integer(string="Number of Coffees",store=True,compute="_number_registers")
    boton_prueba=fields.Boolean(string="PRUEBA")
    

    @api.constrains('distribution_type','partner_id')
    def _check_partner_id_required(self):
        for record in self:
            if record.distribution_type =='ind' and not record.partner_id:
                raise ValidationError("You must provide the 'Customer for individual offers" )

    @api.depends('main_category_selection','origin_selection','fprocess_selection','variety_selection')
    def _number_registers(self):
        filters=[]
        if self.main_category_selection:
            ids=[id for id in self.main_category_selection.ids if isinstance(id,int)]
            if ids:
                filters.append(('main_category.id','in',ids))
        if self.origin_selection:
            ids=[id for id in self.origin_selection.ids if isinstance(id,int)]
            if ids:
                filters.append(('equation_origin_town.id','in',ids))
        if self.fprocess_selection:
            ids=[id for id in self.fprocess_selection.ids if isinstance(id,int)]
            if ids:
                filters.append(('equation_fermentation_process.id','in',ids))
        if self.variety_selection:
            ids=[id for id in self.variety_selection.ids if isinstance(id,int)]
            if ids:
                filters.append(('equation_varietal.id','in',ids))
        records = self.env['muestras.disponible'].search(filters)
        # if self.main_category_selection:
        #     raise ValidationError(f"filters usaddos: {filters}")
        number_records= len(records)
        self.number_registers=number_records

    @api.model
    def _get_salesperson_header_domain(self):
        group = self.env.ref('muestras.muestras_commercial_team_leaders')  
        user_ids = self.env['res.users'].search([('groups_id', 'in', [group.id])])
        return [('id', 'in', user_ids.ids)]

    @api.depends('boton_prueba')
    def _prueba(self):
        if self.main_category_selection:
            raise ValidationError(f"filters usaddos: {filters}")

    @api.depends('main_category_selection')
    def _registers():
        for wizard in self:
            domain = []
            if self.main_category_selection:
                ids=[id for id in self.main_category_selection.ids if isinstance(id,int)]
                if ids:
                    domain.append(('main_category.id','in',ids))
            wizard.coffee_registers=self.evn['muestras.disponible'].search(domain)

    @api.model
    def default_get(self,fields):
        res = super(OfferingPDF,self).default_get(fields)
        products = self.env['muestras.disponible'].search([('available','=','dis')])
        lines=[]
        for product in products:
            lines.append((0,0,{
                'register_id':product.id,
                'equation_varietal':product.equation_varietal if product.equation_varietal else False,
                'equation_varietal_name':product.equation_varietal.name if product.equation_varietal else False,
                'equation_origin':product.equation_origin_town if product.equation_origin_town else False,
                'equation_origin_name':product.equation_origin_town.name if product.equation_origin_town else False,
                'equation_main_category':product.main_category if product.main_category else False,
                'equation_main_category_name': product.main_category.name if product.main_category.name else False,
                'equation_macroprofile': product.equation_macroprofile if product.equation_macroprofile else False,
                'equation_macroprofile_name': product.equation_macroprofile.name if product.equation_macroprofile else False,
                'equation_process_offering':product.equation_fermentation_process if product.equation_fermentation_process else False,
                'equation_process_offering_name':product.equation_fermentation_process.name if product.equation_fermentation_process else False,
                'sca':product.sca_actual,
                'price_fob_usa':str(round(product.price_fob_usa,2)),
                'price_spot_usa':str(round(product.price_spot_usa,2)),
                'price_spot_usa_tariffs':str(round(product.price_spot_usa_tariffs,2)),
                'price_fwb_usa':str(round(product.price_fwb_usa,2)),
                'price_fob_eu':str(round(product.price_fob_eu,2)),
                'price_spot_eu':str(round(product.price_spot_eu,2)),
                'price_fwb_eu':str(round(product.price_fwb_usa,2)),
                'price_exw':str(round(product.price_exw,2)),
                'price_exw_eu':str(round(product.price_exw_eu,2)), 
                'price_exw_kg':str(round(product.price_exw_kg,2)), 

            }))
        trm_register = self.env['muestras.price'].search([['name','=',"USD/COP Exchange Rate"]])
        self.trm = trm_register.value
        price_c_register = self.env['muestras.price'].search([['name','=',"Coffee C Price"]])
        self.price_c = price_c_register.value
        line_prices=[] 
        res.update({
            'line_id':lines ,
            'trm':trm_register.value if trm_register else False,
            'price_c':price_c_register.value if price_c_register else False})

        return res 
    
    @api.onchange('variety_selection','origin_selection','main_category_selection','macp_selection','fprocess_selection')
    def _onchange_filter(self):
        for line in self.line_id:
            if ((not self.variety_selection or line.equation_varietal.id in self.variety_selection.ids) and (not self.origin_selection or line.equation_origin.id in self.origin_selection.ids) and (not self.main_category_selection or line.equation_main_category.id in self.main_category_selection.ids)and (not self.macp_selection or line.equation_macroprofile.id in self.macp_selection.ids)and (not self.fprocess_selection or line.equation_process_offering.id in self.fprocess_selection.ids)):
                line.show_line=True
            else:
                line.show_line=False

    @api.onchange('fob_usa_boolean')
    def _onchange_toggle_fob_usa(self):
        for line in self.line_id:
            line.fob_usa_show = self.fob_usa_boolean

  
    def pdf(self):
        name = self.sequence
        data={
            "commercial_user":self.salesperson_header.name,
            "commercial_mail":self.salesperson_header.login,
            "customer":self.partner_id.name,
            "offering_seq":self.sequence,
            "date":self.create_date.isoformat(),
            "expiration_date":self.expiration_date.isoformat(),
            "sequence":self.sequence,
            "coffees":[],
            "booleans":{
                "Code":1,
                "Origin":1,
                "Process":1,
                "Variety":1,
                "SCA":self.sca_boolean,
                "FOB US/lb":self.fob_usa_boolean,
                "FOB EU/kg":self.fob_eu_boolean,
                "Spot US/lb":self.spot_usa_boolean,
                'Spot US/lb (Tariffs)':self.spot_usa_tariffs_boolean,
                "Spot EU/kg":self.spot_eu_boolean,
                "FWB US/lb":self.fwb_usa_boolean,
                "FWB EU/kg":self.fwb_eu_boolean,
                "EXW US/lb":self.exw_boolean,
                "EXW EU/kg":self.exw_eu_boolean,
                "EXW US/kg":self.exw_kg_boolean,
                "Macroprofile":self.macroprofile_boolean,
                "Availability (bags of 70 Kg)":self.availability_70kg_boolean,
                "Availability (bags of 35 Kg)":self.availability_35kg_boolean,
                "diff_price":0,
            }
            }


        for line in self.line_id:
            if line.show_line == True:
                data['coffees'].append({
                    "Code":line.register_id.lote,
                    "main_category":line.register_id.main_category.name,
                    "Origin":line.register_id.equation_origin_town.name,
                    "Process":line.register_id.equation_fermentation_process.name,
                    "Variety":line.register_id.equation_varietal.name,
                    "SCA":line.register_id.sca_actual,
                    "FOB US/lb":line.price_fob_usa,
                    "FOB EU/kg":line.price_fob_eu,
                    "Spot US/lb":line.price_spot_usa,
                    'Spot US/lb (Tariffs)':line.price_spot_usa_tariffs,
                    "Spot EU/kg":line.price_spot_eu,
                    "FWB US/lb":line.price_fwb_usa,
                    "FWB EU/kg":line.price_fwb_eu,
                    "EXW US/lb":line.price_exw,
                    "EXW EU/kg":line.price_exw_eu,
                    "EXW US/kg":line.price_exw_kg,
                    "Macroprofile":line.register_id.equation_macroprofile.name,
                    "Availability (bags of 70 Kg)":line.register_id.availability_70kg,
                    "Availability (bags of 35 Kg)":line.register_id.availability_35kg,
                    "diff_price":self.diff_price,
                })  
    

         
        _logger.info(data)
        json_str=json.dumps(data)
        _logger.info('Llamando al API para generar PDF')

        url = "https://qmycx2gipfzkrkwgmotvrpwlne0fxfjl.lambda-url.us-east-1.on.aws"  
        payload = {
            "mensaje": f"Hola desde Odoo, modelo ID {self.id}"
        }


        # https://qmycx2gipfzkrkwgmotvrpwlne0fxfjl.lambda-url.us-east-1.on.aws/
        response = requests.post(url, json=json_str, timeout=60)
        # _logger.info(f"Respuesta del servicio: {response.status_code} - {response.text}")
        data =  response.json()
        # print('hola',data)
        b64data = data['filedata']
        file_name = f'{name}.pdf'

        self.write({
            'pdf_file':b64data,
            'pdf_filename':file_name,
        })
        self.state = 'pdf'


        off_register = self.env['muestras.offering_history'].create({
            'partner':self.partner_id.id,
            'date':self.create_date,
            'expiration_date':self.expiration_date,
            'offering_seq':self.sequence,
            'salesperson_header':self.salesperson_header.id,
            'salesperson':self.salesperson.id,
            'pdf_file':self.pdf_file,
            'pdf_filename':self.pdf_filename,
            'trm':self.trm,
            'price_c':self.price_c
        })
        for line in self.line_id:
            if line.show_line == True:
                off_line = self.env['muestras.offering_history_line'].create({
                    'offering_id':off_register.id,
                    'code':line.register_id.lote,
                    'equation_main_category':line.register_id.main_category.id,
                    'equation_origin':line.register_id.equation_origin_town.id,
                    'equation_process_offering':line.register_id.equation_fermentation_process.id,
                    'equation_varietal':line.register_id.equation_varietal.id,
                    'sca':line.register_id.sca_actual,
                    'equation_macroprofile':line.register_id.equation_macroprofile.id,
                    'price_fob_usa':line.price_fob_usa,
                    'price_spot_usa':line.price_spot_usa,
                    'price_spot_usa_tariffs':line.price_spot_usa_tariffs,
                    'price_fwb_usa':line.price_fwb_usa,
                    'price_fob_eu':line.price_fob_eu,
                    'price_spot_eu':line.price_spot_eu,
                    'price_fwb_eu':line.price_fwb_eu,
                    'price_exw':line.price_exw,
                    'price_exw_eu':line.price_exw_eu,
                    'price_exw_kg':line.price_exw_kg,
                    'aval_35':line.register_id.availability_35kg
                }) 


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muestras.offering_pdf_wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new', 
        }
    

    def download(self):
        self.ensure_one()
        if not self.pdf_file:
            raise UserError("There is no file available for download")
        
        return{
            'type':"ir.action.act_url",
            'url':f'/web/content/{self._name}/{self.id}/pdf_file?download=true',
            'target':'self',
        }

    #### Pruebas
    def pdf_offering(self):
        
        offering_report = self.env['muestras.generate_pdf']._pdf_generating()
        print('Hoooooooooooooooooooola')
        _logger.info(offering_report)
        _logger.info("Iniciando la generación del PDF para el wizard")
        _logger.info(f"Tipo de contenido de offering_report: {type(offering_report)}")
        _logger.info(f"Tamaño de offering_report: {len(offering_report)} bytes")


        
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'attachment; filename="offering_report.pdf"'),
        ]
        
        return request.make_response(offering_report, headers=headers)
        
        
    def _get_report_values(self, docids, data=None):
        wizard = self.browse(docids)

        return {
            'wizard': wizard,
            'line_ids': wizard.line_id,  # Asegúrate de pasar las líneas con sus valores Many2one
        }
    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('muestras.offering.wizard') or '/'
        return super().create(vals)
    
    @api.onchange('fob_usa_boolean')
    def _onchange_refresh_lines(self):
        pass


class OfferingLines(models.TransientModel):
    _name='muestras.offering_pdf_wizard_line'
    _description="Lineas a incluir dentro del Offering List"

    wizard_id=fields.Many2one('muestras.offering_pdf_wizard',string="Wizard",required=True)
    register_id=fields.Many2one('muestras.disponible',string="Disponible Original",required=True,ondelete='cascade')
    equation_varietal=fields.Many2one('equation.coffee_varietal',string="Varietal")
    equation_varietal_name=fields.Char(string="Varietal Name",store=True)
    equation_origin=fields.Many2one('equation.coffee_origin',string="Origin")
    equation_origin_name=fields.Char(string="Origin Name",store=True)
    equation_main_category=fields.Many2one('muestras.offeringcat',string="Main Category")
    equation_main_category_name=fields.Char(string="Main Category Name",store=True)
    equation_macroprofile=fields.Many2one('equation.coffee_macroprofile',string="Macroprofile")
    equation_macroprofile_name=fields.Char(string="Macroprofile Name")
    equation_process_offering=fields.Many2one('equation.coffee_fermentation_process',string="Equation Process Offering")
    equation_process_offering_name=fields.Char(string="Equation Process Offering Name")
    sca=fields.Float(string="SCA",store=True)
    price_fob_usa=fields.Char(string="FOB US/lb")
    price_spot_usa=fields.Char(string="Spot USxlb")
    price_spot_usa_tariffs =fields.Char(string="Spot US/lb with Tarrifs")
    price_fwb_usa=fields.Char(string="FWB US/Lb")
    price_fob_eu=fields.Char(string="FOB EUxkg")
    price_spot_eu=fields.Char(string="Spot EUxkg")
    price_fwb_eu=fields.Char(string="FWB EUxkg")
    price_exw=fields.Char(string='EXW US/lb')
    price_exw_eu=fields.Char(string='EXW EU/kg')
    price_exw_kg=fields.Char(string='EXW US/kg')
    aval_35 = fields.Float(string="Availability in 35 kg ")
    
    
    ### booelanos ###

    variety_show=fields.Boolean(related='wizard_id.variety_boolean', store=False)
    

    show_line=fields.Boolean(string="Mostrar", default=True)

    fob_usa_show=fields.Boolean(String="Fob Show")



    


    






