# ================================================
# FIFO Page Replacement Algorithm Simulator (GUI)
# Modern Dark Theme using CustomTkinter
# ================================================

import customtkinter as ctk
from tkinter import messagebox

# Set global appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FIFOSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FIFO Page Replacement Algorithm Simulator")
        width = 1300
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        self.frames_count = 3
        self.reference_string = []
        self.create_widgets()

    # -------------------------------------------------------------
    # UI SETUP
    # -------------------------------------------------------------
    def create_widgets(self):
        # Header
        title = ctk.CTkLabel(
            self,
            text="FIFO Page Replacement Simulator",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(pady=25)

        subtitle = ctk.CTkLabel(
            self,
            text="Visual Step-by-Step Animation",
            font=ctk.CTkFont(size=16),
            text_color="#8888FF"
        )
        subtitle.pack(pady=(0, 20))

        # Input Section
        input_frame = ctk.CTkFrame(self, corner_radius=10)
        input_frame.pack(pady=10, padx=60, fill="x")

        ctk.CTkLabel(
            input_frame,
            text="Reference String (max 10 pages):",
            font=ctk.CTkFont(size=15)
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.entry_ref = ctk.CTkEntry(
            input_frame,
            width=450,
            height=35,
            placeholder_text="Separate pages with spaces",
            font=ctk.CTkFont(size=14)
        )
        self.entry_ref.grid(row=0, column=1, padx=20, pady=15)

        ctk.CTkLabel(
            input_frame,
            text="Number of Frames:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")

        self.frame_var = ctk.StringVar(value="3")
        combo = ctk.CTkComboBox(
            input_frame,
            values=["3", "4", "5"],
            variable=self.frame_var,
            width=120,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        combo.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=20)

        self.simulate_btn = ctk.CTkButton(
            btn_frame,
            text="Start Simulation",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            height=50,
            corner_radius=10,
            command=self.start_simulation
        )
        self.simulate_btn.pack(side="left", padx=30)

        self.reset_btn = ctk.CTkButton(
            btn_frame,
            text="Reset All",
            font=ctk.CTkFont(size=15),
            width=200,
            height=50,
            corner_radius=12,
            fg_color="gray30",
            hover_color="gray20",
            command=self.reset
        )
        self.reset_btn.pack(side="left", padx=30)

        # Result Display Area
        self.result_text = ctk.CTkTextbox(
            self,
            width=1200,
            height=600,
            font=ctk.CTkFont(family="Consolas", size=15),
            corner_radius=15
        )
        self.result_text.pack(pady=20, padx=50)

    # -------------------------------------------------------------
    # START SIMULATION
    # -------------------------------------------------------------
    def start_simulation(self):
        """Validate inputs and begin FIFO animation."""
        try:
            ref_input = self.entry_ref.get().strip()
            if not ref_input:
                messagebox.showwarning("Empty Input", "Please enter a reference string!")
                return

            pages = [int(x) for x in ref_input.split()]
            if len(pages) > 10:
                messagebox.showerror("Too Many Pages", "Maximum 10 pages allowed.")
                return

            self.frames_count = int(self.frame_var.get())
            self.reference_string = pages

            self.run_fifo_simulation()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer pages.")

    # -------------------------------------------------------------
    # FIFO SIMULATION
    # -------------------------------------------------------------
    def run_fifo_simulation(self):
        """Initialize variables and start animation."""
        self.result_text.delete("1.0", "end")

        self.frames = []
        self.queue = []
        self.page_faults = 0
        self.current_step = 0

        # Header
        header = f"{'=' * 25} FIFO SIMULATION {'=' * 25}\n"
        header += f"Reference String: {self.reference_string}\n"
        header += f"Number of Frames: {self.frames_count}\n\n"
        header += f"{'Step':<6} {'Page':<8} {'Frames After':<30} {'Fault':<8}\n"
        header += "─" * 70 + "\n"
        self.result_text.insert("end", header)

        self.animate_step()  # start animation

    # -------------------------------------------------------------
    # ANIMATION FUNCTION
    # -------------------------------------------------------------
    def animate_step(self):
        """Perform each simulation step with non-blocking updates."""
        if self.current_step >= len(self.reference_string):
            summary = f"\n{'=' * 70}\n"
            summary += f"TOTAL PAGE FAULTS: {self.page_faults}\n"
            hit_ratio = ((len(self.reference_string) - self.page_faults) / len(self.reference_string)) * 100
            summary += f"HIT RATIO: {hit_ratio:.1f}%\n"
            summary += f"{'=' * 70}\n"
            self.result_text.insert("end", summary)
            return

        step = self.current_step + 1
        page = self.reference_string[self.current_step]
        fault = "No"

        if page not in self.frames:
            self.page_faults += 1
            fault = "YES"

            if len(self.frames) < self.frames_count:
                self.frames.append(page)
                self.queue.append(page)
            else:
                old = self.queue.pop(0)
                self.frames.remove(old)
                self.frames.append(page)
                self.queue.append(page)

        # Frame display formatting
        display_frames = " ".join(map(str, self.frames))
        if len(self.frames) < self.frames_count:
            display_frames += "  " + "  - " * (self.frames_count - len(self.frames))

        line = f"{step:<6} {page:<8} {display_frames:<30} {fault:<8}\n"
        self.result_text.insert("end", line)
        self.result_text.see("end")

        self.current_step += 1

        # Schedule next step (no freezing)
        self.after(700, self.animate_step)

    # -------------------------------------------------------------
    # RESET FUNCTION
    # -------------------------------------------------------------
    def reset(self):
        self.entry_ref.delete(0, "end")
        self.frame_var.set("3")
        self.result_text.delete("1.0", "end")


# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    app = FIFOSimulator()
    app.mainloop()