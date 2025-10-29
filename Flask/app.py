"""
Examen Unidad III 
Autor: [Tu Nombre]
Fecha: [Fecha Actual]

Descripción:
Objetivo del examen
Desarrollar una API básica con Flask que permita:

Crear un diccionario de dispositivos de red.
Agregar nuevos dispositivos.
Modificar dispositivos existentes.
Mostrar un listado de todos los dispositivos en formato HTML, 
donde cada dispositivo se muestre en un <div> con nombre, 
descripción y características

Requisitos técnicos

Usar Flask.
Usar un diccionario como estructura principal de almacenamiento.
Implementar al menos tres rutas:

GET /dispositivos_html: muestra todos los dispositivos en HTML.
POST /dispositivos: agrega un nuevo dispositivo.
PUT /dispositivos/<id>: modifica un dispositivo existente.

Ejemplo del Diccionario de dispositivos: 
{
  "id": "router01",
  "nombre": "Router Principal",
  "descripcion": "Router de borde para salida a Internet",
  "ip": "192.168.1.1",
  "mac": "00:1A:2B:3C:4D:5E",
  "ubicacion": "Sala de servidores",
  "tipo": "Router",
  "otros": ""
}

Recuerda tener al menos 3 commits en tu repositorio. 

Para puntos extra
Puedes ocupar css para añadir puntos a tu examen, perzonalizalo con estilos como el siguiente:
<style>
    .dispositivo {
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
    }
</style>

Puntos extra para añador formula en el cmapo de otros
la formula es la siguente: 

último octeto de la IP * 3 + longitud del nombre del dispositivo + ":" + nombre (Cambiando los espacios por _)

"""


from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

dispositivos = {
    "router01": {
        "id": "router01",
        "nombre": "Router Principal",
        "descripcion": "Router de borde para salida a Internet",
        "ip": "192.168.1.1",
        "mac": "00:1A:2B:3C:4D:5E",
        "ubicacion": "Sala de servidores",
        "tipo": "Router",
    },
    "Switch01": {
          "id": "SW0183",
        "nombre": "Switch troncal",
        "descripcion": "Switch que divide la red principal",
        "ip": "192.168.129.2",
        "mac": "03:0A:7B:9A:5C:3D",
        "ubicacion": "Sala de servidores",
        "tipo": "Switch Cisco",
    }
}


@app.route('/')
def inicio():
    return "API de Dispositivos"


@app.route('/dispositivos_html', methods=['GET'])
def mostrar_html():
    html = """
    <html>
    <head>
        <style>
            .dispositivo {
                border: 5px solid #ccc;
                padding: 15px;
                margin: 15px;
            }
        </style>
    </head>
    <body>
        <h1 style="color:Red">Dispositivos de red</h1>
        {% for d in dispositivos.values() %}
            <div class="dispositivo">
                <b>{{ d.nombre }}</b><br>
                {{ d.descripcion }}<br>
                IP: {{ d.ip }}<br>
                MAC: {{ d.mac }}<br>
                Ubicación: {{ d.ubicacion }}<br>
                Tipo: {{ d.tipo }}<br>
                Otros: {{ d.otros }}
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, dispositivos=dispositivos)


@app.route('/dispositivos', methods=['POST'])
def agregar():
    data = request.get_json()
    if data["otros"] == "":
        data["otros"] = formula(data["ip"], data["nombre"])
    dispositivos[data["id"]] = data
    return jsonify({"mensaje": "Dispositivo agregado"})

@app.route('/dispositivos/<id_>', methods=['PUT'])
def modificar(id_):
    data = request.get_json()
    dispositivos[id_].update(data)
    if dispositivos[id_]["otros"] == "":
        d = dispositivos[id_]
        d["otros"] = formula(d["ip"], d["nombre"])
    return jsonify({"mensaje": "Dispositivo modificado"})

if __name__ == '__main__':
    app.run(debug=True)
