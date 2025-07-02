import io
import base64
import xlsxwriter
from odoo import models, fields, api
import logging
import json
from datetime import datetime, date as dt_date

_logger = logging.getLogger(__name__)

class CommissionReportWizard(models.TransientModel):
    _name = 'commission.report.wizard'
    _description = 'Wizard para Reporte de Comisiones'

    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    journal_ids = fields.Many2many(comodel_name="account.journal",
                                   relation="report_wizard_journal_rel", column1="wizard_id", column2="journal_id", string="Journals")
    
    def action_generate_report(self):
        account_moves = self._get_account_move()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        worksheet = workbook.add_worksheet()
        bold_format = workbook.add_format({'bold': True})
        headers = [
            'Número', 'Fecha', 'Asociado', 
            'Asociado/ Tipo de documento de identificación', 'Asociado/Número de identificación',
            'Asociado/País', 'Region','Origen', 'Plazos de pago',
            'Estado de pago', 'Estado', 'Fecha de vencimiento',
            'Total Factura en dolares', 'Total Factura en Moneda Local', 
            'Importe adeudado', 'Moneda', 'Vendedor', 'Equipo de ventas', 'Código HS', 'Incoterm', 'Referencia', 'Pagos Moneda Local', 'Pagos USD', 'Fecha pagado', 'Diario','Memo','Líneas de factura','Líneas de factura/Líneas analíticas',
            'Líneas de factura/Producto','Projecto','Programa','Varietal','Líneas de factura/Cantidad','Líneas de factura/Unidad de Medida',
            'Líneas de factura/Precio Unitario','Líneas de factura/Descuento (%)','Total','Líneas de factura/Impuestos','Líneas de factura/Cuenta','Líneas de factura/Diario'
        ]

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold_format)

        row_num = 1
        for move in account_moves:
            initial_row_num = row_num
            total_in_dollars = move.amount_total_in_currency_signed or 0
            total_in_pesos = move.amount_untaxed_signed or 0
            worksheet.write(row_num, 0, move.name or '')
            worksheet.write(row_num, 1, str(move.date) or '')
            worksheet.write(row_num, 2, move.partner_id.name or '')
            worksheet.write(row_num, 3, move.partner_id.l10n_latam_identification_type_id.name or '')
            worksheet.write(row_num, 4, move.partner_id.vat or '')
            worksheet.write(row_num, 5, move.partner_id.country_id.name or '')
            worksheet.write(row_num, 6, move.partner_id.equation_coffee_region or '')
            worksheet.write(row_num, 7, move.journal_id.name or '')
            worksheet.write(row_num, 8, move.invoice_payment_term_id.name or '')
            worksheet.write(row_num, 9, move.payment_state or '')
            worksheet.write(row_num, 10, move.state or '')
            worksheet.write(row_num, 11, str(move.invoice_date_due) or '')
            worksheet.write(row_num, 12, move.amount_total_in_currency_signed or 0)
            worksheet.write(row_num, 13, move.amount_untaxed_signed or 0)
            worksheet.write(row_num, 14, move.amount_residual or '')
            worksheet.write(row_num, 15, move.currency_id.name or '')
            worksheet.write(row_num, 16, move.invoice_user_id.name or '')
            worksheet.write(row_num, 17, move.team_id.name or '')
            worksheet.write(row_num, 18, move.equation_coffee_hs_code or '')
            worksheet.write(row_num, 19, move.invoice_incoterm_id.name or '')
            worksheet.write(row_num, 20, move.equation_coffee_reference or '')

            payment_data = []
            
            if total_in_dollars < 0:
                worksheet.write(row_num, 21, total_in_pesos) 
                worksheet.write(row_num, 22, total_in_dollars) 
            else:
                payments_widget = move.invoice_payments_widget if isinstance(move.invoice_payments_widget, dict) else json.loads(move.invoice_payments_widget or '{}')
                _logger.info(f"Payments widget for move {move.name}: {payments_widget}")
                payment_data  = [
                    {
                        'amount_foreign_currency': payment['amount_foreign_currency'],
                        'amount_company_currency': payment['amount_company_currency'],
                        'date': self._format_date(payment.get('date')),
                        'journal_name': payment.get('journal_name', ''),
                        'ref': payment.get('ref', '')
                    }
                    for payment in payments_widget.get('content', [])
                    if payment.get('name') != 'Diferencia en tasa de cambio de moneda'
                ]

                for payment in payment_data:
                    worksheet.write(row_num, 21, payment['amount_company_currency'])
                    worksheet.write(row_num, 22, payment['amount_foreign_currency'])
                    worksheet.write(row_num, 23, payment['date'])
                    worksheet.write(row_num, 24, payment['journal_name'])
                    worksheet.write(row_num, 25, payment['ref'])
                    row_num += 1

            row_num = initial_row_num
            for move_line in move.invoice_line_ids:
                worksheet.write(row_num, 26, move_line.product_id.name or '')
                worksheet.write(row_num, 27, ', '.join(move_line.analytic_line_ids.mapped('name')) or '')
                worksheet.write(row_num, 28, move_line.product_id.name or '')
                worksheet.write(row_num, 29, move_line.product_id.product_tmpl_id.equation_coffee_project_id.name or '')
                worksheet.write(row_num, 30, move_line.product_id.product_tmpl_id.equation_coffee_program_id.name or '')
                worksheet.write(row_num, 31, move_line.product_id.product_tmpl_id.equation_coffee_varietal_id.name or '')
                worksheet.write(row_num, 32, move_line.quantity or 0)
                worksheet.write(row_num, 33, move_line.product_uom_id.name or '')
                worksheet.write(row_num, 34, move_line.price_unit or 0)
                worksheet.write(row_num, 35, move_line.discount or 0)
                worksheet.write(row_num, 36, move_line.price_subtotal or 0)
                worksheet.write(row_num, 37, ', '.join(move_line.tax_ids.mapped('name')) or '')
                worksheet.write(row_num, 38, move_line.account_id.display_name or '')
                worksheet.write(row_num, 39, move_line.journal_id.name or '')
              
                row_num += 1
                
            row_num = max(row_num, len(payment_data) + initial_row_num)

        workbook.close()

        output.seek(0)
        file_content = output.read()
        output.close()

        attachment = self.env['ir.attachment'].create({
            'name': 'informe_de_comisiones.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(file_content),
            'store_fname': 'informe_de_comisiones.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'self',
        }
    
    def _get_account_move(self):
        account_move = self.env['account.move'].search([
            ("journal_id", "in", self.journal_ids.ids),
            ("date", ">=", self.start_date),
            ("date", "<=", self.end_date)
        ])
        if account_move:
            return account_move
        return False

    def _format_date(self, date_value):
        if isinstance(date_value, (datetime, dt_date)):
            return date_value.strftime('%Y-%m-%d')
        return ''