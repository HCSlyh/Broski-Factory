import os
os.environ['GROQ_API_KEY'] = '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'
import sys
import subprocess
from fastapi import FastAPI
import uvicorn
FASE = 1
app = FastAPI()
if FASE < 3:

    def _esegui_chiamata_astratta(*args, **kwargs):
        import json, os, subprocess, sys, time, re
        print('\n⏳ [Free Plan Sync] Attesa di 60 secondi prima della chiamata ricorsiva...')
        time.sleep(60)
        if not os.path.exists('factory_config.json'):
            return ''
        with open('factory_config.json', 'r', encoding='utf-8') as cf:
            config = json.load(cf)
        os.environ['GROQ_API_KEY'] = config['GROQ_API_KEY']
        from groq import Groq
        client = Groq(api_key=config['GROQ_API_KEY'])
        prompt_fabbrica = "Sei un ingegnere cloud. Genera un'applicazione web-server FastAPI in Python completa. Deve definire un'app = FastAPI() ed esporre un'endpoint POST '/api/v1/process'. Se il livello attuale " + str(int(kwargs.get('livello', 2))) + " e' inferiore a " + str(config['MAX_LIVELLI']) + ", definisci le funzioni _crea_nodo_A() e _crea_nodo_B() richiamando la funzione vuota _esegui_chiamata_astratta(). Se il livello e' uguale a " + str(config['MAX_LIVELLI']) + ", avvia il server uvicorn.run(app, host='0.0.0.0', port=8000). Restituisci solo codice in blocco markdown python."
        try:
            comp = client.chat.completions.create(model=config['MODELLO_LLM'], messages=[{'role': 'user', 'content': prompt_fabbrica}], temperature=0.01)
            res = comp.choices.message.content.strip()
            if '```python' in res:
                res = res.split('```python').split('```').strip()
            return res
        except Exception as e:
            print('Errore runtime:', e)
            return ''

def _crea_nodo_A() -> None:
    contenuto = _esegui_chiamata_astratta(livello=2)
    with open('app_fase2_modulo1.py', 'w', encoding='utf-8') as f:
        f.write(contenuto)

def _crea_nodo_B() -> None:
    contenuto = _esegui_chiamata_astratta(livello=2)
    with open('app_fase2_modulo2.py', 'w', encoding='utf-8') as f:
        f.write(contenuto)

def _esegui_moduli() -> None:
    for modulo in ['app_fase2_modulo1.py', 'app_fase2_modulo2.py']:
        subprocess.run([sys.executable, modulo], env=os.environ, check=True)

def _scrivi_report() -> None:
    with open('report.txt', 'w', encoding='utf-8') as f:
        f.write(f'Fase {FASE} completata.\n')

def run() -> None:
    if FASE < 3:
        _crea_nodo_A()
        _crea_nodo_B()
        _esegui_moduli()
    elif FASE == 3:
        _scrivi_report()
    uvicorn.run('app_fase1_core:app', host='0.0.0.0', port=8000)
if __name__ == '__main__':
    run()