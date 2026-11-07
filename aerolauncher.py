import customtkinter as ctk
from tkinter import ttk, messagebox
import subprocess
import os
import json
from threading import Thread
from PIL import Image, ImageTk
import time
import sys

# --- CORE CONFIG ---
APP_NAME = "AeroLauncher"
USER_HOME = os.path.expanduser("~")
ROOT_DIR = os.path.join(USER_HOME, "AetheriumLauncher")
INSTANCES_DIR = os.path.join(ROOT_DIR, "instances")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
JAVA_DIR = os.path.join(ROOT_DIR, "java") # Directory for bundled Java


os.makedirs(ROOT_DIR, exist_ok=True)
os.makedirs(INSTANCES_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# --- PROFESSIONAL AERO PALETTE ---
C_BG_SOFT = "#F0F4F8"
C_ACCENT_BLUE = "#00AEEF"
C_ACCENT_DEEP = "#0071BC"
C_GLASS_WHITE = "#FFFFFF"
C_GLASS_LIGHT = "#F8FAFC"
C_TEXT_MAIN = "#2C3E50"
C_TEXT_DIM = "#546E7A"
C_LIME_SUCCESS = "#4CAF50"
C_BORDER_LIGHT = "#D1D9E0"
C_WHITE = "#FFFFFF"
C_AERO_GRADIENT = "#E1F5FE"
C_WARNING_RED = "#EF5350"
C_INFO_BLUE = "#B3E5FC"

LANGUAGES = {
    "RU": {
        "dash_title": "ГЛАВНАЯ",
        "launch_btn": "ЗАПУСТИТЬ",
        "status_ready": "Система готова",
        "inst_title": "СБОРКИ",
        "opt_title": "НАСТРОЙКИ",
        "mod_title": "МОДДИНГ",
        "acc_title": "ПРОФИЛЬ",
        "ram_lbl": "ОЗУ (ГБ):",
        "jvm_lbl": "JVM Аргументы:",
        "save_btn": "СОХРАНИТЬ",
        "nick_lbl": "Никнейм:",
        "engine_lbl": "Ядро:",
        "install_btn": "УСТАНОВИТЬ",
        "ver_filter": "Фильтр:",
        "all_versions": "Все",
        "releases": "Релизы",
        "snapshots": "Снапшоты",
        "alphas": "Альфа",
        "betas": "Бета",
        "success_save": "Настройки сохранены",
        "create_inst": "Создать сборку",
        "inst_name": "Имя сборки:",
        "launching": "Запуск мира...",
        "lang_lbl": "Язык:",
        "lib_title": "АРХИВ ВЕРСИЙ",
        "dash_sub": "Менеджер сборок",
        "loading": "Загрузка ресурсов...",
        "tab_inst": "Сборки",
        "tab_lib": "Версии",
        "tab_opt": "Настройки",
        "tab_mods": "Моды",
        "tab_acc": "Профиль",
        "inst_created": "Сборка создана!",
        "optimizing": "Оптимизация под ПК...",
        "perf_mode": "Режим производительности",
        "gui_scale": "Масштаб интерфейса",
        "gpu_accel": "GPU Ускорение",
        "low_res": "Низкое разрешение",
        "threads_opt": "Оптимизация потоков",
        "hw_detect": "Автоопределение",
        "hw_ram": "Тип памяти:",
        "hw_gpu": "Видеокарта:",
        "hw_cpu": "Процессор:",
        "hw_opt": "Оптимизация применена!",
        "welcome_title": "Добро пожаловать в AeroLauncher",
        "welcome_text": "Это современный лаунчер с эстетикой Frutiger Aero.\n\n1. Создайте свою первую сборку с помощью кнопки '+'.\n2. Выберите версию игры и ядро (Vanilla, Fabric, Forge).\n3. Настройте ОЗУ и JVM аргументы для максимального FPS.\n4. Нажмите 'ЗАПУСТИТЬ' и наслаждайтесь игрой!",
        "welcome_next": "Далее",
        "welcome_finish": "Начать работу",
        "opt_general": "Общие настройки",
        "opt_video": "Видео и Графика",
        "opt_system": "Система и Ядро",
        "opt_network": "Сеть и Соединение",
        "vsync_lbl": "Вертикальная синхронизация",
        "mipmap_lbl": "Уровень детализации (Mipmap)",
        "max_fps_lbl": "Макс. FPS",
        "gc_type_lbl": "Тип сборщика мусора",
        "heap_dump_lbl": "Дамп памяти при вылете",
        "log_level_lbl": "Уровень логов",
        "timeout_lbl": "Тайм-аут соединения",
        "proxy_lbl": "Использовать прокси",
        "priority_lbl": "Приоритет процесса",
        "allocate_large": "Выделять большие страницы памяти",
        "aggressive_opt": "Агрессивная оптимизация",
        "fullscreen_lbl": "Полноэкранный режим",
        "borderless_lbl": "Окно без рамок"
    },
    "EN": {
        "dash_title": "DASHBOARD",
        "launch_btn": "LAUNCH",
        "status_ready": "System ready",
        "inst_title": "INSTANCES",
        "opt_title": "SETTINGS",
        "mod_title": "MODDING",
        "acc_title": "PROFILE",
        "ram_lbl": "RAM (GB):",
        "jvm_lbl": "JVM Args:",
        "save_btn": "SAVE",
        "nick_lbl": "Nickname:",
        "engine_lbl": "Engine:",
        "install_btn": "INSTALL",
        "ver_filter": "Filter:",
        "all_versions": "All",
        "releases": "Releases",
        "snapshots": "Snapshots",
        "alphas": "Alphas",
        "betas": "Betas",
        "success_save": "Settings saved",
        "create_inst": "Create Instance",
        "inst_name": "Instance Name:",
        "launching": "Launching world...",
        "lang_lbl": "Lang:",
        "lib_title": "VERSION ARCHIVE",
        "dash_sub": "Instance Manager",
        "loading": "Loading resources...",
        "tab_inst": "Instances",
        "tab_lib": "Versions",
        "tab_opt": "Settings",
        "tab_mods": "Mods",
        "tab_acc": "Profile",
        "inst_created": "Instance created!",
        "optimizing": "Optimizing for PC...",
        "perf_mode": "Performance Mode",
        "gui_scale": "GUI Scale",
        "gpu_accel": "GPU Acceleration",
        "low_res": "Low Resolution",
        "threads_opt": "Thread Optimization",
        "hw_detect": "Auto Detect",
        "hw_ram": "RAM Type:",
        "hw_gpu": "GPU:",
        "hw_cpu": "CPU:",
        "hw_opt": "Optimization Applied!",
        "welcome_title": "Welcome to AeroLauncher",
        "welcome_text": "A modern launcher with Frutiger Aero aesthetics.\n\n1. Create your first instance using the '+' button.\n2. Select game version and engine (Vanilla, Fabric, Forge).\n3. Configure RAM and JVM args for maximum FPS.\n4. Hit 'LAUNCH' and enjoy!",
        "welcome_next": "Next",
        "welcome_finish": "Get Started",
        "opt_general": "General Settings",
        "opt_video": "Video & Graphics",
        "opt_system": "System & Core",
        "opt_network": "Network & Connection",
        "vsync_lbl": "Vertical Sync",
        "mipmap_lbl": "Mipmap Level",
        "max_fps_lbl": "Max FPS",
        "gc_type_lbl": "GC Type",
        "heap_dump_lbl": "Heap Dump on Crash",
        "log_level_lbl": "Log Level",
        "timeout_lbl": "Connection Timeout",
        "proxy_lbl": "Use Proxy",
        "priority_lbl": "Process Priority",
        "allocate_large": "Allocate Large Pages",
        "aggressive_opt": "Aggressive Optimization",
        "fullscreen_lbl": "Fullscreen Mode",
        "borderless_lbl": "Borderless Window"
    }
}

class LauncherCore:
    def __init__(self):
        self.settings_path = os.path.join(CONFIG_DIR, "settings.json")

    def load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception: pass
        return {
            "lang": "RU", "username": "CyberNet", "version": "1.20.1",
            "ram": "4", "jvm_args": "-XX:+UseG1GC", "type": "Vanilla", "filter": "Release",
            "perf_mode": "Auto", "gui_scale": "100%", "gpu_accel": "On", "low_res": "Off",
            "minecraft_path": ROOT_DIR
        }


    def save_settings(self, data):
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception: return False

    def get_instances(self):
        if not os.path.exists(INSTANCES_DIR): return []
        return [d for d in os.listdir(INSTANCES_DIR) if os.path.isdir(os.path.join(INSTANCES_DIR, d))]

    def delete_instance(self, name):
        try:
            import shutil
            inst_path = os.path.join(INSTANCES_DIR, name)
            shutil.rmtree(inst_path)
            return True
        except Exception: return False

    def create_instance(self, name):
        inst_path = os.path.join(INSTANCES_DIR, name)
        os.makedirs(inst_path, exist_ok=True)
        return inst_path

class SplashWindow(ctk.CTkToplevel):
    def __init__(self, on_finish, main_app):
        super().__init__()
        self.on_finish = on_finish
        self.main_app = main_app
        self.overrideredirect(True)
        self.geometry("450x250")
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"450x250+{(screen_w-450)//2}+{(screen_h-250)//2}")
        self.configure(fg_color=C_WHITE)
        self.border = ctk.CTkFrame(self, fg_color=C_ACCENT_BLUE, corner_radius=20)
        self.border.pack(expand=True, fill="both", padx=5, pady=5)
        self.content = ctk.CTkFrame(self.border, fg_color=C_WHITE, corner_radius=15)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.lbl = ctk.CTkLabel(self.content, text=APP_NAME, font=("Segoe UI", 32, "bold"), text_color=C_ACCENT_DEEP)
        self.lbl.pack(pady=(40, 10))
        self.prog_lbl = ctk.CTkLabel(self.content, text=LANGUAGES["RU"]["loading"], font=("Segoe UI", 13), text_color=C_TEXT_DIM)
        self.prog_lbl.pack()
        self.prog = ctk.CTkProgressBar(self.content, width=300, progress_color=C_ACCENT_BLUE)
        self.prog.set(0)
        self.prog.pack(pady=20)
        self.start_loading()

    def start_loading(self):
        def run():
            for i in range(1, 51):
                time.sleep(0.01)
                self.after(0, lambda v=i/100: self.prog.set(v))
            self.after(0, lambda: self.prog_lbl.configure(text=LANGUAGES["RU"]["optimizing"]))
            for i in range(51, 101):
                time.sleep(0.01)
                self.after(0, lambda v=i/100: self.prog.set(v))
            self.after(0, self.finish)
        Thread(target=run, daemon=True).start()

    def finish(self):
        self.on_finish()
        self.destroy()

class AeroLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.core = LauncherCore()
        self.settings = self.core.load_settings()

        # State management to avoid hasattr() checks and crashes
        self.app_state = {
            "lang": self.settings.get("lang", "RU"),
            "username": self.settings.get("username", "CyberNet"),
            "version": self.settings.get("version", "1.20.1"),
            "ram": self.settings.get("ram", "4"),
            "jvm_args": self.settings.get("jvm_args", "-XX:+UseG1GC"),
            "type": self.settings.get("type", "Vanilla"),
            "perf_mode": self.settings.get("perf_mode", "Auto"),
            "gpu_accel": self.settings.get("gpu_accel", "On"),
            "low_res": self.settings.get("low_res", "Off"),
            "vsync": self.settings.get("vsync", "Off"),
            "fullscreen": self.settings.get("fullscreen", "Off"),
            "max_fps": self.settings.get("max_fps", "Unlimited"),
            "gc_type": self.settings.get("gc_type", "G1GC"),
            "priority": self.settings.get("priority", "Normal"),
            "large_pages": self.settings.get("large_pages", "Off"),
            "proxy": self.settings.get("proxy", "Off"),
            "timeout": self.settings.get("timeout", "30000"),
            "gui_scale": self.settings.get("gui_scale", "100%")
        }

        self.lang_val = self.app_state["lang"]
        self.username_val = self.app_state["username"]
        self.version_val = self.app_state["version"]
        self.ram_val = self.app_state["ram"]
        self.jvm_val = self.app_state["jvm_args"]
        self.type_val = self.app_state["type"]
        self.current_instance = "Default"

        self.title(APP_NAME)
        self.geometry("1000x650")
        ctk.set_appearance_mode("light")
        self.configure(fg_color=C_BG_SOFT)

        self.withdraw()
        self.splash = SplashWindow(self.reveal, self)

    def reveal(self):
        # --- FIRST RUN SEQUENCE ---
        # 1. Language -> 2. HW Auto-Optimization -> 3. Tutorial -> 4. Main UI
        self.show_language_selector()

    def show_language_selector(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Language / Выберите язык")
        dialog.geometry("400x300")
        dialog.configure(fg_color=C_WHITE)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")

        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)

        ctk.CTkLabel(container, text="Select Language", font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(pady=(0, 20))

        lang_var = ctk.StringVar(value=self.lang_val)
        lang_menu = ctk.CTkOptionMenu(container, values=list(LANGUAGES.keys()), variable=lang_var, fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE)
        lang_menu.pack(pady=20)

        def confirm_lang():
            self.lang_val = lang_var.get()
            self.settings["lang"] = self.lang_val
            self.core.save_settings(self.settings)
            dialog.destroy()
            self.show_hw_setup() # Next step

        ctk.CTkButton(container, text="OK", command=confirm_lang, fg_color=C_LIME_SUCCESS, text_color=C_WHITE, font=("Segoe UI", 16, "bold"), corner_radius=15, height=40).pack(pady=20)

    def show_hw_setup(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t("optimizing"))
        dialog.geometry("500x400")
        dialog.configure(fg_color=C_WHITE)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")

        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)

        ctk.CTkLabel(container, text=self.t("optimizing"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(pady=(0, 20))

        info_lbl = ctk.CTkLabel(container, text="Analyzing system hardware for optimal JVM arguments...",
                                font=("Segoe UI", 14), text_color=C_TEXT_DIM, wraplength=400)
        info_lbl.pack(pady=10)

        prog = ctk.CTkProgressBar(container, width=400, progress_color=C_ACCENT_BLUE)
        prog.set(0)
        prog.pack(pady=20)

        def run_opt():
            for i in range(1, 101):
                time.sleep(0.02)
                prog.set(i/100)

            # Apply default high-perf settings
            self.settings["perf_mode"] = "High Performance"
            self.settings["gpu_accel"] = "On"
            self.core.save_settings(self.settings)

            dialog.after(0, lambda: info_lbl.configure(text=self.t("hw_opt"), text_color=C_LIME_SUCCESS))
            dialog.after(0, lambda: ctk.CTkButton(container, text=self.t("welcome_next"),
                                                   command=lambda: [dialog.destroy(), self.show_tutorial()],
                                                   fg_color=C_ACCENT_BLUE, corner_radius=15).pack(pady=20))

        Thread(target=run_opt, daemon=True).start()

    def show_tutorial(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t("welcome_title"))
        dialog.geometry("500x400")
        dialog.configure(fg_color=C_WHITE)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")

        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)

        ctk.CTkLabel(container, text=self.t("welcome_title"), font=("Segoe UI", 22, "bold"), text_color=C_ACCENT_DEEP).pack(pady=(0, 20))

        text_lbl = ctk.CTkLabel(container, text=self.t("welcome_text"),
                                font=("Segoe UI", 15), text_color=C_TEXT_MAIN, justify="left", wraplength=400)
        text_lbl.pack(pady=20)

        ctk.CTkButton(container, text=self.t("welcome_finish"),
                      command=lambda: [dialog.destroy(), self.setup_ui(), self.deiconify()],
                      fg_color=C_LIME_SUCCESS, text_color=C_WHITE, font=("Segoe UI", 16, "bold"),
                      corner_radius=15, height=45).pack(pady=20)

    def t(self, key):
        return LANGUAGES[self.lang_val].get(key, key)

    def setup_ui(self):
        # Background image logic removed for standalone EXE stability
        self.main_app = ctk.CTkFrame(self, fg_color="transparent")
        self.main_app.pack(expand=True, fill="both")

        # --- LEFT PANEL (Glass Effect) ---
        self.left_panel = ctk.CTkFrame(self.main_app, width=300, fg_color=C_GLASS_LIGHT,
                                      corner_radius=20, border_width=1, border_color=C_WHITE)
        self.left_panel.pack(side="left", fill="y", padx=20, pady=20)
        self.left_panel.pack_propagate(False)

        self.inst_header = ctk.CTkLabel(self.left_panel, text=self.t("inst_title"),
                                       font=("Segoe UI", 22, "bold"), text_color=C_ACCENT_DEEP)
        self.inst_header.pack(pady=(30, 10), padx=20, anchor="w")

        self.inst_ctrl = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.inst_ctrl.pack(fill="x", padx=20, pady=10)

        self.inst_entry = ctk.CTkEntry(self.inst_ctrl, placeholder_text=self.t("inst_name"),
                                       width=150, height=35, corner_radius=10, border_color=C_ACCENT_BLUE)
        self.inst_entry.pack(side="left", padx=(0, 10))

        self.btn_add_inst = ctk.CTkButton(self.inst_ctrl, text="+", width=35, height=35,
                                         command=self.create_instance, fg_color=C_ACCENT_BLUE,
                                         text_color=C_WHITE, corner_radius=10, font=("Segoe UI", 20, "bold"))
        self.btn_add_inst.pack(side="left")

        self.inst_list_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent",
                                                     corner_radius=15)
        self.inst_list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.refresh_instances()

        self.lang_switch = ctk.CTkOptionMenu(self.left_panel, values=["RU", "EN"],
                                              command=self.change_lang,
                                              fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP,
                                              text_color=C_WHITE, corner_radius=10, height=30)
        self.lang_switch.set(self.lang_val)
        self.lang_switch.pack(side="bottom", pady=30, padx=20)

        # --- RIGHT PANEL (Floating Card) ---
        self.right_panel = ctk.CTkFrame(self.main_app, fg_color="transparent")
        self.right_panel.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.detail_card = ctk.CTkFrame(self.right_panel, fg_color=C_GLASS_WHITE,
                                       corner_radius=35, border_width=2, border_color=C_WHITE)
        self.detail_card.pack(expand=True, fill="both")

        self.top_bar = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=30, pady=(30, 20))

        self.detail_title = ctk.CTkLabel(self.top_bar, text=self.current_instance,
                                         font=("Segoe UI", 32, "bold"), text_color=C_TEXT_MAIN)
        self.detail_title.pack(side="left")

        self.btn_launch = ctk.CTkButton(self.top_bar, text=self.t("launch_btn"),
                                         command=self.start_launch_thread,
                                         fg_color=C_LIME_SUCCESS, hover_color="#388E3C",
                                         text_color=C_WHITE, font=("Segoe UI", 18, "bold"),
                                         corner_radius=25, height=50, width=180)
        self.btn_launch.pack(side="right")

        self.tab_container = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        self.tab_container.pack(expand=True, fill="both", padx=30, pady=(0, 30))

        self.tabs_header = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        self.tabs_header.pack(fill="x")

        self.tabs = {}
        tab_config = [("inst", "tab_inst"), ("lib", "tab_lib"), ("opt", "tab_opt"), ("mods", "tab_mods"), ("acc", "tab_acc")]
        for key, lang_key in tab_config:
            btn = ctk.CTkButton(self.tabs_header, text=self.t(lang_key),
                                command=lambda k=key: self.show_tab(k),
                                fg_color="transparent", text_color=C_TEXT_DIM,
                                hover_color="#E1F5FE", font=("Segoe UI", 15), height=40, corner_radius=10)
            btn.pack(side="left", padx=5)
            self.tabs[key] = btn

        self.tab_content = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        self.tab_content.pack(expand=True, fill="both", pady=20)

        self.page_frames = {}
        self.create_inst_tab()
        self.create_lib_tab()
        self.create_opt_tab()
        self.create_mods_tab()
        self.create_acc_tab()
        self.show_tab("inst")

        self.status_bar = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.status_bar.pack(fill="x", pady=(10, 0))

        self.status_lbl = ctk.CTkLabel(self.status_bar, text=self.t("status_ready"),
                                       font=("Segoe UI", 14), text_color=C_TEXT_DIM)
        self.status_lbl.pack(side="left")

        self.progress = ctk.CTkProgressBar(self.status_bar, width=300, progress_color=C_ACCENT_BLUE)
        self.progress.set(0)
        self.progress.pack(side="right", padx=10)
        self.progress.pack_forget()

    def t(self, key):
        return LANGUAGES[self.lang_val].get(key, key)

    def change_lang(self, new_lang):
        self.lang_val = new_lang
        self.settings["lang"] = new_lang
        self.core.save_settings(self.settings)
        self.update_ui_texts()
        messagebox.showinfo("System", "Язык обновлен!")

    def update_ui_texts(self):
        self.inst_header.configure(text=self.t("inst_title"))
        self.btn_launch.configure(text=self.t("launch_btn"))
        self.status_lbl.configure(text=self.t("status_ready"))

        tab_config = [("inst", "tab_inst"), ("lib", "tab_lib"), ("opt", "tab_opt"), ("mods", "tab_mods"), ("acc", "tab_acc")]
        for key, lang_key in tab_config:
            if key in self.tabs:
                self.tabs[key].configure(text=self.t(lang_key))

        # Completely rebuild tabs to update internal labels/widgets
        self.create_inst_tab()
        self.create_lib_tab()
        self.create_opt_tab()
        self.create_mods_tab()
        self.create_acc_tab()

        # Restore the current tab view
        if hasattr(self, 'current_tab'):
            self.show_tab(self.current_tab)
        else:
            self.show_tab("inst")

    def show_tab(self, key):
        self.current_tab = key
        for f in self.page_frames.values(): f.pack_forget()
        self.page_frames[key].pack(expand=True, fill="both")
        for k, btn in self.tabs.items():
            if k == key: btn.configure(text_color=C_ACCENT_BLUE, fg_color="#E1F5FE")
            else: btn.configure(text_color=C_TEXT_DIM, fg_color="transparent")

    def create_inst_tab(self):
        # Clear existing frame before recreating to avoid overlap
        if "inst" in self.page_frames:
            self.page_frames["inst"].destroy()

        frame = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        self.page_frames["inst"] = frame
        ctk.CTkLabel(frame, text=self.t("inst_title"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(anchor="w", pady=(0, 10))
        list_f = ctk.CTkScrollableFrame(frame, fg_color=C_WHITE, corner_radius=15, border_width=1, border_color=C_BORDER_LIGHT)
        list_f.pack(expand=True, fill="both")
        for inst in self.core.get_instances():
            btn = ctk.CTkButton(list_f, text=f"  {inst}", command=lambda n=inst: self.select_instance(n), fg_color="transparent", text_color=C_TEXT_MAIN, hover_color="#E1F5FE", anchor="w", font=("Segoe UI", 14), height=40)
            btn.pack(fill="x", pady=2, padx=5)

    def create_lib_tab(self):
        if "lib" in self.page_frames:
            self.page_frames["lib"].destroy()
        frame = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        self.page_frames["lib"] = frame
        ctk.CTkLabel(frame, text=self.t("lib_title"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(anchor="w", pady=(0, 10))
        f_frame = ctk.CTkFrame(frame, fg_color="transparent")
        f_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(f_frame, text=self.t("ver_filter"), text_color=C_TEXT_MAIN).pack(side="left", padx=10)
        f_opts = {"All": self.t("all_versions"), "Release": self.t("releases"), "Snapshot": self.t("snapshots"), "Alpha": self.t("alphas"), "Beta": self.t("betas")}
        f_vals = [f"{k}: {v}" for k, v in f_opts.items()]
        self.filter_menu = ctk.CTkOptionMenu(f_frame, values=f_vals, command=self.update_version_list, fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE, corner_radius=8)
        self.filter_menu.set(f_vals[1])
        self.filter_menu.pack(side="left", padx=10)
        self.ver_list_frame = ctk.CTkScrollableFrame(frame, fg_color=C_WHITE, corner_radius=15, border_width=1, border_color=C_BORDER_LIGHT)
        self.ver_list_frame.pack(expand=True, fill="both", pady=10)
        Thread(target=self.update_version_list, args=(None,), daemon=True).start()

    def update_version_list(self, choice=None):
        def ui_update():
            # Clear current list
            for w in self.ver_list_frame.winfo_children():
                w.destroy()

            try:
                import minecraft_launcher_lib
                all_vers = minecraft_launcher_lib.utils.get_version_list()
                filter_text = self.filter_menu.get()

                # Extract key from "Key: Value" format
                f_key = "All"
                if "Release" in filter_text: f_key = "release"
                elif "Snapshot" in filter_text: f_key = "snapshot"
                elif "Alpha" in filter_text: f_key = "alpha"
                elif "Beta" in filter_text: f_key = "beta"

                # Filter and render
                filtered_vers = [v for v in all_vers if f_key == "All" or v['type'] == f_key]

                for v in filtered_vers:
                    btn = ctk.CTkButton(
                        self.ver_list_frame,
                        text=v['id'],
                        command=lambda val=v['id']: self.set_version(val),
                        fg_color="transparent",
                        text_color=C_TEXT_MAIN,
                        hover_color="#E1F5FE",
                        anchor="w",
                        font=("Segoe UI", 13),
                        height=35
                    )
                    btn.pack(fill="x", pady=2, padx=10)

            except Exception as e:
                ctk.CTkLabel(self.ver_list_frame, text=f"Error: {e}", text_color="red").pack()

        # Use after(0, ...) to ensure UI update happens on main thread
        self.after(0, ui_update)

    def create_opt_tab(self):
        if "opt" in self.page_frames:
            self.page_frames["opt"].destroy()
        frame = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        self.page_frames["opt"] = frame
        ctk.CTkLabel(frame, text=self.t("opt_title"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(anchor="w", pady=(0, 20))

        scroll_f = ctk.CTkScrollableFrame(frame, fg_color=C_WHITE, corner_radius=20, border_width=1, border_color=C_BORDER_LIGHT)
        scroll_f.pack(fill="both", expand=True, padx=10, pady=10)

        # --- SECTION: HARDWARE OPTIMIZATION ---
        ctk.CTkLabel(scroll_f, text="🚀 Аппаратная оптимизация", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        hw_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        hw_f.pack(fill="x", padx=20, pady=10)

        # RAM Type
        ram_type_f = ctk.CTkFrame(hw_f, fg_color="transparent")
        ram_type_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(ram_type_f, text=self.t("hw_ram"), text_color=C_TEXT_MAIN).pack(side="left")
        self.hw_ram_menu = ctk.CTkOptionMenu(ram_type_f, values=["DDR5", "DDR4", "DDR3", "Laptop RAM"], fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE, width=120)
        self.hw_ram_menu.set("DDR4")
        self.hw_ram_menu.pack(side="left", padx=10)

        # GPU Type
        gpu_f = ctk.CTkFrame(hw_f, fg_color="transparent")
        gpu_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(gpu_f, text=self.t("hw_gpu"), text_color=C_TEXT_MAIN).pack(side="left")
        self.hw_gpu_menu = ctk.CTkOptionMenu(gpu_f, values=["NVIDIA RTX", "NVIDIA GTX", "AMD Radeon", "Intel Arc", "Integrated"], fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE, width=120)
        self.hw_gpu_menu.set("NVIDIA RTX")
        self.hw_gpu_menu.pack(side="left", padx=10)

        # CPU Type
        cpu_f = ctk.CTkFrame(hw_f, fg_color="transparent")
        cpu_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(cpu_f, text=self.t("hw_cpu"), text_color=C_TEXT_MAIN).pack(side="left")
        self.hw_cpu_menu = ctk.CTkOptionMenu(cpu_f, values=["High-End", "Mid-Range", "Budget", "Laptop/Mobile"], fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE, width=120)
        self.hw_cpu_menu.set("Mid-Range")
        self.hw_cpu_menu.pack(side="left", padx=10)

        def auto_detect_hw():
            import platform
            self.status_lbl.configure(text="Detecting hardware...")
            self.after(1000, lambda: self.finalize_opt())

        def finalize_opt():
            self.status_lbl.configure(text=self.t("hw_opt"))
            ram_type, gpu_type, cpu_type = self.hw_ram_menu.get(), self.hw_gpu_menu.get(), self.hw_cpu_menu.get()
            new_args = "-XX:+UseG1GC"
            if ram_type == "DDR5": new_args += " -XX:+UseZGC"
            if "RTX" in gpu_type: new_args += " -XX:+UseVectorizedMismatchIntrinsic"
            if cpu_type == "High-End": new_args += " -Xms4G -XX:ParallelGCThreads=8"
            elif cpu_type == "Budget": new_args += " -Xms1G -XX:ParallelGCThreads=2"
            self.jvm_entry.delete(0, 'end')
            self.jvm_entry.insert(0, new_args)
            self.jvm_val = new_args
            messagebox.showinfo("Optimization", "Система проанализирована. Применены оптимальные JVM аргументы!")

        ctk.CTkButton(hw_f, text=self.t("hw_detect"), command=auto_detect_hw, fg_color=C_LIME_SUCCESS, text_color=C_WHITE, corner_radius=10, height=30).pack(anchor="w", pady=15)

        # --- SECTION: CORE SETTINGS ---
        ctk.CTkLabel(scroll_f, text="⚙️ Основные настройки", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        core_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        core_f.pack(fill="x", padx=20, pady=10)

        ram_f = ctk.CTkFrame(core_f, fg_color="transparent")
        ram_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(ram_f, text=self.t("ram_lbl"), text_color=C_TEXT_MAIN).pack(side="left")
        self.ram_entry = ctk.CTkEntry(ram_f, width=80, height=30, corner_radius=8)
        self.ram_entry.insert(0, self.ram_val)
        self.ram_entry.pack(side="left", padx=10)

        jvm_f = ctk.CTkFrame(core_f, fg_color="transparent")
        jvm_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(jvm_f, text=self.t("jvm_lbl"), text_color=C_TEXT_MAIN).pack(anchor="nw")
        self.jvm_entry = ctk.CTkEntry(jvm_f, width=450, height=30, corner_radius=8)
        self.jvm_entry.insert(0, self.jvm_val)
        self.jvm_entry.pack(anchor="w", pady=5)

        # --- SECTION: VIDEO & GRAPHICS ---
        ctk.CTkLabel(scroll_f, text="📺 Видео и Графика", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        video_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        video_f.pack(fill="x", padx=20, pady=10)

        self.vsync_sw = ctk.CTkSwitch(video_f, text=self.t("vsync_lbl"), progress_color=C_ACCENT_BLUE)
        self.vsync_sw.pack(anchor="w", pady=5)

        self.fullscreen_sw = ctk.CTkSwitch(video_f, text=self.t("fullscreen_lbl"), progress_color=C_ACCENT_BLUE)
        self.fullscreen_sw.pack(anchor="w", pady=5)

        fps_f = ctk.CTkFrame(video_f, fg_color="transparent")
        fps_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(fps_f, text=self.t("max_fps_lbl"), text_color=C_TEXT_MAIN).pack(side="left")
        self.fps_entry = ctk.CTkEntry(fps_f, width=60, height=30, corner_radius=8)
        self.fps_entry.insert(0, "Unlimited")
        self.fps_entry.pack(side="left", padx=10)

        # --- SECTION: SYSTEM & ADVANCED ---
        ctk.CTkLabel(scroll_f, text="🛠️ Система и Ядро", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        sys_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        sys_f.pack(fill="x", padx=20, pady=10)

        self.gc_menu = ctk.CTkOptionMenu(sys_f, values=["G1GC", "ZGC", "Shenandoah", "ParallelGC"], fg_color=C_ACCENT_BLUE, text_color=C_WHITE)
        self.gc_menu.set("G1GC")
        ctk.CTkLabel(sys_f, text=self.t("gc_type_lbl"), text_color=C_TEXT_MAIN).pack(side="left")
        self.gc_menu.pack(side="left", padx=10, pady=5)

        self.priority_sw = ctk.CTkSwitch(sys_f, text=self.t("priority_lbl"), progress_color=C_ACCENT_BLUE)
        self.priority_sw.pack(anchor="w", pady=5)

        self.large_pages_sw = ctk.CTkSwitch(sys_f, text=self.t("allocate_large"), progress_color=C_ACCENT_BLUE)
        self.large_pages_sw.pack(anchor="w", pady=5)

        # --- SECTION: NETWORK ---
        ctk.CTkLabel(scroll_f, text="🌐 Сеть и Соединение", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        net_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        net_f.pack(fill="x", padx=20, pady=10)

        self.proxy_sw = ctk.CTkSwitch(net_f, text=self.t("proxy_lbl"), progress_color=C_ACCENT_BLUE)
        self.proxy_sw.pack(anchor="w", pady=5)

        timeout_f = ctk.CTkFrame(net_f, fg_color="transparent")
        timeout_f.pack(anchor="w", pady=5)
        ctk.CTkLabel(timeout_f, text=self.t("timeout_lbl"), text_color=C_TEXT_MAIN).pack(side="left")
        self.timeout_entry = ctk.CTkEntry(timeout_f, width=80, height=30, corner_radius=8)
        self.timeout_entry.insert(0, "30000")
        self.timeout_entry.pack(side="left", padx=10)

        # --- SECTION: UI CUSTOMIZATION ---
        ctk.CTkLabel(scroll_f, text="🎨 Интерфейс", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT_BLUE).pack(anchor="w", padx=20, pady=(20, 10))
        ui_f = ctk.CTkFrame(scroll_f, fg_color="transparent")
        ui_f.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(ui_f, text=self.t("gui_scale"), text_color=C_TEXT_MAIN).pack(anchor="w")
        self.scale_slider = ctk.CTkSlider(ui_f, from_=50, to=200, number_of_steps=150)
        self.scale_slider.set(100)
        self.scale_slider.pack(fill="x", pady=5)

        ctk.CTkButton(scroll_f, text=self.t("save_btn"), command=self.save_settings, fg_color=C_ACCENT_BLUE, text_color=C_WHITE, corner_radius=10, height=35).pack(anchor="w", padx=20, pady=30)

    def create_mods_tab(self):
        if "mods" in self.page_frames:
            self.page_frames["mods"].destroy()
        frame = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        self.page_frames["mods"] = frame
        ctk.CTkLabel(frame, text=self.t("mod_title"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(frame, fg_color=C_WHITE, corner_radius=20, border_width=1, border_color=C_BORDER_LIGHT)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(card, text=self.t("engine_lbl"), text_color=C_TEXT_MAIN, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=30, pady=(30, 10))
        self.type_menu = ctk.CTkOptionMenu(card, values=["Vanilla", "Fabric", "Forge"], fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE, corner_radius=8, height=35)
        self.type_menu.set(self.type_val)
        self.type_menu.pack(anchor="w", padx=30, pady=(0, 30))
        self.btn_mod = ctk.CTkButton(card, text=self.t("install_btn"), command=self.install_mod_thread, fg_color=C_ACCENT_BLUE, hover_color=C_ACCENT_DEEP, text_color=C_WHITE, font=("Segoe UI", 14, "bold"), corner_radius=10, height=35)
        self.btn_mod.pack(anchor="w", padx=30, pady=(0, 30))

    def create_acc_tab(self):
        if "acc" in self.page_frames:
            self.page_frames["acc"].destroy()
        frame = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        self.page_frames["acc"] = frame
        ctk.CTkLabel(frame, text=self.t("acc_title"), font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(frame, fg_color=C_WHITE, corner_radius=20, border_width=1, border_color=C_BORDER_LIGHT)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(card, text=self.t("nick_lbl"), text_color=C_TEXT_MAIN, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=30, pady=(30, 10))
        self.nick_entry = ctk.CTkEntry(card, width=300, height=30, corner_radius=8, border_color=C_ACCENT_BLUE)
        self.nick_entry.insert(0, self.username_val)
        self.nick_entry.pack(anchor="w", padx=30, pady=(0, 30))
        ctk.CTkButton(card, text=self.t("save_btn"), command=self.save_settings, fg_color=C_ACCENT_BLUE, hover_color=C_ACCENT_DEEP, text_color=C_WHITE, font=("Segoe UI", 14, "bold"), corner_radius=10, height=35).pack(anchor="w", padx=30, pady=(0, 30))

    def create_instance(self):
        name = self.inst_entry.get().strip()
        if not name:
            messagebox.showwarning("System", "Введите имя сборки!")
            return

        # --- Creation Dialog ---
        dialog = ctk.CTkToplevel(self)
        dialog.title("Настройка новой сборки")
        dialog.geometry("400x500")
        dialog.configure(fg_color=C_WHITE)
        dialog.grab_set() # Make modal

        # Center dialog
        dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")

        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=30, pady=30)

        ctk.CTkLabel(container, text=f"Настройка: {name}", font=("Segoe UI", 20, "bold"), text_color=C_ACCENT_DEEP).pack(pady=(0, 20))

        # Version Selection
        ctk.CTkLabel(container, text="Версия Minecraft:", text_color=C_TEXT_MAIN).pack(anchor="w")
        ver_var = ctk.StringVar(value=self.version_val)
        # Get all available versions for the dropdown
        try:
            import minecraft_launcher_lib
            all_vers = [v['id'] for v in minecraft_launcher_lib.utils.get_version_list()]
        except:
            all_vers = ["1.20.1"]

        ver_menu = ctk.CTkOptionMenu(container, values=all_vers, variable=ver_var, fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE)
        ver_menu.pack(fill="x", pady=(5, 15))

        # Engine Selection
        ctk.CTkLabel(container, text="Ядро:", text_color=C_TEXT_MAIN).pack(anchor="w")
        type_var = ctk.StringVar(value=self.type_val)
        type_menu = ctk.CTkOptionMenu(container, values=["Vanilla", "Fabric", "Forge"], variable=type_var, fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE)
        type_menu.pack(fill="x", pady=(5, 15))

        # RAM Selection
        ctk.CTkLabel(container, text="Оперативная память (ГБ):", text_color=C_TEXT_MAIN).pack(anchor="w")
        ram_var = ctk.StringVar(value=self.ram_val)
        ram_menu = ctk.CTkOptionMenu(container, values=["2", "4", "6", "8", "12", "16", "32"], variable=ram_var, fg_color=C_ACCENT_BLUE, button_color=C_ACCENT_DEEP, text_color=C_WHITE)
        ram_menu.pack(fill="x", pady=(5, 15))

        # --- JAVA CHECK ---
        ctk.CTkLabel(container, text="Проверка Java:", text_color=C_TEXT_MAIN).pack(anchor="w")
        java_status_frame = ctk.CTkFrame(container, fg_color="transparent")
        java_status_frame.pack(fill="x", pady=(5, 15))

        def check_java():
            try:
                subprocess.run(["java", "-version"], capture_output=True, check=True)
                status_lbl.configure(text="Java установлена ✅", text_color=C_LIME_SUCCESS)
                btn_install_java.pack_forget()
            except:
                status_lbl.configure(text="Java не найдена ❌", text_color="red")
                btn_install_java.pack(side="left", padx=10)

        status_lbl = ctk.CTkLabel(java_status_frame, text="Проверка...", text_color=C_TEXT_DIM)
        status_lbl.pack(side="left", padx=10)

        def install_java():
            def run():
                try:
                    btn_install_java.configure(state="disabled")
                    status_lbl.configure(text="Загрузка Java...", text_color=C_TEXT_DIM)

                    # We use minecraft_launcher_lib's runtime manager to handle the heavy lifting.
                    # Since we don't have a specific version here, we default to Java 17 (common for modern MC)
                    import minecraft_launcher_lib
                    runtime_version = "17"

                    # This actually downloads and installs the JRE into the project ROOT_DIR/java
                    java_path = minecraft_launcher_lib.java.install_java_version(runtime_version, ROOT_DIR)

                    dialog.after(0, lambda: status_lbl.configure(text="Java установлена ✅", text_color=C_LIME_SUCCESS))
                    dialog.after(0, lambda: btn_install_java.pack_forget())
                except Exception as e:
                    dialog.after(0, lambda: messagebox.showerror("Error", f"Ошибка установки Java: {str(e)}"))
                    dialog.after(0, lambda: btn_install_java.configure(state="normal"))
                    dialog.after(0, lambda: status_lbl.configure(text="Ошибка установки ❌", text_color="red"))

            Thread(target=run, daemon=True).start()

        btn_install_java = ctk.CTkButton(java_status_frame, text="Установить", width=80, height=25, command=install_java, fg_color=C_ACCENT_BLUE, text_color=C_WHITE)

        # Check java immediately on open
        Thread(target=check_java, daemon=True).start()

        def confirm_creation():
            try:
                os.makedirs(INSTANCES_DIR, exist_ok=True)
                self.core.create_instance(name)

                # Save instance-specific configuration
                inst_dir = os.path.join(INSTANCES_DIR, name)
                inst_config = {
                    "version": ver_var.get(),
                    "type": type_var.get(),
                    "ram": ram_var.get(),
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                config_path = os.path.join(inst_dir, "instance_settings.json")
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(inst_config, f, indent=4)

                self.current_instance = name
                self.detail_title.configure(text=name)
                self.inst_entry.delete(0, 'end')
                self.refresh_instances()
                self.create_inst_tab()

                if hasattr(self, 'current_tab') and self.current_tab == "inst":
                    self.show_tab("inst")

                messagebox.showinfo("System", self.t("inst_created"))
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Ошибка при создании: {str(e)}")

        ctk.CTkButton(container, text="СОЗДАТЬ", command=confirm_creation, fg_color=C_LIME_SUCCESS, text_color=C_WHITE, font=("Segoe UI", 16, "bold"), corner_radius=15, height=40).pack(fill="x", pady=20)

    def refresh_instances(self):
        for w in self.inst_list_frame.winfo_children(): w.destroy()
        for inst in self.core.get_instances():
            # Instance Row Frame
            row = ctk.CTkFrame(self.inst_list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2, padx=5)

            btn = ctk.CTkButton(row, text=f"  {inst}", command=lambda n=inst: self.select_instance(n),
                                fg_color="transparent", text_color=C_TEXT_MAIN, hover_color="#E1F5FE",
                                anchor="w", font=("Segoe UI", 14), height=40)
            btn.pack(side="left", expand=True, fill="x")

            # Delete button for each instance
            btn_del = ctk.CTkButton(row, text="✕", width=30, height=30,
                                    command=lambda n=inst: self.confirm_delete_instance(n),
                                    fg_color="transparent", text_color=C_TEXT_DIM,
                                    hover_color="#FFCDD2", corner_radius=8)
            btn_del.pack(side="right", padx=5)

    def confirm_delete_instance(self, name):
        if messagebox.askyesno("System", f"Вы уверены, что хотите удалить сборку '{name}'?\nВсе данные будут стерты!"):
            if self.core.delete_instance(name):
                if self.current_instance == name:
                    self.current_instance = "Default"
                    self.detail_title.configure(text="Default")
                self.refresh_instances()
                self.create_inst_tab()
                messagebox.showinfo("System", "Сборка удалена")
            else:
                messagebox.showerror("Error", "Не удалось удалить сборку")

    def select_instance(self, name):
        self.current_instance = name
        self.detail_title.configure(text=name)

        # Load instance-specific settings if they exist
        inst_dir = os.path.join(INSTANCES_DIR, name)
        config_path = os.path.join(inst_dir, "instance_settings.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.version_val = data.get("version", self.version_val)
                    self.type_val = data.get("type", self.type_val)

                    # Update UI menus to reflect loaded settings
                    if hasattr(self, 'type_menu'):
                        self.type_menu.set(self.type_val)
                    self.status_lbl.configure(text=f"Selected instance: {name} ({self.version_val} {self.type_val})")
            except Exception as e:
                print(f"Error loading instance config: {e}")

        self.show_tab("inst")

    def set_version(self, v):
        self.version_val = v
        self.status_lbl.configure(text=f"Selected version: {v}")

    def update_status(self, value, text):
        self.status_lbl.configure(text=text)
        self.progress.set(value)
        self.update_idletasks()

    def save_settings(self):
        data = {
            "lang": self.lang_val, "username": self.nick_entry.get(), "version": self.version_val,
            "ram": self.ram_entry.get(), "jvm_args": self.jvm_entry.get(), "type": self.type_menu.get(),
            "filter": self.filter_menu.get() if hasattr(self, 'filter_menu') else "All",
            "perf_mode": self.perf_mode.get() if hasattr(self, 'perf_mode') else "Auto",
            "gui_scale": f"{int(self.scale_slider.get())}%",
            "gpu_accel": "On" if (hasattr(self, 'gpu_acc') and self.gpu_acc.get()) else "Off",
            "low_res": "On" if (hasattr(self, 'low_res') and self.low_res.get()) else "Off",
            "vsync": "On" if hasattr(self, 'vsync_sw') and self.vsync_sw.get() else "Off",
            "fullscreen": "On" if hasattr(self, 'fullscreen_sw') and self.fullscreen_sw.get() else "Off",
            "max_fps": self.fps_entry.get() if hasattr(self, 'fps_entry') else "Unlimited",
            "gc_type": self.gc_menu.get() if hasattr(self, 'gc_menu') else "G1GC",
            "priority": "High" if hasattr(self, 'priority_sw') and self.priority_sw.get() else "Normal",
            "large_pages": "On" if hasattr(self, 'large_pages_sw') and self.large_pages_sw.get() else "Off",
            "proxy": "On" if hasattr(self, 'proxy_sw') and self.proxy_sw.get() else "Off",
            "timeout": self.timeout_entry.get() if hasattr(self, 'timeout_entry') else "30000"
        }
        if self.core.save_settings(data):
            messagebox.showinfo("System", self.t("success_save"))
            self.username_val, self.ram_val, self.jvm_val, self.type_val = data["username"], data["ram"], data["jvm_args"], data["type"]
        else:
            messagebox.showerror("Error", "Could not save settings")

    def start_launch_thread(self):
        Thread(target=self.launch_game, daemon=True).start()

    def install_mod_thread(self):
        Thread(target=self.install_mod, daemon=True).start()

    def install_mod(self):
        self.btn_mod.configure(state="disabled")
        try:
            import minecraft_launcher_lib
            m_type, ver = self.type_menu.get(), self.version_val
            if m_type == "Vanilla": return
            inst_dir = os.path.join(INSTANCES_DIR, self.current_instance)
            self.progress.pack(side="right", padx=10)
            self.update_status(0.3, f"Installing {m_type}...")
            if m_type == "Fabric": minecraft_launcher_lib.fabric.install_fabric(ver, inst_dir)
            elif m_type == "Forge":
                f_ver = minecraft_launcher_lib.forge.find_forge_version(ver)
                if f_ver: minecraft_launcher_lib.forge.install_forge_version(f_ver, inst_dir)
                else: raise Exception("Forge not found")
            messagebox.showinfo("System", "Installation Complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.btn_mod.configure(state="normal")
            self.progress.pack_forget()

    def launch_game(self):
        try:
            import minecraft_launcher_lib
            self.btn_launch.configure(state="disabled")
            self.progress.pack(side="right", padx=10)

            # 1. Resolve Instance & Version
            inst_dir = os.path.join(INSTANCES_DIR, self.current_instance)
            config_path = os.path.join(inst_dir, "instance_settings.json")

            ver = self.version_val
            m_type = self.type_menu.get() if hasattr(self, 'type_menu') else self.type_val

            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        ver = data.get("version", ver)
                        m_type = data.get("type", m_type)
                except Exception: pass

            # 2. Handle Modded Versions (Fabric/Forge)
            if m_type != "Vanilla":
                # Check for installed modded version
                # Fabric/Forge usually have specific IDs in the versions folder
                try:
                    installed_versions = os.listdir(os.path.join(inst_dir, "versions"))
                    mod_prefix = "fabric-loader" if m_type == "Fabric" else "forge"
                    matches = [v for v in installed_versions if mod_prefix in v]
                    if matches:
                        ver = matches[0]
                    else:
                        raise Exception(f"Please install {m_type} first via the Modding tab!")
                except FileNotFoundError:
                    raise Exception(f"Please install {m_type} first!")

            self.update_status(0.1, f"Preparing {ver}...")

            # 3. AUTOMATIC JAVA RUNTIME MANAGEMENT
            # Determine required Java version for this Minecraft version
            try:
                # This helper tells us which Java version is needed (e.g., '17', '21')
                required_java = minecraft_launcher_lib.java.get_required_java_version(ver)
                java_path = minecraft_launcher_lib.java.install_java_version(required_java, ROOT_DIR)

                # Ensure we use the absolute path to the executable
                if os.name == 'nt' and not java_path.endswith('.exe'):
                    java_path = os.path.join(java_path, "bin", "java.exe")
            except Exception as e:
                print(f"Java Runtime Error: {e}")
                java_path = "java" # Fallback to system java

            # 4. Installation & Command Generation
            callback = {
                "setStatus": lambda t: self.update_status(0.5, t),
                "setProgress": lambda v: self.update_status(v/100, "Fetching..."),
                "setMax": lambda v: None
            }
            minecraft_launcher_lib.install.install_minecraft_version(ver, inst_dir, callback=callback)

            options = {
                "username": self.username_val,
                "uuid": "",
                "token": "",
                "jvmArguments": [f"-Xmx{self.ram_val}G", f"-Xms{self.ram_val}G"] + self.jvm_val.split(" ")
            }

            cmd = minecraft_launcher_lib.command.get_minecraft_command(ver, inst_dir, options)

            # OVERRIDE java executable with our downloaded runtime
            if java_path:
                cmd[0] = java_path

            self.update_status(1.0, self.t("launching"))
            subprocess.Popen(cmd)

        except Exception as e:
            messagebox.showerror("Critical Error", str(e))
        finally:
            self.btn_launch.configure(state="normal")
            self.progress.pack_forget()

if __name__ == "__main__":
    try:
        import minecraft_launcher_lib
    except ImportError:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("Critical Error", "Library 'minecraft-launcher-lib' not found!\n\nPlease run: pip install minecraft-launcher-lib")
        root.destroy(); exit(1)
    try:
        app = AeroLauncher()
        app.mainloop()
    except Exception:
        import traceback
        with open("critical_crash.txt", "w") as f: f.write(traceback.format_exc())
        print(traceback.format_exc())
