"""
Tests unitaires pour PolyGen
"""
import unittest
import numpy as np
from pathlib import Path
from src.low_poly import LowPolyGenerator


class TestLowPolyGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Crée une image de test simple"""
        # Cette image de test sera créée si elle n'existe pas
        cls.test_image_path = "data/test_image.png"
        
    def test_initialization(self):
        """Teste l'initialisation du générateur"""
        # On va créer une image de test simple avec numpy
        import cv2
        
        # Créer une image de test (simple dégradé)
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)
        test_img[:100, :100] = [255, 0, 0]  # Rouge
        test_img[:100, 100:] = [0, 255, 0]  # Vert
        test_img[100:, :100] = [0, 0, 255]  # Bleu
        test_img[100:, 100:] = [255, 255, 0]  # Jaune
        
        test_path = "/tmp/test_image.png"
        cv2.imwrite(test_path, test_img)
        
        # Tester l'initialisation
        generator = LowPolyGenerator(test_path, num_points=100)
        self.assertEqual(generator.width, 200)
        self.assertEqual(generator.height, 200)
        self.assertEqual(generator.num_points, 100)
    
    def test_points_generation(self):
        """Teste la génération de points"""
        import cv2
        
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)
        test_path = "/tmp/test_image.png"
        cv2.imwrite(test_path, test_img)
        
        generator = LowPolyGenerator(test_path, num_points=100)
        points = generator.generate_points(use_edges=False)
        
        # Vérifier qu'on a le bon nombre de points (ou proche)
        self.assertGreater(len(points), 90)
        self.assertLess(len(points), 110)
        
        # Vérifier que tous les points sont dans les limites
        self.assertTrue(np.all(points[:, 0] >= 0))
        self.assertTrue(np.all(points[:, 0] < 200))
        self.assertTrue(np.all(points[:, 1] >= 0))
        self.assertTrue(np.all(points[:, 1] < 200))


if __name__ == "__main__":
    unittest.main()
