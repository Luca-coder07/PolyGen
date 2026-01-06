"""
Module pour l'export SVG vectoriel des images low poly
"""
import numpy as np
from scipy.spatial import Delaunay
import xml.etree.ElementTree as ET
from xml.dom import minidom


class SVGExporter:
    """Exporte une triangulation en fichier SVG vectoriel"""
    
    def __init__(self, width: int, height: int):
        """
        Initialise l'exporteur SVG
        
        Args:
            width: Largeur de l'image
            height: Hauteur de l'image
        """
        self.width = width
        self.height = height
        self.root = ET.Element('svg')
        self.root.set('xmlns', 'http://www.w3.org/2000/svg')
        self.root.set('width', str(width))
        self.root.set('height', str(height))
        self.root.set('viewBox', f'0 0 {width} {height}')
    
    def add_triangle(self, points: np.ndarray, color: tuple, outline: tuple = None, 
                    outline_width: float = 1):
        """
        Ajoute un triangle au SVG
        
        Args:
            points: Array de 3 points [x, y]
            color: Couleur de remplissage (R, G, B) ou (B, G, R) selon le format
            outline: Couleur du contour
            outline_width: Épaisseur du contour
        """
        polygon = ET.SubElement(self.root, 'polygon')
        
        # Format les points en chaîne "x1,y1 x2,y2 x3,y3"
        points_str = ' '.join([f'{int(p[0])},{int(p[1])}' for p in points])
        polygon.set('points', points_str)
        
        # Couleur de remplissage (supposé BGR, convertir en RGB pour SVG)
        fill_color = self._format_color(color)
        polygon.set('fill', fill_color)
        
        # Contour
        if outline:
            outline_color = self._format_color(outline)
            polygon.set('stroke', outline_color)
            polygon.set('stroke-width', str(outline_width))
        else:
            polygon.set('stroke', 'none')
    
    def _format_color(self, rgb_tuple: tuple) -> str:
        """
        Convertit un tuple RGB en format hex SVG
        
        Args:
            rgb_tuple: Tuple (R, G, B) ou (B, G, R)
            
        Returns:
            Chaîne hex #RRGGBB
        """
        # Supposer BGR (format OpenCV)
        b, g, r = rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def save(self, file_path: str, pretty: bool = True):
        """
        Sauvegarde le SVG dans un fichier
        
        Args:
            file_path: Chemin du fichier de sortie
            pretty: Si True, formate le SVG de manière lisible
        """
        # Convertir en chaîne
        svg_str = ET.tostring(self.root, encoding='unicode')
        
        if pretty:
            # Parser et reformater pour lisibilité
            dom = minidom.parseString(svg_str)
            svg_str = dom.toprettyxml(indent='  ')
            # Retirer la déclaration XML auto-ajoutée
            svg_str = '\n'.join(svg_str.split('\n')[1:])
        
        with open(file_path, 'w') as f:
            f.write(svg_str)


def generate_svg(image_path: str, output_path: str, num_points: int = 1000,
                blur_strength: int = 18, edge_sensitivity: int = 2,
                add_outlines: bool = True, enhance_colors: bool = True):
    """
    Génère un SVG à partir d'une image
    
    Args:
        image_path: Chemin vers l'image source
        output_path: Chemin de sortie SVG
        num_points: Nombre de points de triangulation
        blur_strength: Force du flou
        edge_sensitivity: Sensibilité de détection de contours
        add_outlines: Ajouter les contours noirs
        enhance_colors: Améliorer les couleurs
    """
    import cv2
    from src.low_poly import LowPolyGenerator
    
    # Charger l'image et générer la triangulation
    generator = LowPolyGenerator(image_path, num_points, blur_strength,
                               enhance_colors, edge_sensitivity)
    
    # Préparer l'image pour l'analyse
    smoothed = generator.smooth_image()
    if enhance_colors:
        smoothed_rgb = cv2.cvtColor(smoothed, cv2.COLOR_BGR2RGB)
        smoothed_rgb = generator.enhance_color_image(smoothed_rgb)
        smoothed = cv2.cvtColor(smoothed_rgb, cv2.COLOR_RGB2BGR)
    
    # Générer les points et triangulation
    points = generator.generate_points(use_edges=True)
    tri = generator.triangulate(points)
    
    # Créer l'exporteur SVG
    exporter = SVGExporter(generator.width, generator.height)
    
    # Ajouter chaque triangle
    for triangle_indices in tri.simplices:
        # Coordonnées des points du triangle
        tri_points = points[triangle_indices]
        
        # Couleur moyenne
        color = generator.get_triangle_color(triangle_indices, points, smoothed)
        
        # Contour
        outline = (0, 0, 0) if add_outlines else None
        outline_width = 1 if add_outlines else 0
        
        # Ajouter au SVG
        exporter.add_triangle(tri_points, color, outline, outline_width)
    
    # Sauvegarder
    exporter.save(output_path)
    print(f"SVG généré: {output_path}")


if __name__ == "__main__":
    # Exemple d'utilisation
    generate_svg("data/input/test1.jpg", "data/output/test1_output.svg", 
                num_points=1000, blur_strength=18)
