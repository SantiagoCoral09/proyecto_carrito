from flask import Flask, render_template
from config import config


app = Flask(__name__)
app.config.from_object(config['default'])

# print(config)

# Configuracion de los BluePrints
from login_registro import login_registro
from productos import productos
from carrito import carrito
from administrador import administrador
from compras import compras

app.register_blueprint(login_registro)
app.register_blueprint(productos)
app.register_blueprint(carrito)
app.register_blueprint(administrador)
app.register_blueprint(compras)



@app.route('/')
def inicio():
    return render_template("index.html")

error_codes = [
    400, 401, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 422, 428, 429, 431, 451, 500, 501, 502, 503, 504, 505
]
for code in error_codes:
    @app.errorhandler(code)
    def client_error(error):
        return render_template('error.html', error=error), error.code


if __name__ == '__main__':
    app.run(port=5000)
