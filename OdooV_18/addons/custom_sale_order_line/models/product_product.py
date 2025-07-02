# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):

    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        """ Compute a multiline description of this product, in the context of sales
                (do not use for purchases or other display reasons that don't intend to use "description_sale").
            It will often be used as the default description of a sale order line referencing this product.
        """
        country_code = self.env.company.country_id.code
        if country_code == 'CO':
            return super(ProductProduct, self).get_product_multiline_description_sale()
        
        name = self.display_name
        if self.description_sale:
            name = self.description_sale

        return name

