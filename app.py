from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Configuración de Flask-Mail para Outlook
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Servidor SMTP de Outlook
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'boris.herrera@uvm.cl'  # Tu correo institucional de Outlook
app.config['MAIL_PASSWORD'] = '2029.,BH*'  # Contraseña o token de aplicación
app.config['MAIL_DEFAULT_SENDER'] = 'boris.herrera@uvm.cl'  # Remitente por defecto

mail = Mail(app)

def enviar_correo(email,nombre, token):
    mensaje = Message(
        subject="Invitación Inauguración Año Académico UVM 2025",
        recipients=[email],
        html=f"""
        <!DOCTYPE html>
        <html lang="es" style="margin:0;padding:0">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Invitación Inauguración Año Académico UVM 2025</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    border: none;
                    background-color: #ffffff;
                    font-family: Arial, sans-serif;
                }}
                .mailpoet_template {{
                    border-collapse: collapse;
                    border-spacing: 0;
                    width: 100%;
                    border: none !important;
                }}
                .mailpoet_content-wrapper {{
                    width: 660px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    max-width: 100%;
                    border: 1px solid #e0e0e0; /* Borde de 1px alrededor del contenido */
                    overflow: hidden;
                }}
                .mailpoet_image img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    padding-top:20px;
                }}
                .mailpoet_text {{
                    font-size: 16px;
                    color: #5b6770;
                    text-align: center;
                    line-height: 1.6;
                }}
                .mailpoet_button {{
                    display: inline-block;
                    margin: 20px 0;
                    padding: 10px 20px;
                    background-color: #5b6770;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                .mailpoet_footer {{
                    text-align: center;
                    color: #5b6770;
                    font-size: 12px;
                    padding: 10px 20px;
                }}
            </style>
        </head>
        <body>
            <table class="mailpoet_template" border="0" width="100%" cellpadding="0" cellspacing="0">
                <tbody>
                    <!-- Contenido Principal -->
                    <tr>
                        <td class="mailpoet_content" align="center">
                            <table class="mailpoet_content-wrapper" border="0" cellpadding="0" cellspacing="0">
                                <tbody>
                                    <!-- Logo UVM -->
                                    <tr>
                                        <td class="mailpoet_image" align="center">
                                            <img src="https://comunicaciones.uvm.cl/wp-content/uploads/2023/12/l-uvm.png" alt="Universidad Viña del Mar" width="109">
                                        </td>
                                    </tr>
        
                                    <!-- Imagen Central de Rodelillo -->
                                    <tr>
                                        <td class="mailpoet_image" align="center" style="padding: 10px 20px;">
                                            <img src="https://comunicaciones.uvm.cl/wp-content/uploads/2025/04/invitacion-rodelillo.jpg" alt="Invitación Rodelillo" width="620">
                                        </td>
                                    </tr>
        
                                    <!-- Texto de Invitación -->
                                    <tr>
                                        <td class="mailpoet_text" style="padding: 10px 20px;">
                                            <p>
                                                <strong>Carlos Isaac Pályi</strong>, rector de la Universidad Viña del Mar, tiene el agrado de invitar a usted a la
                                            </p>
                                            <h1 style="font-size: 22px; color: #333333;">INAUGURACIÓN DEL AÑO ACADÉMICO 2025</h1>
                                            <p>
                                                En la oportunidad, <strong>Rodrigo Mundaca Cabrera</strong>, gobernador de la Región de Valparaíso, dictará la clase magistral:
                                                <em>"La descentralización le cambia la vida a las personas".</em>
                                            </p>
                                            <p>
                                                El encuentro se realizará el <strong>jueves 24 de abril de 2025</strong>, a las <strong>10.30 hrs.</strong>,
                                                en el <strong>Auditorio -240 del Campus Rodelillo</strong> (Avda. Agua Santa 7055, Viña del Mar.)
                                            </p>
                                        </td>
                                    </tr>
        
                                    <!-- Botón de Confirmación -->
                                    <tr>
                                        <td align="center">
                                            <a href="http://127.0.0.1:5000/confirmar/{token}" class="mailpoet_button">Confirmar Asistencia AQUÍ</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="mailpoet_footer">
                                            <span>Contacto: 32 246 2420 · Viña del Mar, abril 2025</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        """
    )
    mail.send(mensaje)

# Modelo actualizado con un campo "token"
class Invitacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # pendiente, aceptado, rechazado
    token = db.Column(db.String(50), unique=True, nullable=False)  # Token único

# Ruta para Crear Invitaciones
@app.route('/crear_invitacion', methods=['GET', 'POST'])
def crear_invitacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        token = secrets.token_urlsafe(16)  # Genera un token único
        nueva_invitacion = Invitacion(nombre=nombre, email=email, token=token)
        db.session.add(nueva_invitacion)
        db.session.commit()

        # Envía el correo con el enlace
        enviar_correo(email, nombre, token)

        return redirect(url_for('admin'))
    return render_template('crear_invitacion.html')

# Ruta para Ver el Formulario de Invitación (actualizada para usar el token)
@app.route('/invitacion/<string:token>')
def invitacion(token):
    invitacion = Invitacion.query.filter_by(token=token).first_or_404()
    return render_template('invitacion.html', invitacion=invitacion)

# Ruta para Confirmar Asistencia (actualizada para usar el token)
@app.route('/confirmar/<string:token>', methods=['GET'])
def confirmar_asistencia(token):
    # Buscar la invitación en la base de datos
    invitacion = Invitacion.query.filter_by(token=token).first_or_404()

    # Actualizar el estado a "aceptado"
    invitacion.estado = "aceptado"
    db.session.commit()

    # Redirigir a la página de "Gracias"
    return redirect(url_for('gracias', token=token))

# Ruta de Inicio
@app.route('/')
def index():
    return render_template('index.html')


# Ruta del Administrador
@app.route('/admin')
def admin():
    invitaciones = Invitacion.query.all()
    return render_template('admin.html', invitaciones=invitaciones)

@app.route('/gracias/<string:token>')
def gracias(token):
    # Buscar la invitación en la base de datos
    invitacion = Invitacion.query.filter_by(token=token).first_or_404()

    # Renderizar la página de "Gracias"
    return render_template('gracias.html', invitacion=invitacion)


@app.route('/cancelar/<string:token>', methods=['POST'])
def cancelar_asistencia(token):
    # Buscar la invitación en la base de datos
    invitacion = Invitacion.query.filter_by(token=token).first_or_404()

    # Actualizar el estado a "rechazado"
    invitacion.estado = "rechazado"
    db.session.commit()

    # Renderizar la página de cancelación
    return render_template('cancelado.html')


# Crear la Base de Datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)