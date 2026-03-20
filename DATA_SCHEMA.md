# METASOC SOC — Esquema de Datos para IA Local

Guía para que Ollama/OpenClaw registre incidentes correctamente.

---

## Archivo: `site/data/incidents.json`

### Campos de cada incidente

| Campo | Tipo | Valores válidos | Requerido |
|-------|------|-----------------|-----------|
| `id` | string | "INC-XXX" (secuencial, 3 dígitos) | ✅ |
| `date` | string | "YYYY-MM-DD" | ✅ |
| `country` | string | ISO 3166-1 alpha-2 (CO, MX, AR, BR, CL, PE...) | ✅ |
| `country_name` | string | Nombre completo del país | ✅ |
| `lat` | number | Latitud decimal del país/ciudad | ✅ |
| `lng` | number | Longitud decimal del país/ciudad | ✅ |
| `industry` | string | Ver tabla de industrias abajo | ✅ |
| `taxonomy` | string | Ver taxonomía ENISA abajo | ✅ |
| `severity` | string | `critica` `alta` `media` `baja` | ✅ |
| `description` | string | Descripción breve, máx 150 chars | ✅ |
| `resolved` | boolean | `true` o `false` | ✅ |

---

### Taxonomía ENISA (campo `taxonomy`)

| Valor | Descripción |
|-------|-------------|
| `ransomware` | Cifrado malicioso con extorsión |
| `malware` | Software malicioso genérico (troyanos, wipers, spyware) |
| `phishing` | Engaño por correo/web para robar credenciales |
| `ddos` | Denegación de servicio distribuida |
| `data_breach` | Exposición/robo de datos |
| `web_attack` | Ataques a aplicaciones web (SQLi, XSS, defacement) |
| `insider_threat` | Amenaza interna (empleado o contratista) |
| `supply_chain` | Compromiso a través de proveedores o software de terceros |
| `vulnerabilidad` | Explotación de CVE conocido o zero-day |
| `desinformacion` | Campañas de desinformación o manipulación de información |

---

### Industrias (campo `industry`)

`gobierno` | `educacion` | `salud` | `finanzas` | `energia` |
`transporte` | `telecomunicaciones` | `manufactura` | `retail` | `otros`

---

### Coordenadas de referencia (capitales LATAM)

| País | `country` | `lat` | `lng` |
|------|-----------|-------|-------|
| Colombia | CO | 4.71 | -74.07 |
| México | MX | 19.43 | -99.13 |
| Brasil | BR | -15.78 | -47.93 |
| Argentina | AR | -34.60 | -58.38 |
| Chile | CL | -33.45 | -70.67 |
| Perú | PE | -12.05 | -77.04 |
| Ecuador | EC | -0.18 | -78.47 |
| Bolivia | BO | -16.50 | -68.15 |
| Paraguay | PY | -25.28 | -57.64 |
| Uruguay | UY | -34.90 | -56.19 |
| Venezuela | VE | 10.48 | -66.88 |
| Costa Rica | CR | 9.93 | -84.08 |
| Panamá | PA | 8.99 | -79.52 |
| Guatemala | GT | 14.64 | -90.51 |

---

## Cómo agregar un incidente (instrucciones para IA local)

### Prompt para Ollama:

```
Eres el asistente de datos de Metasoc SOC. Lee el archivo incidents.json
y agrega el siguiente nuevo incidente:

- País: [PAÍS]
- Industria: [INDUSTRIA]
- Taxonomía ENISA: [TIPO]
- Severidad: [critica|alta|media|baja]
- Descripción: [DESCRIPCION]
- Fecha: [YYYY-MM-DD]
- ¿Resuelto?: [true|false]

Usa las coordenadas de la tabla de referencia.
El ID debe ser el siguiente número secuencial (INC-XXX).

Responde SOLO con el JSON completo y actualizado del archivo incidents.json,
sin explicaciones, sin bloques de código, solo el JSON puro.
```

### Pasos después de recibir el JSON:

```bash
# 1. Sobrescribir el archivo
nano ~/metasoc-portal/site/data/incidents.json
# (pegar el JSON generado por Ollama)

# 2. Desplegar
bash ~/scripts-metasoc/auto_deploy.sh
```

---

## Archivo: `site/data/costs.json`

Agregar nuevos meses al array `monthly_costs`:

```json
{
  "month": "2025-05",
  "label": "May 2025",
  "items": [
    { "category": "infraestructura", "name": "Cloudflare Pages", "amount": 0, "notes": "Plan gratuito" },
    { "category": "operaciones", "name": "Electricidad", "amount": 4.50, "notes": "Estimado" }
  ]
}
```

Categorías válidas: `infraestructura` | `herramientas` | `operaciones`
