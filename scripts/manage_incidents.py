#!/usr/bin/env python3
"""
MetaSOC — Gestor de Incidentes CLI
Agrega, lista y actualiza incidentes en incidents.json
"""

import json
import sys
import os
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'site', 'data', 'incidents.json')

INDUSTRIES  = ['educacion', 'gobierno', 'pyme']
SEVERITIES  = ['baja', 'media', 'alta', 'critica']
TYPES       = ['phishing', 'ip_maliciosa', 'ransomware', 'ddos', 'malware', 'credential_stuffing', 'otro']

COUNTRIES   = {
    'MX': ('México',       23.6345, -102.5528),
    'CO': ('Colombia',      4.5709,  -74.2973),
    'AR': ('Argentina',   -38.4161,  -63.6167),
    'PE': ('Perú',         -9.1900,  -75.0152),
    'CL': ('Chile',       -35.6751,  -71.5430),
    'GT': ('Guatemala',    15.7835,  -90.2308),
    'BR': ('Brasil',      -14.2350,  -51.9253),
    'EC': ('Ecuador',      -1.8312,  -78.1834),
    'VE': ('Venezuela',     6.4238,  -66.5897),
    'US': ('Estados Unidos',37.0902, -95.7129),
    'ES': ('España',       40.4637,   -3.7492),
    'BO': ('Bolivia',     -16.2902,  -63.5887),
    'PY': ('Paraguay',    -23.4425,  -58.4438),
    'UY': ('Uruguay',     -32.5228,  -55.7658),
    'CR': ('Costa Rica',    9.7489,  -83.7534),
    'PA': ('Panamá',        8.5380,  -80.7821),
    'HN': ('Honduras',     15.2000,  -86.2419),
    'SV': ('El Salvador',  13.7942,  -88.8965),
    'NI': ('Nicaragua',    12.8654,  -85.2072),
    'DO': ('Rep. Dominicana', 18.7357, -70.1627),
    'CU': ('Cuba',         21.5218,  -77.7812),
}

# ─────────────────────────────────────────────────────────────

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    data['meta']['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Datos guardados en {DATA_FILE}")

def next_id(data):
    ids = [inc['id'] for inc in data['incidents']]
    nums = [int(i.split('-')[1]) for i in ids if '-' in i]
    return f"INC-{(max(nums) + 1 if nums else 0):03d}"

def ask(prompt, options=None, default=None):
    if options:
        print(f"\n{prompt}")
        for i, o in enumerate(options, 1):
            print(f"  [{i}] {o}")
        while True:
            val = input(f"Selecciona (1-{len(options)}): ").strip()
            if val.isdigit() and 1 <= int(val) <= len(options):
                return options[int(val) - 1]
            print("  ⚠ Opción inválida.")
    else:
        val = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
        return val if val else default

# ─────────────────────────────────────────────────────────────
# COMANDOS
# ─────────────────────────────────────────────────────────────

def cmd_add():
    """Agregar un nuevo incidente"""
    print("\n" + "═" * 50)
    print("  MetaSOC — AGREGAR INCIDENTE")
    print("═" * 50)

    data = load_data()

    # País
    print("\nPaíses disponibles:")
    country_keys = list(COUNTRIES.keys())
    for i, k in enumerate(country_keys, 1):
        print(f"  [{i:2}] {k} — {COUNTRIES[k][0]}")
    while True:
        val = input("\nSelecciona país (número o código): ").strip().upper()
        if val in COUNTRIES:
            country_code = val
            break
        if val.isdigit() and 1 <= int(val) <= len(country_keys):
            country_code = country_keys[int(val) - 1]
            break
        print("  ⚠ País no encontrado.")

    country_name, lat, lng = COUNTRIES[country_code]

    inc_type    = ask("Tipo de incidente", TYPES)
    industry    = ask("Sector afectado",   INDUSTRIES)
    severity    = ask("Severidad",         SEVERITIES)
    description = ask("Descripción breve")
    date_input  = ask("Fecha (YYYY-MM-DD)", default=datetime.now().strftime('%Y-%m-%d'))
    resolved    = ask("¿Resuelto?", ['no', 'si']) == 'si'

    inc = {
        "id":           next_id(data),
        "date":         date_input,
        "country":      country_code,
        "country_name": country_name,
        "lat":          lat,
        "lng":          lng,
        "type":         inc_type,
        "industry":     industry,
        "severity":     severity,
        "description":  description,
        "resolved":     resolved,
    }

    data['incidents'].append(inc)
    data['meta']['total_organizations_helped'] = len(data.get('organizations_helped', [])) + 1

    print(f"\n📋 Nuevo incidente:")
    for k, v in inc.items():
        print(f"   {k}: {v}")

    confirm = input("\n¿Confirmar? (s/N): ").strip().lower()
    if confirm == 's':
        save_data(data)
        print(f"\n✅ Incidente {inc['id']} agregado correctamente.")
    else:
        print("❌ Operación cancelada.")

def cmd_list():
    """Listar todos los incidentes"""
    data = load_data()
    incs = data['incidents']
    print(f"\n{'═' * 70}")
    print(f"  MetaSOC — {len(incs)} INCIDENTES REGISTRADOS")
    print(f"{'═' * 70}")
    print(f"{'ID':<10} {'FECHA':<12} {'PAÍS':<12} {'TIPO':<20} {'SECTOR':<12} {'SEV':<8} {'EST'}")
    print("─" * 70)
    for inc in sorted(incs, key=lambda x: x['date'], reverse=True):
        status = "✓" if inc['resolved'] else "●"
        print(f"{inc['id']:<10} {inc['date']:<12} {inc['country']:<12} {inc['type']:<20} {inc['industry']:<12} {inc['severity']:<8} {status}")
    print()

def cmd_stats():
    """Mostrar estadísticas"""
    data = load_data()
    incs = data['incidents']

    by_type     = {}
    by_industry = {}
    by_country  = {}

    for inc in incs:
        by_type[inc['type']]         = by_type.get(inc['type'], 0) + 1
        by_industry[inc['industry']] = by_industry.get(inc['industry'], 0) + 1
        by_country[inc['country']]   = by_country.get(inc['country'], 0) + 1

    print(f"\n{'═' * 40}")
    print(f"  MetaSOC — ESTADÍSTICAS")
    print(f"{'═' * 40}")
    print(f"  Total incidentes:    {len(incs)}")
    print(f"  Resueltos:           {sum(1 for i in incs if i['resolved'])}")
    print(f"  Activos:             {sum(1 for i in incs if not i['resolved'])}")
    print(f"  Países cubiertos:    {len(by_country)}")
    print(f"\n  Por sector:")
    for k, v in sorted(by_industry.items(), key=lambda x: -x[1]):
        print(f"    {k:<15} {v} incidentes")
    print(f"\n  Por tipo:")
    for k, v in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"    {k:<22} {v}")
    print()

def cmd_resolve(inc_id):
    """Marcar un incidente como resuelto"""
    data = load_data()
    for inc in data['incidents']:
        if inc['id'].upper() == inc_id.upper():
            inc['resolved'] = True
            save_data(data)
            print(f"✅ Incidente {inc_id} marcado como resuelto.")
            return
    print(f"❌ Incidente {inc_id} no encontrado.")

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def print_help():
    print("""
MetaSOC — Gestor de Incidentes CLI

Uso:
  python3 manage_incidents.py add              Agregar nuevo incidente
  python3 manage_incidents.py list             Listar todos los incidentes
  python3 manage_incidents.py stats            Estadísticas del sistema
  python3 manage_incidents.py resolve INC-XXX  Marcar incidente como resuelto
  python3 manage_incidents.py help             Mostrar esta ayuda
""")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    if cmd == 'add':
        cmd_add()
    elif cmd == 'list':
        cmd_list()
    elif cmd == 'stats':
        cmd_stats()
    elif cmd == 'resolve':
        if len(sys.argv) < 3:
            print("Uso: python3 manage_incidents.py resolve INC-XXX")
        else:
            cmd_resolve(sys.argv[2])
    else:
        print_help()
