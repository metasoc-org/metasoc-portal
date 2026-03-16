# MetaSOC — Portal de Operaciones de Seguridad

Portal estático de inteligencia de amenazas para LATAM. Enfocado en educación, gobierno y PyMEs.

---

## 📁 Estructura del Proyecto

```
metasoc-portal/
├── site/
│   ├── index.html               ← Dashboard principal (lo que ve el mundo)
│   └── data/
│       └── incidents.json       ← Fuente de verdad de todos los incidentes
├── scripts/
│   ├── auto_deploy.sh           ← Script de deploy automático (cada hora)
│   └── manage_incidents.py      ← CLI para gestionar incidentes
└── README.md
```

---

## 🚀 Configuración Inicial (paso a paso)

### 1. Instalar Git (si no lo tienes)
```bash
# Linux/WSL
sudo apt-get install git -y

# macOS
brew install git
```

### 2. Configurar Git con tu identidad
```bash
git config --global user.name  "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 3. Crear el repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `metasoc-portal`
3. Visibilidad: **Público** (necesario para Cloudflare Pages gratis)
4. NO inicialices con README
5. Haz clic en **Create repository**

### 4. Inicializar el repo local y conectar con GitHub
```bash
cd /ruta/a/metasoc-portal

git init
git add -A
git commit -m "feat: MetaSOC portal inicial"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/metasoc-portal.git
git push -u origin main
```

### 5. Conectar Cloudflare Pages
1. Ve a https://dash.cloudflare.com → **Pages** → **Create a project**
2. Conecta con GitHub y selecciona el repo `metasoc-portal`
3. Configura el build:
   - **Build command:** *(dejar vacío)*
   - **Build output directory:** `site`
   - **Root directory:** *(dejar vacío)*
4. Haz clic en **Save and Deploy**
5. ¡Tu portal estará en `https://metasoc-portal.pages.dev`!

---

## ⚙️ Configurar Deploy Automático (cada hora)

### Dar permisos al script
```bash
chmod +x /ruta/a/metasoc-portal/scripts/auto_deploy.sh
```

### Configurar autenticación SSH con GitHub (recomendado)
```bash
# Generar llave SSH
ssh-keygen -t ed25519 -C "metasoc-deploy"

# Mostrar la llave pública (copiar todo el contenido)
cat ~/.ssh/id_ed25519.pub

# Ir a GitHub → Settings → SSH Keys → New SSH Key → pegar la llave
# Luego cambiar el remote a SSH:
cd /ruta/a/metasoc-portal
git remote set-url origin git@github.com:TU_USUARIO/metasoc-portal.git
```

### Configurar cron (Linux/macOS)
```bash
# Abrir el editor de cron
crontab -e

# Agregar esta línea (reemplaza la ruta):
0 * * * * /ruta/a/metasoc-portal/scripts/auto_deploy.sh >> /tmp/metasoc_cron.log 2>&1
```

### Configurar Tarea Programada (Windows)
Si usas Windows sin WSL:
```powershell
# En PowerShell como administrador:
$action  = New-ScheduledTaskAction -Execute 'bash' -Argument '-c "/mnt/c/ruta/metasoc-portal/scripts/auto_deploy.sh"'
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -Once -At (Get-Date)
Register-ScheduledTask -TaskName "MetaSOC-Deploy" -Action $action -Trigger $trigger -RunLevel Highest
```

---

## 📝 Gestionar Incidentes

```bash
# Agregar nuevo incidente (menú interactivo)
python3 scripts/manage_incidents.py add

# Ver todos los incidentes
python3 scripts/manage_incidents.py list

# Ver estadísticas
python3 scripts/manage_incidents.py stats

# Marcar como resuelto
python3 scripts/manage_incidents.py resolve INC-003
```

### Editar directamente el JSON
También puedes editar `site/data/incidents.json` con cualquier editor de texto.
El cron detectará los cambios y hará deploy en la próxima hora.

#### Campos de cada incidente:
```json
{
  "id":           "INC-013",
  "date":         "2025-03-15",
  "country":      "MX",
  "country_name": "México",
  "lat":          23.6345,
  "lng":          -102.5528,
  "type":         "phishing",
  "industry":     "educacion",
  "severity":     "alta",
  "description":  "Descripción breve del incidente",
  "resolved":     false
}
```

**Tipos válidos:** `phishing` | `ip_maliciosa` | `ransomware` | `ddos` | `malware` | `credential_stuffing`  
**Industrias:** `educacion` | `gobierno` | `pyme`  
**Severidades:** `baja` | `media` | `alta` | `critica`  

---

## 🔍 Verificar el Deploy

```bash
# Ver el log del último deploy
cat scripts/deploy.log

# Forzar deploy manual inmediato
bash scripts/auto_deploy.sh
```

---

## 🌐 Flujo Completo

```
Tu Notebook
│
├── Editas incidents.json (o usas el CLI)
│
└── Cron (cada hora)
     │
     └── auto_deploy.sh
          ├── Actualiza timestamp en JSON
          ├── git add -A
          ├── git commit
          └── git push → GitHub → Cloudflare Pages → 🌐 Sitio actualizado
```

---

## 📞 Soporte

Portal desarrollado para MetaSOC — Seguridad accesible para educación, gobierno y PyMEs de LATAM.
