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


class ResCountry(models.Model):

    _inherit = "res.country"

    enforce_cities=fields.Boolean(string='Enforce_cities')

