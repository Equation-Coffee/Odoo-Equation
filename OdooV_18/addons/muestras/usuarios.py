import odoo
import odoo.modules.registry
from odoo import api, SUPERUSER_ID

def crear_usuarios(env):
    # Crear los partners asociados a los usuarios
    partners = [
        env['res.partner'].create({'name': 'Usuario 1', 'email': 'usuario1@email.com'}),
        env['res.partner'].create({'name': 'Usuario 2', 'email': 'usuario2@email.com'}),
        env['res.partner'].create({'name': 'Usuario 3', 'email': 'usuario3@email.com'}),
    ]

    # Crear los usuarios con los partners asociados
    for i, partner in enumerate(partners):
        usuario = env['res.users'].create({
            'name': f'Usuario {i + 1}',
            'login': f'usuario{i + 1}',
            'password': f'password_usuario{i + 1}',
            'partner_id': partner.id,
            'company_id': 1,  # Asegúrate que esta sea la empresa correcta
        })
        print(f"Usuario creado: {usuario.name} (ID: {usuario.id})")

if __name__ == "__main__":
    # Inicializar el entorno de Odoo
    odoo.tools.config.parse_config()
