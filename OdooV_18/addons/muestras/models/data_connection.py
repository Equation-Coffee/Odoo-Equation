import requests

class ExternalAPIModel(models.Model):
    _name="atlas.api.model"
    _description="Modelo de conexión de ATlas con el modulo de muestras"


    def fetch_data_from_atlas(self):
        url = ''
        try : 
            response=requests.get(url)
            if response.status_Code == 200:
                data = response.json()

                for record in data :
                    self.env['models']