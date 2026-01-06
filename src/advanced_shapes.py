"""
Module avancé pour générer des formes géométriques variées
Au lieu de seulement des triangles, utilise carré, rectangle, cercle, hexagone, etc.
"""
import cv2
import numpy as np
from scipy.spatial import Delaunay
from PIL import Image
import math


class PolygonType:
    """Types de polygones disponibles"""
    TRIANGLE = "triangle"
    SQUARE = "square"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    HEXAGON = "hexagon"
    PENTAGON = "pentagon"


class AdvancedShapeGenerator:
    """Génère des formes géométriques variées pour le low poly"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    @staticmethod
    def create_triangle(center: tuple, size: float) -> np.ndarray:
        """Crée un triangle équilatéral"""
        cx, cy = center
        angles = np.array([90, 210, 330]) * np.pi / 180
        points = []
        for angle in angles:
            x = cx + size * np.cos(angle)
            y = cy + size * np.sin(angle)
            points.append([x, y])
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def create_square(center: tuple, size: float) -> np.ndarray:
        """Crée un carré"""
        cx, cy = center
        half_size = size / 2
        points = [
            [cx - half_size, cy - half_size],
            [cx + half_size, cy - half_size],
            [cx + half_size, cy + half_size],
            [cx - half_size, cy + half_size]
        ]
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def create_rectangle(center: tuple, width: float, height: float) -> np.ndarray:
        """Crée un rectangle"""
        cx, cy = center
        half_w = width / 2
        half_h = height / 2
        points = [
            [cx - half_w, cy - half_h],
            [cx + half_w, cy - half_h],
            [cx + half_w, cy + half_h],
            [cx - half_w, cy + half_h]
        ]
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def create_circle(center: tuple, radius: float, sides: int = 16) -> np.ndarray:
        """Crée un cercle (polygone régulier)"""
        cx, cy = center
        points = []
        for i in range(sides):
            angle = 2 * np.pi * i / sides
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append([x, y])
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def create_hexagon(center: tuple, size: float) -> np.ndarray:
        """Crée un hexagone régulier"""
        cx, cy = center
        points = []
        for i in range(6):
            angle = (i * 60 + 30) * np.pi / 180
            x = cx + size * np.cos(angle)
            y = cy + size * np.sin(angle)
            points.append([x, y])
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def create_pentagon(center: tuple, size: float) -> np.ndarray:
        """Crée un pentagone régulier"""
        cx, cy = center
        points = []
        for i in range(5):
            angle = (i * 72 - 90) * np.pi / 180
            x = cx + size * np.cos(angle)
            y = cy + size * np.sin(angle)
            points.append([x, y])
        return np.array(points, dtype=np.int32)
    
    @staticmethod
    def choose_best_shape(edge_density: float) -> str:
        """
        Choisit la meilleure forme selon la densité de contours
        
        Args:
            edge_density: Densité de contours (0-1)
            
        Returns:
            Type de polygone optimal
        """
        if edge_density < 0.2:
            return PolygonType.SQUARE  # Zones lisses
        elif edge_density < 0.4:
            return PolygonType.RECTANGLE
        elif edge_density < 0.6:
            return PolygonType.HEXAGON  # Zone moyenne
        elif edge_density < 0.8:
            return PolygonType.PENTAGON
        else:
            return PolygonType.TRIANGLE  # Zones avec beaucoup de contours


class HybridLowPolyGenerator:
    """
    Générateur low poly utilisant plusieurs formes géométriques
    pour des résultats optimisés selon les zones de l'image
    """
    
    def __init__(self, image_path: str, enable_shape_mixing: bool = True):
        """
        Initialise le générateur hybride
        
        Args:
            image_path: Chemin vers l'image
            enable_shape_mixing: Si True, mélange les formes, sinon seulement triangles
        """
        self.image = cv2.imread(image_path)
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width = self.image.shape[:2]
        self.enable_shape_mixing = enable_shape_mixing
        self.shape_gen = AdvancedShapeGenerator(self.width, self.height)
    
    def detect_edges(self) -> np.ndarray:
        """Détecte les contours"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray_enhanced = clahe.apply(gray)
        edges = cv2.Canny(gray_enhanced, 50, 150)
        return edges
    
    def analyze_region_edges(self, region_mask: np.ndarray) -> float:
        """
        Analyse la densité de contours dans une région
        
        Args:
            region_mask: Masque de la région
            
        Returns:
            Densité de contours (0-1)
        """
        edges = self.detect_edges()
        region_edges = edges[region_mask > 0]
        
        if len(region_edges) == 0:
            return 0.0
        
        edge_ratio = np.sum(region_edges > 0) / len(region_edges)
        return min(1.0, edge_ratio * 3)  # Normaliser
    
    def get_best_shape_for_region(self, region_mask: np.ndarray) -> str:
        """Détermine la meilleure forme pour une région"""
        edge_density = self.analyze_region_edges(region_mask)
        return self.shape_gen.choose_best_shape(edge_density)
    
    def generate_hybrid(self, grid_size: int = 30, smoothed_image: np.ndarray = None) -> Image.Image:
        """
        Génère une image low poly avec formes géométriques mixtes
        
        Args:
            grid_size: Taille des cellules de grille (pixels)
            smoothed_image: Image pré-lissée (optionnel)
            
        Returns:
            Image PIL
        """
        if smoothed_image is None:
            smoothed_image = cv2.GaussianBlur(self.image, (15, 15), 0)
        
        output = np.zeros_like(smoothed_image)
        
        # Parcourir l'image par grille
        shapes_used = {
            PolygonType.TRIANGLE: 0,
            PolygonType.SQUARE: 0,
            PolygonType.RECTANGLE: 0,
            PolygonType.HEXAGON: 0,
            PolygonType.PENTAGON: 0,
            PolygonType.CIRCLE: 0,
        }
        
        for y in range(0, self.height, grid_size):
            for x in range(0, self.width, grid_size):
                # Définir les limites de la cellule
                x_end = min(x + grid_size, self.width)
                y_end = min(y + grid_size, self.height)
                
                # Créer un masque de la région
                region_mask = np.zeros((self.height, self.width), dtype=np.uint8)
                region_mask[y:y_end, x:x_end] = 255
                
                # Déterminer la meilleure forme
                if self.enable_shape_mixing:
                    shape_type = self.get_best_shape_for_region(region_mask)
                else:
                    shape_type = PolygonType.TRIANGLE
                
                shapes_used[shape_type] += 1
                
                # Calculer couleur moyenne de la région
                region_colors = smoothed_image[y:y_end, x:x_end]
                if len(region_colors) > 0:
                    mean_color = np.mean(region_colors.reshape(-1, 3), axis=0).astype(int)
                else:
                    mean_color = [128, 128, 128]
                
                mean_color = tuple(int(c) for c in mean_color)
                
                # Créer la forme
                center = ((x + x_end) // 2, (y + y_end) // 2)
                size = grid_size / 2
                
                if shape_type == PolygonType.TRIANGLE:
                    polygon = self.shape_gen.create_triangle(center, size)
                elif shape_type == PolygonType.SQUARE:
                    polygon = self.shape_gen.create_square(center, size)
                elif shape_type == PolygonType.RECTANGLE:
                    polygon = self.shape_gen.create_rectangle(center, size, size * 0.7)
                elif shape_type == PolygonType.HEXAGON:
                    polygon = self.shape_gen.create_hexagon(center, size)
                else:  # CIRCLE
                    polygon = self.shape_gen.create_circle(center, size)
                
                # Dessiner la forme
                cv2.drawContours(output, [polygon], 0, mean_color, -1)
                cv2.drawContours(output, [polygon], 0, (0, 0, 0), 1)
        
        # Rapport des formes utilisées
        total_shapes = sum(shapes_used.values())
        if total_shapes > 0:
            print("\n📊 Formes géométriques utilisées:")
            for shape_type, count in sorted(shapes_used.items()):
                if count > 0:
                    percentage = (count / total_shapes) * 100
                    print(f"  {shape_type:12} : {count:4} cellules ({percentage:5.1f}%)")
        
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return Image.fromarray(output_rgb)


def test_hybrid_generation():
    """Teste la génération hybride"""
    input_path = "data/input/test1.jpg"
    
    print("🎨 Génération LOW POLY HYBRID (formes mixtes)...\n")
    
    # Sans mélange (triangles uniquement)
    print("1️⃣  Mode TRIANGLES UNIQUEMENT:")
    gen = HybridLowPolyGenerator(input_path, enable_shape_mixing=False)
    img_triangles = gen.generate_hybrid(grid_size=25)
    img_triangles.save("data/output/hybrid_triangles_only.png")
    print("   ✅ Sauvegardé: hybrid_triangles_only.png\n")
    
    # Avec mélange (formes adaptées)
    print("2️⃣  Mode HYBRID (formes adaptées):")
    gen = HybridLowPolyGenerator(input_path, enable_shape_mixing=True)
    img_hybrid = gen.generate_hybrid(grid_size=25)
    img_hybrid.save("data/output/hybrid_mixed_shapes.png")
    print("   ✅ Sauvegardé: hybrid_mixed_shapes.png\n")
    
    print("✨ Comparaison générique 📊")
    print("   - hybrid_triangles_only.png : Tous les triangles")
    print("   - hybrid_mixed_shapes.png   : Formes adaptées par zone")


if __name__ == "__main__":
    test_hybrid_generation()
