import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font # Adicionado import font
import json
import os
import zlib
import base64
import shutil
import sys
import threading

# Nome fixo do arquivo de patch
PATCH_FILENAME = "patch_traducao.json"

class TranslationInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Instalador de Tradução - Ghost of a Tale")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        
        # Variáveis
        self.target_file = tk.StringVar()
        
        # --- Configuração de Estilo (Aparência) ---
        self.setup_styles() # Configura estilos antes de checar fontes para garantir tema
        
        # Definir fontes com fallback seguro
        self.header_font = ("Segoe UI", 16, "bold") if self.check_font("Segoe UI") else ("Arial", 16, "bold")
        self.sub_font = ("Segoe UI", 10) if self.check_font("Segoe UI") else ("Arial", 10)
        self.norm_font = ("Segoe UI", 9) if self.check_font("Segoe UI") else ("Arial", 9)
        self.bold_font = ("Segoe UI", 9, "bold") if self.check_font("Segoe UI") else ("Arial", 9, "bold")
        self.console_font = ("Consolas", 9) if self.check_font("Consolas") else ("Courier New", 9)

        # Configurar peso das colunas para centralização
        self.root.columnconfigure(0, weight=1)
        
        # Criar interface
        self.create_widgets()

    def check_font(self, font_name):
        """Verifica se uma fonte existe no sistema"""
        # Correção aplicada aqui: usa 'font.families()' diretamente
        return font_name in font.families()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('alt')
        
        # Cores
        bg_color = "#fdfdfd"      
        accent_color = "#6200EA"  
        text_color = "#333333"

        self.root.configure(bg=bg_color)

        # Configuração genérica
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color)
        style.configure("TLabelframe", background=bg_color, foreground=text_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=text_color)

        # Estilo do Botão Normal
        style.configure("TButton", padding=5)
        style.map("TButton",
                  foreground=[('pressed', 'black'), ('active', 'black')],
                  background=[('pressed', '!disabled', '#dedede'), ('active', '#ececec')]
                  )

        # Estilo do Botão de Ação Principal
        style.configure("Accent.TButton", 
                        font=("Segoe UI", 11, "bold"), 
                        background=accent_color, 
                        foreground="white",
                        padding=10)
        style.map("Accent.TButton",
                  background=[('pressed', '!disabled', '#3700B3'), ('active', '#5300d6')],
                  foreground=[('pressed', 'white'), ('active', 'white')]
                  )
        
        style.configure("TProgressbar", thickness=20)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- Cabeçalho ---
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 25))

        title_label = tk.Label(header_frame, text="Instalador de Tradução", 
                              font=self.header_font, fg="#6200EA", bg=self.root["bg"])
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Ghost of a Tale — Português Brasil", 
                                 font=self.sub_font, fg="#666666", bg=self.root["bg"])
        subtitle_label.pack(pady=(5, 0))

        version_label = tk.Label(header_frame, text="Versão base: 8.33 (GOG)", 
                                font=("Segoe UI", 8), fg="#E65100", bg=self.root["bg"])
        version_label.pack(pady=(2, 0))
        
        # --- Frame de Seleção ---
        input_frame = ttk.LabelFrame(main_frame, text="Localização do Arquivo", padding="20")
        input_frame.pack(fill=tk.X, pady=(0, 25))
        input_frame.columnconfigure(0, weight=1)

        ttk.Label(input_frame, text="Selecione o arquivo 'resources.assets' na pasta do jogo:", font=self.bold_font).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        self.entry_file = ttk.Entry(input_frame, textvariable=self.target_file, font=self.norm_font)
        self.entry_file.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=3)
        
        browse_btn = ttk.Button(input_frame, text="Procurar...", command=self.browse_target)
        browse_btn.grid(row=1, column=1)
        
        # --- Área de Ação ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, expand=True, anchor=tk.S)

        self.install_button = ttk.Button(action_frame, text="INSTALAR TRADUÇÃO", 
                                       style="Accent.TButton",
                                       command=self.apply_patch_thread,
                                       cursor="hand2")
        self.install_button.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_label = ttk.Label(action_frame, text="Aguardando início...", font=self.sub_font)
        self.progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress = ttk.Progressbar(action_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # --- Console ---
        console_frame = ttk.Frame(action_frame, relief="solid", borderwidth=1)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(console_frame, height=6, wrap=tk.WORD, 
                                 font=self.console_font, bg="#F8F9FA", fg="#333333",
                                 relief="flat", padx=10, pady=10, state="disabled")
        self.status_text.pack(fill=tk.BOTH, expand=True)

        self.log("Inciado. Selecione o arquivo do jogo para começar.")

    def get_resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def browse_target(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo resources.assets",
            filetypes=[("Unity Assets", "resources.assets"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            self.target_file.set(filename)
    
    def log(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update_idletasks()
    
    def clear_status(self):
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state="disabled")
        self.progress['value'] = 0
        self.progress_label.config(text="Preparando...")
    
    def update_progress(self, value, text=""):
        self.progress['value'] = value
        if text:
            self.progress_label.config(text=text)
        self.root.update_idletasks()
    
    def apply_patch_thread(self):
        thread = threading.Thread(target=self.apply_patch, daemon=True)
        thread.start()
    
    def apply_patch(self):
        target_path = self.target_file.get()
        patch_path = self.get_resource_path(PATCH_FILENAME)

        if not target_path:
            messagebox.showerror("Erro", "Por favor, selecione o arquivo resources.assets!", parent=self.root)
            return
        
        if not os.path.exists(patch_path):
            messagebox.showerror("Erro Fatal", f"O arquivo de patch '{PATCH_FILENAME}' não foi encontrado!\nEle deve estar na mesma pasta do instalador.", parent=self.root)
            return
        
        self.install_button.state(['disabled'])
        self.entry_file.state(['disabled'])
        self.root.config(cursor="watch")
        self.clear_status()
        
        try:
            self.log("🛡️ Iniciando backup de segurança...")
            self.update_progress(5, "Criando backup...")
            
            target_dir = os.path.dirname(target_path)
            backup_dir = os.path.join(target_dir, "backup resources")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                
            backup_file_path = os.path.join(backup_dir, "resources.assets")
            
            shutil.copy2(target_path, backup_file_path)
            self.log(f"✓ Backup salvo em: {backup_dir}")

            self.log("📊 Lendo arquivo do jogo para memória...")
            self.update_progress(15, "Lendo resources.assets...")
            
            with open(target_path, 'rb') as f:
                target_data = bytearray(f.read())
            
            self.log(f"✓ Arquivo carregado: {len(target_data)/1024/1024:.2f} MB")
            
            self.log("📖 Lendo dados da tradução...")
            with open(patch_path, 'r', encoding='utf-8') as f:
                patch_data = json.load(f)
            
            differences = patch_data.get('d', patch_data.get('differences', []))
            original_size = patch_data.get('oS', patch_data.get('originalSize', 0))
            translated_size = patch_data.get('tS', patch_data.get('translatedSize', 0))
            
            if len(target_data) != original_size:
                raise Exception(
                    f"Arquivo incompatível!\n"
                    f"O patch espera um arquivo de: {original_size} bytes\n"
                    f"Você selecionou um de: {len(target_data)} bytes\n\n"
                    f"Verifique se o jogo está atualizado ou se já não está modificado."
                )
            
            self.log("🔧 Aplicando modificações...")
            self.update_progress(30, "Aplicando tradução...")
            
            if translated_size > len(target_data):
                target_data.extend(b'\x00' * (translated_size - len(target_data)))
            elif translated_size < len(target_data):
                target_data = target_data[:translated_size]
            
            total_diffs = len(differences)
            for i, diff in enumerate(differences):
                offset = diff.get('o', diff.get('offset', 0))
                data_b64 = diff.get('d', diff.get('data', ''))
                
                compressed = base64.b64decode(data_b64)
                new_data = zlib.decompress(compressed)
                
                target_data[offset:offset + len(new_data)] = new_data
                
                if i % 100 == 0:
                    prog = 30 + int((i / total_diffs) * 50)
                    self.update_progress(prog, f"Processando blocos... ({int(i/total_diffs*100)}%)")

            self.log("💾 Salvando novo arquivo no disco...")
            self.update_progress(90, "Finalizando instalação...")
            
            with open(target_path, 'wb') as f:
                f.write(target_data)
                
            self.update_progress(100, "Instalação Concluída!")
            self.log("\n✅ SUCESSO! Tradução instalada.")
            
            messagebox.showinfo("Sucesso", 
                                "Tradução instalada com sucesso!\n\n"
                                f"Um backup do original foi criado na pasta:\n'backup resources'", parent=self.root)
            
            self.root.destroy()

        except Exception as e:
            self.log(f"\n❌ Erro Fatal: {str(e)}")
            messagebox.showerror("Erro na Instalação", str(e), parent=self.root)
            self.install_button.state(['!disabled'])
            self.entry_file.state(['!disabled'])
        finally:
            self.root.config(cursor="")

if __name__ == "__main__":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    try:
        root.iconbitmap(default='') 
    except:
        pass 
        
    app = TranslationInstaller(root)
    root.mainloop()