<div align="center">
<h1> Sección de Ordenes y flujo de las muestras
</div>
<div align="center">
    <em>Juan Pablo Vallejo Montañez</em><br>
    <em>Data & Development Analyst</em><br>
    <em>ia@equationcoffee.com</em>
</div>


## 1. Flujo


## 2. Atributos
De una forma al corregir el sistema se tienen los siguientes subsecciones de campos:
    - Campos temporales que aun no tienen division
    - General info 
    - Inventory
    - Price
    - Methods


Claramente para la construccion del modelo de ordebes no habran las mismas separaciones que hay en los diagramas o esquemas de productos.
En Ordenes tendremos las siguientes separaciones. Hay que separar las categorias en subcategoruas mas pequelas para distrubuir la informacion mas facil y de manera mas correcta
    - Order Info
name  
state    --- TRACK
data_order 
order_lines 
coffee_sample
typesample
release_date
notes
custom_location
quantity
booking
region
location
create_date
deadline
country
date
days
lote_quantity
sample_quantity
salesperson
salesperson_header  - TRACK
crm_team
email_sent
email_content
email_to
quotation
total
company
    - Partner 
partner_id   --- TRACKER 
country_partner
---- lOS SIGUIENTES CAMPOS SON COMPUTADOS -----
partner_invoice_id  -- TRACKER 
partner_country
partner_addres
partner_city
partner_state
partner_phones
parnter_email
partner_zip
partner_contact
boolean_customs_info
country_customer
delivery_address  -- TRACKER 
    - No category
internal_code
project
category
edition


-----------------------------------------
DE AQUI PARA ABAJO CORRESPONDE AL MODULO DE ORDER LINES. La distribucion es similar sin embargo hay campos que varian a comtinuacion los listo

    - Order Info 
order_id
notes


    - Product
product_id  
project 
variety
program
category
location
warehouse
country_origin
region 
lote
internal_code
edition
process
score
macroprofile
fuente
state
farm
uom
boolean_booking
sale_check
booking_change
feedback_selection
line_state

    - Visualizaciin en Send Samples
order_name
order_create_date
salesperson_name
partner_name    





## 3. Metódos




## 4. Grupos y Permisos 


## 5. Elementos Estáticos


---------------
Logica de estados con la orden general 

sent (OR) and active (OL) 

Estados - Declinada ---> rechazados todos
        - "Pendiente"  ---> ninguno de compra y alguno rechazado
        - venta ---> Al menos uno de compra 
        - venta total  ---> Total

Creado los ultimos movimientos 



Claro. Aquí tienes una explicación clara y documentada sobre el uso del diccionario res en el método default_get, que puedes incluir como parte de tu documentación o comentarios en el código.

📘 ¿Qué es default_get?
El método default_get(fields) en Odoo se usa para establecer los valores predeterminados de los campos al crear un nuevo registro (por ejemplo, al abrir un wizard).

📌 ¿Qué es res?
En este contexto, res es un diccionario donde:

Las claves son los nombres de los campos.

Los valores son los valores predeterminados que se asignarán al crear el registro.

💡 ¿Cómo funciona?
Cuando Odoo crea un nuevo registro transitorio (como un wizard), llama automáticamente a default_get para llenar los campos con valores por defecto.
Primero llama al super() para obtener los defaults estándar definidos por Odoo o por otros módulos:

python
Copiar
Editar
res = super().default_get(fields)
Después puedes modificar el diccionario res agregando o sobreescribiendo valores:

python
Copiar
Editar
res['active_model'] = self.env.context.get('active_model')
res['order_id'] = self.env.context.get('active_id')
Finalmente, devuelves el diccionario:

python
Copiar
Editar
return res
📝 Comentario sugerido para tu código:
python
Copiar
Editar
@api.model
def default_get(self, fields):
    """
    Sobrescribe el método default_get para inicializar campos del wizard con valores
    provenientes del contexto.

    El diccionario `res` contiene los valores por defecto que se asignarán al crear el registro.
    Se parte del resultado de super(), y luego se personaliza según el contexto activo.

    - 'active_model' se llena con el nombre del modelo que abrió el wizard.
    - 'order_id' se llena con el ID del registro activo, suponiendo que es un 'muestras.order'.
    """
    res = super().default_get(fields)
    res['active_model'] = self.env.context.get('active_model')
    res['order_id'] = self.env.context.get('active_id')
    return res
¿Te gustaría que te prepare una plantilla de docstring estándar para tus métodos en este módulo?