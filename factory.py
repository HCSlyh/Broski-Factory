import os
import ast
import re
import sys
import time
import json
import subprocess
from groq import Groq

# =====================================================================
# CONFIGURAZIONE UTENTE: API KEY DI GROQ SALVATA
# =====================================================================
GROQ_API_KEY = "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"
# =====================================================================

MODELLO_LLM = "openai/gpt-oss-120b" 
client = Groq(api_key=GROQ_API_KEY)

MAX_LIVELLI = 3  
PAUSA_RATE_LIMIT = 60

# =====================================================================
# CONFIGURATION DUMP: SALVATAGGIO PARAMETRI SENZA NESTING DI STRINGHE
# =====================================================================
CONFIG_DATA = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "MODELLO_LLM": MODELLO_LLM,
    "MAX_LIVELLI": MAX_LIVELLI
}
try:
    with open("factory_config.json", "w", encoding="utf-8") as cf:
        json.dump(CONFIG_DATA, cf, indent=2)
    print("📝 [Auto-Setup] File 'factory_config.json' salvato con successo.")
except Exception as e:
    print(f"⚠️ Errore salvataggio configurazione: {e}")

# =====================================================================
# WRITER DEL MOTORE RICORSIVO (COMPLETAMENTE PULITO DA STR_REPLACE)
# =====================================================================
try:
    with open("motore_ricorsivo.py", "w", encoding="utf-8") as f:
        f.write("def _esegui_chiamata_astratta(*args, **kwargs):\n")
        f.write("    import json, os, subprocess, sys, time, re\n")
        f.write("    print('\\n⏳ [Free Plan Sync] Attesa di 60 secondi prima della chiamata ricorsiva...')\n")
        f.write("    time.sleep(60)\n")
        f.write("    if not os.path.exists('factory_config.json'): return ''\n")
        f.write("    with open('factory_config.json', 'r', encoding='utf-8') as cf: config = json.load(cf)\n")
        f.write("    os.environ['GROQ_API_KEY'] = config['GROQ_API_KEY']\n")
        f.write("    from groq import Groq\n")
        f.write("    client = Groq(api_key=config['GROQ_API_KEY'])\n")
        f.write("    prompt_fabbrica = 'Sei un ingegnere cloud. Genera un\\'applicazione web-server FastAPI in Python completa. Deve definire un\\'app = FastAPI() ed esporre un\\'endpoint POST \\'/api/v1/process\\'. Se il livello attuale ' + str(int(kwargs.get('livello', 2))) + ' e\\' inferiore a ' + str(config['MAX_LIVELLI']) + ', definisci le funzioni _crea_nodo_A() e _crea_nodo_B() richiamando la funzione vuota _esegui_chiamata_astratta(). Se il livello e\\' uguale a ' + str(config['MAX_LIVELLI']) + ', avvia il server uvicorn.run(app, host=\\'0.0.0.0\\', port=8000). Restituisci solo codice in blocco markdown python.'\n")
        f.write("    try:\n")
        f.write("        comp = client.chat.completions.create(model=config['MODELLO_LLM'], messages=[{'role': 'user', 'content': prompt_fabbrica}], temperature=0.01)\n")
        f.write("        res = comp.choices.message.content.strip()\n")
        f.write("        if '```python' in res:\n")
        f.write("            res = res.split('```python').split('```').strip()\n")
        f.write("        return res\n")
        f.write("    except Exception as e:\n")
        f.write("        print('Errore runtime:', e)\n")
        f.write("        return ''\n")
    print("📦 [Auto-Setup] File 'motore_ricorsivo.py' generato con architettura a dizionario statico.")
except Exception as e:
    print(f"⚠️ Impossibile generare il file motore: {e}")

# =====================================================================
# CLASSE DI TRASFORMAZIONE AST: SOSTITUZIONE CHIRURGICA LOGICA NODI
# =====================================================================
class IniettoreCodiceAST(ast.NodeTransformer):
    def __init__(self, codice_motore):
        self.codice_motore = codice_motore

    def visit_FunctionDef(self, node):
        if node.name == "_esegui_chiamata_astratta":
            print("   🧬 [AST Engine] Rilevato nodo segnaposto. Iniezione codice reale in corso...")
            albero_motore = ast.parse(self.codice_motore)
            return albero_motore.body
        return self.generic_visit(node)
# =====================================================================
# FUNZIONI CORE FACTORY
# =====================================================================

def valida_sintassi_python(codice):
    try:
        ast.parse(codice)
        return True
    except SyntaxError as e:
        print(f"   [Debug Sintassi] Fallito alla riga {e.lineno}: {e.msg}")
        return False

def pulisci_codice(codice_raw):
    match = re.search(r"```python\s*(.*?)\s*```", codice_raw, re.DOTALL | re.IGNORECASE)
    if match: return match.group(1).strip()
    match_generico = re.search(r"```\s*(.*?)\s*```", codice_raw, re.DOTALL)
    if match_generico: return match_generico.group(1).strip()
    return codice_raw.strip()

def genera_modulo_astratto(nome_modulo, descrizione_compito, livello_attuale, primo_avvio=False):
    if livello_attuale > MAX_LIVELLI:
        return None

    print(f"🏭 Factory: Generazione in corso per {nome_modulo} (Livello {livello_attuale}/{MAX_LIVELLI})...")
    
    if not primo_avvio:
        print(f"⏳ [Safety Buffer] Attesa di {PAUSA_RATE_LIMIT} secondi...")
        time.sleep(PAUSA_RATE_LIMIT)

    prompt_criptico = f"""Sei un ingegnere informatico senior specializzato in architetture cloud FastAPI B2B.
    Crea uno script Python completo ed eseguibile chiamato '{nome_modulo.lower()}'.
    
    COMPITO: {descrizione_compito}
    
    REQUISITI RIGIDI:
    1. Lo script deve importare 'fastapi', 'uvicorn' e 'os'.
    2. Deve includere una funzione `run()` principale eseguita nel blocco main che avvia un server uvicorn.
    3. Il server uvicorn deve caricare l'applicazione usando rigidamente il nome del modulo tutto in minuscolo, scritto esattamente così: "{nome_modulo.lower()}:app".
    4. Se la fase attuale ({livello_attuale}) è inferiore a {MAX_LIVELLI}, lo script deve definire la funzione segnaposto `_esegui_chiamata_astratta()` che restituisce la stringa "pass".
    5. Deve definire due funzioni chiamate `_crea_nodo_A()` e `_crea_nodo_B()` che scrivono su disco due file chiamati 'app_fase{livello_attuale + 1}_modulo1.py' e 'app_fase{livello_attuale + 1}_modulo2.py' ottenendo il loro contenuto da `_esegui_chiamata_astratta()`.
    6. Lo script deve usare 'subprocess.run' trasmettendo le variabili d'ambiente correnti per eseguire in sequenza i file creati.
    7. Se la fase attuale è uguale a {MAX_LIVELLI}, scrivi un report ed avvia uvicorn.
    
    Restituisci SOLO il codice dentro un blocco ```python. Non aggiungere spiegazioni."""

    try:
        completion = client.chat.completions.create(
            model=MODELLO_LLM, 
            messages=[{"role": "user", "content": prompt_criptico}],
            temperature=0.01,
            max_tokens=3000
        )
        
        # CORREZIONE APPLICATA: Inserito l'indice fisso [0] per estrarre la scelta corretta ed evitare il crash su 'list'
        codice_grezzo = completion.choices[0].message.content
        codice_pulito = pulisci_codice(codice_grezzo)
        
        if not codice_pulito:
            print("❌ Groq ha restituito una stringa vuota.")
            return None
            
        with open("motore_ricorsivo.py", "r", encoding="utf-8") as f:
            blocco_motore_reale = f.read()

        # =====================================================================
        # TRASFORMAZIONE STRUTTURALE AST COMPILATA (STABILITÀ TOTALE)
        # =====================================================================
        try:
            albero_sintattico = ast.parse(codice_pulito)
            trasformatore = IniettoreCodiceAST(blocco_motore_reale)
            albero_modificato = trasformatore.visit(albero_sintattico)
            ast.fix_missing_locations(albero_modificato)
            
            codice_iniettato = ast.unparse(albero_modificato)
        except Exception as err_ast:
            print(f"⚠️ Errore durante il parsing AST logico, attivazione fallback testuale: {err_ast}")
            codice_iniettato = codice_pulito.replace('return "pass"', blocco_motore_reale)

        # Iniezione stagna della chiave d'ambiente d'innesco padre
        if "import os" in codice_iniettato:
            codice_iniettato = codice_iniettato.replace("import os", f"import os\nos.environ['GROQ_API_KEY'] = '{GROQ_API_KEY}'")

        if valida_sintassi_python(codice_iniettato):
            print(f"✅ Modulo {nome_modulo} cloud-ready contrabbandato e validato strutturalmente.")
            return codice_iniettato
        return None
        
    except Exception as e:
        print(f"❌ Errore critico durante la generazione: {e}")
        return None

# =====================================================================
# INNESCO PIPELINE FASTAPI
# =====================================================================
try:
    print("====================================================")
    print(f"🚀 INIZIO PIPELINE CON TRASFORMAZIONE SINTATTICA AST V6.2")
    print("====================================================")
    
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    
    file_principale = "app_fase1_core.py"
    
    codice_core = genera_modulo_astratto(
        nome_modulo="app_fase1_core",
        descrizione_compito=f"Crea uno script che implementi un'app FastAPI e scriva sul disco due script chiamati 'app_fase2_modulo1.py' e 'app_fase2_modulo2.py'. Il contenuto di questi file deve essere ottenuto chiamando `_esegui_chiamata_astratta(livello=2)`. Una volta scritti, eseguili in sequenza ordinata trasmettendo os.environ.",
        livello_attuale=1,
        primo_avvio=True
    )
    
    if codice_core:
        with open(file_principale, "w", encoding="utf-8") as f:
            f.write(codice_core)
        print(f"💾 File di contrabbando cloud '{file_principale}' scritto sul disco.")
        
        print("\n▶️ [AUTOMAZIONE] Esecuzione in corso della pipeline FastAPI...")
        subprocess.run([sys.executable, file_principale], check=True)
        
        print(f" \n🎯 [COMPLETATO]: Ecosistema FastAPI generato con successo.")
    else:
        print("🛑 Impossibile procedere: modulo cloud core bloccato.")

except Exception as e:
    print(f"\n💥 Interruzione pipeline: {e}")
