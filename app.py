import flask
from flask import render_template, send_file
from main import generate_barcode_pdf_multiple_pages

app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

default_values = {
    'base_code': 'CC',
    'start_number': 0,
    'total_codes': 10,
    'rows': 6,
    'cols': 4,
    'margins_mm': (10, 10),
    'gap_mm': (5, 5)
}



@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    print(flask.request.json)
    base_code = flask.request.json['barcode'][0:2]
    start_number = int(flask.request.json['barcode'][2:])
    total_codes = int(flask.request.json['amount'])
    rows = int(flask.request.json['rows'])
    cols = int(flask.request.json['cols'])
    margins_mm = (float(flask.request.json['margin_x']), float(flask.request.json['margin_y']))
    gap_mm = (float(flask.request.json['gap_x']), float(flask.request.json['gap_y']))

    draw_lines = flask.request.json['draw_lines'] == True

    # Llamar a la función
    canvas_object = generate_barcode_pdf_multiple_pages(base_code, start_number, total_codes, rows, cols, margins_mm, gap_mm, draw_lines=draw_lines)

    # Guardar el PDF
    canvas_object.save()
    return {'status': 'ok'}, 200

@app.route('/get-pdf', methods=['GET'])
def get_pdf():
    return send_file('temp.pdf', as_attachment=True)

if __name__ == '__main__':
    debug = False
    # generar un pdf al iniciar el servidor
    canvas_object = generate_barcode_pdf_multiple_pages(**default_values)
    canvas_object.save()
    if not debug:
        context = ('secrets/fullchain.pem', 'secrets/privkey.pem')#certificate and key files host='manu365.dev'
        app.run(debug=False, ssl_context=context, port=4433 , host='manu365.dev')
    else:
        app.run(debug=True, port=12344 , host='0.0.0.0')