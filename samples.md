<div align="center">
<h1> Módulo de muestras
</div>
<div align="center">
    <em>Juan Pablo Vallejo Montañez</em><br>
    <em>Data & Development Analyst</em><br>
    <em>ia@equationcoffee.com</em>
</div>


## 1. Flujo completo del proceso




## 2. Modelos   

### 2.1 Modelo Product Father

<div align="justify">
Dado que los lotes de productos muestreables pueden originarse desde distintas fuentes, se define un modelo base denominado <strong>ProductFather</strong>, el cual actúa como plantilla para los demás modelos de productos. La estructura de atributos de este modelo se organiza en cinco secciones principales. Cada modelo hijo hereda esta estructura base y define atributos únicos dentro de cada una de estas secciones, de acuerdo con las necesidades específicas del producto correspondiente.
</div>

#### 2.1.1 Atributos

<div align="justify">
Dentro de este modelo se definen 5 categorias para agrupar los atributos del modelo de una forma organizada

- <strong>General Information</strong>

| Campo       | Descripcion  | Ejemplos        | 
|-------------|--------------|-----------------|
| name        | 120,000      | 5.2%            |
| sku         | 98,500       | 3.1%            | 
| lot         | 110,300      | 4.8%            | 
| internal_code | 75,000     | 6.0%            |
| code | 75,000     | 6.0%            | 
| project | 75,000     | 6.0%            |
| program | 75,000     | 6.0%            |
| category | 75,000     | 6.0%            |
| variety | 75,000     | 6.0%            |
| process | 75,000     | 6.0%            |
| f_process | 75,000     | 6.0%            |

- <strong>Equation Information</strong>

- <strong>Technical Information</strong>

- <strong>Inventory</strong>

- <strong>Price</strong>
</div>

<div style="display: flex; align-items: center;">
  <div style="flex: 1; padding: 10px;">
    <img src="https://via.placeholder.com/300" alt="Imagen" style="max-width: 100%;">
  </div>
  <div style="flex: 1; padding: 10px;">
    <h3>Título del texto</h3>
    <p>
      Este es un párrafo de ejemplo que se muestra al lado derecho de la imagen.
      Puedes agregar más contenido aquí, como listas, enlaces o lo que necesites.
    </p>
  </div>
</div>

#### 2.1.2 Métodos

El modelo <strong>ProductFather</strong> cuenta inicialmente con 8 metods que parametrizan los campos de categorización de productos. Dichos métodos replican o copian el valor del campo de selección al campo tipo Char para una variable. 

Un ejemplo. Al seleccionar un valor de proyecto en el atributo <u>Equation Project</u> como <em>La Palma & el Túcan </em> el método   <em> _project()</em> asignara el valor La Palma & el Túcan al campo <em> project</em>. De esta manera, se oculta el campo de tipo texto y se deja a la vista del usuario el campo de selección para parametrizar de manera eficaz cada uno de los productos pero dejando el mismo valor a ambos campos para situaciones de trazabilidad

### 2.2 Modelo Atlas 

<div align='justify'>
El modelo <strong>Atlas - Projects</strong> nace de la necesidad de tener un reflejo exacto del inventario registrado para los cafés de Proyectos en el ERP de <em>Atlas</em>. De esta manera, el equipo de calidades crea y actualiza lotes de cafes desde el ERP y tanto el administrador como el mismo equipo de calidades puede visualizar el inventario en Odoo mediante el uso de un botón.
</div>



#### 2.2.1 Atributos

<div>
En este modelo se heredan atributos y métodos de <strong>ProductFather</strong>. A continuación se listan de manera separada los campos que se heredan con modificaciones nuevas para ese modelo y los campos  totalmente nuevos.
</div>
<br>

- <em>Campos heredados con modificaciones </em>

<table>
  <thead>
    <tr>
      <th style="text-align: center;">Campo</th>
      <th style="text-align: center;">Tipo de Campo</th>
      <th style="text-align: center;">Descripción</th>
      <th style="text-align: center;">Categoría</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">price_us</td>
      <td style="text-align: center;">Float</td>
      <td style="text-align: justify;">El campo pasa a un campo no obligatorio </td>
      <td style="text-align: center;">Price</td>
    </tr>
    <tr>
      <td style="text-align: center;">pricelb</td>
      <td style="text-align: center;">Float</td>
      <td style="text-align: justify;">El campo pasa a un campo no obligatorio </td>
      <td style="text-align: center;">Price</td>
    </tr>
  </tbody>
</table>

 - <em>Campos Nuevos </em>

<div align='justify'>
Se añade una nueva categoria de atributos denominada <strong><em>API</em></strong> que agrupará  los campos relacionados con la conexión Atlas - Odoo.
</div> 
<br>

<table>
  <thead>
    <tr>
      <th style="text-align: center;">Campo</th>
      <th style="text-align: center;">Tipo de Campo</th>
      <th style="text-align: center;">Descripción</th>
      <th style="text-align: center;">Categoría</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">update_mode</td>
      <td style="text-align: center;">Selection</td>
      <td style="text-align: justify;">Indica el tipo de creación del lote. Este campo se hizo para solucionar la contingencia generada por la falta de uso de la herramienta <em>Atlas</em> por parte del equipo de calidades Panamá. La idea es dejar de usar este campo a largo plazo. En escencia, este campo permite al <u>usuario administrador</u> crear lotes desde Odoo y aislarlos del flujo de actualización <em>Atlas-Odoo</em> </td>
      <td style="text-align: center;">General Info</td>
    </tr>
    <tr>
      <td style="text-align: center;">peso_neto</td>
      <td style="text-align: center;">Float</td>
      <td style="text-align: justify;">Almacena la cantidad incial del lote registrado en <em>Atlas</em></td>
      <td style="text-align: center;">Inventory</td>
    </tr>
    <tr>
      <td style="text-align: center;">peso_salida</td>
      <td style="text-align: center;">Float</td>
      <td style="text-align: justify;">Almacena la cantidad total de salidas en kg del lote registrado en <em>Atlas</em></td>
      <td style="text-align: center;">Inventory</td>
    </tr>
    <tr>
      <td style="text-align: center;">quantityUSA - quantityEU - quantityAsia</td>
      <td style="text-align: center;">Float</td>
      <td style="text-align: justify;">Estos campos estan destinados a almancenar la distribución de la cantidad actual del lote en las regiones comerciales</td>
      <td style="text-align: center;">Inventory</td>
    </tr>
    <tr>
      <td style="text-align: center;">needsRegionUpdate</td>
      <td style="text-align: center;">Boolean</td>
      <td style="text-align: justify;">Booleano que evalua diferencias entre la cantidad actual del lote y la suma de las cantidades distribuidas en regiones.</td>
      <td style="text-align: center;">Inventory</td>
    </tr>
    <tr>
      <td style="text-align: center;">update_boolean</td>
      <td style="text-align: center;">Boolean</td>
      <td style="text-align: justify;">Marca la actualización correcta del lote y la generación (o no en caso de que el lote tenga cantidad 0 ) de lotes distribuidos en el modelo <em>muestras.allproductos</em></td>
      <td style="text-align: center;">Inventory</td>
    </tr>
    <tr>
      <td style="text-align: center;">last_execution_date</td>
      <td style="text-align: center;">Datetime</td>
      <td style="text-align: justify;">Ultima fecha de actualización
      <td style="text-align: center;">API</td>
    </tr>
    <tr>
      <td style="text-align: center;">entry_id</td>
      <td style="text-align: center;">Char</td>
      <td style="text-align: justify;">ID del lote asociado a la base de datos de <em>Atlas</em>.
      <td style="text-align: center;">API</td>
    </tr>
  </tbody>
</table>


<div align="justify">
</div>

<br>

A grandez rasgos el modulo tienen 5 memtodos
METODOS DE CREACION ESCRITURA.
Estos dos metodos se heredan de la clase base de modelos en Odoo, se hereda la creacion y al escritur con el super(Pruebas,self) y se le añade la funcion  de normalizacion de todos los productos para generar los productos en la visual general de todo el sistema.

METODOS DE VALIDACION.
En los metodos de validacion se definen las restricciones para generar bien los lotes y los productos. esta la suma por region que necesita unas veridicaciones extras para que este funcionando a plena maquina y estaria el campo que me permite diferenciar entre un lote disponible y otro no disponible.



## 3. Vistas

## 4. Grupos y Permisos

## 5. Elementos Estáticos 

### 5.1 Botones en vistas tipo List

<div align="justify">
Este módulo de <strong>JavaScript</strong> extiende el comportamiento de las vistas <strong>List</strong> con el fin de agregar un botón personalizado.
La clase personalizada <strong><italic>CustomListController</italic></strong> extiende o hereda la clase <em>ListController</em> la cual incluye el controlador principal para las vistas <em>List</em>. Dentro de esta herencia se incluye un método adicional <strong>customMethod().</strong>
</div>

<div align="justify">
Este método permite ejecutar una acción que complementa la función del módulo. A continuación se muestra la estructura básica de la clase de JS.
</div>
<br>

```javascript
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

class CustomController extends ListController {
    customMethod{
      // Definir acción a realizar por el botón.
    }

}
```

<div align="justify">
Paralelamente se genera la <strong>Plantilla OWL (XML)</strong> en la cual se define visualmente el botón y se enlaza a un manejador de eventos, que en este caso es nuestra función en <em>JS</em>.
La estrucura de esta plantilla se realiza en un archivo xml definiendo:
</div>
<br>

<table>
  <thead>
    <tr>
      <th style="text-align: center;">Campo</th>
      <th style="text-align: center;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">t-name</td>
      <td>Nombre único del template</td>
    </tr>
    <tr>
      <td style="text-align: center;">t-inherit</td>
      <td>Se define la herencia de los botones estándar de la vista tipo List (<code>web.ListView.Buttons</code>)</td>
    </tr>
    <tr>
      <td style="text-align: center;">xpath expr</td>
      <td>Ubicación dentro de la plantilla heredada donde se insertará el contenido. <code>o_list_buttons</code> es la clase usada por Odoo para los botones estándar en vistas tipo lista.</td>
    </tr>
    <tr>
      <td style="text-align: center;">type="button"</td>
      <td>Etiqueta HTML para definir un botón.</td>
    </tr>
    <tr>
      <td style="text-align: center;">t-on-click</td>
      <td>Nombre del método en el controlador JS que se ejecutará al hacer clic. No se deben incluir paréntesis.</td>
    </tr>
    <tr>
      <td style="text-align: center;">&lt;&gt;&quot;&quot;&lt;/&gt;</td>
      <td>Texto visible dentro del botón HTML.</td>
    </tr>
  </tbody>
</table>

<br>

```xml
<?xml version="1.0" encoding="utf-8"?>
<templates>
   <t t-name="id plantilla" t-inherit="web.ListView.Buttons">
       <xpath expr="//div[hasclass('o_list_buttons')]" position="after">
           <button type="button" class="btn btn-primary" style="margin-left: 10px;"  t-on-click="customMethod">
              Nombre del botón
           </button>
       </xpath>
   </t>
</templates>
```





<div align="justify">
Como último, se registra la nueva configuración de la vista bajo el nombre <em>button_registry</em> en el <strong>Registry</strong> de Odoo, incluyendo el controlador generado y la plantilla visual del botón. El nombre puede ser cambiado con total libertad por el desarrolador
</div>
<br>

```javascript
registry.category("views").add("button_registry", {
  // El nombre del botón puede ser modificado
    ...listView,
    Controller: CustomController,
    buttonTemplate: "id plantilla",
});
```

<div align="justify">
Una vez creado el registro, se añade el botón a la vista <em>List</em> de la siguiente forma:
</div>
<br>

```xml
<list js_class="button_registry"> 
<!-- O el nombre que asigne a su registro -->
```



## 8. Desarrollos pendientes y anexos del desarollo 

## 9. Oportunidades de mejora