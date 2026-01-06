"""
Script pour tester et afficher les configurations optimales
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.low_poly import LowPolyGenerator


def test_configurations():
    """Test plusieurs configurations pour trouver l'optimale"""
    
    input_path = "data/input/test1.jpg"
    
    configurations = [
        {
            "name": "Équilibré (recommandé)",
            "points": 1000,
            "blur": 18,
            "enhance": True,
            "sensitivity": 2,
            "outlines": True,
            "output": "data/output/config_balanced.png"
        },
        {
            "name": "Très artistique (lissé)",
            "points": 800,
            "blur": 25,
            "enhance": True,
            "sensitivity": 1,
            "outlines": True,
            "output": "data/output/config_artistic.png"
        },
        {
            "name": "Ultra détaillé",
            "points": 1800,
            "blur": 12,
            "enhance": True,
            "sensitivity": 3,
            "outlines": False,
            "output": "data/output/config_detailed.png"
        },
        {
            "name": "Cartoon expressif",
            "points": 1200,
            "blur": 20,
            "enhance": True,
            "sensitivity": 3,
            "outlines": True,
            "output": "data/output/config_expressive.png"
        },
        {
            "name": "Minimaliste",
            "points": 500,
            "blur": 28,
            "enhance": True,
            "sensitivity": 1,
            "outlines": True,
            "output": "data/output/config_minimal.png"
        }
    ]
    
    print("🎨 Test des configurations optimales...")
    print("=" * 60)
    
    for config in configurations:
        print(f"\n📊 {config['name']}")
        print(f"   Points: {config['points']} | Flou: {config['blur']} | Sensibilité: {config['sensitivity']}")
        print(f"   Contours: {'Oui' if config['outlines'] else 'Non'} | Couleurs: {'Oui' if config['enhance'] else 'Non'}")
        print(f"   → {config['output']}")
        
        try:
            generator = LowPolyGenerator(
                input_path,
                num_points=config['points'],
                blur_strength=config['blur'],
                enhance_colors=config['enhance'],
                edge_sensitivity=config['sensitivity']
            )
            
            image = generator.generate(
                use_edge_detection=True,
                add_outlines=config['outlines']
            )
            
            generator.save(config['output'], image)
            print("   ✅ Succès!")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test complété!")
    print("\n📌 Recommandation: Utilisez 'Équilibré' comme configuration par défaut")
    print("   - Bon équilibre entre détails et style cartoon")
    print("   - Couleurs vives et contours expressifs")
    print("   - Temps de traitement raisonnable")


if __name__ == "__main__":
    test_configurations()
