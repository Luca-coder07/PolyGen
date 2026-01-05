"""
Module principal pour la génération d'images low poly
"""
import cv2
import numpy as np
from scipy.spatial import Delaunay
from PIL import Image
import os


class LowPolyGenerator:
    """Classe principale pour convertir une image en style low poly cartoon"""
    
    def __init__(self, image_path: str, num_points: int = 1000, blur_strength: int = 15):
        """
        Initialise le générateur low poly
        
        Args:
            image_path: Chemin vers l'image d'entrée
            num_points: Nombre de points pour la triangulation (plus élevé = plus de détails)
            blur_strength: Force du flou pour lisser l'image (doit être impair)
        """
        self.image_path = image_path
        self.num_points = num_points
        self.blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
        
        # Charger l'image
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
        
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width = self.image.shape[:2]
        
    def detect_edges(self) -> np.ndarray:
        """
        Détecte les contours de l'image pour identifier les zones importantes
        
        Returns:
            Image des contours détectés
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges
    
    def generate_points(self, use_edges: bool = True) -> np.ndarray:
        """
        Génère les points pour la triangulation
        Combine points aléatoires et points basés sur les contours
        
        Args:
            use_edges: Si True, priorise les points sur les contours
            
        Returns:
            Array de points [x, y]
        """
        points = []
        
        # Ajouter les coins de l'image (important pour la triangulation)
        points.extend([
            [0, 0],
            [self.width - 1, 0],
            [0, self.height - 1],
            [self.width - 1, self.height - 1]
        ])
        
        if use_edges:
            # Déterminer les contours
            edges = self.detect_edges()
            
            # Trouver les pixels de contour
            edge_points = np.argwhere(edges > 0)  # Returns [y, x]
            
            # Garder ~30% des points détectés sur les contours
            if len(edge_points) > 0:
                edge_sample = np.random.choice(len(edge_points), 
                                             min(int(self.num_points * 0.3), len(edge_points)), 
                                             replace=False)
                for idx in edge_sample:
                    y, x = edge_points[idx]
                    points.append([x, y])
        
        # Ajouter des points aléatoires pour compléter
        num_random = max(0, self.num_points - len(points))
        random_points = np.random.rand(num_random, 2)
        random_points[:, 0] *= self.width
        random_points[:, 1] *= self.height
        points.extend(random_points.tolist())
        
        return np.array(points, dtype=np.float32)
    
    def triangulate(self, points: np.ndarray) -> Delaunay:
        """
        Crée une triangulation de Delaunay à partir des points
        
        Args:
            points: Array de points [x, y]
            
        Returns:
            Objet Delaunay contenant la triangulation
        """
        return Delaunay(points)
    
    def get_triangle_color(self, triangle_indices: np.ndarray, points: np.ndarray) -> tuple:
        """
        Calcule la couleur moyenne d'un triangle
        
        Args:
            triangle_indices: Indices des 3 points du triangle
            points: Array des points
            
        Returns:
            Tuple RGB (r, g, b)
        """
        # Obtenir les coordonnées du triangle
        tri_points = points[triangle_indices].astype(np.int32)
        
        # Créer un masque du triangle
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        cv2.drawContours(mask, [tri_points], 0, 255, -1)
        
        # Calculer la couleur moyenne dans le triangle
        colors = self.image_rgb[mask > 0]
        if len(colors) > 0:
            mean_color = np.mean(colors, axis=0).astype(np.uint8)
            return tuple(mean_color)
        else:
            return (128, 128, 128)  # Gris par défaut
    
    def smooth_image(self) -> np.ndarray:
        """
        Applique un flou pour lisser les couleurs
        
        Returns:
            Image lissée
        """
        return cv2.GaussianBlur(self.image_rgb, 
                               (self.blur_strength, self.blur_strength), 0)
    
    def generate(self, use_edge_detection: bool = True, add_outlines: bool = True) -> Image.Image:
        """
        Génère l'image low poly cartoon
        
        Args:
            use_edge_detection: Si True, détecte les contours pour améliorer les détails
            add_outlines: Si True, dessine les contours des triangles
            
        Returns:
            Image PIL de l'image low poly
        """
        # Lisser l'image pour réduire le bruit
        smoothed = self.smooth_image()
        
        # Générer les points
        points = self.generate_points(use_edges=use_edge_detection)
        
        # Triangulation
        tri = self.triangulate(points)
        
        # Créer l'image de sortie
        output = np.zeros_like(smoothed)
        
        # Dessiner chaque triangle
        for triangle_indices in tri.simplices:
            # Obtenir les points du triangle
            tri_points = points[triangle_indices].astype(np.int32)
            
            # Calculer la couleur moyenne
            color = self.get_triangle_color(triangle_indices, points)
            
            # Remplir le triangle avec la couleur
            cv2.drawContours(output, [tri_points], 0, color, -1)
            
            # Ajouter les contours si demandé
            if add_outlines:
                cv2.drawContours(output, [tri_points], 0, (0, 0, 0), 1)
        
        # Convertir en image PIL
        output_pil = Image.fromarray(output)
        return output_pil
    
    def save(self, output_path: str, image: Image.Image = None) -> None:
        """
        Sauvegarde l'image low poly
        
        Args:
            output_path: Chemin de sortie
            image: Image à sauvegarder (si None, génère une nouvelle image)
        """
        if image is None:
            image = self.generate()
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        image.save(output_path)
        print(f"Image sauvegardée: {output_path}")


def process_image(input_path: str, output_path: str, num_points: int = 1000, 
                 blur_strength: int = 15, add_outlines: bool = True) -> None:
    """
    Fonction utilitaire pour traiter une image en low poly
    
    Args:
        input_path: Chemin de l'image d'entrée
        output_path: Chemin de l'image de sortie
        num_points: Nombre de points pour la triangulation
        blur_strength: Force du flou
        add_outlines: Ajouter les contours des triangles
    """
    generator = LowPolyGenerator(input_path, num_points, blur_strength)
    image = generator.generate(use_edge_detection=True, add_outlines=add_outlines)
    generator.save(output_path, image)
