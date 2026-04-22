from __future__ import annotations

import threading

import customtkinter as ctk

from core.assistant import JarvisAssistant
from core.config import load_config
from core.memory import MemoryStore
from core.state import AssistantState


class JarvisApp:
    def __init__(self) -> None:
        self.config = load_config()
        self.state = AssistantState()
        self.memory = MemoryStore()

        ctk.set_appearance_mode("dark")
        self.app = ctk.CTk()
        self.app.title("J.A.R.V.I.S")
        self.app.geometry("240x130")
        self.app.overrideredirect(True)
        self.app.attributes("-topmost", True)
        self.app.attributes("-alpha", 0.92)
        self.app.configure(fg_color="#08080C")

        self.app.update_idletasks()
        self.app.geometry(f"+{self.app.winfo_screenwidth() - 260}+{self.app.winfo_screenheight() - 180}")

        self._build_ui()
        self.assistant = JarvisAssistant(
            config=self.config,
            state=self.state,
            memory=self.memory,
            update_ui=self.update_ui,
        )

    def _build_ui(self) -> None:
        def start_move(event):
            self.app.x = event.x
            self.app.y = event.y

        def do_move(event):
            x = self.app.winfo_x() + (event.x - self.app.x)
            y = self.app.winfo_y() + (event.y - self.app.y)
            self.app.geometry(f"+{x}+{y}")

        title_frame = ctk.CTkFrame(self.app, corner_radius=0, fg_color="#101016", height=26)
        title_frame.pack(fill="x", side="top")
        title_frame.bind("<ButtonPress-1>", start_move)
        title_frame.bind("<B1-Motion>", do_move)

        title_label = ctk.CTkLabel(title_frame, text="⬡ J.A.R.V.I.S", font=("Consolas", 11, "bold"), text_color="#00E5FF")
        title_label.pack(side="left", padx=8, pady=3)
        title_label.bind("<ButtonPress-1>", start_move)
        title_label.bind("<B1-Motion>", do_move)

        close_btn = ctk.CTkButton(
            title_frame,
            text="✕",
            width=24,
            height=20,
            font=("Consolas", 12, "bold"),
            fg_color="transparent",
            hover_color="#FF4444",
            text_color="#666666",
            command=self.close_app,
            corner_radius=4,
        )
        close_btn.pack(side="right", padx=4, pady=2)

        separator = ctk.CTkFrame(self.app, height=1, fg_color="#00E5FF", corner_radius=0)
        separator.pack(fill="x")

        self.status_label = ctk.CTkLabel(self.app, text="💤 Bekleme", font=("Consolas", 10), text_color="#444444", height=18)
        self.status_label.pack(pady=2)

        btn_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        btn_frame.pack(pady=2, fill="x", padx=8)

        self.sw_mon = ctk.CTkSwitch(
            btn_frame,
            text="Ekran",
            font=("Consolas", 10),
            width=40,
            command=self.toggle_monitor,
            progress_color="#00E5FF",
            button_color="#00E5FF",
            button_hover_color="#00B8D4",
        )
        self.sw_mon.pack(side="left", padx=4)

        self.sw_mic = ctk.CTkSwitch(
            btn_frame,
            text="Mikrofon",
            font=("Consolas", 10),
            width=40,
            command=self.toggle_mic,
            progress_color="#00E5FF",
            button_color="#00E5FF",
            button_hover_color="#00B8D4",
        )
        self.sw_mic.pack(side="right", padx=4)

    def update_ui(self, text: str, color: str = "white") -> None:
        try:
            self.app.after(0, lambda: self.status_label.configure(text=text, text_color=color))
        except Exception:
            pass

    def toggle_monitor(self) -> None:
        self.state.monitor_active = self.sw_mon.get() == 1
        if self.state.monitor_active:
            self.update_ui("👁️ İzleniyor", "#00FFDD")
        elif not self.state.mic_active:
            self.update_ui("💤 Bekleme", "#444444")

    def toggle_mic(self) -> None:
        self.state.mic_active = self.sw_mic.get() == 1
        if self.state.mic_active:
            self.update_ui("🎙️ Dinleniyor", "#00FFDD")
        elif not self.state.monitor_active:
            self.update_ui("💤 Bekleme", "#444444")

    def close_app(self) -> None:
        self.state.stop_event.set()
        self.app.destroy()

    def run(self) -> None:
        print("═══════════════════════════════════════")
        print("  J.A.R.V.I.S v4.0 | Personal Assistant")
        print("═══════════════════════════════════════")
        threading.Thread(target=self.assistant.monitor_loop, daemon=True).start()
        threading.Thread(target=self.assistant.continuous_mic_loop, daemon=True).start()
        self.app.mainloop()


if __name__ == "__main__":
    JarvisApp().run()
