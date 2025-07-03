from flask import Flask, render_template_string, abort

app = Flask(__name__)

protocolos = ["protocolo1", "protocolo2", "protocolo3", "protocolo4", "protocolo5"]

@app.route('/<protocolo>')
def exibir_protocolo(protocolo):
    if protocolo not in protocolos:
        abort(404)
    template = """
    <!DOCTYPE html>
    <html>
      <head><title>{{ protocolo }}</title></head>
      <body>
        <h1>Você acessou: {{ protocolo }}</h1>
      </body>
    </html>
    """
    return render_template_string(template, protocolo=protocolo)


app.run(use_reloader=False)