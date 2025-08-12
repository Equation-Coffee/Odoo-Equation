Aqui pondre documentacion termporal relacionada con los procesos o etapas de SQL.


SQL de constulras para manejo de invetarios 

WITH lotes_input AS (
    SELECT UNNEST(ARRAY[
        'PTNLG24020', 'PTNLS24031', 'PTNLG24040', 'PTNLS24050',
        'PTNLG24054', 'PTNLG24055', 'PTNLG24061', 'PTNLA25001',
        'PTNLS25004', 'PTNLS25005', 'PTNLS25011', 'PTNLS25012',
        'PTNLS25014', 'PTNLG25015', 'PTNLG25016', 'PTNLS25018',
        'PTNLG25019', 'PTNLS25021', 'PTNLS25022', 'PTNLG25023',
        'PTNLG25024', 'PTNLG25025', 'PTNLS25027', 'PTNLS25032'
    ]) AS lote
)
select  mp.lote,mp.project,i.lote,
	case when i.lote is not null then 'Existe' else 'No existe' end as "Existecia"
from muestras_prueba mp
left join lotes_input i on i.lote = mp.lote  
where equation_project = 1 and mp.available ='dis'

El codigo anterior me permite reviasr que lotes estan marcados como disponibles pero que no estan en el ofertable (Lotes que estando en Odoo no deberia estar para la muestra).
Variar el project FP es 5 , LP es 1.

Para saber que lotes que faltan en odoo se usa la siguiente consulta partiendo del select 'lote'

WITH lotes_input AS (
SELECT unnest(ARRAY[
  'FPNLG25011','FPNL825012','FPNLG25013','FPNLG25015','FPNLG25019',
  'FPNLG25027','FPNLG25028','FPNLG25030','FPNLG25031','FPNLG25032',
  'FPNLG25036','FPNLG25037','FPNLG25038','FPNLG25042','FPNLG25048',
  'FPNLG25050','FPNLG25052','FPNLG25056','FPNLG25057','FPNLG25058',
  'FPNLG25059','FPNLG25060','FPNLG25065','FPNLG25069','FPNLG25070',
  'FPNLG25072','FPNLG25073','FPNLG25074','FPNLG25075','FPNLG25076',
  'FPNLG25079','FPNLG25080','FPNLG25081','FPNLG25082','FPNLG25084'
]) AS lote
),atlas as(
	select * from muestras_prueba where available = 'dis'
) 
select  i.Lote as ofertable, a.lote as atlas,a.project,a.available,
	case when a.lote is not null then 'Existe' else 'No existe' end as "Existecia"
from lotes_input i 
left join atlas a on i.lote = a.lote 
_________________________________________

Tareas con lotes pendientes en Odoo este lote esta repedito FPNLG25013 pensar que hacer con esto 
FPNLG25027 Tambien tiene problmas de duplicados 


Para buscar menus 

SELECT id, name, parent_id 
FROM ir_ui_menu 
WHERE name->>'en_US' ='CRM';

SELECT module, name 
FROM ir_model_data 
WHERE model='ir.ui.menu' AND res_id=143;

reemplzar el id por el que arroje la consylta anteriro 