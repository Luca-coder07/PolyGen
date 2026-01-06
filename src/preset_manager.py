"""
Gestion des presets - Permet de sauvegarder et charger des configurations personnalisées
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Preset:
    """Représente un preset de configuration"""
    name: str
    description: str = ""
    mode: str = "classic"  # "classic" ou "hybrid"
    
    # Paramètres classiques
    points: int = 1000
    blur_strength: int = 18
    edge_sensitivity: int = 2
    enhance_colors: bool = True
    add_outlines: bool = True
    
    # Paramètres hybrides
    grid_size: int = 25
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> "Preset":
        """Crée un preset depuis un dictionnaire"""
        return Preset(**data)
    
    def __str__(self) -> str:
        """Représentation textuelle"""
        mode_str = "HYBRIDE" if self.mode == "hybrid" else "CLASSIQUE"
        if self.mode == "hybrid":
            return f"{self.name:15} | {mode_str:8} | grid={self.grid_size}px | {self.description}"
        else:
            return f"{self.name:15} | {mode_str:8} | pts={self.points} blur={self.blur_strength} | {self.description}"


class PresetManager:
    """Gestionnaire de presets"""
    
    # Dossier de configuration par défaut
    DEFAULT_CONFIG_DIR = Path.home() / ".polygen"
    PRESETS_FILE = "presets.json"
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialise le gestionnaire de presets
        
        Args:
            config_dir: Dossier de configuration (par défaut: ~/.polygen)
        """
        self.config_dir = config_dir or self.DEFAULT_CONFIG_DIR
        self.presets_path = self.config_dir / self.PRESETS_FILE
        self.presets: Dict[str, Preset] = {}
        
        # Créer le dossier s'il n'existe pas
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Charger les presets existants
        self._load_presets()
        
        # Créer les presets par défaut s'ils n'existent pas
        if not self.presets:
            self._create_default_presets()
    
    def _create_default_presets(self):
        """Crée les presets par défaut"""
        defaults = [
            Preset(
                name="Équilibré",
                description="Rendu équilibré - recommandé pour la plupart des images",
                mode="classic",
                points=1000,
                blur_strength=18,
                edge_sensitivity=2,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Artistique",
                description="Style artistique - lisse et abstrait",
                mode="classic",
                points=800,
                blur_strength=25,
                edge_sensitivity=1,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Détaillé",
                description="Haute fidélité - préserve les détails",
                mode="classic",
                points=1800,
                blur_strength=12,
                edge_sensitivity=3,
                enhance_colors=True,
                add_outlines=False
            ),
            Preset(
                name="Expressif",
                description="Cartoon expressif - contours prononcés",
                mode="classic",
                points=1200,
                blur_strength=20,
                edge_sensitivity=3,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Minimaliste",
                description="Très abstrait - formes minimales",
                mode="classic",
                points=500,
                blur_strength=28,
                edge_sensitivity=1,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Hybride Équilibré",
                description="Formes mixtes - rendu naturel et efficace",
                mode="hybrid",
                grid_size=25,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Hybride Détaillé",
                description="Formes mixtes - haute résolution",
                mode="hybrid",
                grid_size=15,
                enhance_colors=True,
                add_outlines=True
            ),
            Preset(
                name="Hybride Minimaliste",
                description="Formes mixtes - très abstrait",
                mode="hybrid",
                grid_size=35,
                enhance_colors=True,
                add_outlines=True
            ),
        ]
        
        for preset in defaults:
            self.presets[preset.name] = preset
        
        self.save_all()
    
    def _load_presets(self):
        """Charge les presets depuis le fichier"""
        if self.presets_path.exists():
            try:
                with open(self.presets_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.presets = {
                        name: Preset.from_dict(preset_data)
                        for name, preset_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"⚠️  Erreur en chargeant les presets: {e}")
                self.presets = {}
    
    def save_all(self):
        """Sauvegarde tous les presets dans le fichier"""
        try:
            data = {
                name: preset.to_dict()
                for name, preset in self.presets.items()
            }
            
            with open(self.presets_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Impossible de sauvegarder les presets: {e}")
    
    def save_preset(self, preset: Preset) -> bool:
        """
        Sauvegarde un preset
        
        Args:
            preset: Le preset à sauvegarder
        
        Returns:
            True si succès, False sinon
        """
        try:
            self.presets[preset.name] = preset
            self.save_all()
            return True
        except Exception as e:
            print(f"❌ Erreur en sauvegardant le preset: {e}")
            return False
    
    def load_preset(self, name: str) -> Optional[Preset]:
        """
        Charge un preset par nom
        
        Args:
            name: Nom du preset
        
        Returns:
            Le preset ou None s'il n'existe pas
        """
        return self.presets.get(name)
    
    def delete_preset(self, name: str) -> bool:
        """
        Supprime un preset
        
        Args:
            name: Nom du preset
        
        Returns:
            True si succès, False sinon
        """
        if name not in self.presets:
            print(f"❌ Preset '{name}' n'existe pas")
            return False
        
        # Empêcher la suppression des presets par défaut
        default_names = {"Équilibré", "Artistique", "Détaillé", "Expressif", "Minimaliste",
                        "Hybride Équilibré", "Hybride Détaillé", "Hybride Minimaliste"}
        if name in default_names:
            print(f"⚠️  Cannot delete default preset '{name}'")
            return False
        
        try:
            del self.presets[name]
            self.save_all()
            return True
        except Exception as e:
            print(f"❌ Erreur en supprimant le preset: {e}")
            return False
    
    def rename_preset(self, old_name: str, new_name: str) -> bool:
        """
        Renomme un preset
        
        Args:
            old_name: Ancien nom
            new_name: Nouveau nom
        
        Returns:
            True si succès, False sinon
        """
        if old_name not in self.presets:
            print(f"❌ Preset '{old_name}' n'existe pas")
            return False
        
        if new_name in self.presets:
            print(f"❌ Un preset nommé '{new_name}' existe déjà")
            return False
        
        try:
            preset = self.presets[old_name]
            preset.name = new_name
            self.presets[new_name] = preset
            del self.presets[old_name]
            self.save_all()
            return True
        except Exception as e:
            print(f"❌ Erreur en renommant le preset: {e}")
            return False
    
    def list_presets(self) -> List[Preset]:
        """
        Liste tous les presets
        
        Returns:
            Liste des presets
        """
        return sorted(self.presets.values(), key=lambda p: p.name)
    
    def get_all_names(self) -> List[str]:
        """
        Obtient tous les noms de presets
        
        Returns:
            Liste des noms
        """
        return sorted(self.presets.keys())
    
    def export_preset(self, name: str, export_path: Path) -> bool:
        """
        Exporte un preset dans un fichier
        
        Args:
            name: Nom du preset
            export_path: Chemin du fichier de sortie
        
        Returns:
            True si succès, False sinon
        """
        preset = self.load_preset(name)
        if not preset:
            print(f"❌ Preset '{name}' n'existe pas")
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(preset.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"❌ Erreur en exportant le preset: {e}")
            return False
    
    def import_preset(self, import_path: Path) -> bool:
        """
        Importe un preset depuis un fichier
        
        Args:
            import_path: Chemin du fichier d'import
        
        Returns:
            True si succès, False sinon
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                preset = Preset.from_dict(data)
                return self.save_preset(preset)
        except (IOError, json.JSONDecodeError, TypeError) as e:
            print(f"❌ Erreur en important le preset: {e}")
            return False
    
    def print_summary(self):
        """Affiche un résumé des presets"""
        presets = self.list_presets()
        
        print("\n" + "="*80)
        print("📋 PRESETS DISPONIBLES")
        print("="*80)
        
        classic_presets = [p for p in presets if p.mode == "classic"]
        hybrid_presets = [p for p in presets if p.mode == "hybrid"]
        
        if classic_presets:
            print("\n🎨 MODE CLASSIQUE:")
            for preset in classic_presets:
                print(f"  {preset}")
        
        if hybrid_presets:
            print("\n🔷 MODE HYBRIDE:")
            for preset in hybrid_presets:
                print(f"  {preset}")
        
        print("="*80 + "\n")
    
    def get_config_dir(self) -> Path:
        """Retourne le dossier de configuration"""
        return self.config_dir


# Instance globale du gestionnaire
_preset_manager: Optional[PresetManager] = None


def get_preset_manager() -> PresetManager:
    """Obtient l'instance globale du gestionnaire de presets"""
    global _preset_manager
    if _preset_manager is None:
        _preset_manager = PresetManager()
    return _preset_manager


def print_presets():
    """Affiche les presets disponibles"""
    manager = get_preset_manager()
    manager.print_summary()


if __name__ == "__main__":
    # Test du module
    manager = PresetManager()
    
    print("\n✅ Presets chargés:")
    manager.print_summary()
    
    # Créer un preset personnalisé
    print("\n📝 Création d'un preset personnalisé...")
    custom = Preset(
        name="Ma Configuration",
        description="Un preset personnalisé",
        mode="classic",
        points=1500,
        blur_strength=22
    )
    manager.save_preset(custom)
    
    print("✅ Preset sauvegardé!")
    print("\n📋 Presets après ajout:")
    manager.print_summary()
    
    # Charger le preset personnalisé
    loaded = manager.load_preset("Ma Configuration")
    if loaded:
        print(f"✅ Preset chargé: {loaded}")
