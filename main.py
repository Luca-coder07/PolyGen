#!/usr/bin/env python3
"""
Script principal - Interface CLI pour PolyGen
"""
import argparse
import sys
from pathlib import Path
from src.low_poly import LowPolyGenerator
from src.svg_export import SVGExporter
from src.advanced_shapes import HybridLowPolyGenerator
from src.batch_processor import batch_process_cli


def main():
    parser = argparse.ArgumentParser(
        description="PolyGen - Convertit des images en style low poly cartoon"
    )
    
    parser.add_argument(
        "input",
        type=str,
        help="Chemin vers l'image d'entrée"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Chemin de sortie (par défaut: data/output/output.png)"
    )
    
    parser.add_argument(
        "-p", "--points",
        type=int,
        default=1000,
        help="Nombre de points pour la triangulation (par défaut: 1000)"
    )
    
    parser.add_argument(
        "-b", "--blur",
        type=int,
        default=18,
        help="Force du flou (par défaut: 18)"
    )
    
    parser.add_argument(
        "--no-outlines",
        action="store_true",
        help="Ne pas dessiner les contours des triangles"
    )
    
    parser.add_argument(
        "--no-edges",
        action="store_true",
        help="Ignorer la détection des contours"
    )
    
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Ne pas améliorer les couleurs (saturation/contraste)"
    )
    
    parser.add_argument(
        "-s", "--sensitivity",
        type=int,
        default=2,
        help="Sensibilité de détection des contours 1-5 (défaut: 2)"
    )
    
    parser.add_argument(
        "--svg",
        action="store_true",
        help="Exporter en SVG vectoriel au lieu de PNG"
    )
    
    parser.add_argument(
        "--hybrid",
        action="store_true",
        help="Utiliser des formes géométriques mixtes (carrés, hexagones, etc.) au lieu de seulement des triangles"
    )
    
    parser.add_argument(
        "--grid-size",
        type=int,
        default=25,
        help="Taille de la grille pour le mode hybride en pixels (défaut: 25)"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Mode traitement par lots (batch mode) - traite toutes les images d'un dossier"
    )
    
    parser.add_argument(
        "-d", "--output-dir",
        type=str,
        default="data/output",
        help="Dossier de sortie pour le mode batch (défaut: data/output)"
    )
    
    args = parser.parse_args()
    
    # Mode traitement par lots (batch)
    if args.batch:
        exit_code = batch_process_cli(
            input_dir=args.input,
            output_dir=args.output_dir,
            hybrid=args.hybrid,
            grid_size=args.grid_size,
            num_points=args.points,
            blur_strength=args.blur,
            sensitivity=args.sensitivity,
            enhance=not args.no_enhance,
            outlines=not args.no_outlines
        )
        sys.exit(exit_code)
    
    # Mode standard (image unique)
    if not Path(args.input).exists():
        print(f"Erreur: Le fichier {args.input} n'existe pas")
        sys.exit(1)
    
    # Définir le chemin de sortie par défaut
    if args.output is None:
        args.output = "data/output/output.png"
    
    print(f"📸 Chargement: {args.input}")
    if args.hybrid:
        print(f"⚙️  Mode: HYBRIDE (formes mixtes)")
        print(f"⚙️  Paramètres: grid_size={args.grid_size}px")
    else:
        print(f"⚙️  Paramètres: {args.points} points, flou={args.blur}")
    
    try:
        # Mode hybride avec formes géométriques mixtes
        if args.hybrid:
            print("🎨 Génération avec formes géométriques mixtes...")
            hybrid_gen = HybridLowPolyGenerator(args.input, enable_shape_mixing=True)
            image = hybrid_gen.generate_hybrid(grid_size=args.grid_size)
            
            # Sauvegarder
            image.save(args.output)
            print(f"✅ Succès! Image sauvegardée: {args.output}")
        # Mode classique avec triangles
        else:
            # Créer le générateur
            generator = LowPolyGenerator(
                args.input,
                num_points=args.points,
                blur_strength=args.blur,
                enhance_colors=not args.no_enhance,
                edge_sensitivity=args.sensitivity
            )
            
            # Export SVG ou PNG
            if args.svg:
                print("🎨 Génération SVG vectoriel...")
                import cv2
                
                # Préparer l'image
                smoothed = generator.smooth_image()
                if not args.no_enhance:
                    smoothed_rgb = cv2.cvtColor(smoothed, cv2.COLOR_BGR2RGB)
                    smoothed_rgb = generator.enhance_color_image(smoothed_rgb)
                    smoothed = cv2.cvtColor(smoothed_rgb, cv2.COLOR_RGB2BGR)
                
                # Générer triangulation
                points = generator.generate_points(use_edges=not args.no_edges)
                tri = generator.triangulate(points)
                
                # Créer l'exporteur SVG
                exporter = SVGExporter(generator.width, generator.height)
                
                # Ajouter les triangles
                for triangle_indices in tri.simplices:
                    tri_points = points[triangle_indices]
                    color = generator.get_triangle_color(triangle_indices, points, smoothed)
                    outline = (0, 0, 0) if not args.no_outlines else None
                    exporter.add_triangle(tri_points, color, outline, 1)
                
                # Sauvegarder
                exporter.save(args.output)
                print(f"✅ Succès! SVG généré: {args.output}")
            else:
                print("🎨 Génération de l'image low poly...")
                image = generator.generate(
                    use_edge_detection=not args.no_edges,
                    add_outlines=not args.no_outlines
                )
                
            # Sauvegarder
            generator.save(args.output, image)
            print(f"✅ Succès! Image sauvegardée: {args.output}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
