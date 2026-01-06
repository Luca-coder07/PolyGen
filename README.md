# PolyGen 🎨

Un générateur d'images 2D low poly automatisé en **Python**, convertissant des photos de paysage réel en style **cartoon low poly** grâce à des algorithmes de triangulation et de traitement d'image avancés.

## 🎯 Objectifs

- ✅ Conversion d'images réelles en style low poly cartoon
- ✅ Triangulation de Delaunay automatique avec détection de contours
- ✅ Amélioration des couleurs (saturation/contraste)
- ✅ Interface CLI simple avec paramètres ajustables
- 🔄 Interface GUI interactive (Tkinter) - en cours
- 📦 Export en PNG/SVG - en cours

## 🚀 Installation

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 💻 Utilisation

### Ligne de commande (CLI)

```bash
# Utilisation simple (avec paramètres par défaut optimisés)
python3 main.py data/input/photo.jpg -o data/output/result.png

# Avec paramètres personnalisés
python3 main.py data/input/photo.jpg \
  -o data/output/result.png \
  -p 1000 \           # Nombre de triangles
  -b 18 \             # Force du flou
  -s 2 \              # Sensibilité de contours (1-5)
  --no-enhance        # Sans amélioration des couleurs
```

### Options disponibles

| Option | Défaut | Description |
|--------|--------|-------------|
| `-p, --points` | 1000 | Nombre de points de triangulation (200-2000) |
| `-b, --blur` | 18 | Force du flou gaussien (5-30) |
| `-s, --sensitivity` | 2 | Sensibilité détection de contours (1-5) |
| `--no-outlines` | - | Retire les contours noirs des triangles |
| `--no-edges` | - | Désactive la détection de contours |
| `--no-enhance` | - | Désactive l'amélioration des couleurs |

## 📊 Configurations recommandées

### 1. **Équilibré** (par défaut)
```bash
python3 main.py input.jpg -p 1000 -b 18 -s 2
```
- ✅ Bon équilibre détails/cartoon
- ✅ Couleurs vives et expressives
- ✅ Contours lisibles
- ⏱️ Temps raisonnable (~30-60s selon image)

### 2. **Très artistique** (Style épuré)
```bash
python3 main.py input.jpg -p 800 -b 25 -s 1
```
- ✅ Style cartoon très marqué
- ✅ Moins de détails
- ✅ Plus rapide
- ❌ Perte de nuances

### 3. **Ultra détaillé** (Plus proche original)
```bash
python3 main.py input.jpg -p 1800 -b 12 -s 3 --no-outlines
```
- ✅ Beaucoup de détails
- ✅ Ressemble plus à l'original
- ❌ Moins "cartoon"
- ❌ Plus lent

### 4. **Cartoon expressif**
```bash
python3 main.py input.jpg -p 1200 -b 20 -s 3
```
- ✅ Style cartoon marqué
- ✅ Bonne définition
- ✅ Contours expressifs

### 5. **Minimaliste** (Ultra abstrait)
```bash
python3 main.py input.jpg -p 500 -b 28 -s 1
```
- ✅ Très abstrait
- ✅ Moins de couleurs
- ✅ Très rapide
- ❌ Peu de détails

## 🔧 Paramètres en détail

### Points de triangulation (`-p`)
- **200-400** : Abstrait, très stylisé
- **500-800** : Artistique, minimaliste
- **1000-1200** : Équilibré (recommandé)
- **1500-2000** : Détaillé, proche original
- **2000+** : Ultra-détaillé (long à traiter)

### Force du flou (`-b`)
- **5-10** : Minimal, préserve détails
- **12-18** : Équilibré, style cartoon
- **20-25** : Cartoon épuré, plus abstrait
- **25+** : Ultra lissé, très abstrait

### Sensibilité de contours (`-s`)
- **1** : Peu de contours, plus fluide
- **2-3** : Équilibré (recommandé)
- **4-5** : Beaucoup de contours, très détaillé

## 📁 Structure du projet

```
PolyGen/
├── src/
│   ├── __init__.py
│   └── low_poly.py          # Moteur principal
├── tests/
│   └── test_low_poly.py     # Tests unitaires
├── data/
│   ├── input/               # Mettez vos images ici
│   └── output/              # Résultats générés
├── main.py                  # Interface CLI
├── test_configurations.py   # Test des presets
├── requirements.txt
└── README.md
```

## 🎨 Algorithme

1. **Chargement** : Lecture de l'image source
2. **Détection de contours** : Canny + morphologie
3. **Génération de points** : Coin + contours + aléatoire
4. **Triangulation** : Delaunay (scipy)
5. **Lissage** : Flou gaussien pour effet cartoon
6. **Amélioration** : Augmentation saturation/contraste
7. **Remplissage** : Coloration par triangle (moyenne)
8. **Contours** : Traits noirs optionnels
9. **Export** : PNG ou SVG

## 🐛 Dépannage

### L'image est trop abstrait/détaillée
→ Ajustez le nombre de points (`-p`)

### Les contours sont trop visibles/invisibles
→ Ajustez la sensibilité (`-s`) ou retirez-les (`--no-outlines`)

### Les couleurs ne sont pas assez vives
→ Augmentez le flou ou utilisez l'amélioration couleurs

### Ça prend trop longtemps
→ Réduisez le nombre de points ou l'image source

## 📚 Dépendances

- **OpenCV** : Traitement d'image
- **NumPy** : Calculs numériques
- **SciPy** : Triangulation Delaunay
- **Pillow** : Gestion PNG/JPG
- **scikit-image** : Filtres avancés

## 🔮 Prochaines améliorations

- [ ] Interface GUI avec Tkinter (aperçu en temps réel)
- [ ] Export SVG vectoriel
- [ ] Mode batch (traiter dossier entier)
- [ ] Presets sauvegardables
- [ ] Histogramme de couleurs
- [ ] Support des filtres personnalisés

## 📝 Licence

MIT

## 👨‍💻 Auteur

Créé avec ❤️ en Python 3.11
