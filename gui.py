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
from src.preset_manager import get_preset_manager, Preset


class PolyGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PolyGen - Low Poly Cartoon Generator")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.current_image_path = None
        self.generator = None
        self.is_generating = False
        
        # Gestionnaire de presets
        self.preset_manager = get_preset_manager()
        
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
        preset_frame = ttk.LabelFrame(main_frame, text="🎨 Presets (Prédéfinis et Personnalisés)", padding="10")
        preset_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Sélecteur de preset
        ttk.Label(preset_frame, text="Charger:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.preset_names = self.preset_manager.get_all_names()
        self.preset_selector = ttk.Combobox(preset_frame, values=self.preset_names, state="readonly", width=20)
        self.preset_selector.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.preset_selector.current(0)  # Sélectionner le premier par défaut
        self.preset_selector.bind("<<ComboboxSelected>>", lambda e: self.load_selected_preset())
        
        # Boutons de gestion des presets
        ttk.Button(preset_frame, text="⬇️ Charger", command=self.load_selected_preset).grid(row=1, column=0, sticky=(tk.W, tk.E), padx=2, pady=2)
        ttk.Button(preset_frame, text="💾 Sauvegarder", command=self.save_current_preset).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        ttk.Button(preset_frame, text="🔄 Renommer", command=self.rename_preset).grid(row=2, column=0, sticky=(tk.W, tk.E), padx=2, pady=2)
        ttk.Button(preset_frame, text="🗑️ Supprimer", command=self.delete_preset).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        ttk.Button(preset_frame, text="📋 Liste", command=self.show_presets_list).grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        preset_frame.columnconfigure(1, weight=1)
        
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
        """Applique un preset de paramètres (format ancien pour compatibilité)"""
        self.points_var.set(params.get("points", 1000))
        self.blur_var.set(params.get("blur", 18))
        self.sensitivity_var.set(params.get("sensitivity", 2))
        self.outlines_var.set(params.get("outlines", True))
        self.enhance_var.set(params.get("enhance", True))
    
    def load_selected_preset(self):
        """Charge le preset sélectionné dans le combobox"""
        preset_name = self.preset_selector.get()
        if not preset_name:
            return
        
        preset = self.preset_manager.load_preset(preset_name)
        if not preset:
            messagebox.showerror("Erreur", f"Impossible de charger le preset '{preset_name}'")
            return
        
        # Appliquer le preset
        if preset.mode == "hybrid":
            self.hybrid_var.set(True)
            self.grid_size_var.set(preset.grid_size)
            self.toggle_hybrid_options()
        else:
            self.hybrid_var.set(False)
            self.points_var.set(preset.points)
            self.blur_var.set(preset.blur_strength)
            self.sensitivity_var.set(preset.edge_sensitivity)
            self.toggle_hybrid_options()
        
        self.outlines_var.set(preset.add_outlines)
        self.enhance_var.set(preset.enhance_colors)
        
        self.status_var.set(f"✅ Preset chargé: {preset_name}")
    
    def save_current_preset(self):
        """Sauvegarde les paramètres actuels comme preset"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sauvegarder un nouveau preset")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nom du preset:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5, padx=20)
        name_entry.focus()
        
        ttk.Label(dialog, text="Description (optionnel):").pack(pady=5)
        desc_entry = ttk.Entry(dialog, width=40)
        desc_entry.pack(pady=5, padx=20)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Erreur", "Le nom du preset est requis")
                return
            
            if name in self.preset_manager.presets:
                if not messagebox.askyesno("Confirmer", f"Le preset '{name}' existe déjà. Le remplacer?"):
                    return
            
            # Créer le preset
            preset = Preset(
                name=name,
                description=desc_entry.get().strip(),
                mode="hybrid" if self.hybrid_var.get() else "classic",
                points=int(self.points_var.get()),
                blur_strength=int(self.blur_var.get()),
                edge_sensitivity=int(self.sensitivity_var.get()),
                enhance_colors=self.enhance_var.get(),
                add_outlines=self.outlines_var.get(),
                grid_size=int(self.grid_size_var.get())
            )
            
            # Sauvegarder
            if self.preset_manager.save_preset(preset):
                messagebox.showinfo("Succès", f"Preset '{name}' sauvegardé avec succès!")
                
                # Mettre à jour le combobox
                self.preset_names = self.preset_manager.get_all_names()
                self.preset_selector['values'] = self.preset_names
                self.preset_selector.set(name)
                
                self.status_var.set(f"✅ Preset sauvegardé: {name}")
                dialog.destroy()
            else:
                messagebox.showerror("Erreur", "Impossible de sauvegarder le preset")
        
        ttk.Button(dialog, text="Sauvegarder", command=save).pack(pady=10)
    
    def rename_preset(self):
        """Renomme le preset sélectionné"""
        old_name = self.preset_selector.get()
        if not old_name:
            messagebox.showwarning("Erreur", "Sélectionnez un preset à renommer")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Renommer '{old_name}'")
        dialog.geometry("400x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nouveau nom:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5, padx=20)
        name_entry.insert(0, old_name)
        name_entry.focus()
        
        def rename():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("Erreur", "Le nom ne peut pas être vide")
                return
            
            if self.preset_manager.rename_preset(old_name, new_name):
                messagebox.showinfo("Succès", f"Preset renommé en '{new_name}'")
                
                # Mettre à jour le combobox
                self.preset_names = self.preset_manager.get_all_names()
                self.preset_selector['values'] = self.preset_names
                self.preset_selector.set(new_name)
                
                self.status_var.set(f"✅ Preset renommé: {new_name}")
                dialog.destroy()
            else:
                messagebox.showerror("Erreur", "Impossible de renommer le preset")
        
        ttk.Button(dialog, text="Renommer", command=rename).pack(pady=10)
    
    def delete_preset(self):
        """Supprime le preset sélectionné"""
        preset_name = self.preset_selector.get()
        if not preset_name:
            messagebox.showwarning("Erreur", "Sélectionnez un preset à supprimer")
            return
        
        if messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer '{preset_name}'?"):
            if self.preset_manager.delete_preset(preset_name):
                messagebox.showinfo("Succès", f"Preset '{preset_name}' supprimé")
                
                # Mettre à jour le combobox
                self.preset_names = self.preset_manager.get_all_names()
                self.preset_selector['values'] = self.preset_names
                if self.preset_names:
                    self.preset_selector.current(0)
                
                self.status_var.set(f"✅ Preset supprimé: {preset_name}")
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer ce preset")
    
    def show_presets_list(self):
        """Affiche la liste de tous les presets"""
        presets = self.preset_manager.list_presets()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Liste des presets")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        
        # Text widget avec scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(frame, yscrollcommand=scrollbar.set, height=20, width=70)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # Afficher les presets
        text.insert(tk.END, "═" * 65 + "\n")
        text.insert(tk.END, "PRESETS DISPONIBLES\n")
        text.insert(tk.END, "═" * 65 + "\n\n")
        
        classic = [p for p in presets if p.mode == "classic"]
        hybrid = [p for p in presets if p.mode == "hybrid"]
        
        if classic:
            text.insert(tk.END, "MODE CLASSIQUE:\n")
            text.insert(tk.END, "─" * 65 + "\n")
            for p in classic:
                text.insert(tk.END, f"{p.name:20} | pts={p.points:4} blur={p.blur_strength:2} sens={p.edge_sensitivity}\n")
                if p.description:
                    text.insert(tk.END, f"  → {p.description}\n")
            text.insert(tk.END, "\n")
        
        if hybrid:
            text.insert(tk.END, "MODE HYBRIDE:\n")
            text.insert(tk.END, "─" * 65 + "\n")
            for p in hybrid:
                text.insert(tk.END, f"{p.name:20} | grid={p.grid_size:2}px\n")
                if p.description:
                    text.insert(tk.END, f"  → {p.description}\n")
        
        text.config(state=tk.DISABLED)
        
        ttk.Button(dialog, text="Fermer", command=dialog.destroy).pack(pady=10)
    
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
