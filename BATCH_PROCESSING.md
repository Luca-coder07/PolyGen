# Batch Processing Guide

## Overview

PolyGen supports batch processing to convert multiple images in a single command. This is useful for processing entire folders of images with consistent parameters.

## Features

- **Folder Processing**: Automatically discovers all images in a folder
- **Recursive Search**: Finds images in subdirectories
- **Progress Reporting**: Real-time status for each image
- **Error Handling**: Continues processing even if individual images fail
- **Comprehensive Statistics**: Detailed summary with timing and file size data
- **Both Modes**: Works with classic triangulation and hybrid shape modes

## Quick Start

### Classic Mode (Triangles)
```bash
# Process all images in a folder
python3 main.py data/input/my_images --batch -d data/output/processed

# With custom parameters
python3 main.py data/input/my_images --batch -d data/output/processed -p 1200 -b 20 -s 3
```

### Hybrid Mode (Mixed Shapes)
```bash
# Process with hybrid shapes
python3 main.py data/input/my_images --batch --hybrid --grid-size 25 -d data/output/processed

# With smaller grid for more detail
python3 main.py data/input/my_images --batch --hybrid --grid-size 15 -d data/output/processed
```

## CLI Usage

### Basic Syntax
```bash
python3 main.py <input_folder> --batch [options]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--batch` | N/A | N/A | Enable batch processing mode |
| `--output-dir` | `-d` | `data/output` | Output folder for processed images |
| `--hybrid` | N/A | False | Use hybrid shape mode |
| `--grid-size` | N/A | 25 | Grid cell size for hybrid mode (pixels) |
| `--points` | `-p` | 1000 | Points for classic mode triangulation |
| `--blur` | `-b` | 18 | Blur strength for classic mode |
| `--sensitivity` | `-s` | 2 | Edge detection sensitivity (1-5) |
| `--no-enhance` | N/A | False | Disable color enhancement |
| `--no-outlines` | N/A | False | Disable triangle outlines |

## Examples

### Example 1: Basic Batch Processing
```bash
python3 main.py data/input/photos --batch
```
- Processes all images in `data/input/photos`
- Saves to default `data/output`
- Uses default parameters (1000 points, blur=18)

### Example 2: Batch with Custom Parameters
```bash
python3 main.py data/input/photos --batch -d results -p 1500 -b 25
```
- Higher point count (1500) for more detail
- Stronger blur (25) for more stylized effect
- Output to `results` folder

### Example 3: Hybrid Batch Processing
```bash
python3 main.py data/input/photos --batch --hybrid --grid-size 20 -d results/hybrid
```
- Uses hybrid shape generation
- 20px grid size (smaller = more shapes, more detail)
- Creates `results/hybrid` automatically if missing

### Example 4: Artistic Batch Processing
```bash
python3 main.py data/input/landscape --batch -p 800 -b 28 -s 1 -d results/artistic
```
- Lower point count (800) for abstract look
- High blur (28) for painterly effect
- Low sensitivity (1) for minimal edges

## Output

### File Naming
Output files follow the pattern: `original_filename_polygen.png`

Examples:
- `photo.jpg` → `photo_polygen.png`
- `vacation_2024.jpg` → `vacation_2024_polygen.png`
- `landscape.png` → `landscape_polygen.png`

### Summary Statistics

After processing completes, you'll see a summary like:

```
======================================================================
📊 RÉSUMÉ DU TRAITEMENT PAR LOTS
======================================================================
Total des images:       10
Réussies:              ✅ 9
Échouées:              ❌ 1
Taux de réussite:      90.0%

Temps total:           65.30s
Temps moyen/image:     6.53s

Taille entrée totale:  2.5MB
Taille sortie totale:  1.8MB
Compression:           +28.0%
======================================================================
```

### What It Shows
- **Total images**: Number of images processed
- **Successful/Failed**: Count of successful and failed conversions
- **Success rate**: Percentage of successful conversions
- **Total time**: Cumulative processing time
- **Average time**: Time per image
- **Size analysis**: Input vs output file sizes and compression ratio

## Supported Image Formats

By default, the following formats are supported:
- `.jpg`, `.jpeg`
- `.png`
- `.bmp`

The search is case-insensitive, so `.JPG`, `.PNG`, etc. are also recognized.

## Performance

### Benchmarks (on test system)
- **Classic mode** (~1000 points): 6-8 seconds per image
- **Hybrid mode** (20px grid): 10-15 seconds per image
- **Batch overhead**: Minimal (< 1 second for small batches)

Processing time depends on:
- Image resolution
- Number of points (classic) or grid size (hybrid)
- Blur strength and edge detection sensitivity
- System performance (CPU)

## Error Handling

### What Happens on Error

If an image fails to process, the batch processor:
1. **Logs the error** in the progress output
2. **Continues processing** remaining images
3. **Reports it** in the final summary

Example output when an error occurs:
```
❌ [  3/10] corrupted_file.jpg
      Erreur: Cannot identify image file 'corrupted_file.jpg'
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "No images found" | Check folder path and file extensions |
| Permission denied | Ensure write permission to output folder |
| Out of memory | Process in smaller batches or use lower point counts |
| Very slow processing | Reduce points/blur or use smaller images |

## Advanced Usage

### Processing with Specific Presets

While presets are primarily for GUI, you can replicate them with CLI:

**Équilibré (Balanced)**
```bash
python3 main.py input --batch -p 1000 -b 18 -s 2
```

**Artistique (Artistic)**
```bash
python3 main.py input --batch -p 800 -b 25 -s 1
```

**Détaillé (Detailed)**
```bash
python3 main.py input --batch -p 1800 -b 12 -s 3 --no-outlines
```

**Expressif (Expressive)**
```bash
python3 main.py input --batch -p 1200 -b 20 -s 3
```

**Minimaliste (Minimal)**
```bash
python3 main.py input --batch -p 500 -b 28 -s 1
```

### Organizing Output

Use descriptive output folder names for different styles:

```bash
# Create various stylized versions
python3 main.py photos --batch -d results/detailed -p 1800
python3 main.py photos --batch -d results/artistic -p 800 -b 28
python3 main.py photos --batch -d results/hybrid --hybrid --grid-size 20
```

## Batch API (Python)

For programmatic access, import the batch processor:

```python
from src.batch_processor import BatchProcessor, BatchConfig

# Configure batch processing
config = BatchConfig(
    input_dir="data/input/photos",
    output_dir="data/output/results",
    num_points=1200,
    blur_strength=20,
    edge_sensitivity=2,
    hybrid_mode=False,
    enhance_colors=True,
    add_outlines=True
)

# Process
processor = BatchProcessor(config)
results = processor.process_batch()

# Print summary
processor.print_summary()

# Access results programmatically
for result in results:
    if result.success:
        print(f"✅ {result.input_file} → {result.output_file} ({result.processing_time:.2f}s)")
    else:
        print(f"❌ {result.input_file}: {result.error_message}")
```

## Tips for Best Results

1. **Start with defaults**: Try the default parameters first
2. **Test first**: Process a single image to preview results before batch
3. **Organize input**: Group similar images by style/content
4. **Monitor progress**: The progress display shows real-time status
5. **Check output**: Review first few processed images to verify quality
6. **Adjust and retry**: Use different parameters for different needs

## Troubleshooting

### Slow Processing
- Use fewer points (reduce `-p` value)
- Reduce blur strength (lower `-b` value)
- Use hybrid mode with larger grid size

### Memory Issues
- Process in smaller batches
- Close other applications
- Reduce image resolution if possible

### Quality Issues
- Try hybrid mode (often produces better results)
- Increase point count or reduce grid size
- Increase blur strength for smoothing

### Unsupported Images
- Check file format is supported
- Verify file integrity
- Try opening in image viewer first

## See Also

- [Main README](README.md) - Project overview
- [GUI Guide](GUI_GUIDE.md) - Interactive interface
- [Usage Examples](USAGE_EXAMPLES.md) - More command examples
