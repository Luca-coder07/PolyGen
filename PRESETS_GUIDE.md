# Presets Management Guide

## Overview

PolyGen includes a comprehensive presets system that allows you to save, load, and manage custom configurations. Presets store all generation parameters and can be used from both the CLI and GUI.

## Features

- **8 Built-in Presets**: 5 classic + 3 hybrid presets optimized for different styles
- **Persistent Storage**: Presets are saved in `~/.polygen/presets.json`
- **Full Parameter Support**: Save all parameters including mode, points, blur, sensitivity, etc.
- **GUI Management**: Create, rename, delete presets directly from the interface
- **CLI Integration**: Load and save presets from command line
- **Protection**: Default presets cannot be accidentally deleted
- **Descriptions**: Add descriptions to presets for organization

## Built-in Presets

### Classic Mode (Triangulation)

| Name | Points | Blur | Sensitivity | Description |
|------|--------|------|-------------|-------------|
| **Équilibré** | 1000 | 18 | 2 | Balanced - recommended for most images |
| **Artistique** | 800 | 25 | 1 | Artistic smooth - abstract style |
| **Détaillé** | 1800 | 12 | 3 | High fidelity - preserves fine details |
| **Expressif** | 1200 | 20 | 3 | Expressive cartoon - strong outlines |
| **Minimaliste** | 500 | 28 | 1 | Ultra abstract - minimal shapes |

### Hybrid Mode (Mixed Shapes)

| Name | Grid Size | Description |
|------|-----------|-------------|
| **Hybride Équilibré** | 25px | Balanced - natural and efficient |
| **Hybride Détaillé** | 15px | High resolution - more shapes |
| **Hybride Minimaliste** | 35px | Very abstract - minimal shapes |

## GUI Usage

### Loading a Preset

1. Open the application: `./run_gui.sh`
2. In the **Presets** section, select a preset from the dropdown
3. Click **⬇️ Charger** to apply it
4. Parameters automatically update
5. Click **🎨 Générer** to generate the image

### Saving Custom Presets

1. Adjust parameters (points, blur, sensitivity, etc.)
2. Click **💾 Sauvegarder**
3. Enter a name for your preset
4. (Optional) Add a description
5. Click **Sauvegarder**

### Managing Presets

**Rename:**
1. Select a preset from dropdown
2. Click **🔄 Renommer**
3. Enter new name
4. Click **Renommer**

**Delete:**
1. Select a preset from dropdown
2. Click **🗑️ Supprimer**
3. Confirm deletion (default presets cannot be deleted)

**View All:**
1. Click **📋 Liste**
2. View formatted list of all presets with descriptions

## CLI Usage

### List Presets

```bash
python3 main.py --list-presets
```

Shows:
- All available presets
- Organized by mode (classic/hybrid)
- Full parameters for each preset
- Descriptions

### Save a Preset

```bash
# Basic
python3 main.py --save-preset "My Preset" -p 1500 -b 20

# With description
python3 main.py --save-preset "My Style" --preset-description "Custom settings" -p 1200 -b 22 -s 2

# Hybrid preset
python3 main.py --save-preset "Hybrid Custom" --hybrid --grid-size 18
```

### Load and Use a Preset

```bash
# Load preset for image generation
python3 main.py image.jpg --load-preset "Minimaliste" -o output.png

# Load hybrid preset
python3 main.py image.jpg --load-preset "Hybride Détaillé" -o output.png

# Load and customize (override preset values)
python3 main.py image.jpg --load-preset "Équilibré" -p 800 -o output.png
```

### Batch Processing with Presets

```bash
# Use preset for batch processing
python3 main.py input_folder --batch --load-preset "Artistique" -d results

# Load hybrid preset for batch
python3 main.py input_folder --batch --load-preset "Hybride Équilibré" -d results
```

## Storage Location

Presets are stored in: `~/.polygen/presets.json`

### Manual Management

You can also edit presets manually:

```bash
# View all presets (as JSON)
cat ~/.polygen/presets.json

# Import a preset from JSON
python3 -c "from src.preset_manager import get_preset_manager; \
    m = get_preset_manager(); \
    m.import_preset('my_preset.json')"
```

### Preset JSON Format

```json
{
  "My Preset": {
    "name": "My Preset",
    "description": "My custom settings",
    "mode": "classic",
    "points": 1500,
    "blur_strength": 20,
    "edge_sensitivity": 2,
    "enhance_colors": true,
    "add_outlines": true,
    "grid_size": 25
  }
}
```

## Workflow Examples

### Example 1: Save and Reuse a Custom Style

```bash
# Experiment with settings and save when you like the result
python3 main.py --save-preset "My Style" -p 1100 -b 19 --preset-description "Balanced with slightly more blur"

# Use the preset for multiple images
python3 main.py photo1.jpg --load-preset "My Style" -o results/photo1.png
python3 main.py photo2.jpg --load-preset "My Style" -o results/photo2.png
```

### Example 2: Create Style Variations

```bash
# Save different variations
python3 main.py --save-preset "Artistic v1" -p 800 -b 25 -s 1
python3 main.py --save-preset "Artistic v2" -p 800 -b 28 -s 1
python3 main.py --save-preset "Artistic v3" -p 700 -b 25 -s 1

# List all
python3 main.py --list-presets

# Process entire folder with each style
python3 main.py photos --batch --load-preset "Artistic v1" -d results/v1
python3 main.py photos --batch --load-preset "Artistic v2" -d results/v2
python3 main.py photos --batch --load-preset "Artistic v3" -d results/v3
```

### Example 3: Hybrid Presets for Batch

```bash
# Save hybrid variation
python3 main.py --save-preset "Hybrid Fast" --hybrid --grid-size 30

# Use for batch - faster processing, fewer shapes
python3 main.py large_photo_folder --batch --load-preset "Hybrid Fast" -d results
```

## Preset API (Python)

For programmatic access:

```python
from src.preset_manager import get_preset_manager, Preset

# Get manager
manager = get_preset_manager()

# List presets
for preset in manager.list_presets():
    print(f"{preset.name}: {preset.mode} mode")

# Load a preset
preset = manager.load_preset("Équilibré")
if preset:
    print(f"Points: {preset.points}")
    print(f"Blur: {preset.blur_strength}")

# Save a custom preset
new_preset = Preset(
    name="Custom",
    description="My custom preset",
    mode="classic",
    points=1200,
    blur_strength=18,
    edge_sensitivity=2
)
manager.save_preset(new_preset)

# Delete a preset
manager.delete_preset("Custom")

# Rename
manager.rename_preset("Old Name", "New Name")
```

## Tips

### Creating Effective Presets

1. **Start with defaults**: Base new presets on built-in ones
2. **Test thoroughly**: Generate several test images before saving
3. **Add descriptions**: Help yourself remember what each preset does
4. **Name clearly**: Use descriptive names like "Portrait" or "Landscape"
5. **Document settings**: Include target use case in description

### Organization Strategy

```bash
# Organize by style
"Artistic - Smooth"
"Artistic - Detailed"

# Or by use case
"Portrait - Balanced"
"Landscape - Detailed"

# Or by client
"Client A - Standard"
"Client A - Minimal"
```

### Performance Tips

- **Faster results**: Use larger grid sizes for hybrid or fewer points for classic
- **Better quality**: Increase points or reduce grid size
- **Balance**: Use default "Équilibré" as starting point

## Troubleshooting

### Preset not found
```bash
# List all presets to verify name
python3 main.py --list-presets

# Check exact spelling and case
```

### Cannot delete default presets
- Default presets are protected
- You can rename/duplicate them with custom names
- Or save new variations

### Settings not applied
- Verify preset exists: `python3 main.py --list-presets`
- Check CLI syntax: `python3 main.py img.jpg --load-preset "Name"`
- Ensure quotes around preset names with spaces

### Presets lost after update
- Presets are stored in `~/.polygen/presets.json`
- Always safe from code updates
- Back up this file before major changes

## See Also

- [Main README](README.md) - Project overview
- [Batch Processing](BATCH_PROCESSING.md) - Batch mode guide
- [Usage Examples](USAGE_EXAMPLES.md) - More CLI examples
- [GUI Guide](GUI_GUIDE.md) - Interactive interface
