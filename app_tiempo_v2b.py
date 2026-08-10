import calendar
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import locale

# Intentar configurar el idioma a español para las fechas
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    pass

class TimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tiempo - V1, V2, V3")

        # Sistema de pestañas principal para separar V1, V2 y V3
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Inicializar las vistas solicitadas
        self.init_v1()
        self.init_v2()
        self.init_v3()

    def init_v1(self):
        """V1: Hora actual"""
        self.frame_v1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_v1, text="V1 - Hora")

        lbl_title = ttk.Label(self.frame_v1, text="Hora Actual del Sistema", font=("Segoe UI", 14, "bold"))
        lbl_title.pack(pady=20)

        format_frame = ttk.Frame(self.frame_v1)
        format_frame.pack(pady=5)

        self.use_24h = tk.BooleanVar(value=False)
        ttk.Label(format_frame, text="Formato de hora:").pack(side='left', padx=(0, 10))
        ttk.Radiobutton(format_frame, text="24H", variable=self.use_24h, value=True, command=self.update_time).pack(side='left')
        ttk.Radiobutton(format_frame, text="12H", variable=self.use_24h, value=False, command=self.update_time).pack(side='left')

        self.lbl_time = tk.Label(self.frame_v1, text="", font=("Segoe UI", 28, "bold"), fg="#007ACC")
        self.lbl_time.pack(pady=(20, 5))

        self.lbl_full_date = ttk.Label(self.frame_v1, text="", font=("Segoe UI", 12))
        self.lbl_full_date.pack(pady=(0, 10))

        self.calendar_frames = []
        self.calendar_cells = []

        for title in ["Mes anterior", "Mes actual", "Mes siguiente"]:
            section = ttk.Frame(self.frame_v1)
            section.pack(pady=(0, 8), fill='x')

            label = ttk.Label(section, text=title, font=("Segoe UI", 10, "bold"))
            label.pack(pady=(0, 4))

            grid_frame = ttk.Frame(section)
            grid_frame.pack()

            day_names = ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"]
            for idx, name in enumerate(day_names):
                ttk.Label(grid_frame, text=name, font=("Segoe UI", 8, "bold"), width=4, anchor='center').grid(row=0, column=idx)

            cells = []
            for week in range(6):
                row_cells = []
                for col in range(7):
                    cell = tk.Label(grid_frame, text="", font=("Segoe UI", 8), width=4, height=1, anchor='center', borderwidth=1, relief='ridge')
                    cell.grid(row=week + 1, column=col, padx=0, pady=0)
                    row_cells.append(cell)
                cells.append(row_cells)

            self.calendar_frames.append((label, cells))
            self.calendar_cells.append(cells)

        self.update_time()

    def update_time(self):
        now = datetime.now()
        if self.use_24h.get():
            current_time = now.strftime("%H:%M:%S")
        else:
            current_time = now.strftime("%I:%M:%S %p")

        date_str = f"{now.strftime('%a').lower()}-{now.day}-{now.strftime('%b').lower()}-{now.strftime('%y')}"

        self.lbl_time.config(text=current_time)
        self.lbl_full_date.config(text=date_str)

        months = []
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        next_month = now.month + 1 if now.month < 12 else 1
        next_year = now.year if now.month < 12 else now.year + 1
        months.append((prev_month, prev_year))
        months.append((now.month, now.year))
        months.append((next_month, next_year))

        for idx, (month, year) in enumerate(months):
            month_label = f"{calendar.month_name[month].capitalize()} {year}"
            self.calendar_frames[idx][0].config(text=month_label)

            month_days = calendar.Calendar(firstweekday=calendar.SUNDAY).monthdayscalendar(year, month)
            weeks = len(month_days)
            for week_idx in range(6):
                row_visible = week_idx < weeks
                for col_idx in range(7):
                    day = month_days[week_idx][col_idx] if row_visible else 0
                    label_text = str(day) if day != 0 else ""
                    cell = self.calendar_cells[idx][week_idx][col_idx]
                    cell.config(text=label_text)
                    if year == now.year and month == now.month and day == now.day:
                        cell.config(background="#cfeaff")
                    else:
                        cell.config(background="SystemButtonFace")
                    if row_visible:
                        cell.grid()
                    else:
                        cell.grid_remove()

        self.root.after(1000, self.update_time)

    def init_v2(self):
        """V2: Calendario anual con selector de año"""
        self.frame_v2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_v2, text="V2 - Fecha")

        now = datetime.now()
        current_year = now.year

        header_frame = ttk.Frame(self.frame_v2)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))

        lbl_title = ttk.Label(header_frame, text="Calendario Anual", font=("Segoe UI", 14, "bold"))
        lbl_title.pack(side='left')

        selector_frame = ttk.Frame(header_frame)
        selector_frame.pack(side='right')

        ttk.Label(selector_frame, text="Año:").pack(side='left', padx=(0, 5))

        self.year_var = tk.IntVar(value=current_year)
        year_range = list(range(current_year - 75, current_year + 26))
        year_values = [str(year) for year in year_range]

        self.year_combo = ttk.Combobox(selector_frame, values=year_values, width=6, textvariable=self.year_var, state='readonly')
        self.year_combo.pack(side='left')
        self.year_combo.set(str(current_year))
        self.year_combo.bind('<<ComboboxSelected>>', lambda event: self.update_year_calendar())

        self.btn_current_year = ttk.Button(selector_frame, text="Año actual", command=self.reset_to_current_year)
        self.btn_current_year.pack(side='left', padx=(8, 0))

        self.lbl_calendar_year = ttk.Label(self.frame_v2, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_calendar_year.pack(pady=(0, 10))

        self.calendar_container = ttk.Frame(self.frame_v2)
        self.calendar_container.pack(fill='both', expand=True, padx=10, pady=5)

        self.calendar_cells = []

        day_names = ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"]
        for month in range(1, 13):
            month_frame = ttk.Frame(self.calendar_container, relief='ridge', borderwidth=1)
            month_frame.grid(row=(month - 1) // 4, column=(month - 1) % 4, padx=5, pady=5, sticky='nsew')

            month_name = calendar.month_name[month].capitalize()
            ttk.Label(month_frame, text=month_name, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=7, pady=(6, 4))

            for col, name in enumerate(day_names):
                ttk.Label(month_frame, text=name, font=("Segoe UI", 8, "bold"), anchor='center').grid(row=1, column=col, padx=1, pady=1, sticky='nsew')

            cells = []
            for week in range(6):
                row_cells = []
                for col in range(7):
                    cell = tk.Label(month_frame, text="", font=("Segoe UI", 8), width=3, height=1,
                                    relief='ridge', borderwidth=1, anchor='center', background="SystemButtonFace")
                    cell.grid(row=week + 2, column=col, padx=1, pady=1, sticky='nsew')
                    row_cells.append(cell)
                cells.append(row_cells)
            self.calendar_cells.append(cells)

        for row_index in range(3):
            self.calendar_container.grid_rowconfigure(row_index, weight=1)
        for col_index in range(4):
            self.calendar_container.grid_columnconfigure(col_index, weight=1)

        self.current_year = current_year
        self.update_year_calendar()

    def reset_to_current_year(self):
        self.year_var.set(self.current_year)
        self.year_combo.set(str(self.current_year))
        self.update_year_calendar()

    def update_year_calendar(self):
        selected_year = self.year_var.get()
        today = datetime.now()
        today_day = today.day if selected_year == today.year else None
        self.lbl_calendar_year.config(text=f"Año seleccionado: {selected_year}")

        for month_idx in range(12):
            month = month_idx + 1
            month_days = calendar.Calendar(firstweekday=calendar.SUNDAY).monthdayscalendar(selected_year, month)
            for week_idx in range(6):
                for col_idx in range(7):
                    cell = self.calendar_cells[month_idx][week_idx][col_idx]
                    day = month_days[week_idx][col_idx] if week_idx < len(month_days) else 0
                    if day == 0:
                        cell.config(text="", background="SystemButtonFace")
                    else:
                        cell.config(text=str(day))
                        if selected_year == today.year and month == today.month and day == today.day:
                            cell.config(background="#ffecb3")
                        else:
                            cell.config(background="SystemButtonFace")

    def init_v3(self):
        """V3: Cronómetro y Timer"""
        self.frame_v3 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_v3, text="V3 - Utilidades")

        # Sub-pestañas para separar el cronómetro del temporizador
        notebook_v3 = ttk.Notebook(self.frame_v3)
        notebook_v3.pack(fill='both', expand=True, padx=5, pady=5)

        # --- Sub-sección: Cronómetro ---
        self.tab_cron = ttk.Frame(notebook_v3)
        notebook_v3.add(self.tab_cron, text="Cronómetro")

        self.stopwatch_time = 0
        self.is_running_stopwatch = False

        self.lbl_stopwatch = ttk.Label(self.tab_cron, text="00:00:00", font=("Segoe UI", 24, "bold"))
        self.lbl_stopwatch.pack(pady=20)

        btn_frame_sw = ttk.Frame(self.tab_cron)
        btn_frame_sw.pack(pady=10)

        self.btn_sw_start = ttk.Button(btn_frame_sw, text="Iniciar", command=self.start_stopwatch)
        self.btn_sw_start.pack(side='left', padx=5)

        self.btn_sw_stop = ttk.Button(btn_frame_sw, text="Detener", command=self.stop_stopwatch)
        self.btn_sw_stop.pack(side='left', padx=5)

        self.btn_sw_reset = ttk.Button(btn_frame_sw, text="Reiniciar", command=self.reset_stopwatch)
        self.btn_sw_reset.pack(side='left', padx=5)

        # --- Sub-sección: Timer (Cuenta regresiva) ---
        self.tab_timer = ttk.Frame(notebook_v3)
        notebook_v3.add(self.tab_timer, text="Timer")

        self.timer_seconds = 0
        self.is_running_timer = False

        self.lbl_timer = ttk.Label(self.tab_timer, text="00:00", font=("Segoe UI", 24, "bold"))
        self.lbl_timer.pack(pady=10)

        entry_frame = ttk.Frame(self.tab_timer)
        entry_frame.pack(pady=5)

        ttk.Label(entry_frame, text="Segundos:").pack(side='left', padx=5)
        self.entry_timer = ttk.Entry(entry_frame, width=10)
        self.entry_timer.pack(side='left', padx=5)
        self.entry_timer.insert(0, "60")

        btn_frame_t = ttk.Frame(self.tab_timer)
        btn_frame_t.pack(pady=10)

        self.btn_t_start = ttk.Button(btn_frame_t, text="Iniciar", command=self.start_timer)
        self.btn_t_start.pack(side='left', padx=5)

        self.btn_t_stop = ttk.Button(btn_frame_t, text="Detener", command=self.stop_timer)
        self.btn_t_stop.pack(side='left', padx=5)

    def start_stopwatch(self):
        if not self.is_running_stopwatch:
            self.is_running_stopwatch = True
            self.update_stopwatch()

    def stop_stopwatch(self):
        self.is_running_stopwatch = False

    def reset_stopwatch(self):
        self.is_running_stopwatch = False
        self.stopwatch_time = 0
        self.lbl_stopwatch.config(text="00:00:00")

    def update_stopwatch(self):
        if self.is_running_stopwatch:
            self.stopwatch_time += 1
            hours = self.stopwatch_time // 3600
            minutes = (self.stopwatch_time % 3600) // 60
            seconds = self.stopwatch_time % 60
            self.lbl_stopwatch.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_stopwatch)

    def start_timer(self):
        if not self.is_running_timer:
            try:
                self.timer_seconds = int(self.entry_timer.get())
            except ValueError:
                self.timer_seconds = 60
            self.is_running_timer = True
            self.update_timer()

    def stop_timer(self):
        self.is_running_timer = False

    def update_timer(self):
        if self.is_running_timer and self.timer_seconds > 0:
            mins = self.timer_seconds // 60
            secs = self.timer_seconds % 60
            self.lbl_timer.config(text=f"{mins:02d}:{secs:02d}")
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.is_running_timer and self.timer_seconds == 0:
            self.lbl_timer.config(text="¡Tiempo!")
            self.is_running_timer = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeApp(root)
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
    root.mainloop()