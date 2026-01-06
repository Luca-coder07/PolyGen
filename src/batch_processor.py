"""
Module de traitement par lots (batch processing)
Permet de traiter plusieurs images en une seule commande
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import time
from src.low_poly import LowPolyGenerator
from src.advanced_shapes import HybridLowPolyGenerator


@dataclass
class BatchConfig:
    """Configuration pour le traitement par lots"""
    input_dir: str
    output_dir: str
    num_points: int = 1000
    blur_strength: int = 18
    edge_sensitivity: int = 2
    enhance_colors: bool = True
    add_outlines: bool = True
    hybrid_mode: bool = False
    grid_size: int = 25
    file_extensions: tuple = (".jpg", ".jpeg", ".png", ".bmp")
    parallel: bool = False  # Possibilité future pour traitement parallèle


@dataclass
class ProcessResult:
    """Résultat du traitement d'une image"""
    input_file: str
    output_file: str
    success: bool
    error_message: Optional[str] = None
    processing_time: float = 0.0
    file_size_input: int = 0
    file_size_output: int = 0


class BatchProcessor:
    """Processeur d'images par lots"""
    
    def __init__(self, config: BatchConfig):
        """
        Initialise le processeur batch
        
        Args:
            config: Configuration BatchConfig
        """
        self.config = config
        self.results: List[ProcessResult] = []
        self._validate_config()
    
    def _validate_config(self):
        """Valide la configuration"""
        input_path = Path(self.config.input_dir)
        if not input_path.exists():
            raise ValueError(f"Dossier d'entrée n'existe pas: {self.config.input_dir}")
        
        if not input_path.is_dir():
            raise ValueError(f"Le chemin d'entrée n'est pas un dossier: {self.config.input_dir}")
        
        # Créer le dossier de sortie s'il n'existe pas
        output_path = Path(self.config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    def find_images(self) -> List[Path]:
        """
        Trouve toutes les images dans le dossier d'entrée
        
        Returns:
            Liste des chemins d'images
        """
        input_path = Path(self.config.input_dir)
        images = []
        
        for ext in self.config.file_extensions:
            # Recherche récursive
            images.extend(input_path.rglob(f"*{ext}"))
            images.extend(input_path.rglob(f"*{ext.upper()}"))
        
        # Retirer les doublons
        images = list(set(images))
        images.sort()
        
        return images
    
    def process_batch(self, progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[ProcessResult]:
        """
        Traite toutes les images du dossier d'entrée
        
        Args:
            progress_callback: Fonction optionnelle pour rapporter la progression
                              signature: (current: int, total: int, message: str)
        
        Returns:
            Liste des résultats de traitement
        """
        images = self.find_images()
        total = len(images)
        
        if total == 0:
            print("⚠️  Aucune image trouvée dans le dossier d'entrée")
            return []
        
        print(f"\n📦 Traitement par lots")
        print(f"📂 Dossier entrée: {self.config.input_dir}")
        print(f"📂 Dossier sortie: {self.config.output_dir}")
        print(f"🖼️  Images trouvées: {total}")
        if self.config.hybrid_mode:
            print(f"🎨 Mode: HYBRIDE (grid_size={self.config.grid_size}px)")
        else:
            print(f"🎨 Mode: CLASSIQUE (points={self.config.num_points}, blur={self.config.blur_strength})")
        print()
        
        self.results = []
        
        for index, image_path in enumerate(images, 1):
            try:
                if progress_callback:
                    progress_callback(index, total, f"Traitement: {image_path.name}")
                
                result = self._process_single_image(image_path)
                self.results.append(result)
                
                # Afficher le statut
                status = "✅" if result.success else "❌"
                print(f"{status} [{index:3d}/{total}] {image_path.name}")
                if not result.success:
                    print(f"      Erreur: {result.error_message}")
                
            except Exception as e:
                result = ProcessResult(
                    input_file=str(image_path),
                    output_file="",
                    success=False,
                    error_message=str(e)
                )
                self.results.append(result)
                print(f"❌ [{index:3d}/{total}] {image_path.name}")
                print(f"      Erreur: {str(e)[:100]}")
        
        return self.results
    
    def _process_single_image(self, image_path: Path) -> ProcessResult:
        """
        Traite une seule image
        
        Args:
            image_path: Chemin vers l'image
        
        Returns:
            ProcessResult avec les détails du traitement
        """
        start_time = time.time()
        input_file_str = str(image_path)
        
        try:
            # Déterminer le nom de fichier de sortie
            output_filename = image_path.stem + "_polygen.png"
            output_path = Path(self.config.output_dir) / output_filename
            output_file_str = str(output_path)
            
            # Récupérer les tailles de fichiers
            file_size_input = image_path.stat().st_size
            
            # Traitement
            if self.config.hybrid_mode:
                generator = HybridLowPolyGenerator(
                    input_file_str,
                    enable_shape_mixing=True
                )
                output_image = generator.generate_hybrid(grid_size=self.config.grid_size)
            else:
                generator = LowPolyGenerator(
                    input_file_str,
                    num_points=self.config.num_points,
                    blur_strength=self.config.blur_strength,
                    enhance_colors=self.config.enhance_colors,
                    edge_sensitivity=self.config.edge_sensitivity
                )
                output_image = generator.generate(
                    use_edge_detection=True,
                    add_outlines=self.config.add_outlines
                )
            
            # Sauvegarder
            output_image.save(output_file_str)
            file_size_output = Path(output_file_str).stat().st_size
            
            processing_time = time.time() - start_time
            
            return ProcessResult(
                input_file=input_file_str,
                output_file=output_file_str,
                success=True,
                processing_time=processing_time,
                file_size_input=file_size_input,
                file_size_output=file_size_output
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessResult(
                input_file=input_file_str,
                output_file="",
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
    
    def print_summary(self):
        """Affiche un résumé des résultats"""
        if not self.results:
            return
        
        successful = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        total = len(self.results)
        total_time = sum(r.processing_time for r in self.results)
        total_input_size = sum(r.file_size_input for r in self.results)
        total_output_size = sum(r.file_size_output for r in self.results)
        
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DU TRAITEMENT PAR LOTS")
        print("="*70)
        print(f"Total des images:       {total}")
        print(f"Réussies:              ✅ {successful}")
        print(f"Échouées:              ❌ {failed}")
        print(f"Taux de réussite:      {(successful/total)*100:.1f}%")
        print(f"\nTemps total:           {total_time:.2f}s")
        print(f"Temps moyen/image:     {total_time/total:.2f}s")
        if total > 0:
            print(f"\nTaille entrée totale:  {self._format_size(total_input_size)}")
            print(f"Taille sortie totale:  {self._format_size(total_output_size)}")
            if total_input_size > 0:
                compression = ((total_input_size - total_output_size) / total_input_size) * 100
                print(f"Compression:           {compression:+.1f}%")
        print("="*70 + "\n")
    
    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """Formate une taille de fichier en unité lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f}{unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f}TB"


def batch_process_cli(
    input_dir: str,
    output_dir: str,
    hybrid: bool = False,
    grid_size: int = 25,
    num_points: int = 1000,
    blur_strength: int = 18,
    sensitivity: int = 2,
    enhance: bool = True,
    outlines: bool = True
) -> int:
    """
    Fonction CLI wrapper pour le traitement par lots
    
    Args:
        input_dir: Dossier d'entrée
        output_dir: Dossier de sortie
        hybrid: Utiliser le mode hybride
        grid_size: Taille de grille (mode hybride)
        num_points: Nombre de points (mode classique)
        blur_strength: Force du flou (mode classique)
        sensitivity: Sensibilité des contours (mode classique)
        enhance: Améliorer les couleurs (mode classique)
        outlines: Afficher les contours (mode classique)
    
    Returns:
        Code de retour (0 = succès, 1 = erreur)
    """
    try:
        config = BatchConfig(
            input_dir=input_dir,
            output_dir=output_dir,
            hybrid_mode=hybrid,
            grid_size=grid_size,
            num_points=num_points,
            blur_strength=blur_strength,
            edge_sensitivity=sensitivity,
            enhance_colors=enhance,
            add_outlines=outlines
        )
        
        processor = BatchProcessor(config)
        results = processor.process_batch()
        processor.print_summary()
        
        # Retourner 0 si au moins une image a été traitée avec succès
        successful = sum(1 for r in results if r.success)
        return 0 if successful > 0 else 1
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
