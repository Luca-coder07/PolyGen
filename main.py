#!/usr/bin/env python3
"""
Script principal - Interface CLI pour PolyGen
"""
import argparse
import sys
from pathlib import Path
from src.low_poly import LowPolyGenerator


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
    
    args = parser.parse_args()
    
    # Vérifier que l'image d'entrée existe
    if not Path(args.input).exists():
        print(f"Erreur: Le fichier {args.input} n'existe pas")
        sys.exit(1)
    
    # Définir le chemin de sortie par défaut
    if args.output is None:
        args.output = "data/output/output.png"
    
    print(f"📸 Chargement: {args.input}")
    print(f"⚙️  Paramètres: {args.points} points, flou={args.blur}")
    
    try:
        # Créer le générateur
        generator = LowPolyGenerator(
            args.input,
            num_points=args.points,
            blur_strength=args.blur,
            enhance_colors=not args.no_enhance,
            edge_sensitivity=args.sensitivity
        )
        
        # Générer l'image
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
