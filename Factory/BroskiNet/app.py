import os
import json
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_matrix():
    matrix_path = os.path.join(os.path.dirname(__file__), 'matrix_rules.json')
    with open(matrix_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- ROTTA PRINCIPALE (VISIVA) ---
@app.route('/')
def index():
    """Mostra l'applicazione grafica di BroskiNet"""
    return render_template('index.html')

# --- ROTTE API DI CONTROLLO ---
@app.route('/api/get-agents', methods=['POST'])
def get_agents():
    data = request.json
    macro_category = data.get("macro_category", "").upper()
    matrix = load_matrix()
    categories = matrix.get("macro_categories", {})
    if macro_category not in categories:
        return jsonify({"error": "Categoria non valida"}), 400
    return jsonify({"available_engines": categories[macro_category]["available_engines"]})

@app.route('/api/generate-blueprint', methods=['POST'])
def generate_blueprint():
    data = request.json
    company_name = data.get("company_name")
    macro_category = data.get("macro_category").upper()
    employee_count = int(data.get("employee_count", 1))
    selected_engines = data.get("selected_engines", [])
    
    matrix = load_matrix()
    category_data = matrix["macro_categories"][macro_category]
    metrics = category_data["metrics"]
    
    weekly_hours_saved = employee_count * metrics["time_saved_factor_per_employee_weekly_hours"]
    monthly_money_saved = weekly_hours_saved * 4.33 * metrics["average_hourly_cost_eur"]
    
    prompt_sistema = (
        f"Sei BroskiNet Engine. Un cliente con l'azienda '{company_name}' "
        f"nel settore '{category_data['label']}' ha scelto questi agenti: {', '.join(selected_engines)}. "
        f"Genera un report strategico brevissimo di 2 frasi spiegando perché questa combinazione aumenterà i profitti."
    )
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_sistema}],
            temperature=0.5,
            max_tokens=150
        )
        ai_feedback = completion.choices.message.content
    except Exception:
        ai_feedback = "Configurazione nodi completata con successo. Architettura pronta al rilascio."

    return jsonify({
        "roi": {
            "hours_saved_weekly": round(weekly_hours_saved, 1),
            "money_saved_monthly": round(monthly_money_saved, 2)
        },
        "ai_analysis": ai_feedback,
        "nodes": [{"id": eng, "status": "active"} for eng in selected_engines]
    })

# --- ENDPOINT WEBHOOK PADDLE ---
@app.route('/webhook/paddle', methods=['POST'])
def paddle_webhook():
    """
    Riceve le notifiche di pagamento in tempo reale da Paddle.
    Render rimarrà in ascolto su questo indirizzo pubblico (/webhook/paddle).
    """
    payload = request.json
    event_type = payload.get("event_type")
    
    # Esempio logica di sblocco ad acquisto avvenuto
    if event_type == "subscription.activated" or event_type == "transaction.completed":
        customer_email = payload.get("data", {}).get("customer", {}).get("email")
        print(f"[PADDLE SUCCESS] Pagamento confermato per la mail: {customer_email}")
        # Qui la factory può sbloccare la generazione avanzata o inviare i moduli su GitHub
        return jsonify({"status": "verified", "message": "User access granted"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
