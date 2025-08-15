from odoo import models, fields, api
from datetime import date

class Price(models.Model):
    _name = "muestras.price"
    _description = "Precios Productos Disponibles"

    name = fields.Char(string="Nombre", required=True)
    value = fields.Float(string="Valor")
    date = fields.Date(string="Fecha")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Price Type must be unique!'),
    ]

    def write(self, vals):
        res = super(Price, self).write(vals)  
        if 'value' in vals:
            for record in self:
                if record.name == "USD/COP Exchange Rate":
                    trm_value = vals.get("value", record.value) or record.value  
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"trm": trm_value})
                if record.name == "Coffee C Price":
                    price_c_value = vals.get("value", record.value) or record.value  
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"price_c": price_c_value})
                if record.name == "EUR/USD Exchange Rate":
                    eu_us_value = vals.get("value", record.value) or record.value  
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"eu_us": eu_us_value})
                if record.name == "Utilidad Microlote":
                    uml_value = vals.get("value",record.value) or record.value
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"uml":uml_value})
                if record.name == "Utilidad Regional":
                    ur_value = vals.get("value",record.value) or record.value
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"ur":ur_value})
                if record.name == "FOB Cost":
                    c_fob_value = vals.get("value",record.value) or record.value
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"c_fob":c_fob_value})
                if record.name == "Coffee Load":
                    coffee_load = vals.get("value",record.value) or record.value
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({"coffee_load":coffee_load})
                if record.name == "SPOT Cost US":
                    spot_cost_us = vals.get("value",record.value) or record.value
                    for disponible in record.env["muestras.disponible"].search([]):
                        disponible.write({'spot_cost_us':spot_cost_us})        
                if record.name == "SPOT Cost EU":
                    spot_cost_eu = vals.get("value",record.value) or record.value
                    for disponible in record.env['muestras.disponible'].search([]):
                        disponible.write({'spot_cost_eu':spot_cost_eu}) 
                if record.name == "Decaf Cost":
                    decaf_cost = vals.get("value",record.value) or record.value
                    for disponible in record.env['muestras.disponible'].search([]):
                        disponible.write({'decaf_cost':decaf_cost})
                if record.name == "US Tariffs":
                    us_tariffs = vals.get("value",record.value) or record.value
                    for disponible in record.env['muestras.disponible'].search([]):
                        disponible.write({'us_tariffs':us_tariffs}) 
        return res
    
    
    @api.model
    def usd_cop(self,date=None):
        date = date or fields.Date.today()
        us_base = self.env.ref('base.USD')
        cop_base = self.env.ref('base.COP')
        company =  self.env.company

        rate = us_base._get_conversion_rate(
            us_base,
            cop_base,
            company,
            date
        )
        return rate 
    

    @api.model
    def cron_trm(self):
        import requests
        from bs4 import BeautifulSoup
        url_trm = 'https://www.dolar-colombia.com/'
        print(url_trm)
        response = requests.get(url_trm,timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            exchange_rate = soup.find('h2', class_='box-exchange-rate')
            if exchange_rate:
                value = exchange_rate.find('span', class_='exchange-rate')
                if value:
                    trm = float(value.text.strip().replace(',',''))
                    print(f"TRM: {trm}")
                    trm_register =self.env['muestras.price'].search([('name','=',"USD/COP Exchange Rate")],limit=1)
                    if trm_register:
                        trm_register.write({'value':trm,'date':date.today()})
                    return trm
                else:
                    print("No se encontró el valor dentro del span 'exchange-rate'.")
            else:
                print("No se encontró el elemento 'box-exchange-rate'.")
        else:
            print(f"Error al hacer la solicitud: {response.status_code}")



# zjXLSp_3Z5pDxzFkqiYf
    