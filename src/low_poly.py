"""
Module principal pour la génération d'images low poly
Version améliorée avec meilleure détection de contours et traitement des couleurs
"""
import cv2
import numpy as np
from scipy.spatial import Delaunay
from PIL import Image
import os


class LowPolyGenerator:
    """Classe principale pour convertir une image en style low poly cartoon"""
    
    def __init__(self, image_path: str, num_points: int = 1000, blur_strength: int = 15,
                 enhance_colors: bool = True, edge_sensitivity: int = 2):
        """
        Initialise le générateur low poly
        
        Args:
            image_path: Chemin vers l'image d'entrée
            num_points: Nombre de points pour la triangulation (plus élevé = plus de détails)
            blur_strength: Force du flou pour lisser l'image (doit être impair)
            enhance_colors: Si True, augmente la saturation et le contraste
            edge_sensitivity: Sensibilité de détection des contours (1-5)
        """
        self.image_path = image_path
        self.num_points = num_points
        self.blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
        self.enhance_colors = enhance_colors
        self.edge_sensitivity = max(1, min(5, edge_sensitivity))
        
        # Charger l'image
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
        
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width = self.image.shape[:2]
        
    def detect_edges(self) -> np.ndarray:
        """
        Détecte les contours de l'image avec une meilleure sensibilité
        Utilise une combinaison de techniques pour une meilleure détection
        
        Returns:
            Image des contours détectés
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Appliquer CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # pour améliorer le contraste local
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray_enhanced = clahe.apply(gray)
        
        # Adapter les seuils Canny selon la sensibilité
        low_threshold = max(30, 100 - (self.edge_sensitivity * 15))
        high_threshold = min(200, 200 - (self.edge_sensitivity * 20))
        
        edges = cv2.Canny(gray_enhanced, low_threshold, high_threshold)
        
        # Appliquer une dilatation légère pour épaissir les contours
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def enhance_color_image(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Améliore la saturation et le contraste de l'image
        
        Args:
            image_rgb: Image en RGB
            
        Returns:
            Image améliorée
        """
        # Convertir en HSV pour manipuler la saturation
        hsv = cv2.cvtColor(cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Augmenter la saturation (canal S)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        
        # Augmenter légèrement la luminosité (canal V)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
        
        # Convertir back to RGB
        hsv = hsv.astype(np.uint8)
        enhanced_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)
        
        return enhanced_rgb
    
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
            
            # Garder ~40% des points détectés sur les contours (augmenté de 30%)
            if len(edge_points) > 0:
                edge_ratio = min(0.4, max(0.2, 0.4 - (self.edge_sensitivity - 1) * 0.05))
                num_edge_points = min(int(self.num_points * edge_ratio), len(edge_points))
                edge_sample = np.random.choice(len(edge_points), num_edge_points, replace=False)
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
    
    def get_triangle_color(self, triangle_indices: np.ndarray, points: np.ndarray,
                          base_image: np.ndarray) -> tuple:
        """
        Calcule la couleur moyenne d'un triangle
        
        Args:
            triangle_indices: Indices des 3 points du triangle
            points: Array des points
            base_image: Image de base en BGR pour le sampling
            
        Returns:
            Tuple BGR (b, g, r) - format OpenCV
        """
        # Obtenir les coordonnées du triangle
        tri_points = points[triangle_indices].astype(np.int32)
        
        # Créer un masque du triangle
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        cv2.drawContours(mask, [tri_points], 0, 255, -1)
        
        # Calculer la couleur moyenne dans le triangle
        colors = base_image[mask > 0]
        if len(colors) > 0:
            mean_color = np.mean(colors, axis=0).astype(int)
            # Retourner en tuple pour OpenCV
            return (int(mean_color[0]), int(mean_color[1]), int(mean_color[2]))
        else:
            return (128, 128, 128)  # Gris par défaut
    
    def smooth_image(self) -> np.ndarray:
        """
        Applique un flou gaussien pour lisser les couleurs
        
        Returns:
            Image lissée en BGR
        """
        return cv2.GaussianBlur(self.image, 
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
        
        # Améliorer les couleurs si demandé
        if self.enhance_colors:
            smoothed_rgb = cv2.cvtColor(smoothed, cv2.COLOR_BGR2RGB)
            smoothed_rgb = self.enhance_color_image(smoothed_rgb)
            smoothed = cv2.cvtColor(smoothed_rgb, cv2.COLOR_RGB2BGR)
        
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
            color = self.get_triangle_color(triangle_indices, points, smoothed)
            
            # Remplir le triangle avec la couleur
            cv2.drawContours(output, [tri_points], 0, color, -1)
            
            # Ajouter les contours si demandé
            if add_outlines:
                cv2.drawContours(output, [tri_points], 0, (0, 0, 0), 2)
        
        # Convertir en image PIL
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        output_pil = Image.fromarray(output_rgb)
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
                 blur_strength: int = 15, add_outlines: bool = True,
                 enhance_colors: bool = True, edge_sensitivity: int = 2) -> None:
    """
    Fonction utilitaire pour traiter une image en low poly
    
    Args:
        input_path: Chemin de l'image d'entrée
        output_path: Chemin de l'image de sortie
        num_points: Nombre de points pour la triangulation
        blur_strength: Force du flou
        add_outlines: Ajouter les contours des triangles
        enhance_colors: Augmenter la saturation et le contraste
        edge_sensitivity: Sensibilité de détection des contours (1-5)
    """
    generator = LowPolyGenerator(input_path, num_points, blur_strength, 
                                enhance_colors, edge_sensitivity)
    image = generator.generate(use_edge_detection=True, add_outlines=add_outlines)
    generator.save(output_path, image)
