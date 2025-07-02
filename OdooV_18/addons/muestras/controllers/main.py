from odoo import http
from odoo.http import request

class OfferingPDFController(http.Controller):
    @http.route('/muestras/offering/pdf/<int:wizard_id>', type='http', auth='user')
    def download_offering_pdf(self, wizard_id, **kwargs):
        wizard = request.env['muestras.offering_pdf_wizard'].sudo().browse(wizard_id)
        if not wizard.exists():
            return request.not_found()

        pdf_data = wizard.pdf_offering()
        if not isinstance(pdf_data, bytes):
            return request.make_response("PDF inválido", [('Content-Type', 'text/plain')])

        return request.make_response(
            pdf_data,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'attachment; filename="offering_1.pdf"')
            ]   
        )
