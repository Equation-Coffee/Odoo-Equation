

Controladores --- Se usan para manejar peticiones del tipo HTTP. DEmasiado util a la hora de :

    - Exponer rutas web (URLs)
    - Construccion de sitios webs y portales
    - APIs
    - Personalizacion  de endpoints estandars

    @http.route(
    '/shopify/webhook/order',  # Ruta del endpoint
    type='json',               # Tipo de contenido esperado
    auth='none',               # Nivel de autenticación
    csrf=False                 # Protección CSRF (desactivada para webhooks externos)
)



Entornos de pruebas ---  Para hacer pruebas con el controlador necesito hacer visibile el endpoint en linea para que shopify    pueda mandar las peticiones. Por ende ya que tengo el entorno de prubas de manera local, usare ngrok para hacer accesible el endpoint.


Instalacion ngrok

Abir el powershell como administrador 

ingresar este comando (mas adelante investigar que hace y como funciona)

Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
    [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

En toeria este script hace las siguientes operaciones 

✅ Asegura soporte TLS 1.2
✅ Descarga el instalador de Chocolatey
✅ Instala en C:\ProgramData\chocolatey



Luego de esto se reincia el powershell y nuevamente en una pestaña con permisos de administador se verficia la instalacion de choco ( Explicar posteriormente que es choco)

choco --version


luego de esto se hace la instralacon de ngrok con 

choco install ngrok

Con ngrok hay que incializar la el endporint. Para esto en primera instancia se debe crear una cuenta en https://dashboard.ngrok.com/signup y se debe obtener un token de autenticacion. con el token de autentcacion generado la idea es añadir la clave ( como si se tratase de una conexion ssh)

ngrok config add-authtoken <TOKEN>

con la autenticacion verificada, se ejecuta el levantamiento del endpoint de la siguiente manera 

ngrok http <puerto local> esto usara un tunel publico mediante el cual ya se puede hacer llamadaos o petinicones por apis externas que se encuentren en linea.

ahora en shopify para generar el webhook se determina mediante el id de conexion que ngrok nos genera mas la direccion de endpoint generada en el controlador creado para esta funcion 


https://26e375f8c970.ngrok-free.app/shopify/prueba/  (en mi caso ) * A ESTE LE HACE FALTA EL ODOO DENTRO DELA DIRECCION 
LA REDACCIÓN DE ESTE PUNTO FUE PREVIO A DESCUBRIR EL ERROR EN LA DIRECCIÓN QUE ME COSTO COMO DOS DIAS DE ESTRES

inicialiar elngrok







OJO EL SHELL INTERACTIVO DE ODOO SOLO ADMITE INSTRUCCIONES TIPO PYTHON

__________________________________________________________________________________________________

Verificacion de creaciones de controaldores a partir del entorno de Odoo para veridicar funcionamietno.

Problemas con la vinculacion de controlador y priebas inteernas

Claramente los primeros signos de error pueden indicar fallas en la creacion del controlador. Por lo cual hay que verificar la vinculacion de los controladores en el init del modulo y la vinculacion de los scripts en el init del controlador. 

Verificando esto es importante verificar la direccion incial donde esta odoo. Por ejemplo, mi Odoo estaba montado en el puerto 8070:8069, pero cuando incio Odoo mantiene la direccion localhost:8070/odoo. Esta es ladireccion a la cual se debe hacer la llamada. Si solo se incluye localhost8070: generara error.
Adicionalmente se debe escoger base de datos de la siguiente forma ?db=<nombre_base_de_datos>


De esta manera las pruebas desde el power shell para verificacion conexion del controlador deberia ser de esta forma

curl http://localhost:8070/odoo/shopify/ping?db=dk

en dado caso que se necesite realizar un post o algo similar necesitariamos la siguiente direccion 

curl -Method POST http://localhost:8070/odoo/shopify/prueba?db=dk -Body '{"mensaje":"Hola desde curl"}' -ContentType "application/json"






