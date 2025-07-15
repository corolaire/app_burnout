import smtplib
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

preguntas = [
    {"id": 1, "texto": "¿Cuántas horas por día trabajás?", "opciones": ["Menos de 6", "Entre 6 y 9", "Más de 9"]},
    {"id": 2, "texto": "¿Te cuesta dormir o desconectarte del trabajo?", "opciones": ["Nunca", "A veces", "Siempre"]},
    {"id": 3, "texto": "¿Sentís que lo que hacés tiene sentido?", "opciones": ["Sí, totalmente", "No siempre", "Casi nunca"]},
    {"id": 4, "texto": "¿Te sentís valorada por tu trabajo o esfuerzo?", "opciones": ["Sí", "No mucho", "Para nada"]},
    {"id": 5, "texto": "¿Tenés tiempo libre real cada día?", "opciones": ["Sí", "A veces", "No"]},
    {"id": 6, "texto": "¿Te cuesta concentrarte últimamente?", "opciones": ["No", "Un poco", "Sí, mucho"]},
]

def evaluar_burnout(puntaje_total):
    if puntaje_total <= 12:
        return "🔵 Riesgo bajo", "Vas bien. Mantené tus espacios de descanso y equilibrio."
    elif 13 <= puntaje_total <= 18:
        return "🟠 Riesgo medio", "Prestá atención. Quizás estás entrando en un ritmo que agota."
    else:
        return "🔴 Riesgo alto", "Alerta. Necesitás frenar y reconectar con vos."

def enviar_mail_simulado(destinatario, cuerpo):
    print(f"📧 Simulando envío de correo a {destinatario}")
    print("------")
    print(cuerpo)
    print("------")

@app.route('/')
def index():
    return render_template('index_moderno.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(preguntas)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    respuestas = data.get('respuestas', {})
    email = data.get('email')
    puntaje = 0
    cuerpo = "Cuestionario de Burnout completado:\n\n"

    for p in preguntas:
        respuesta_idx = respuestas.get(str(p["id"]))
        if respuesta_idx:
            idx = int(respuesta_idx) - 1
            texto_opcion = p["opciones"][idx]
            cuerpo += f"- {p['texto']} → {texto_opcion}\n"
            puntaje += int(respuesta_idx)

    nivel, consejo = evaluar_burnout(puntaje)
    cuerpo += f"\nResultado: {nivel}\nConsejo: {consejo}"

    # Simular envío (acá podrías usar smtplib real)
    if email:
        enviar_mail_simulado("test@correo.com", cuerpo)

    return jsonify({"nivel": nivel, "consejo": consejo})

if __name__ == '__main__':
    app.run(debug=True)

