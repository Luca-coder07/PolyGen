"""
Interface GUI interactive pour PolyGen
Permet de visualiser en temps réel les paramètres et générer des images
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import os
from pathlib import Path
from src.low_poly import LowPolyGenerator
from src.advanced_shapes import HybridLowPolyGenerator


class PolyGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PolyGen - Low Poly Cartoon Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.current_image_path = None
        self.generator = None
        self.is_generating = False
        
        # Créer l'interface
        self.create_widgets()
        
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Section Chargement ===
        load_frame = ttk.LabelFrame(main_frame, text="📂 Chargement d'image", padding="10")
        load_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.path_var = tk.StringVar(value="Aucune image sélectionnée")
        self.path_label = ttk.Label(load_frame, textvariable=self.path_var, foreground="gray")
        self.path_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(load_frame, text="Ouvrir une image", command=self.load_image).grid(row=0, column=1, padx=5)
        
        # === Section Paramètres ===
        params_frame = ttk.LabelFrame(main_frame, text="⚙️ Paramètres", padding="10")
        params_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Points
        ttk.Label(params_frame, text="Points (triangles):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.points_var = tk.IntVar(value=1000)
        self.points_scale = ttk.Scale(params_frame, from_=200, to=2000, orient=tk.HORIZONTAL,
                                     variable=self.points_var, command=self.update_points_label)
        self.points_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.points_label = ttk.Label(params_frame, text="1000", width=5)
        self.points_label.grid(row=0, column=2)
        
        # Blur
        ttk.Label(params_frame, text="Flou:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.blur_var = tk.IntVar(value=18)
        self.blur_scale = ttk.Scale(params_frame, from_=5, to=35, orient=tk.HORIZONTAL,
                                   variable=self.blur_var, command=self.update_blur_label)
        self.blur_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        self.blur_label = ttk.Label(params_frame, text="18", width=5)
        self.blur_label.grid(row=1, column=2)
        
        # Sensibilité
        ttk.Label(params_frame, text="Sensibilité contours:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sensitivity_var = tk.IntVar(value=2)
        self.sensitivity_scale = ttk.Scale(params_frame, from_=1, to=5, orient=tk.HORIZONTAL,
                                          variable=self.sensitivity_var, command=self.update_sensitivity_label)
        self.sensitivity_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        self.sensitivity_label = ttk.Label(params_frame, text="2", width=5)
        self.sensitivity_label.grid(row=2, column=2)
        
        # Options
        ttk.Label(params_frame, text="Options:").grid(row=3, column=0, sticky=tk.W, pady=10)
        
        self.outlines_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Afficher contours", variable=self.outlines_var).grid(row=3, column=1, sticky=tk.W)
        
        self.enhance_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Améliorer couleurs", variable=self.enhance_var).grid(row=4, column=1, sticky=tk.W)
        
        self.hybrid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(params_frame, text="Mode Hybride (formes mixtes)", variable=self.hybrid_var, 
                       command=self.toggle_hybrid_options).grid(row=5, column=1, sticky=tk.W)
        
        # Grid Size (pour mode hybride)
        ttk.Label(params_frame, text="Taille grille (hybride):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.grid_size_var = tk.IntVar(value=25)
        self.grid_size_scale = ttk.Scale(params_frame, from_=10, to=50, orient=tk.HORIZONTAL,
                                        variable=self.grid_size_var, command=self.update_grid_size_label)
        self.grid_size_scale.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=5)
        self.grid_size_label = ttk.Label(params_frame, text="25", width=5)
        self.grid_size_label.grid(row=6, column=2)
        self.grid_size_scale.config(state=tk.DISABLED)  # Désactivé par défaut
        
        # === Section Presets ===
        preset_frame = ttk.LabelFrame(main_frame, text="🎨 Presets", padding="10")
        preset_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        presets = [
            ("Équilibré", {"points": 1000, "blur": 18, "sensitivity": 2, "outlines": True, "enhance": True}),
            ("Artistique", {"points": 800, "blur": 25, "sensitivity": 1, "outlines": True, "enhance": True}),
            ("Détaillé", {"points": 1800, "blur": 12, "sensitivity": 3, "outlines": False, "enhance": True}),
            ("Expressif", {"points": 1200, "blur": 20, "sensitivity": 3, "outlines": True, "enhance": True}),
            ("Minimaliste", {"points": 500, "blur": 28, "sensitivity": 1, "outlines": True, "enhance": True}),
        ]
        
        for i, (name, params) in enumerate(presets):
            ttk.Button(preset_frame, text=name, 
                      command=lambda p=params: self.apply_preset(p)).grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # === Section Actions ===
        action_frame = ttk.LabelFrame(main_frame, text="▶️ Actions", padding="10")
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.generate_btn = ttk.Button(action_frame, text="🎨 Générer l'image", command=self.generate_image)
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(action_frame, text="💾 Sauvegarder", command=self.save_image).grid(row=0, column=1, padx=5)
        
        self.status_var = tk.StringVar(value="Prêt")
        ttk.Label(action_frame, textvariable=self.status_var, foreground="blue").grid(row=0, column=2, padx=10)
        
        # === Aperçu ===
        preview_frame = ttk.LabelFrame(main_frame, text="👁️ Aperçu", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.canvas = tk.Canvas(preview_frame, bg="lightgray", height=300)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurer les poids
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        params_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
    def update_points_label(self, value):
        """Met à jour le label des points"""
        self.points_label.config(text=str(int(float(value))))
    
    def update_blur_label(self, value):
        """Met à jour le label du flou"""
        self.blur_label.config(text=str(int(float(value))))
    
    def update_sensitivity_label(self, value):
        """Met à jour le label de sensibilité"""
        self.sensitivity_label.config(text=str(int(float(value))))
    
    def update_grid_size_label(self, value):
        """Met à jour le label de taille de grille"""
        self.grid_size_label.config(text=str(int(float(value))))
    
    def toggle_hybrid_options(self):
        """Active/désactive les options du mode hybride"""
        if self.hybrid_var.get():
            # Activer les sliders du mode classique
            self.points_scale.config(state=tk.DISABLED)
            self.blur_scale.config(state=tk.DISABLED)
            self.sensitivity_scale.config(state=tk.DISABLED)
            # Activer le slider du mode hybride
            self.grid_size_scale.config(state=tk.NORMAL)
        else:
            # Réactiver les sliders du mode classique
            self.points_scale.config(state=tk.NORMAL)
            self.blur_scale.config(state=tk.NORMAL)
            self.sensitivity_scale.config(state=tk.NORMAL)
            # Désactiver le slider du mode hybride
            self.grid_size_scale.config(state=tk.DISABLED)
    
    
    def load_image(self):
        """Charge une image"""
        file_path = filedialog.askopenfilename(
            title="Sélectionnez une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("Tous", "*.*")],
            initialdir="data/input"
        )
        
        if file_path:
            self.current_image_path = file_path
            self.path_var.set(f"Chargé: {Path(file_path).name}")
            self.display_preview(file_path)
            self.status_var.set("Image chargée. Cliquez sur 'Générer'")
    
    def display_preview(self, image_path):
        """Affiche l'aperçu de l'image"""
        try:
            img = Image.open(image_path)
            # Redimensionner pour l'aperçu
            img.thumbnail((600, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo  # Garder une référence
        except Exception as e:
            self.status_var.set(f"Erreur affichage aperçu: {e}")
    
    def apply_preset(self, params):
        """Applique un preset de paramètres"""
        self.points_var.set(params["points"])
        self.blur_var.set(params["blur"])
        self.sensitivity_var.set(params["sensitivity"])
        self.outlines_var.set(params["outlines"])
        self.enhance_var.set(params["enhance"])
    
    def generate_image(self):
        """Génère l'image low poly"""
        if not self.current_image_path:
            messagebox.showwarning("Erreur", "Veuillez d'abord charger une image!")
            return
        
        if self.is_generating:
            messagebox.showinfo("Info", "Génération en cours, veuillez patienter...")
            return
        
        # Lancer la génération dans un thread pour ne pas bloquer l'UI
        thread = threading.Thread(target=self._generate_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_thread(self):
        """Génère l'image dans un thread séparé"""
        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED)
        self.status_var.set("⏳ Génération en cours...")
        self.root.update()
        
        try:
            # Mode hybride
            if self.hybrid_var.get():
                hybrid_gen = HybridLowPolyGenerator(
                    self.current_image_path,
                    enable_shape_mixing=True
                )
                self.current_image = hybrid_gen.generate_hybrid(
                    grid_size=int(self.grid_size_var.get())
                )
            # Mode classique
            else:
                self.generator = LowPolyGenerator(
                    self.current_image_path,
                    num_points=int(self.points_var.get()),
                    blur_strength=int(self.blur_var.get()),
                    enhance_colors=self.enhance_var.get(),
                    edge_sensitivity=int(self.sensitivity_var.get())
                )
                
                self.current_image = self.generator.generate(
                    use_edge_detection=True,
                    add_outlines=self.outlines_var.get()
                )
            
            # Afficher le résultat
            self.display_preview_pil(self.current_image)
            self.status_var.set("✅ Généré! Cliquez 'Sauvegarder' pour exporter.")
            
        except Exception as e:
            self.status_var.set(f"❌ Erreur: {str(e)[:50]}")
            messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{e}")
        
        finally:
            self.is_generating = False
            self.generate_btn.config(state=tk.NORMAL)
    
    def display_preview_pil(self, pil_image):
        """Affiche l'aperçu d'une image PIL"""
        try:
            img_copy = pil_image.copy()
            img_copy.thumbnail((600, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)
            
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
        except Exception as e:
            self.status_var.set(f"Erreur affichage: {e}")
    
    def save_image(self):
        """Sauvegarde l'image générée"""
        if not hasattr(self, 'current_image') or self.current_image is None:
            messagebox.showwarning("Erreur", "Veuillez d'abord générer une image!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Tous", "*.*")],
            initialdir="data/output"
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                self.status_var.set(f"✅ Sauvegardé: {Path(file_path).name}")
                messagebox.showinfo("Succès", f"Image sauvegardée:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{e}")


def main():
    root = tk.Tk()
    app = PolyGenGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
