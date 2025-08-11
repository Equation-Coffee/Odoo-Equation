from odoo import http
from odoo.http import request 
import logging

_logger = logging.getLogger(__name__) 
_logger.warning("🚨 Cargando archivo shopify.py")


class ShopifyController(http.Controller):
    
    @http.route('/odoo/shopify/prueba',type='http',auth='public',csrf=False)
    def prueba(self,**kwargs):
        data = request.jsonrequest
        _logger.info("Pedido recibido desde Shopify:")
        _logger.info(data)
        return {"status": "ok"}
    
    @http.route('/shopify/ping',type='http',auth='public')
    def prueba_k(self):
        return "pong"
    
    