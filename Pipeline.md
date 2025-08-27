Tareas pendientes del Pipeline 

Prioritarias 
    PRIMEROS MOVIMEINTOS DEL PIPELINE
    modulo de contactos
        - Filtros predeterminados segmenrado UNICAMENTE CLIENTES CORRSPONDIENTES AL EQUIPO DE TRABAJO ---> Variable en la base de datos.(filtro de clientes) 
        Filtro ---> Clinete equipos de ventas.    vista.search = team_id  
        - Campos dentro de los contacntos obligatorios ---- Campos de informaicon contable por ejemplo+
            REvisar que campos se deben quitar/dejar como no obligatorios.
        - Cada creación por parte del equipo comercial --->  Debe ser marcado como cliente.
        - Las malditass listas de trabajo ---> Campo de trabajo  --- Se me hace una maricada pero toca hacerlo.
        - 







Hay demasiadas cosas por hacer el dia de hoy.
Inicialmente lo que haremos sera la siguiente.

    - Modificar el action window de la pestaña de clientes para realizar todos los filtros de usuario pertinentes.El objetivo es que los clientes que pueda ver un usuario sean unicamente los que tiene asignado equipo comercial.

    De este cambio inicial tenemos 3 espacios. El primer es generar un campo que me permita seleccionar el equipo comercial o la region a la que pertenece.

    Dos es generar un filtro por el equipo al que pertenece el usuario.

    Tres difurcar las visuales en dos grupos. Uno con todos estos usuarios y el otro    


    Respecto al filtro de la vista de clients o de contactos se hizo un filtro default a paritir del campo equation_coffee_sales_team (Equipo de ventsa) y de esta manera se tiene una visual de los clinetes unicamente de su región. Ahora, esto no soluciona el error de que todos los clientes aparezcan en las listas de compra,venta muestras entre otros. Por esta razón, dejo como mapeado una tarea que es vincular alguna función de registros que permita a los usuarios filtrar cada una de las listas de contactos por su region comercial y por usuarios. Esta parte esta clara.

    Ahora, para hacer el filtro completo de cliente, proovedor, y demas cosas. Vamos a enlazar un modelo en el cual se almacenen los disintintos tipos de usuarios que se requieren para mapear de manera excelente todo el material de clientes.

    Ahora en contactos solo quiero tener a los contactos que se llaman contactos valga la redundancia, auqellos que sean direcciones de delivery las pienso ocultar para que solo salgan compañias como tal y los contactos de delivery unicamente esten en la pestaña asociada a cada persona. Al igual no quiero perder la visibilidad de esos campos en el modelo. Solo quiero que no se carguen en la vista tipo list o tipo kanban pero si donde tienen que ir.


    Prioridad Numero 1. Quitar este triple hpta campo de contabilidad.  LOGRADO
    Prioirdad Numero 2. Hacer que la busqueda por nombre permita completar el usuario.
    Prioridad Numero 3. Colocar actividades en las interaccione.
    Prioridad Numero 4. 