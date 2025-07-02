# -*- coding: utf-8 -*-
import logging
import operator
import pandas as pd
import base64
import io
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, date, timedelta
from functools import reduce


from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError

from odoo.addons.l10n_co_exogenous_information_reporting.tools.utils import _column_name_field
from odoo.addons.l10n_co_exogenous_information_reporting.tools.utils import dian_countries_codes
from odoo.addons.l10n_co_exogenous_information_reporting.tools.utils import dian_department_codes
from odoo.addons.l10n_co_exogenous_information_reporting.tools.utils import _check_dv


_logger = logging.getLogger(__name__)


class L10ncoExogenousFormatSetting(models.Model):
    _name = "l10n_co.exogenous_format_setting"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exogenous formats configuration model"
    _rec_name = 'format_id'

    @api.constrains('is_it_with_date_range', 'date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.is_it_with_date_range and record.date_start and record.date_end:
                if record.date_start > record.date_end:
                    raise ValidationError(
                        _("The start date must be less than the end date"))

                if record.date_start.year != record.date_end.year:
                    raise ValidationError(
                        _("The start date and end date must be in the same year"))

    active = fields.Boolean(string='Active', default=True, tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', default=lambda self: self.env.company.id)
    format_id = fields.Many2one(
        comodel_name='l10n_co.exogenous_format', string='Format', tracking=True)
    format_setting_line_ids = fields.One2many(
        comodel_name='l10n_co.exogenous_format_setting_line', inverse_name='format_setting_id', string='Format Setting Lines')
    apply_concepts = fields.Boolean(
        string='Apply Concepts', related='format_id.apply_concepts', readonly=True, store=True)

    is_it_with_date_range = fields.Boolean(
        string='Is it with date range?', related='format_id.is_it_with_date_range', readonly=True, store=True)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    journal_ids = fields.Many2many(
        comodel_name='account.journal', string='Journals to be excluded')
    partner_ids = fields.Many2many(
        comodel_name='res.partner', string='Contacts to be excluded')

    binary_file = fields.Binary(string='File', tracking=True)
    binary_file_name = fields.Char(string='File name', tracking=True)
    
    def _get_fields_many2one(self, fields_contact):
        """
            Función que nos permite obtener de los campo de Odoo de contacto cuales son de tipo Many2one
        """
        return fields_contact.mapped('field_odoo_id').filtered(lambda field: field.ttype == 'many2one')

    def _get_last_day_pass_year(self):
        """
            Función que nos permite obtener el ultimo día del año pasado
        """
        return date(date.today().year, 1, 1) - timedelta(days=1)

    def _dynamic_search_read(self, model, domain, fields, order=None):
        """
            Esta función nos permite hacer search_read de manera dinamica
        """
        result = self.env[model].search_read(
            domain=domain,
            fields=fields,
            order=order,
        )
        return result

    def _get_type_documents_by_format(self):
        """
            Esta función nos permite obtener de acuerdo al formato los tipos de documentos de la dian
        """
        model = 'l10n_co.exogenous_document_type'
        domain = [('document_type_table_ids', 'in',
                   self.format_id.document_type_table_id.id), ('type_document_id', '!=', False)]
        fields = ['type_document_id', 'code']
        return self._dynamic_search_read(model=model, domain=domain, fields=fields)

    def _get_columns_account_move_line_by_format(self):
        fields_use_account_move_line = self._get_fields_use_account_move_line()
        return fields_use_account_move_line + ['date', 'partner_id', 'account_id','move_id']

    def _get_accounts_by_format(self):
        vals = {}
        for setting_line in self.format_setting_line_ids:
            if self.format_id.apply_concepts:
                for field_account in setting_line.format_field_id.field_account_ids:
                    for account in field_account.account_ids:
                        if account.id not in vals:
                            vals[account.id] = field_account.concept_id.code
            else:
                for account in setting_line.format_field_id.field_account_ids.account_ids:
                    if account.id not in vals:
                        vals[account.id] = setting_line.format_field_id.id

        return vals

    def _normalice_data_dataframe_partner(self, fields_many2one, df_partners, df_type_documents, df_other_info, fields_to_clear_contact, fields_to_clear_company):
        for key, value in fields_many2one.items():
            if key in df_partners.columns and key in df_other_info.columns:
                mapping_dict = {d['id']: d.get(
                    value, None) for element in df_other_info[key] for d in element}
                df_partners[key] = df_partners[key].apply(
                    lambda x: mapping_dict.get(x[0] if isinstance(x, (list, tuple)) else x, x))
        
        mapping_dict = dict(zip(df_type_documents['type_document_id'].apply(
            lambda x: x[1]), df_type_documents['code']))
        

        df_partners['l10n_latam_identification_type_id'] = df_partners['l10n_latam_identification_type_id'].apply(
            lambda x: mapping_dict.get(x[1] if isinstance(x, (list, tuple)) else x, x))

        for index, row in df_partners.iterrows():
            fields_to_clear = fields_to_clear_company if row['is_company'] else fields_to_clear_contact
            for column in fields_to_clear:
                df_partners.at[index, column] = None

        return df_partners

    def _normalice_and_merge_data_dataframe_account_move_line(self, df_account_move_lines, df_partners):
        
        df_account_move_lines['partner_id'] = df_account_move_lines['partner_id'].apply(
            lambda x: x[0])

        # Realizar la mezcla basada en la columna partner_id y la columna id
        df_result = pd.merge(df_account_move_lines, df_partners,
                             left_on='partner_id', right_on='id', how='left')

        # Eliminar la columna id duplicada, si es necesario
        df_result.drop('id_y', axis=1, inplace=True)
        df_result.drop('id_x', axis=1, inplace=True)
        df_result.drop('partner_id', axis=1, inplace=True)
        
        return df_result

    def _get_field_name_second_field_many2one(self, fields_contact):
        vals = dict()
        for field in fields_contact.filtered(lambda field: field.ttype == 'many2one'):
            if field.field_odoo_id.name not in vals:
                vals[field.field_odoo_id.name] = field.field_odoo_internal_id.name
            else:
                vals[field.field_odoo_id.name] = list(
                    vals.get(field.field_odoo_id.name)).append(field.field_odoo_internal_id.name)
        return vals

    def _get_information_by_account_move_line(self, field_account):

        domain = [('parent_state', '=', 'posted'), ('company_id', '=',
                                                    self.company_id.id), ('account_id', 'in', field_account.account_ids.ids)]

        fields = self._get_columns_account_move_line_by_format()
        order = 'date asc'

        if not self.is_it_with_date_range or field_account.name == 'closing_balance':
            domain.append(('date', '<=', self._get_last_day_pass_year()))
        else:
            domain += [('date', '>=', self.date_start),
                       ('date', '<=', self.date_end)]

        if self.journal_ids:
            domain.append(('journal_id', 'not in', self.journal_ids.ids))


        if self.partner_ids:
            domain += [('partner_id', 'not in', self.partner_ids.ids)]

        partner_ids = set()
        account_move_lines = self._dynamic_search_read(
            model='account.move.line', domain=domain, fields=fields, order=order)

        for aml in account_move_lines:
            if aml['partner_id']:
                partner_ids.add(aml['partner_id'][0])

        return [partner_ids, account_move_lines]

    def _get_values_form_many2one(self, data_source, fields_many2one):
        """ 
            Funcion que nos permite de acuerdo a una informacion obtenida por un search_read
            y con base a unos campos que son de tipo many2one obtener los ids de esos modelos
            y llevarlos en una lista
        """
        values_fields_many2one = dict()
        for ds in data_source:
            for field_many2one in fields_many2one:
                if not isinstance(ds[field_many2one], bool):
                    if field_many2one not in values_fields_many2one:
                        values_fields_many2one[field_many2one] = [
                            ds[field_many2one][0]]
                    else:
                        values_fields_many2one[field_many2one].append(
                            ds[field_many2one][0])
        return values_fields_many2one

    def _get_values_form_dynamic_search_read(self, search_read_by_dynamic_model, field_odoo_internal):
        values = list()
        for value in search_read_by_dynamic_model:
            values.append(value[field_odoo_internal.name])
        return values

    def _get_data_from_dynamic_model(self, partner_info, fields_contact):

        fields_many2one_odoo = self._get_fields_many2one(fields_contact)
        fields_names_many2one_odoo = fields_many2one_odoo.mapped("name")
        values_fields_many2one = self._get_values_form_many2one(
            partner_info, fields_names_many2one_odoo)

        list_fields_name_and_models = fields_contact.mapped('field_odoo_id').filtered(
            lambda field: field.ttype == 'many2one').mapped(lambda field: {field.name: field.relation})
        values_by_dynamic_models = dict()

        for dict_field_name_and_model in list_fields_name_and_models:
            for values in dict_field_name_and_model:
                if values_fields_many2one.get(values, False):
                    field_odoo_internal = fields_contact.filtered(
                        lambda field_line: field_line.field_odoo_id.name == values).mapped('field_odoo_internal_id')

                    model = dict_field_name_and_model[values]
                    domain = [
                        ('id', 'in', list(set(values_fields_many2one.get(values))))]
                    fields = field_odoo_internal.mapped('name')
                    search_read_by_dynamic_model = self._dynamic_search_read(
                        model=model, domain=domain, fields=fields)

                    if values not in values_by_dynamic_models:
                        values_by_dynamic_models[values] = search_read_by_dynamic_model
                    else:
                        values_by_dynamic_models[values].extend(
                            search_read_by_dynamic_model)

        return values_by_dynamic_models

    def _get_information_partner(self, partner_ids, fields_contact):

        if not fields_contact:
            return self._show_message_error(f"No fields are configured for the company: {self.company_id.name}")

        fields_odoo = fields_contact.mapped('field_odoo_id.name')
        fields_odoo.append('is_company')

        model = 'res.partner'
        domain = [('id', 'in', list(partner_ids)), '|', ('active', '=', True), ('active', '=', False)]
        fields = fields_odoo

        partner_info = self._dynamic_search_read(
            model=model, domain=domain, fields=fields)

        other_info_contact = self._get_data_from_dynamic_model(
            partner_info, fields_contact)
        return partner_info, other_info_contact

    def _get_field_account(self, format_setting_line):
        return format_setting_line.mapped('format_field_id').mapped('field_account_ids')

    def _get_field_concept(self):
        return self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_cpt', raise_if_not_found=True)

    def _get_columns_ordered(self, format_fields) -> list:
        vals = list()
        for format_field in format_fields:
            if format_field.id == self._get_field_concept().id:
                vals.append('account_id')
            elif format_field.field_odoo_id:
                vals.append(format_field.field_odoo_id.name)
        return vals

    def _get_fields_to_clear_contact(self, fields_contact):
        return list(set(fields_contact.mapped('field_odoo_id').mapped('name')) - set(fields_contact.filtered(lambda field: field.source == 'contact' and field.applies_to_contact).mapped('field_odoo_id').mapped('name')))

    def _get_fields_to_clear_company(self, fields_contact):
        return list(set(fields_contact.mapped('field_odoo_id').mapped('name')) - set(fields_contact.filtered(lambda field: field.source == 'contact' and field.applies_to_company).mapped('field_odoo_id').mapped('name')))

    def _format_field_by_accumulated(self, format_setting_line):
        vals = dict()
        accounts_accumulated_by = dict()
        for field_account in format_setting_line.format_field_id.field_account_ids:
            for account in field_account.account_ids:
                accounts_accumulated_by[(account.id, account.display_name)] = field_account.name
        vals[format_setting_line.format_field_id.name] = accounts_accumulated_by
        return vals

    def _get_fields_use_account_move_line(self):
        return ['credit', 'debit', 'balance', 'tax_base_amount']

    def _get_fields_format_id(self, format_setting_line):
        return format_setting_line.mapped('format_field_id').mapped('name')

    def _create_original_dataframe(self, format_fields):
        return pd.DataFrame(columns=format_fields.mapped('name'))

    def _get_fields_odoo_and_format(self, fields_contact):
        vals = dict()
        if self.format_id.apply_concepts:
            vals['account_id'] = self._get_field_concept().name

        for field_contact in fields_contact: 
            vals[field_contact.field_odoo_id.name] = field_contact.name

        return vals

    def _get_fields_fill_smaller_amount(self):
        return {
            self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_tdoc', raise_if_not_found=True).name : '43',
            self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_nid', raise_if_not_found=True).name : '222222222',
            self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_raz', raise_if_not_found=True).name : 'cuantías menores',
        }
    

    def _generate_row_by_smaller_amount(self, row_smaller_amount, df):
        new_row = pd.DataFrame(row_smaller_amount, index=[0])
        new_row_columns = df.columns
        new_row = new_row.reindex(columns=new_row_columns)
        df = df.append(new_row, ignore_index=True)
        return df


    def _get_names_columns_direction_contact(self):
        return {
            self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_dpto', raise_if_not_found=True).name: dian_department_codes,
            #self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_mun', raise_if_not_found=True).name: dian_cities_by_department,
            self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_pais', raise_if_not_found=True).name: dian_countries_codes
        }

    def _normalize_partner_street(self, names_columns_direction_contact, original_dataframe):
        for column in names_columns_direction_contact:
            replacement_dict = {key.lower(): value for key, value in names_columns_direction_contact[column].items()}
            if column in original_dataframe.columns:
                original_dataframe[column] = original_dataframe[column].str.lower().map(replacement_dict)
        return original_dataframe

    def _normalize_partner_identification(self, original_dataframe):
        def procesar_identificacion(row):
            nit = row[field_identification_number_name]
            dv_actual = None
            dv_nuevo = None
            numero = nit
            if nit:
                if '-' in nit:
                    numero, dv_actual = nit.split('-')
                else:
                    numero, dv_actual = nit[:-1], nit[-1]

                try:
                    dv_nuevo = _check_dv(numero) if self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_nid', raise_if_not_found=True).name in original_dataframe.columns else None
                except:
                    dv_nuevo = dv_actual

            return pd.Series([numero, dv_nuevo if dv_nuevo != dv_actual else dv_actual])

        filter = original_dataframe[self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_tdoc', raise_if_not_found=True).name] == '31'
        field_identification_number_name = self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_nid', raise_if_not_found=True).name
        field_dv_name = self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_dv', raise_if_not_found=True).name if self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_nid', raise_if_not_found=True).name in original_dataframe.columns else None

        filtered_dataframe = original_dataframe[filter].reset_index()
        results = filtered_dataframe.apply(procesar_identificacion, axis=1)
        if field_dv_name:
            original_dataframe.loc[filter, [field_identification_number_name, field_dv_name]] = results.values
        else:
            original_dataframe.loc[filter, field_identification_number_name] = results[0].values

        return original_dataframe

    def _select_fields_from_account_move_line(self, setting_line, df_account_move_lines):

        format_field_accumulated = self._format_field_by_accumulated(setting_line)
        def get_column_value(row, key):
            column_to_get = format_field_accumulated.get(key, None)
            if isinstance(column_to_get, dict):
                # Obtén el account_id de la fila actual
                account_id = row['account_id']
                # Obtén el valor correspondiente al account_id
                operation = column_to_get.get(account_id, None)
                if operation:
                    # Mapea las operaciones a las columnas correspondientes
                    operation_to_column = {
                        'credit': 'credit',
                        'debit': 'debit',
                        'balance': 'balance',
                        'tax_base_amount': 'tax_base_amount',
                        'closing_balance': 'closing_balance'
                    }
                    # Obtén la columna correspondiente a la operación
                    column = operation_to_column.get(operation, None)
                    if column:
                        # Calcula el valor de la columna
                        if operation == 'closing_balance':
                            if account_id[1].startswith(('1')):
                                return row['debit'] - row['credit']
                            elif account_id[1].startswith(('2')):
                                return  row['credit'] - row['debit']
                        return row[column]
            return 0.0

        clave_diccionario, valor_diccionario = next(iter(format_field_accumulated.items()))

        df_account_move_lines[clave_diccionario] = df_account_move_lines.apply(
            lambda row: get_column_value(row, clave_diccionario), axis=1)

        return df_account_move_lines

    def _get_field_or_concepts_and_field(self):
        vals = {}
        for setting_line in self.format_setting_line_ids:
            if self.format_id.apply_concepts:
                for field_account in setting_line.format_field_id.field_account_ids:
                    if field_account.concept_id.code not in vals:
                        vals[field_account.concept_id.code] = [field_account.format_field_id.name]
                    else:
                        vals[field_account.concept_id.code].append(field_account.format_field_id.name)
            else:
                for field_account in setting_line.format_field_id.field_account_ids:
                        vals[setting_line.format_field_id.name] = setting_line.format_field_id.name
        return vals


    def process_smaller_amount_dataframe(self, original_dataframe):
        if not self.format_id.applying_smaller_amounts:
            return original_dataframe

        concept_or_field = self._get_field_or_concepts_and_field()

        if self.format_id.apply_concepts:
            for concept in concept_or_field:
                # Crear una nueva fila con los campos correspondientes para el concepto
                new_row = self._get_fields_fill_smaller_amount()
                new_row.update({self._get_field_concept().name: concept})
                
                # Bandera para verificar si se necesita agregar una nueva fila
                add_new_row = False
                
                for field in concept_or_field[concept]:
                    # Filtrar las filas que tienen valores menores al umbral
                    smaller_values_mask = (original_dataframe[field] <= self.format_id.smaller_ammounts) & (original_dataframe[field] >= (-1 * self.format_id.smaller_ammounts)) &\
                                        (original_dataframe[self._get_field_concept().name] == concept)
                    
                    # Sumar los valores absolutos menores al umbral
                    smaller_amounts = original_dataframe.loc[smaller_values_mask, field].sum()
                    
                    # Si hay valores menores al umbral, actualiza la nueva fila y el DataFrame original
                    if smaller_amounts != 0:
                        # Poner los valores menores a cero en el DataFrame original
                        original_dataframe.loc[smaller_values_mask, field] = 0
                        
                        # Actualizar la nueva fila con la suma de los valores absolutos menores
                        new_row.update({field: smaller_amounts})
                        add_new_row = True
                
                # Agregar la nueva fila al DataFrame si tiene valores actualizados
                if add_new_row:
                    original_dataframe = self._generate_row_by_smaller_amount(new_row, original_dataframe)
        else:
            new_row = self._get_fields_fill_smaller_amount()
            
            # Bandera para verificar si se necesita agregar una nueva fila
            add_new_row = False
            
            for field in concept_or_field:
                # Filtrar las filas que tienen valores menores al umbral
                smaller_values_mask = (original_dataframe[field] <= self.format_id.smaller_ammounts) & (original_dataframe[field] >= (-1 * self.format_id.smaller_ammounts))
                
                # Sumar los valores absolutos menores al umbral
                smaller_amounts = original_dataframe.loc[smaller_values_mask, field].sum()
                
                # Si hay valores menores al umbral, actualiza la nueva fila y el DataFrame original
                if smaller_amounts != 0:
                    # Poner los valores menores a cero en el DataFrame original
                    original_dataframe.loc[smaller_values_mask, field] = 0
                    
                    # Actualizar la nueva fila con la suma de los valores absolutos menores
                    new_row.update({field: smaller_amounts})
                    add_new_row = True
            
            # Agregar la nueva fila al DataFrame si tiene valores actualizados
            if add_new_row:
                original_dataframe = self._generate_row_by_smaller_amount(new_row, original_dataframe)

        return original_dataframe

    def _group_dataframe(self, setting_line, columns_ordered, unique_keys_by_format, fields_contact, df_account_move_lines):
        operations = {column: 'first' if column not in self._get_fields_format_id(setting_line) else 'sum'
                    for column in columns_ordered}

        df_account_move_lines_copy = df_account_move_lines.copy(deep=True)
        filtered_grouped = df_account_move_lines_copy.groupby(unique_keys_by_format)

        result = filtered_grouped.agg(operations).round(0)
        if fields_contact:
            return result.rename(columns=self._get_fields_odoo_and_format(fields_contact))
        return result

    def generate_and_download_report(self):
        # Check if format settings are available
        if not self.format_setting_line_ids:
            return self._show_message_error(f"No format settings configured for format: {self.format_id.code}")

        # Retrieve format fields
        format_fields = self.env['l10n_co.exogenous_format_field'].search(
            [('format_ids', 'in', self.format_id.id)], order="sequence asc")

        if not format_fields:
            return self._show_message_error(f"No fields configured for format: {self.format_id.code}")

        # Filter fields based on source
        fields_contact = format_fields.filtered(lambda ff: ff.source == 'contact')

        # Get fields to clear for contact and company
        fields_to_clear_contact = self._get_fields_to_clear_contact(fields_contact)
        fields_to_clear_company = self._get_fields_to_clear_company(fields_contact)

        # Get unique keys for format
        unique_keys_by_format = format_fields.filtered(lambda ff: ff.is_unique_key).mapped(
            'field_odoo_id').mapped('name')

        unique_keys_by_format_field = format_fields.filtered(lambda ff: ff.is_unique_key).mapped('name')

        if self.format_id.apply_concepts:
            unique_keys_by_format = unique_keys_by_format + ['account_id']

        wb = Workbook()
        ws = wb.active
        ws = _column_name_field(format_fields.mapped('name'), ws)

        # Create original dataframe
        original_dataframe = self._create_original_dataframe(format_fields)
        columnas_originales = original_dataframe.columns
        original_dataframe_without_partner = original_dataframe.copy(deep=True)

        row_smaller_amount = self._get_fields_fill_smaller_amount()
        names_columns_direction_contact = self._get_names_columns_direction_contact()
        concepts = self._get_accounts_by_format()

        get_information = list()

        for setting_line in self.format_setting_line_ids:
            
            field_accounts = self._get_field_account(setting_line)
            account_move_lines = list()
            partner_ids = list()
            
            for field_account in field_accounts:
                data = self._get_information_by_account_move_line(field_account)
                partner_ids += data[0]
                account_move_lines += data[1]

            if not account_move_lines or not partner_ids:
                get_information.append(False)
                continue
            else:
                get_information.append(True)

            partners, other_info_contact = self._get_information_partner(partner_ids, fields_contact)

            if isinstance(partners, dict) and partners.get('tag', False):
                return partners

            df_type_documents = pd.DataFrame(self._get_type_documents_by_format())
            df_account_move_lines = pd.DataFrame(account_move_lines)
            df_account_move_lines_without_partner = df_account_move_lines[df_account_move_lines['partner_id'].isna() | (df_account_move_lines['partner_id'] == '') | (df_account_move_lines['partner_id'] == False)]
            df_account_move_lines = df_account_move_lines[~df_account_move_lines['partner_id'].isna() & (df_account_move_lines['partner_id'] != '') & (df_account_move_lines['partner_id'] != False)]
            df_partners = pd.DataFrame(partners)
            df_partners = df_partners.fillna('')
            df_partners = df_partners.replace(False, '')
            df_other_info = pd.DataFrame([other_info_contact])

            df_partners = self._normalice_data_dataframe_partner(
                self._get_field_name_second_field_many2one(fields_contact),
                df_partners, df_type_documents, df_other_info, fields_to_clear_contact, fields_to_clear_company
            )

            df_account_move_lines = self._normalice_and_merge_data_dataframe_account_move_line(
                df_account_move_lines, df_partners)

            df_account_move_lines = self._select_fields_from_account_move_line(setting_line, df_account_move_lines)
            df_account_move_lines_without_partner = self._select_fields_from_account_move_line(setting_line, df_account_move_lines_without_partner)

            columns_ordered = self._get_columns_ordered(format_fields)
            columns_ordered = columns_ordered + [setting_line.format_field_id.name]

            df_account_move_lines['account_id'] = df_account_move_lines['account_id'].apply(lambda x: concepts.get(x[0], x[0]))
            df_account_move_lines_without_partner['account_id'] = df_account_move_lines_without_partner['account_id'].apply(lambda x: concepts.get(x[0], x[0]))

            #result = self._group_dataframe(setting_line, columns_ordered, unique_keys_by_format, fields_contact, df_account_move_lines)
            result = df_account_move_lines.rename(columns=self._get_fields_odoo_and_format(fields_contact))
            original_dataframe = pd.concat([original_dataframe, result], ignore_index=True)
            
            original_dataframe_without_partner = pd.concat([original_dataframe_without_partner, df_account_move_lines_without_partner], ignore_index=True)

        if not any(get_information):
            return self._show_message_error("No information found with these parameters")

        original_dataframe = original_dataframe.reindex(columns=columnas_originales)
        #original_dataframe_without_partner = original_dataframe_without_partner.reindex(columns=columnas_originales)

        original_dataframe = self._normalize_partner_street(names_columns_direction_contact, original_dataframe)
        original_dataframe = self._normalize_partner_identification(original_dataframe)

        operations = {column: 'first' if column not in self.format_setting_line_ids.mapped('format_field_id').mapped('name') else 'sum'
            for column in columnas_originales}

        filtered_grouped = original_dataframe.groupby(unique_keys_by_format_field)
        original_dataframe = filtered_grouped.agg(operations).round(0)
        original_dataframe = self.process_smaller_amount_dataframe(original_dataframe)


        if self.format_id.apply_concepts:
            operaitions_2 = {}
            for field in self.format_setting_line_ids.mapped('format_field_id').mapped('name'):
                operaitions_2[field] = 'sum'
            operaitions_2['account_id'] = 'first'
            filtered_grouped2 = original_dataframe_without_partner.groupby(['account_id'])
            original_dataframe_without_partner = filtered_grouped2.agg(operaitions_2).round(0)
        else:
            sum_row = original_dataframe_without_partner[self.format_setting_line_ids.mapped('format_field_id').mapped('name')].sum()
            original_dataframe_without_partner = pd.DataFrame([sum_row])
        
        for row_data in dataframe_to_rows(original_dataframe_without_partner, index=False, header=False):
            new_row = self._get_fields_fill_smaller_amount()
            
            # Llenar new_row de manera dinámica usando dynamic_columns
            if self.format_id.apply_concepts:
                new_row.update({self._get_field_concept().name: row_data[original_dataframe_without_partner.columns.get_loc('account_id')]})

            for col_name in self.format_setting_line_ids.mapped('format_field_id').mapped('name'):
                new_row[col_name] = row_data[original_dataframe_without_partner.columns.get_loc(col_name)]

            new_row[self.env.ref('l10n_co_exogenous_information_reporting.l10n_co_exogenous_format_field_raz', raise_if_not_found=True).name] = 'Movimientos sin terceros'
            original_dataframe = self._generate_row_by_smaller_amount(new_row, original_dataframe)
 
        condition = reduce(operator.or_, [(original_dataframe[col] != 0) for col in self.format_setting_line_ids.mapped('format_field_id').mapped('name')])

        # Filtrar el DataFrame
        original_dataframe = original_dataframe[condition]

        for row_data in dataframe_to_rows(original_dataframe, index=False, header=False):                   
            ws.append(row_data)

        output = io.BytesIO()
        wb.save(output)
        file_name = f"exogena_{self.format_id.code}_{datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)}"
        self.binary_file = base64.b64encode(output.getvalue())
        self.binary_file_name = f"{file_name}.xlsx"


    def _show_message_error(self, message):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'danger',
                'sticky': True,
                'message': _(message),
            }
        }
