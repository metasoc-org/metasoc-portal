# METASOC — Esquema de Datos para IA Local

Este documento explica la estructura de `metas.json` para que la IA local (Ollama/OpenClaw) pueda registrar, actualizar y consultar datos sin errores.

---

## Archivo: `site/data/metas.json`

### Campos de `meta` (metadatos globales)

```json
"meta": {
  "last_updated": "2025-03-20T00:00:00Z",  // ISO 8601, actualizar siempre
  "organization": "Metasoc",
  "total_victorias": 8,                     // contar metas con estado "victoria"
  "total_en_batalla": 5,                    // contar metas con estado "en_batalla"
  "total_pendientes": 3                     // contar metas con estado "pendiente"
}
```

---

### Campos de cada `meta`

| Campo | Tipo | Valores válidos | Requerido |
|-------|------|-----------------|-----------|
| `id` | string | "META-XXX" (número secuencial) | ✅ |
| `titulo` | string | Texto libre, máx 80 chars | ✅ |
| `descripcion` | string | Texto libre | ✅ |
| `categoria` | string | `empresarial`, `organizacional`, `filosofica`, `tecnologica`, `financiera`, `personal` | ✅ |
| `estado` | string | `victoria`, `en_batalla`, `pendiente`, `retirada` | ✅ |
| `prioridad` | string | `critica`, `alta`, `media`, `baja` | ✅ |
| `fecha_inicio` | string | "YYYY-MM-DD" | ✅ |
| `fecha_limite` | string | "YYYY-MM-DD" | ✅ |
| `fecha_victoria` | string\|null | "YYYY-MM-DD" o null si no completada | ✅ |
| `progreso` | number | 0–100 (porcentaje) | ✅ |
| `tacticas` | array | Lista de strings | ✅ |
| `obstaculos` | array | Lista de strings | ✅ |
| `cita_motivacion` | string | Cita + " — Autor" | ❌ |
| `responsable` | string | Nombre del responsable | ✅ |
| `legion` | string | Área/equipo responsable | ✅ |

### Estados válidos y su significado

- `victoria` → Meta completada exitosamente (progreso = 100)
- `en_batalla` → Meta en progreso activo (progreso 1–99)
- `pendiente` → Meta planificada pero no iniciada (progreso = 0)
- `retirada` → Meta cancelada o abandonada

---

### Campos de cada `reporte`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | string | "REP-XXX" secuencial |
| `fecha` | string | "YYYY-MM-DD" |
| `titulo` | string | Nombre del reporte |
| `victorias_nuevas` | number | Metas completadas en este período |
| `batallas_activas` | number | Metas activas al momento |
| `resumen` | string | Texto narrativo del reporte |
| `metas_ids` | array | Lista de IDs de metas incluidas |
| `indice_moral` | number | 0–100, índice de motivación del equipo |

---

## Instrucciones para la IA local (Ollama/OpenClaw)

### Para AGREGAR una nueva meta:

1. Leer el archivo `site/data/metas.json`
2. Obtener el último ID del array `metas` y sumar 1
3. Crear el objeto con todos los campos requeridos
4. Agregar al final del array `metas`
5. Actualizar `meta.last_updated` con la fecha y hora actual en ISO 8601
6. Recalcular `total_victorias`, `total_en_batalla`, `total_pendientes`
7. Guardar el archivo

### Para ACTUALIZAR el estado de una meta:

1. Buscar la meta por `id`
2. Cambiar `estado` al nuevo valor
3. Si el estado es `victoria`: poner `progreso = 100` y `fecha_victoria = hoy`
4. Actualizar `meta.last_updated`
5. Recalcular totales en `meta`
6. Guardar el archivo

### Para CREAR un nuevo reporte semanal:

1. Leer metas activas (`en_batalla`)
2. Contar victorias de la semana (metas que cambiaron a `victoria`)
3. Crear objeto en array `reportes` con datos calculados
4. Actualizar `meta.last_updated`
5. Guardar el archivo

### Prompt de ejemplo para Ollama:

```
Eres el asistente de datos de Metasoc. Lee el archivo metas.json y agrega la siguiente nueva meta:
- Titulo: [TITULO]
- Categoría: [CATEGORIA]
- Responsable: [NOMBRE]
- Prioridad: [PRIORIDAD]
- Fecha límite: [FECHA]
- Descripción: [DESCRIPCION]

Responde SOLO con el JSON completo y actualizado del archivo, sin explicaciones.
```

---

## Archivo: `site/data/costs.json`

Ver estructura en el archivo. Los campos principales son:
- `monthly_costs[].month` → "YYYY-MM"
- `monthly_costs[].items[].category` → "infraestructura", "herramientas", "operaciones"
- `monthly_costs[].items[].amount` → número decimal en USD

---

## Deploy automático

Después de modificar cualquier JSON, ejecutar:
```bash
bash ~/scripts-metasoc/auto_deploy.sh
```

El script hace commit y push a GitHub, Cloudflare Pages despliega en ~1 minuto.
