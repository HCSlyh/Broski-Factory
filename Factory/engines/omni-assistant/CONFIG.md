# ENGINE_ID: BN_OMNI_ASSISTANT_01
## Modulo: Assistente di Accoglienza e Triage Universale

### 📋 Definizione Funzionale
Questo modulo agisce come primo punto di contatto. Analizza la richiesta in ingresso di un cliente, ne estrae l'urgenza e formula una risposta o un instradamento corretto basandosi sull'identità dell'azienda.

### 🔌 Requisiti di Iniezione (BroskiData)
* Legge il profilo aziendale compilato nel file `brand_template.json`.

### 📤 Specifiche di Output
1. **Risposta**: Testo pronto da inviare al cliente finale secondo il tono di voce aziendale.
2. **Triage**: Assegnazione di una categoria interna (Urgente / Info / Commerciale) per il titolare dell'attività.
