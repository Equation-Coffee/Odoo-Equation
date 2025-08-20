
<div align="center">
<h1> Automatización Offering List
</div>
<div align="center">
    <em>Juan Pablo Vallejo Montañez</em><br>
    <em>Data & Development Analyst</em><br>
    <em>ia@equationcoffee.com</em>
</div>




## 1. Flujo completo del proceso


## 2. Esquema de Precios 

<p align="center">
  <img width="60%" align="center" src="Images/price_schema.png"/>
 </p>
<p align="center">
  <em>Figura 2 : Esquema calculo de precios ofertable EQN</em>
 </p>


## 2. Modelos   

Un Community Lot es un cafe con dos o tres productores. En ese caso la categorua no es Everyday Blend si no Farm Select Microlots. REvisar esto a profundidad.  ---> Parametrizar en funcion del campo de productor 

A continuación tienen 


Descripción de campos obligatorios al menos para el modelo de productos disponibles.
  - Equation Project --- En el caso de la creacion de modelos desde el modulo se precargara el valoe de "Equation Coffee" 
  - Equation Varietal --- YA ESTA COMO OBLIGATORIO
  - Equation Program --- YA ESTA COMO OBLIGATIO


OJO ANTENCION CON ESTO.
VOY A DEJAR TODOS LOS CAMPOS OBLIGATORIOS UNICMANETE EN EL OFERTABLE. pOSTERIORMENTE DEBERIA APARECEN OBLIGATORIOS EN TODOS LOS MODELOS PERO POR AHORA LO DEJARMOS ASI


PROCESOS 
  - Equation Drying Process  --- Este lo podemos dejar temporalmente deshabilitado.
  - Equation Fermentation Process  -- Este debe ser obligatorio ya que es el campo que se visualiza en el ofertable.
  - Equation Offering Process ---  Este es importante porque este decide cual es el factor de rendimiento asi que tambien es super importante

De la pestaña de inventario tengo los siguientes campos obligatorios :
 - location lo pongo como un campo obligatorio pero le cargo por defecto el valor de Colombia
 - El valor disponible en saco de 70 kg tambien se coloca como un campo obligatorio. Pero ya que se necesita que este campo sea distinto de 0.0 si el lote se esta considerando como un lote disponible necesito hacer una funcion tipo constrain o onechange para que los se verfiquen 3 cosas independietes a la hora de seleccionar un lote como disponible.

 Cada vez que se euncia que un lote esta disponible, lo que se debe verificar son tres cosas
  - el campo de cantidad disponible en 70 kg es mayor a 0
  - el campo de price_selector debe tener valor
  - el campo asociado a la opcion selecionada de sde el price selectordebe ser mayor a 0. Menos para la opcion de df (Diferencial de Compra) , ya que estos elementos pueden tener valores nulos o negativos 


  1️⃣ @api.constrains
Cuándo se ejecuta:
Después de que el registro se guarda en la base de datos (o se intenta guardar).

Ámbito:
Funciona tanto en la interfaz como en llamadas externas (API, imports, automatizaciones, XML-RPC, etc.).

Objetivo:
Garantizar integridad de datos a nivel de servidor, sin importar de dónde venga la información.

Comportamiento:
Si la condición no se cumple, lanza un ValidationError y cancela la transacción.

2️⃣ @api.onchange
Cuándo se ejecuta:
Solo mientras el usuario está editando un registro en el formulario de la interfaz web, antes de guardar.

Ámbito:
No se ejecuta en llamadas externas, imports, ni al guardar directamente. Solo en la vista.

Objetivo:
Cambiar valores de otros campos, mostrar advertencias (Warning), o actualizar dinámicamente la interfaz.

Comportamiento:
No bloquea por sí mismo el guardado (a menos que devuelvas un warning y el usuario decida corregir).

Ejemplo:


## 3. Vistas

Color de fondo de las tablas.
Fuentes.


## 4. Grupos y Permisos

## 5. Desarrollos pendientes y anexos del desarollo 

## 6. Oportunidades de mejora

## 7.Resumen Proyectos

## 8. Resumen de Proyectos