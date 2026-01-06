# Guide d'utilisation - Interface GUI

## Lancer la GUI

```bash
# Option 1: Script de lancement
chmod +x run_gui.sh
./run_gui.sh

# Option 2: Directement
source venv/bin/activate
python3 gui.py
```

## Interface

### 1. Chargement d'image
- Cliquez sur "Ouvrir une image"
- Sélectionnez une photo JPG, PNG, etc.
- L'aperçu s'affiche automatiquement

### 2. Paramètres (sliders)

#### Points de triangulation
- **Gauche (200)** : Très abstrait
- **Milieu (1000)** : Équilibré (recommandé)
- **Droite (2000)** : Très détaillé

#### Flou
- **Bas (5)** : Près de l'original
- **Moyen (18)** : Style cartoon équilibré
- **Haut (35)** : Ultra lissé

#### Sensibilité de contours
- **1** : Peu de contours
- **2-3** : Équilibré
- **4-5** : Beaucoup de contours

### 3. Options
- **Afficher contours** : Active les traits noirs
- **Améliorer couleurs** : Augmente saturation/contraste

### 4. Presets rapides
Cliquez sur un preset pour appliquer les paramètres recommandés:
- **Équilibré** : Bon pour la plupart des images
- **Artistique** : Style épuré et lissé
- **Détaillé** : Maximum de détails
- **Expressif** : Cartoon avec contours marqués
- **Minimaliste** : Ultra-abstrait

### 5. Génération
1. Cliquez sur "🎨 Générer l'image"
2. Attendez la génération (visible en bas)
3. L'aperçu du résultat s'affiche

### 6. Sauvegarde
1. Après génération, cliquez "💾 Sauvegarder"
2. Choisissez le dossier et le format (PNG/JPG)
3. Le fichier est sauvegardé

## Conseils

### Générer rapidement
- Réduisez les points (200-500)
- Augmentez le flou (25+)
- Utilisez le preset "Minimaliste"

### Meilleure qualité
- Augmentez les points (1500+)
- Réduisez le flou (10-15)
- Activez "Améliorer couleurs"
- Utilisez le preset "Détaillé"

### Affiner les contours
- Augmentez la sensibilité (4-5)
- Activez "Afficher contours"
- Réduisez le flou

### Personnalisé
- Adaptez chaque slider indépendamment
- Utilisez les presets comme point de départ
- Ajustez finement avec les sliders

## Dépannage

**La GUI ne démarre pas**
```bash
source venv/bin/activate
python3 -c "import tkinter; print('OK')"
```

**Erreur "tkinter not found"**
```bash
# Installer tkinter
sudo apt-get install python3-tk  # Linux
brew install python-tk@3.11      # macOS
```

**Génération très lente**
- Réduisez le nombre de points
- Augmentez le flou (traitement plus rapide)
- Utilisez une image plus petite

## Raccourcis clavier
(À venir)
