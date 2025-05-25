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
  Tento projekt slúži na automatické sťahovanie, validáciu a porovnanie konfigurácií sieťových zariadení cez Telnet,  
  s exportom výsledkov do DOCX a ZIP formátu.
</p>

## 📝 Obsah

- [O projekte](#o-projekte)  
- [Začíname](#zaciname)  
- [Použitie](#pouzitie)  
- [Nasadenie](#nasadenie)  
- [Použité technológie](#pouzite-technologie)  
- [TODO](TODO.md)  
- [Príspevky](CONTRIBUTING.md)  
- [Autori](#autori)  
- [Poďakovanie](#podakovanie)  

## 🧐 O projekte <a name="o-projekte"></a>

**Automatické sťahovanie a vyhodnocovanie konfigurácie sieťových zariadení** je webová aplikácia, ktorá kombinuje:

- **Flask** (front-end)  
- **FastAPI** (validácia API)  
- Vlastné Python moduly pre Telnet komunikáciu a validáciu  

Aplikácia umožňuje:

1. Sťahovať konfigurácie zo zariadení cez Telnet  
2. Validovať a porovnávať konfigurácie riadok po riadku  
3. Generovať výsledky do DOCX dokumentov  
4. Baliť výsledky do ZIP archívov  
5. Spravovať zariadenia cez `.env` konfiguráciu  
6. Používať jednoduché webové rozhranie s Jinja2 a vlastným CSS  

## 🏁 Začíname <a name="zaciname"></a>

Nasledujúci postup vám umožní spustiť projekt lokálne.

### Požiadavky

- **Python 3.11+**  
- **Git**

### Inštalácia

```bash
# Klonovanie repozitára
git clone https://github.com/tomanAdrian/Projekt2.git
cd Projekt2

# Vytvorenie a aktivácia virtuálneho prostredia
python3 -m venv .venv
source .venv/bin/activate

# Inštalácia závislostí
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 🎈 Použitie <a name="pouzitie"></a>

Spustite aplikáciu a otvorte webové rozhranie, z ktorého môžete:

1. **Porovnávať zariadenia**  
2. **Sťahovať konfigurácie**  

#### Spustenie servera

```bash
python app.py
```

- Aplikácia beží na <http://localhost:5000>  

#### Rozhranie pre porovnávanie konfigurácií

1. Vyberte kartu **Porovnanie konfigurácií**  
2. Zadajte referenčnú konfiguráciu (správna):
   - **Vyberte možnosť:**  
     - Stiahnuť konfiguráciu zo zariadenia/zariadení `(<ip_adresa>:<port>)`  
     - Stiahnuť konfiguráciu zo zariadenia/zariadení `(<ip_adresa>:<port>;<meno>;<heslo>)`  
     - Nahrať konfigurácie zo súborov (poradie = poradie zariadení zľava)  
   - **Nahrať súbory:**  
     - [Pridať súbory]  
   - Zadajte **Poradie súborov** podľa poradia zariadení.

3. Zadajte konfiguráciu na porovnanie:
   - **Vyberte možnosť:**  
     - Stiahnuť konfiguráciu zo zariadenia/zariadení `(<ip_adresa>:<port>)`  
     - Stiahnuť konfiguráciu zo zariadenia/zariadení `(<ip_adresa>:<port>;<meno>;<heslo>)`  
     - Nahrať konfigurácie zo súborov (poradie = poradie zariadení zľava)  
   - **Nahrať súbory:**  
     - [Pridať súbory]  
   - Zadajte **Poradie súborov** podľa poradia zariadení.

4. Kliknite na **Porovnať** a výsledky sa zobrazia priamo v prehliadači.

#### Rozhranie pre sťahovanie konfigurácií

1. Vyberte kartu **Sťahovanie konfigurácií**  
2. Zadajte zoznam zariadení rovnako ako vyššie  
3. Kliknite na **Stiahnuť**  
4. Výsledné súbory si môžete stiahnuť v ZIP balíku alebo ako samostatné TXT.

## 🚀 Nasadenie <a name="nasadenie"></a>

Pre produkčné prostredie odporúčame:

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

## ⛏️ Použité technológie <a name="pouzite-technologie"></a>

- [Flask](https://palletsprojects.com/p/flask/)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [python-dotenv](https://github.com/theskumar/python-dotenv)  
- [paramiko](https://www.paramiko.org/)  
- [python-docx](https://python-docx.readthedocs.io/)  
- `zipfile` (Python stdlib)  
- [Jinja2](https://palletsprojects.com/p/jinja/)  

## ✍️ Autori <a name="autori"></a>

- **Adrian Toman** – [tomanAdrian](https://github.com/tomanAdrian)

## 🎉 Poďakovanie <a name="podakovanie"></a>

- Inšpirácia z pôvodného projektu “Automatické sťahovanie a vyhodnocovanie konfigurácie sieťových zariadení”  
- Vďaka open-source komunite za knižnice  
