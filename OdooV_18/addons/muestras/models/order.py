from odoo import models, fields, api, _
import csv 
import os 
import logging 
from datetime import datetime, date, timedelta 
from odoo.exceptions import UserError 
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Order(models.Model):
    _name="muestras.order"
    _description="Vista de order de muestars"

    ### FIEELDS ###
    name=fields.Char(string ="Order Reference",required=True,
        copy=False,readonly=True,index= 'trigram',default=lambda self: _('New')) 
    partner_id = fields.Many2one(comodel_name="res.partner",string="Costumer"
        #  ,required=True,readonly=False,change_default=True,index=True,tracking=1
        )
    country_partner=fields.Char(string="Country",index=True)
    state = fields.Selection(
        selection=[
            ('draft',"Draft"),
            ('sent',"Sample Shipment"),
            ("cancels","Shipment Cancelled"),
            ("cancelb","Booking Cancelled"),
            ("expering","Reserve to Expire"),
            ("cancelba","Booking Cancelled (Auto)"),
            ('sale',"Order Sale"),
        ],
        string = "Status",
        readonly=True, copy=False,index=True,
        default='draft'
    )
    internal_code=fields.Char(string="Interal Code",index=True)
    project=fields.Char(string="Project",index=True)
    category=fields.Char(string="Category",index=True)
    edition=fields.Char(string="Edition",index=True)
    quantity=fields.Char(string="Amount of kg reserved",index=True,store=True)
    booking=fields.Float(string="Amount of Booking",index=True,store=True,compute="_kg_reserved",default=0.0)
    region=fields.Char(string="Región Comercial",index=True,store=True,compute="region_order")
    location=fields.Char(string="Ubicación",index=True,store=True,compute="location_order")
    create_date=fields.Date(string= "Creation Date",index=True,readonly=True,default=None)
    deadline=fields.Date(string="Deadline",index=True,readonly=True)
    country=fields.Char(string="Región Comercial",index=True)
    date=fields.Date(string="Date",index=True,default=None)
    days=fields.Integer(string="Days")
    salesperson=fields.Many2one(string="Salesperson ",comodel_name="res.users",readonly=True,
        default=lambda self: self.env.user)
    crm_team=fields.Char(string="Equipo de Ventas",store=True,compute="crm_team_compute")
    email_sent=fields.Boolean(string="Email Send")
    email_content = fields.Html(string='Email Content', sanitize=False)
    email_to=fields.Char(string="Recipient")
    quotation=fields.Many2one(string="Quotation")
    total=fields.Float(string="Total Amount",store=True,compute="total_sample_price")
    salesperson_header=fields.Many2one(comodel_name='res.users',
        string="Main Salesperson",
        default=lambda self: self.env.user)
    company=fields.Many2many(
        'res.company',
        string="Company"
    )

    custom_location=fields.Selection(
        selection=[
            ('pd','Por Defecto'),
            ('col','Colombia'),
            ('usa','United States'),
        ],
        string="Equipo de Calidades",
        default='pd',
        required=True
    )
 



    date_order=fields.Datetime(string='Order Date',required=True,readonly=False,
        copy=False,help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",default=fields.Datetime.now)
    
    ### Partner -based compute fields ##

    partner_invoice_id = fields.Many2one(comodel_name='res.partner',
        string="Invoice Adress", compute='_compute_partner_invoice_id',
        store=True, readonly=False,required=True,precompute=True
        )
    order_lines=fields.One2many(string="Ordenes de compra",comodel_name='muestras.order.line',
        inverse_name='order_id',copy=True,auto_join=True
        )
    coffee_sample=fields.Selection(
        selection=[
            ('pss','Pre Shipment Sample'),
            ('ss','Shipment Sample'),
            ('cs','Comercial Sample'),
            ('rp','Replicable Sample'),
        ],
        string="Coffee Sample Type",
        default=None,
        required=True
        )
    typesample=fields.Selection(
        selection=[
            ('gre',"Verde"),
            ('tos',"Tostado"),
        ],
        string="Sample Type",
        default=None,
        required=True
        )

    #### CUSTOMER FIELDS #####
    # contact =fields.    
    country_customer=fields.Char(string="Country",index=True,compute='_compute_country_customer',default=None)
    delivery_address=fields.Char(string="Delivery Address",index=True)
    # postal_code=fields
    # phone_contact
    # email_contact
    # customs   ## ADUANAS    

    release_date=fields.Date(string="Release Date")



    # ### COMPUTE FIELDS ###

    notes = fields.Text(string="Notas Adicionales",required=False) 
    partner_country=fields.Char(string="Country",required=True)
    partner_address=fields.Char(string="Address",required=True)
    partner_city=fields.Char(string="City",required=True)
    partner_state=fields.Char(string="State",required=True, default=" ")
    partner_phone=fields.Char(string="Phone",required=True)
    partner_email=fields.Char(string="E-mail",required=True)
    partner_zip=fields.Char(string="Zip",required=True, default=" ")
    partner_contact=fields.Char(string="Contact",required=True,default=" ")
    boolean_customs_info=fields.Boolean(string="Información Adicional Requerida")
    customs_info=fields.Char(string="Custom Info")
    lote_quantity=fields.Integer(string="Número de Lotes",store=True,compute='_number_lots')
    sample_quantity=fields.Float(string="Cantidad Total de muestra",store=True,compute="")
    
    @api.onchange('partner_id')
    def partner_info(self):
        if self.partner_id:
            self.partner_country=self.partner_id.country_id.name
            # self.partner_address=self.partner_id.contact_address_complete
            self.partner_city=self.partner_id.city
            self.partner_phone=self.partner_id.phone
            self.partner_email=self.partner_id.email
            self.partner_zip=self.partner_id.zip
            self.partner_state=self.partner_id.state_id.name



    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        for order in self :
            if order.partner_id:
                order.partner_invoice_id = order.partner_id.address_get(['invoice'])['invoice']

    @api.depends('partner_id')
    def _compute_country_customer(self):
        for order in self:
            if order.partner_id:
                order.country_customer=order.partner_id.country_id.name
            else:
                order.country_customer=None



    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) ==_('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('muestras.order')
        if 'salesperson' not in vals:
            vals['salesperson']=self.env.user.id
        return super(Order,self).create(vals)

    def _update_days(self):
        records = self.search([])
        for record in records:
            if record.state=='sent' and record.create_date:
                current_date=date.today()
                delta=current_date - record.create_date
                record.days=delta.days
            else:
                record.days=None

    def _validate_records(self):
        # Lógica de validación
        for record in self:
            if not record.field_to_validate:
                raise ValidationError("El campo no está configurado correctamente.")



#### ACTION METHODS ####
    def send_sample(self):
        try:
            # Validación de disponibilidad de productos
            for line in self.order_lines:
                product = line.product_id
                if product.disponible < line.booking:
                    raise UserError(f"Not enough quantity available for lot {product.lote}.")
                else:
                    product.disponible -= line.booking
                    product.booking += line.booking

            # Si el bucle se completa correctamente, ejecuta el resto
            self.state = 'sent'
            self.create_date = date.today()
            self.deadline = date.today() + timedelta(days=21)
            region_list = self.regions()
            self.recipient(region_list)

            # Envío del correo electrónico
            template = self.env.ref('muestras.muestras_email_template_order')
            if template:
                template.send_mail(self.id, force_send=True)
                self.email_sent = True
                self.email_content = self.generate_table_html()

        except UserError as e:
            # Manejo de errores específicos
            raise e
        except Exception as e:
            # Manejo de errores generales
            raise UserError(f"Unexpected error: {str(e)}")



    def cancel_book(self):
        self.state='cancelb'
        for line in self.order_lines:
            if line.fuente == "Disponibles":
                product=line.disponible_id
            else:
                product=line.product_id
            product.avalible+=line.booking
            product.booking-=line.booking
            self.release_date=date.today()


    def cancel_shipment(self):
        self.state='cancels'
        for line in self.order_lines:
            product=line.product_id
            product.avalible+=line.booking
            product.booking-=line.booking

    def sale_order_without_shipment(self):
        _logger.info('KKKKK')
        return self.open_wizard_sale()
        # self.state="sale"

    def sale_order(self):
        _logger.info('KKKKK')
        return self.open_wizard_sale()
        # self.state="sale"
        
        # purchase_order_lines=[]
        # for line in self.order_lines:
        #     product=line.product_id
        #     product.sale+=line.booking
        #     product.booking-=line.booking


#____________________________________________________________


         #   ______________________________________
        #     purchase_order_lines.append((0,0,{
        #         'product_id':line.product_id.id,
        #         'name':line.product_id.name,
        #         'product_qty':line.booking,
        #         'price_unit':line.price,
        #     }))
        #     purchase_order=self.env['purchase.order'].create({
        #         'order_line':purchase_order_lines,
        #         'partner_id':self.partner_id.id,
        #     })

    @api.depends('days')
    def _timeout_booking(self):
        for record in self:
            if 16 < record.days <= 21:
                record.state="expering"
            if record.days>21:
                record.state="cancelba"
                for line in record.order_lines:
                    product=line.product_id
                    product.quantity+=line.booking
                    product.booking-=line.booking



    def generate_table(self):
        products=self.order_lines
        table_rows=[]
        for product in products:
            table_rows.append({
            'product': product.product_id.name,  
            'project': product.project,         
            'process': product.process,         
            'variety': product.variety,        
            'sample_quantity': product.quantity, 
            'booking_quantity': product.booking 
        })

        return table_rows

    
    def generate_table_html(self):
    # Llamar al método que genera las filas de datos
        table_rows = self.generate_table()

        # Iniciar la estructura HTML de la tabla
        table_html = """
        <table style="width: 100%; border-collapse: collapse; text-align: left; border: 1px solid #ddd;">
            <thead>
                <tr style="background-color: #f4f4f4; border-bottom: 2px solid #ddd;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Product</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Project</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Process</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Variety</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Sample Quantity</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Booking Quantity</th>
                </tr>
            </thead>
            <tbody>
        """

        
        for row in table_rows:
            table_html += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['product']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['project']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['process']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['variety']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['sample_quantity']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['booking_quantity']}</td>
            </tr>
            """
        table_html += "</tbody></table>"

       
        return table_html


    def recipient(self,region):
        sales_head_eamil=self.salesperson_header.login
        sales_email=self.salesperson.login
        email_to="viviana@equationcoffee.com,operaciones@equationcoffee.com,laura@equationcoffee.com,analitica@thecoffeehub.co"
        mails=["viviana@equationcoffee.com","operaciones@equationcoffee.com","laura@equationcoffee.com","analitica@thecoffeehub.co"]
        panama=["admin@creativacoffeedistrict.com","calidad@creativacoffeedistrict.com","auxlaboratorio@equationcoffee.com","coo@flyingpumas.com","procesos@thecoffeehub.co","sales@flyingpumas.com"]
        ## Colombia y Europa comparten el mismo equipo de calidades.
        colombia=["produccion@equationcoffee.com","auxcalidad@equationcoffee.com","auxlaboratorio@equationcoffee.com"]
        usa=["produccion@equationcoffee.com","auxcalidad@equationcoffee.com","auxlaboratorio@equationcoffee.com","qc@thecoffeehub.co"]
        europe=["produccion@equationcoffee.com","auxcalidad@equationcoffee.com","auxlaboratorio@equationcoffee.com","sebastianv@equationcoffee.com","angelica@equationcoffee.com"]
        if self.custom_location=='pd':
            if "Panama"  in region:
                for mail in panama:
                    if mail not in mails:
                        mails.append(mail)
                        email_to+=f",{mail}"
            if "USA"  in region:
                for mail in usa:
                    if mail not in mails:
                        mails.append(mail)
                        email_to+=f",{mail}"
            if "Colombia"  in region:
                for mail in colombia:
                    if mail not in mails:
                        mails.append(mail)
                        email_to+=f",{mail}"
            if "Europe"  in region:
                for mail in europe:
                    if mail not in mails:
                        mails.append(mail)
                        email_to+=f",{mail}"
            if sales_email not in email_to:
                email_to+=f",{sales_email}"
            if sales_head_eamil not in email_to:
                email_to+=f",{sales_head_eamil}"
        elif self.custom_location=='col':
            for mail in colombia:
                if mail not in mails:
                    mails.append(mail)
                    email_to+=f",{mail}"
        elif self.custom_location=='usa':
            for mail in usa:
                if mail not in mails:
                    mails.append(mail)
                    email_to+=f",{mail}"
        self.email_to=email_to

    def regions(self):
        regions_sample=[]
        for line in self.order_lines:
            region=line.product_id.location
            if region not in regions_sample:
                regions_sample.append(region)

        return regions_sample


    def quotation(self):
        sale_order_lines=[]
        for line in self.order_lines:
            sale_order_lines.append(
                (
                    0, 0, {  # Línea de pedido (0 indica nueva línea)
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.booking,
                        'price_unit': line.product_id.price,  # Precio unitario
                    }
                ))
        default_values = {
            'partner_id': self.partner_id.id,  # Cliente
            'order_line':sale_order_lines
        }
        sale_order = self.env['sale.order'].create(default_values)
        return sale_order

    @api.depends('order_lines')
    def _kg_reserved(self):
        for record in self:
            record.booking=sum(line.booking for line in record.order_lines)

    @api.depends('order_lines')
    def _number_lots(self):
        lots=0
        for record in self:
            record.lote_quantity=len(record.order_lines)
            record.sample_quantity=sum(line.quantity for line in record.order_lines)

    @api.depends('order_lines')
    def total_sample_price(self):
        price_Total=0
        for record in self:
            record.total=sum(record.order_lines.mapped('subtotal'))


    @api.constrains('order_lines')
    def same_region(self):
        for order in self:
            regions = order.order_lines.mapped('location')
            unique_regions = set(regions)
            
            # Condición: Si hay más de una región y no son exactamente Colombia y Europa, lanza un error
            if len(unique_regions) > 1 and unique_regions != {"Colombia", "Europe"}:
                raise ValidationError("Todas las líneas del pedido de muestras deben ser de la misma región, excepto si son de Colombia y Europa.")

    @api.depends('order_lines.location')
    def location_order(self):
        for order in self:
            regions=order.order_lines.mapped('location')
            if regions and len(set(regions))==1:
                order.location=regions[0]
            else:
                order.location=" "

    @api.depends('order_lines.region')
    def region_order(self):
        for order in self:
            regions=order.order_lines.mapped('region')
            if regions and len(set(regions))==1:
                order.region=regions[0]
            else:
                order.region=" "


    @api.constrains('order_lines')
    def booking_nonzero(self):
        for line in self.order_lines:
            if line.boolean_booking:   
                if line.booking==0:
                    raise ValidationError("El valor de la reserva tiene que ser mayor a 0")

    @api.depends('salesperson')
    def crm_team_compute(self):
        # self.crm_team="jP"
        self.crm_team=self.salesperson.sale_team_id.name

    def _get_order_lines_to_report(self):
        return self.order_lines


    def open_wizard_sale(self):
        _logger.info('Entrado al wizard')
        """Abrir el Wizard para editar las líneas."""
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Editar Líneas de la Orden',
        #     'res_model': 'muestras.wizard_sale',
        #     'view_mode': 'form',
        #     'target': 'new',  # Mostrar como ventana emergente
        #     'context': {'active_id': self.id},  # Pasar la orden activa
        # }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muestras.wizard_sale',  # Cualquier modelo que exista
            'view_mode': 'form',
            'name':'Sale',
            'target': 'new',  # Mostrar como ventana emergente
        }
    
    def open_wizard_crm(self):
        return {
            'type':'ir.actions.act_window',
            'res_model' : 'muestras.wizard_order_crm_selection',
            'view_mode':'form',
            'name':'Link to Lead Confirmation',
            'target':'new',
            'context':{
                'default_partner_id':self.partner_id.id,
                'default_order_id':self.id
            }
        }


    def create_crm_lead(self):
        # Buscar la etapa específica (estado fijo)
        stage = self.env['crm.stage'].search([('name', '=', 'Sample Request')], limit=1)
        if not stage:
            raise ValueError("La etapa 'Nueva etapa' no existe en el pipeline de CRM.")

        # Crear el lead
        lead_data = {
            'name': f"Orden de Muestra: {self.name}",
            'partner_id': self.partner_id.id,
            'description': f"Lead generado automáticamente para la orden de muestra {self.name}.",
            # 'tag_ids': [(4, category.id)],  # Asociar la categoría al lead
            # 'sale_team_id': self.env['crm.team'].search([], limit=1).id,  # Equipo de ventas
            'stage_id': stage.id,  # Asignar la etapa fija
            'sample_order_id': self.id,
            'type':'opportunity',
            'user_id':self.salesperson_header.id,

        }
        self.env['crm.lead'].create(lead_data)

    def update_crm_lead(self,lead_id):
        lead = self.env['crm.lead'].browse(lead_id)
        if not lead.exists():
            return False
        stage = self.env['crm.stage'].search([('name', '=', 'Sample Request')], limit=1)
        if not stage:
            raise ValueError("La etapa 'Nueva etapa' no existe en el pipeline de CRM.")
        lead.write({
            'sample_order_id':self.id,
            'stage_id':stage.id
        })



class SaleWizard(models.TransientModel):
    _name = "muestras.wizard_sale"
    _description="Wizard de Compra"

    order_id = fields.Many2one('muestras.order', string='Orden', required=True)
    line_id = fields.One2many('muestras.wizard_sale.line', 'wizard_id', string="Muestras")

    @api.model
    def default_get(self, fields):
        res = super(SaleWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        
        if active_id:
            order = self.env['muestras.order'].browse(active_id)
            if order:
                lines = []
                for line in order.order_lines:
                    lines.append((0, 0, {
                        'line_id': line.id,
                        'product_id': line.product_id.id,
                        'variety': line.variety,
                        'program': line.program,
                        'quantity': line.quantity,
                        'booking': line.booking,
                        'sale_check': line.sale_check,
                    }))
                res.update({'order_id': order.id, 'line_id': lines})
        
        return res

    def apply_changes_l(self):
        """Aplica cambios a las líneas de la orden de venta y actualiza stock"""
        if not self.order_id:
            raise UserError("No se ha encontrado una orden de venta válida.")

        for wizard_line in self.line_id:
            if not wizard_line.line_id:
                continue  # Si la línea no está vinculada, omitir

            # Actualizar la línea de pedido con write()
            wizard_line.line_id.write({
                'sale_check': wizard_line.sale_check,
                'booking_change': wizard_line.booking_change,
                'feedback_notes': wizard_line.feedback_notes,
                'feedback_selection': wizard_line.feedback_selection
            })

            product = wizard_line.line_id.product_id

            if self.order_id.state == 'sent':
                sale_extra = wizard_line.booking_change - wizard_line.booking

                if wizard_line.sale_check == 'sl':
                    if product.disponible < sale_extra:
                        raise UserError(f"No hay suficiente cantidad disponible para el lote {product.lote}.")
                    else:
                        product.write({
                            'disponible': product.disponible - sale_extra,
                            'booking': product.booking - wizard_line.booking,
                            'sale': product.sale + wizard_line.booking_change
                        })

                elif wizard_line.sale_check == "ns":
                    product.write({
                        'disponible': product.disponible + wizard_line.booking,
                        'booking': product.booking - wizard_line.booking
                    })

            elif self.order_id.state == 'draft':
                if wizard_line.sale_check == 'sl':
                    if product.disponible < wizard_line.booking_change:
                        raise UserError(f"No hay suficiente cantidad disponible para el lote {product.lote}.")
                    else:
                        product.write({
                            'disponible': product.disponible - wizard_line.booking_change,
                            'sale': product.sale + wizard_line.booking_change
                        })

        # Si todo está bien, actualizar el estado de la orden
        self.order_id.write({'state': "sale"})
        return {'type': 'ir.actions.act_window_close'}


class Sale_wizard_line(models.TransientModel):
    _name="muestras.wizard_sale.line"
    _description="Wizard de Compra"
    m=fields.Integer(string="ID new")
    wizard_id=fields.Many2one('muestras.wizard_sale',string='Wizard',required=True)
    line_id=fields.Many2one('muestras.order.line',string='Linea Original',required=False,ondelete='cascade')
    product_id=fields.Many2one('muestras.allproducts',string='Product',ondelete='cascade',required=False)
    variety=fields.Char(string='Variedad',readonly=True)
    program=fields.Char(string='Categoria',readonly=True)
    quantity=fields.Float(string='Cantidad',readonly=True)
    booking=fields.Float(string="Reserva",readonly=True)
    booking_change=fields.Float(string="Cambios en la Reserva")
    sale_quantity=fields.Float(string='Venta',readonly=True)
    verification=fields.Boolean(string='Verificacion')
    sale_check=fields.Selection(
        selection=[
            ('ns','No venta'),
            ('sl','Venta'),
        ],
        string='Venta',
        default=None,
        required=True
    )
    feedback_selection= fields.Many2many(
        'muestras.feedback',
        string="Feedback"
    )
    feedback_notes=fields.Text(string="Notas Feedback")


class CRMConfirmation(models.TransientModel):
    _name='muestras.wizard_order_crm_selection'
    _description='Sample Request - Link to Lead Confirmation'

    order_id = fields.Many2one('muestras.order',string="Order ID")
    partner_id=fields.Many2one('res.partner',string="Partner")
    crm_option=fields.Selection([
        ('create', 'Create a new lead'),
        ('select', 'Link to an existing lead'),
        ('none', 'Send Sample Without Linking a Lead'),
    ],string='Select an option')

    lead_id=fields.Many2one('crm.lead',string='Existing Lead',domain=[])

    def confirm_link_to_lead(self):
        for wizard in self:
            if wizard.crm_option=="none":
                wizard.order_id.send_sample()
            if wizard.crm_option=="select":
                wizard.order_id.send_sample()
                wizard.order_id.update_crm_lead(wizard.lead_id.id)
            if wizard.crm_option=="create":
                wizard.order_id.send_sample()
                wizard.order_id.create_crm_lead()
        return {'type':'ir.actions.act_window_close'}
    





    
