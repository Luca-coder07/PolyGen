# 💡 Exemples d'utilisation - PolyGen

## 📝 Exemples CLI

### 1. Utilisation simple (recommandée)
```bash
python3 main.py data/input/photo.jpg -o output.png
```
✅ Utilise les paramètres par défaut optimisés
- 1000 points de triangulation
- Flou: 18
- Sensibilité: 2
- Avec contours noirs
- Couleurs améliorées

### 2. Style artistique lissé
```bash
python3 main.py paysage.jpg -o paysage_artistic.png -p 800 -b 25 -s 1
```
Résultat:
- Moins de triangles (plus abstrait)
- Beaucoup de flou (très lissé)
- Peu de contours (style doux)

### 3. Style ultra-détaillé
```bash
python3 main.py photo.jpg -o photo_detailed.png -p 2000 -b 10 -s 4 --no-outlines
```
Résultat:
- Beaucoup de détails
- Moins de flou
- Sans contours noirs (plus painterly)
- Très sensible aux contours

### 4. Export SVG vectoriel
```bash
python3 main.py photo.jpg -o photo.svg --svg -p 1000
```
✅ Format vectoriel infiniment scalable

### 5. Sans amélioration de couleurs
```bash
python3 main.py photo.jpg -o photo_no_enhance.png --no-enhance
```
✅ Conserve les couleurs originales (moins vives)

### 6. Sans contours noirs
```bash
python3 main.py photo.jpg -o soft.png --no-outlines
```
✅ Style plus doux, sans traits noirs

### 7. Configuration personnalisée
```bash
python3 main.py input.jpg \
  -o output.png \
  -p 1200 \           # 1200 triangles
  -b 20 \             # Flou moyen
  -s 3 \              # Sensibilité élevée
  --svg               # Export SVG aussi
```

---

## 🖱️ Exemples GUI

### Lancer la GUI
```bash
./run_gui.sh
```

### Workflow dans la GUI

1. **Charger une image**
   - Cliquez "Ouvrir une image"
   - Sélectionnez une photo
   - Aperçu s'affiche instantanément

2. **Choisir un preset**
   - "Équilibré" pour usage général
   - "Artistique" pour art abstrait
   - "Détaillé" pour haut-fidèle
   - "Expressif" pour cartoon bold
   - "Minimaliste" pour ultra-abstrait

3. **Affiner les paramètres**
   - Ajustez les sliders indépendamment
   - Les valeurs se mettent à jour en temps réel
   - Cochez/décochez les options

4. **Générer**
   - Cliquez "🎨 Générer l'image"
   - Attendez la barre de progression
   - Aperçu du résultat s'affiche

5. **Sauvegarder**
   - Cliquez "💾 Sauvegarder"
   - Choisissez le format (PNG/JPG)
   - Sélectionnez le dossier
   - C'est sauvegardé!

---

## 🎨 Cas d'usage recommandés

### Portrait
```bash
python3 main.py portrait.jpg -o portrait_art.png -p 1500 -b 18 -s 2
```

### Paysage montagneux
```bash
python3 main.py montagne.jpg -o montagne_art.png -p 1200 -b 20 -s 3
```

### Coucher de soleil
```bash
python3 main.py coucher.jpg -o coucher_art.png -p 800 -b 25 -s 1
```

### Photo urbaine
```bash
python3 main.py ville.jpg -o ville_art.png -p 1500 -b 15 -s 3
```

### Très haute résolution
```bash
# Pour une image 4K, réduisez les points
python3 main.py 4K.jpg -o 4K_art.png -p 1500 -b 18
```

### Très basse résolution
```bash
# Pour une petite image, réduisez aussi
python3 main.py small.jpg -o small_art.png -p 500 -b 20
```

---

## 📊 Paramètres par type d'image

| Type | Points | Blur | Sensibilité | Contours | Couleurs |
|------|--------|------|-------------|----------|----------|
| Portrait | 1200 | 18 | 2 | ✓ | ✓ |
| Paysage | 1000 | 20 | 2 | ✓ | ✓ |
| Architecture | 1500 | 15 | 3 | ✓ | ✓ |
| Abstrait | 600 | 25 | 1 | ✓ | ✓ |
| Nature | 1000 | 18 | 2 | ✓ | ✓ |
| Stylisé | 800 | 22 | 2 | ✗ | ✓ |
| Détaillé | 2000 | 10 | 4 | ✗ | ✓ |
| Minimaliste | 400 | 30 | 1 | ✓ | ✓ |

---

## 🔧 Astuces de dépannage

### Résultat trop abstrait?
→ Augmentez les points: `-p 1500`

### Trop détaillé?
→ Réduisez les points: `-p 500`

### Couleurs pas assez vives?
→ Gardez l'amélioration: (par défaut)

### Contours trop visibles?
→ Réduisez la sensibilité: `-s 1`

### Contours invisibles?
→ Augmentez la sensibilité: `-s 4`

### Ça prend trop longtemps?
→ Réduisez les points et augmentez le flou

### Résultat flou?
→ Réduisez le flou: `-b 10`

### Résultat pixelisé?
→ Augmentez le flou: `-b 25`

---

## 🎬 Exemples de batch

### Traiter plusieurs images
```bash
for img in data/input/*.jpg; do
  python3 main.py "$img" -o "data/output/$(basename $img).png"
done
```

### Avec preset spécifique
```bash
for img in data/input/photos/*.jpg; do
  python3 main.py "$img" -o "data/output/$(basename $img .jpg)_art.png" -p 1200 -b 20
done
```

---

## 🎯 Résultats attendus

### Configuration "Équilibré" (par défaut)
- Traitement: 30-60 secondes
- Taille PNG: 80-150 KB
- Style: Cartoon moyen, équilibré
- Usage: Plupart des photos

### Configuration "Minimaliste"
- Traitement: 10-30 secondes
- Taille PNG: 30-60 KB
- Style: Ultra-abstrait, épuré
- Usage: Signatures, art conceptuel

### Configuration "Détaillé"
- Traitement: 60-120 secondes
- Taille PNG: 150-300 KB
- Style: Haut-fidèle, riche en détails
- Usage: Préserver nuances et détails

### Export SVG
- Taille: 2-3x plus grande que PNG
- Qualité: Infinie (vectoriel)
- Usage: Impression, scaling infini

---

## 💡 Pro Tips

1. **Testez d'abord avec les presets** dans la GUI pour voir les styles
2. **Sauvegardez vos paramètres préférés** en notepad pour réutilisation CLI
3. **Exportez en SVG** si vous voulez imprimer grand format
4. **Réduisez la résolution source** pour traitement plus rapide
5. **Augmentez points pour détails fins**, réduisez pour style abstrait
6. **Sans contours** = style plus doux et painterly
7. **Haute sensibilité** = plus de contours détectés
8. **Utilisez GUI pour explorer**, CLI pour production

---

## 📸 Images de test recommandées

**Bon pour PolyGen:**
- Paysages avec contraste clair
- Photos bien éclairées
- Images avec formes géométriques
- Couchers de soleil
- Nature et architecture

**Plus difficile:**
- Photos très nuancées (gradient doux)
- Très sombres ou surexposées
- Beaucoup de petits détails
- Brouillard ou flou de mouvement

---

Amusez-vous avec PolyGen! 🎨✨
