"""
Script pour créer une image de test (paysage simple)
"""
import numpy as np
from PIL import Image, ImageDraw


def create_test_landscape():
    """Crée une image de paysage simple pour le test"""
    
    # Créer une image 600x400 (blanc par défaut)
    width, height = 600, 400
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Remplir le ciel (bleu)
    draw.rectangle([0, 0, width, 250], fill=(135, 206, 235))
    
    # Soleil
    sun_pos = (500, 80)
    draw.ellipse([sun_pos[0]-40, sun_pos[1]-40, sun_pos[0]+40, sun_pos[1]+40], 
                 fill=(255, 200, 0))
    
    # Montagne 1 (gauche)
    mountain1 = [(0, 250), (150, 80), (300, 250)]
    draw.polygon(mountain1, fill=(100, 150, 80))
    
    # Montagne 2 (centre)
    mountain2 = [(200, 250), (350, 100), (500, 250)]
    draw.polygon(mountain2, fill=(80, 130, 60))
    
    # Montagne 3 (droite)
    mountain3 = [(400, 250), (550, 120), (600, 250)]
    draw.polygon(mountain3, fill=(90, 140, 70))
    
    # Arbres (simples)
    tree_positions = [(100, 280), (250, 300), (450, 290)]
    for tx, ty in tree_positions:
        # Tronc
        draw.rectangle([tx-8, ty, tx+8, ty+40], fill=(101, 67, 33))
        # Feuillage
        draw.ellipse([tx-30, ty-30, tx+30, ty+20], fill=(34, 139, 34))
    
    # Herbe (bas)
    draw.rectangle([0, 250, width, height], fill=(50, 120, 50))
    
    # Ajouter un peu de variation avec du bruit
    img_array = np.array(img)
    
    # Ajouter du bruit
    noise = np.random.normal(0, 5, img_array.shape).astype(np.int16)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img_array)


if __name__ == "__main__":
    # Créer et sauvegarder l'image de test
    landscape = create_test_landscape()
    landscape.save("data/input/test_landscape.jpg")
    print("✅ Image de test créée: data/input/test_landscape.jpg")
    print(f"   Dimensions: {landscape.size}")
