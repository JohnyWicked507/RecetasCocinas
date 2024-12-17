import os
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from celery import Celery
from time import sleep

# Configuración de Flask
app = Flask(__name__)

# Configuración de Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEFAULT_SENDER"] = "your_email@gmail.com"

mail = Mail(app)


# Configuración de Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    return celery


# Configura Celery para usar Redis
app.config.update(
    CELERY_BROKER_URL="redis://localhost:6379/0",  # Configura Redis como broker
    CELERY_RESULT_BACKEND="redis://localhost:6379/0",  # Usamos el mismo Redis para resultados
)

celery = make_celery(app)


# Ruta de ejemplo para el formulario de envío de correo
@app.route("/")
def index():
    return render_template("index.html")


# Tarea asíncrona para enviar un correo
@celery.task
def send_email_async(subject, recipient, body):
    sleep(5)  # Simulamos una tarea pesada (por ejemplo, un proceso largo)
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        return str(e)
    return f"Email sent to {recipient}"


# Ruta para enviar el correo electrónico
@app.route("/send_email", methods=["POST"])
def send_email():
    subject = request.form["subject"]
    recipient = request.form["recipient"]
    body = request.form["body"]

    # Llamada asíncrona a la tarea de envío de correo
    send_email_async.apply_async(args=[subject, recipient, body])

    return jsonify({"message": "Email is being sent asynchronously."})


if __name__ == "__main__":
    app.run(debug=True)
