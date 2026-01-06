# 📚 PolyGen - Index et Navigation

## 🎯 Par où commencer?

### 👤 Je suis un utilisateur
1. **Lire** → `README.md` (2 min)
2. **Installer** → `pip install -r requirements.txt`
3. **Essayer CLI** → `python3 main.py input.jpg -o output.png`
4. **Essayer GUI** → `./run_gui.sh`
5. **Apprendre** → `GUI_GUIDE.md` ou `USAGE_EXAMPLES.md`

### 👨‍💻 Je suis un développeur
1. **Comprendre le projet** → `DEVELOPMENT_SUMMARY.md`
2. **Explorer le code** → `src/low_poly.py` (moteur principal)
3. **Comprendre l'algo** → `README.md` (section Algorithme)
4. **Voir les features** → `src/svg_export.py` (export vectoriel)
5. **Modifier** → Personnalisez `src/low_poly.py`

### 🎨 Je veux des idées créatives
1. **Voir les exemples** → `USAGE_EXAMPLES.md`
2. **Tester les presets** → `GUI GUIDE.md` → Section "Presets"
3. **Lire les cas d'usage** → `USAGE_EXAMPLES.md` → "Cas d'usage"
4. **Explorer les paramètres** → `README.md` → "Paramètres en détail"

---

## 📖 Documentation complète

### 🚀 Pour commencer
| Fichier | Description | Durée |
|---------|-------------|-------|
| **README.md** | Vue d'ensemble complète | 5 min |
| **GUI_GUIDE.md** | Guide interface graphique | 10 min |
| **USAGE_EXAMPLES.md** | Exemples pratiques | 15 min |
| **BATCH_PROCESSING.md** | Traitement par lots | 10 min |
| **PRESETS_GUIDE.md** | Gestion des presets | 10 min |

### 🔧 Pour développeurs
| Fichier | Description |
|---------|-------------|
| **DEVELOPMENT_SUMMARY.md** | Architecture et implémentation |
| **src/low_poly.py** | Code du moteur principal (300 lines) |
| **src/svg_export.py** | Export vectoriel (150 lines) |
| **main.py** | Interface CLI (130 lines) |
| **gui.py** | Interface GUI (350 lines) |

---

## 🗂️ Structure des fichiers

```
PolyGen/
│
├── 📄 README.md                  ← Lisez ça en premier!
├── 📄 GUI_GUIDE.md               ← Guide GUI
├── 📄 USAGE_EXAMPLES.md          ← Exemples d'utilisation
├── 📄 BATCH_PROCESSING.md        ← Guide traitement par lots
├── 📄 PRESETS_GUIDE.md           ← Guide gestion des presets
├── 📄 DEVELOPMENT_SUMMARY.md     ← Architecture du projet
│
├── 🐍 main.py                    ← Interface CLI
├── 🐍 gui.py                     ← Interface GUI Tkinter
├── 🐍 test_configurations.py     ← Test des presets
├── 🐍 create_test_image.py       ← Crée image de test
│
├── 📁 src/
│   ├── __init__.py
│   ├── low_poly.py              ← Moteur principal ⭐
│   ├── svg_export.py            ← Export SVG
│   └── batch_processor.py        ← Traitement par lots
│
├── 📁 tests/
│   ├── __init__.py
│   └── test_low_poly.py         ← Tests unitaires
│
├── 📁 data/
│   ├── input/                   ← Mettez vos images ici
│   │   ├── test1.jpg            ← Image de test
│   │   └── test_landscape.jpg   ← Paysage généré
│   └── output/                  ← Résultats générés
│       ├── config_*.png         ← Exemples par preset
│       └── cli_test*.svg        ← Exemples SVG
│
├── 📦 venv/                      ← Environnement virtuel
├── 📄 requirements.txt           ← Dépendances Python
├── 🚀 run_gui.sh                 ← Launcher GUI
└── 🔗 .git/                      ← Git repository
```

---

## 🚀 Commandes essentielles

### Installation & Setup
```bash
# Créer environnement
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

### Utilisation
```bash
# CLI simple
python3 main.py input.jpg -o output.png

# Batch (traiter un dossier)
python3 main.py data/input/photos --batch -d results

# GUI interactive
./run_gui.sh

# Tester configurations
python3 test_configurations.py

# Export SVG
python3 main.py input.jpg -o output.svg --svg
```

### Développement
```bash
# Voir les logs git
git log --oneline

# Voir les changements
git diff

# Status du repo
git status
```

---

## 💡 Guides rapides

### 📸 Je veux convertir une image
→ Allez à `GUI_GUIDE.md` ou lancez `./run_gui.sh`

### 📦 Je veux traiter un dossier complet
→ Allez à `BATCH_PROCESSING.md`

### 💾 Je veux gérer des presets
→ Allez à `PRESETS_GUIDE.md`

### 🎨 Je veux comprendre l'algorithme
→ Lisez `DEVELOPMENT_SUMMARY.md` section "Algorithme"

### 🔧 Je veux modifier le code
→ Lisez `DEVELOPMENT_SUMMARY.md` puis modifiez `src/low_poly.py`

### 💾 Je veux exporter en SVG
→ Lisez `README.md` section "SVG" ou `USAGE_EXAMPLES.md`

### ⚙️ Je veux des paramètres personnalisés
→ Lisez `USAGE_EXAMPLES.md` section "Exemples CLI"

### 🎯 Je suis bloqué
→ Consultez `USAGE_EXAMPLES.md` section "Dépannage"

---

## 📊 Statistiques du projet

- **Langage** : Python 3.11
- **Lignes de code** : ~1600 (src)
- **Lignes de docs** : ~3500
- **Commits** : 16
- **Fonctionnalités** : 20+
- **Presets** : 8 (5 classic + 3 hybrid)
- **Formats export** : 2 (PNG + SVG)
- **Interfaces** : 3 (CLI + GUI + Batch)

---

## ✨ Features principales

✅ Triangulation Delaunay
✅ Edge detection avancée
✅ Amélioration des couleurs
✅ Interface CLI
✅ Interface GUI Tkinter
✅ Export PNG
✅ Export SVG vectoriel
✅ Formes géométriques hybrides
✅ Traitement par lots (batch)
✅ Gestion des presets
✅ 8 presets optimisés
✅ Paramètres ajustables
✅ Documentation complète

---

## 🔗 Liens rapides

| Besoin | Fichier |
|--------|---------|
| Démarrer | README.md |
| Utiliser GUI | GUI_GUIDE.md |
| Exemples CLI | USAGE_EXAMPLES.md |
| Batch processing | BATCH_PROCESSING.md |
| Gérer presets | PRESETS_GUIDE.md |
| Code source | src/low_poly.py |
| Architecture | DEVELOPMENT_SUMMARY.md |

---

## 📞 Support & Questions

**CLI problématique?**
→ `python3 main.py --help`

**GUI non responsive?**
→ `GUI_GUIDE.md` → "Dépannage"

**Résultat pas bon?**
→ `USAGE_EXAMPLES.md` → "Dépannage"

**Veux personnaliser?**
→ `USAGE_EXAMPLES.md` → "Cas d'usage"

---

## 🎊 Vous êtes prêt!

Choisissez votre chemin :
1. **👤 Utilisateur** → Lancez `./run_gui.sh`
2. **👨‍💻 Développeur** → Lisez `DEVELOPMENT_SUMMARY.md`
3. **🎨 Créatif** → Explorez `USAGE_EXAMPLES.md`

Bon amusement! 🎨✨
