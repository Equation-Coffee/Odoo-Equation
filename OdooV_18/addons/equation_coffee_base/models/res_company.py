# -*- coding: utf-8 -*-
#

import json
import logging
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):

    _inherit = "res.company"

    url_superfinancial_service = fields.Char(
        string='Url superfinancial service')

    body_superfinancial_request = fields.Text(
        string='Body superfinancial request')

    def _get_currency_exchange_cop_to_usd(self):
        records = self.search([('url_superfinancial_service', '!=', False),
                              ('body_superfinancial_request', '!=', False), 
                              ('currency_id', '=', self.env.ref('base.COP').id)])
        for record in records:

            url = record.url_superfinancial_service
            xml_body = record.body_superfinancial_request

            headers = {
                'Content-Type': 'text/xml',
                'charset': 'utf-8',
            }

            response = requests.post(url, data=xml_body, headers=headers)

            if response:
                response_data = response.text
                root = ET.fromstring(response_data)
                value_element = root.find(".//value")
                value_element = float(value_element.text)
                validity_to_datetime = (datetime.now()).replace(
                    hour=0, minute=0, second=0).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                if value_element and validity_to_datetime:
                    curreny = self.env.ref('base.USD')
                    self.env['res.currency.rate'].create({'company_rate': (1.0/value_element), 'currency_id': curreny.id, 'name': str(validity_to_datetime), 'company_id': record.id})

