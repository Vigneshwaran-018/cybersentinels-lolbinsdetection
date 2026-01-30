import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import queue
from datetime import datetime

event_queue = queue.Queue()

# Global detector state shared with process_watcher
detector_state = {"running": True}

def push_event(message, level="info"):
    event_queue.put((message, level))

def start_dashboard():
    root = tk.Tk()
    root.title("LOLBINS-X | Advanced Endpoint Defense")
    root.geometry("1200x700")
    root.configure(bg="#0a0e27")
    
    # ============ HEADER SECTION ============
    header_frame = tk.Frame(root, bg="#1a1f3a", height=100)
    header_frame.pack(fill=tk.X, padx=0, pady=0)
    
    title_frame = tk.Frame(header_frame, bg="#1a1f3a")
    title_frame.pack(side=tk.LEFT, padx=25, pady=15)
    
    title = tk.Label(
        title_frame,
        text="🛡️Cyber Sentinels Detection System",
        font=("Segoe UI", 28, "bold"),
        fg="#00ffd5",
        bg="#1a1f3a"
    )
    title.pack(anchor=tk.W)

    subtitle = tk.Label(
        title_frame,
        text="Advanced Endpoint Defense & Living-Off-The-Land Detection",
        font=("Segoe UI", 11),
        fg="#94a3b8",
        bg="#1a1f3a"
    )
    subtitle.pack(anchor=tk.W, pady=(2, 0))
    
    # ============ CONTROL BUTTONS SECTION ============
    control_frame = tk.Frame(header_frame, bg="#1a1f3a")
    control_frame.pack(side=tk.RIGHT, padx=25, pady=15)
    
    # Status indicator
    status_label = tk.Label(
        control_frame,
        text="● RUNNING",
        font=("Segoe UI", 11, "bold"),
        fg="#22c55e",
        bg="#1a1f3a"
    )
    status_label.pack(side=tk.LEFT, padx=(0, 20))
    
    def toggle_detection():
        if detector_state["running"]:
            detector_state["running"] = False
            btn_start_stop.config(
                text="▶ START",
                bg="#22c55e",
                fg="#000000"
            )
            status_label.config(
                text="● STOPPED",
                fg="#ef4444"
            )
            push_event(f"[{datetime.now().strftime('%H:%M:%S')}] Detection STOPPED", "info")
        else:
            detector_state["running"] = True
            btn_start_stop.config(
                text="⏹ STOP",
                bg="#ef4444",
                fg="#ffffff"
            )
            status_label.config(
                text="● RUNNING",
                fg="#22c55e"
            )
            push_event(f"[{datetime.now().strftime('%H:%M:%S')}] Detection STARTED", "info")
    
    def clear_logs():
        log_area.config(state=tk.NORMAL)
        log_area.delete("1.0", tk.END)
        log_area.config(state=tk.NORMAL)
        push_event(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Log cleared (GUI only)", "system")
    
    btn_start_stop = tk.Button(
        control_frame,
        text="⏹ STOP",
        command=toggle_detection,
        bg="#ef4444",
        fg="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8,
        border=0,
        activebackground="#ff6b6b",
        activeforeground="#ffffff",
        cursor="hand2"
    )
    btn_start_stop.pack(side=tk.LEFT, padx=8)
    
    btn_reset = tk.Button(
        control_frame,
        text="🗑 RESET LOG",
        command=clear_logs,
        bg="#6366f1",
        fg="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8,
        border=0,
        activebackground="#818cf8",
        activeforeground="#ffffff",
        cursor="hand2"
    )
    btn_reset.pack(side=tk.LEFT, padx=8)
    
    # ============ MAIN CONTENT SECTION ============
    content_frame = tk.Frame(root, bg="#0a0e27")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Log label
    log_label = tk.Label(
        content_frame,
        text="📋 DETECTION EVENT LOG",
        font=("Segoe UI", 12, "bold"),
        fg="#00ffd5",
        bg="#0a0e27"
    )
    log_label.pack(anchor=tk.W, pady=(0, 8))
    
    log_area = ScrolledText(
        content_frame,
        width=150,
        height=26,
        font=("Courier New", 9), 
        bg="#020617",
        fg="#e5e7eb",
        insertbackground="#00ffd5",
        borderwidth=1,
        relief=tk.FLAT,
        wrap=tk.WORD
    )
    log_area.pack(fill=tk.BOTH, expand=True)
    
    # Configure text tags
    log_area.tag_config("low", foreground="#22c55e")        
    log_area.tag_config("medium", foreground="#facc15")     
    log_area.tag_config("high", foreground="#ef4444")
    log_area.tag_config("critical", foreground="#ff0033")       
    log_area.tag_config("blocked", foreground="#ff00ff")    
    log_area.tag_config("info", foreground="#38bdf8")       
    log_area.tag_config("system", foreground="#a78bfa")
    
    # ============ FOOTER SECTION ============
    footer_frame = tk.Frame(root, bg="#1a1f3a", height=40)
    footer_frame.pack(fill=tk.X, padx=0, pady=0, side=tk.BOTTOM)
    
    footer_text = tk.Label(
        footer_frame,
        text="© 2026 LOLBINS-X Security Engine | Press ⏹ STOP to pause detection | 🗑 RESET LOG to clear (GUI only)",
        font=("Segoe UI", 9),
        fg="#4b5563",
        bg="#1a1f3a"
    )
    footer_text.pack(pady=8)

    def update_logs():
        while not event_queue.empty():
            msg, level = event_queue.get()
            log_area.insert(tk.END, msg + "\n", level)
            log_area.see(tk.END)
        root.after(250, update_logs)

    update_logs()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
