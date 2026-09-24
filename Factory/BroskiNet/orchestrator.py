import json
import os
import sys

def load_matrix():
    """Carica la matrice universale di BroskiNet"""
    matrix_path = os.path.join(os.path.dirname(__file__), 'matrix_rules.json')
    with open(matrix_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_available_agents(macro_category):
    """
    STEP 1 PIATTAFORMA: Il cliente inserisce la categoria (es. COMMERCE).
    Il sistema risponde alla piattaforma dicendo quali agenti mostrare nel menu delle scelte.
    """
    matrix = load_matrix()
    categories = matrix.get("macro_categories", {})
    
    if macro_category not in categories:
        return None
    
    return categories[macro_category]["available_engines"]

def process_selected_map(macro_category, employee_count, selected_engines):
    """
    STEP 2 PIATTAFORMA: Il cliente ha cliccato e scelto i suoi agenti.
    La matrice elabora le ore e i nodi dinamici in base alle scelte reali ricevute.
    """
    matrix = load_matrix()
    category_data = matrix["macro_categories"][macro_category]
    metrics = category_data["metrics"]
    
    # Calcolo ROI puro basato sulle variabili inviate dalla piattaforma
    factor = metrics["time_saved_factor_per_employee_weekly_hours"]
    hourly_cost = metrics["average_hourly_cost_eur"]
    
    weekly_hours_saved = int(employee_count) * factor
    monthly_money_saved = weekly_hours_saved * 4.33 * hourly_cost
    
    output_data = {
        "roi": {
            "hours_saved_weekly": round(weekly_hours_saved, 1),
            "money_saved_monthly": round(monthly_money_saved, 2)
        },
        "map_nodes": [
            {"node_id": engine, "status": "active"} for engine in selected_engines
        ]
    }
    return output_data

if __name__ == "__main__":
    # Questo blocco permette a Render o al file .bat di passare dati dinamici alla factory
    if len(sys.argv) > 1:
        # Se vengono passati argomenti via terminale, li elabora dinamici
        mode = sys.argv[1]
        if mode == "--get-options" and len(sys.argv) == 3:
            cat = sys.argv[2].upper()
            agents = get_available_agents(cat)
            print(json.dumps({"category": cat, "show_to_user_in_menu": agents}, indent=2))
    else:
        # Se lanciato senza dati, avvisa che la piattaforma è in attesa di input esterni
        print("\n[BroskiNet Core] Factory attiva e in ascolto. In attesa di input dalla piattaforma...")
        print("Usa il nuovo file .bat per testare l'inserimento dati dinamico (Parrucchiere vs Broker).")
