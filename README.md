<p align="center">
  <a href="https://github.com/tomanAdrian/Projekt2" rel="noopener">
    <img width="200" height="200" src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo">
  </a>
</p>

<h3 align="center">Automatické sťahovanie a vyhodnocovanie konfigurácie sieťových zariadení</h3>

<div align="center">
  [![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/tomanAdrian/Projekt2)  
  [![GitHub Issues](https://img.shields.io/github/issues/tomanAdrian/Projekt2.svg)](https://github.com/tomanAdrian/Projekt2/issues)  
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/tomanAdrian/Projekt2.svg)](https://github.com/tomanAdrian/Projekt2/pulls)  
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
</div>

---

<p align="center">
  Tento projekt slúži na automatické sťahovanie konfigurácií sieťových zariadení cez Telnet, ich validáciu, porovnanie a export výsledkov do DOCX a ZIP formátu.
</p>

## 📝 Table of Contents

- [About](#about)  
- [Getting Started](#getting-started)  
- [Usage](#usage)  
- [Deployment](#deployment)  
- [Built Using](#built-using)  
- [TODO](TODO.md)  
- [Contributing](CONTRIBUTING.md)  
- [Authors](#authors)  
- [Acknowledgments](#acknowledgments)  

## 🧐 About <a name="about"></a>

Automatické sťahovanie a vyhodnocovanie konfigurácie sieťových zariadení je webová aplikácia kombinujúca **Flask** (front-end) a vlastné Python moduly (**FastAPI** pre validation), ktorá umožňuje:

- Automatizované sťahovanie konfigurácií sieťových zariadení cez Telnet  
- Validáciu výstupu príkazov pomocou vlastníckych validatorov  
- Porovnanie konfigurácií riadok po riadku a zvýraznenie rozdielov  
- Generovanie DOCX dokumentov a balenie výsledkov do ZIP archívov  
- Jednoduché webové rozhranie s Jinja2 šablónami a vlastným CSS  
- Správu referenčných a porovnávaných zariadení cez `.env` konfiguráciu  

## 🏁 Getting Started <a name="getting-started"></a>

Postup pre lokálne spustenie projektu:

### Prerequisites

- **Python 3.11+**  
- Git

### Installing

```bash
# Klonujte repozitár
git clone https://github.com/tomanAdrian/Projekt2.git
cd Projekt2

# Vytvorte a aktivujte virtuálne prostredie
python3 -m venv .venv
source .venv/bin/activate

# Aktualizujte pip a nainštalujte závislosti
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 🎈 Usage <a name="usage"></a>

1. Vytvorte súbor `.env` v koreňovom adresári s:
   ```dotenv
   TELNET_HOST=192.168.1.1
   TELNET_PORT=23
   ADMIN_USER=admin
   ADMIN_PASS=secret
   ```
2. Spustite Flask backend:
   ```bash
   python app.py
   ```
   Otvorte <http://localhost:5000>  
3. (Voliteľne) Spustite FastAPI časť:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🚀 Deployment <a name="deployment"></a>

Na produkčné nasadenie odporúčame použiť WSGI server (napr. Gunicorn) alebo kontajnerizáciu:

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

## ⛏️ Built Using <a name="built-using"></a>

- [Flask](https://palletsprojects.com/p/flask/)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [python-dotenv](https://github.com/theskumar/python-dotenv)  
- [paramiko](https://www.paramiko.org/)  
- [python-docx](https://python-docx.readthedocs.io/)  
- `zipfile` (stdlib)  
- [Jinja2](https://palletsprojects.com/p/jinja/)  

## ✍️ Authors <a name="authors"></a>

- **Adrian Toman** – [tomanAdrian](https://github.com/tomanAdrian)

## 🎉 Acknowledgments <a name="acknowledgments"></a>

- Inšpirácia a pôvodný koncept z pôvodného projektu  
- Všetky open-source knižnice, ktoré umožňujú fungovanie tejto aplikácie  
