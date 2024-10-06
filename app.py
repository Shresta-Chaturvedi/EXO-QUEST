import tkinter as tk
from tkinter import Canvas, Button, Frame, Label, messagebox
import math

# Sample Solar System Data
solar_system_data = {
    'Sun': {'size': 30, 'color': '#FFD700'},
    'Mercury': {'size': 3, 'color': '#B0C4DE'},
    'Venus': {'size': 5, 'color': '#FF6347'},
    'Earth': {'size': 6, 'color': '#1E90FF'},
    'Mars': {'size': 4, 'color': '#FF4500'},
    'Jupiter': {'size': 12, 'color': '#8B4513'},
    'Saturn': {'size': 10, 'color': '#FFD700'},
    'Uranus': {'size': 8, 'color': '#AFEEEE'},
    'Neptune': {'size': 7, 'color': '#00008B'},
}

# Expanded Exoplanet Data
exoplanet_data = {
    'Kepler-186f': {'details': 'Earth-sized exoplanet.', 'color': '#00FF00', 'orbital_radius': 200},
    'TRAPPIST-1e': {'details': 'Potentially habitable exoplanet.', 'color': '#FF00FF', 'orbital_radius': 250},
    'Proxima Centauri b': {'details': 'Closest exoplanet to Earth.', 'color': '#0000FF', 'orbital_radius': 300},
}

class ExoplanetExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exoplanet and Star Exploration App")
        self.geometry("900x600")
        self.configure(bg="#1E1E1E")
        self.zoom_factor = 1.0  # Zoom factor

        # Main Frame
        self.main_frame = Frame(self, bg="#1E1E1E")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Navigation Buttons
        self.nav_frame = Frame(self.main_frame, bg="#2E2E2E", bd=2, relief=tk.RAISED)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.show_solar_system_button = Button(self.nav_frame, text="Solar System", command=self.show_solar_system, bg="#007ACC", fg="white", font=("Helvetica", 12))
        self.show_solar_system_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.show_constellation_button = Button(self.nav_frame, text="Draw Constellation", command=self.show_constellation_frame, bg="#FFA500", fg="white", font=("Helvetica", 12))
        self.show_constellation_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Animation Canvas
        self.canvas = Canvas(self.main_frame, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.angle = 0  # Starting angle for animation
        self.exoplanet_angle = 0  # Starting angle for exoplanet animation
        self.constellation_points = []

        self.show_solar_system()

        # Bind mouse scroll for zoom functionality
        self.canvas.bind("<MouseWheel>", self.zoom)

    def show_solar_system(self):
        self.canvas.delete("all")
        self.constellation_points.clear()  # Clear any previous constellation points
        self.create_solar_system_ui()

    def create_solar_system_ui(self):
        # UI for Solar System
        self.label = Label(self.canvas, text="Select a Planet:", font=("Helvetica", 14), bg="#1E1E1E", fg="white")
        self.canvas.create_window(100, 30, window=self.label)

        self.body_var = tk.StringVar(self)
        self.body_var.set('Sun')
        self.body_menu = tk.OptionMenu(self.canvas, self.body_var, *solar_system_data.keys())
        self.canvas.create_window(100, 60, window=self.body_menu)

        self.show_body_button = Button(self.canvas, text="Show Body", command=self.show_body, bg="#007ACC", fg="white", font=("Helvetica", 10))
        self.canvas.create_window(100, 100, window=self.show_body_button)

        self.animate_button = Button(self.canvas, text="Start Animation", command=self.start_animation, bg="#28A745", fg="white", font=("Helvetica", 10))
        self.canvas.create_window(100, 140, window=self.animate_button)

        self.exoplanet_var = tk.StringVar(self)
        self.exoplanet_var.set('Kepler-186f')
        self.exoplanet_menu = tk.OptionMenu(self.canvas, self.exoplanet_var, *exoplanet_data.keys())
        self.canvas.create_window(100, 180, window=self.exoplanet_menu)

        self.show_exoplanet_button = Button(self.canvas, text="Show Exoplanet Details", command=self.show_exoplanet_details, bg="#FF4500", fg="white", font=("Helvetica", 10))
        self.canvas.create_window(100, 220, window=self.show_exoplanet_button)

    def show_body(self):
        body_name = self.body_var.get()
        if body_name in solar_system_data:
            self.canvas.delete("all")
            self.create_solar_system_ui()
            size = solar_system_data[body_name]['size'] * self.zoom_factor
            color = solar_system_data[body_name]['color']
            self.canvas.create_oval(440 - size, 290 - size, 440 + size, 290 + size, fill=color)

    def start_animation(self):
        self.canvas.delete("all")
        self.angle = 0  # Reset angle for each animation
        self.animate_planets()
        self.animate_exoplanets()

    def animate_planets(self):
        self.canvas.delete("all")
        # Draw the Sun
        self.canvas.create_oval(440 - solar_system_data['Sun']['size'], 290 - solar_system_data['Sun']['size'], 440 + solar_system_data['Sun']['size'], 290 + solar_system_data['Sun']['size'], fill=solar_system_data['Sun']['color'])

        # Draw planets
        for planet_name, planet_data in solar_system_data.items():
            if planet_name == 'Sun':
                continue
            distance = 40 * (planet_data['size'] + 20) * self.zoom_factor  # Adjust distance
            x = 440 + distance * math.cos(math.radians(self.angle))
            y = 290 + distance * math.sin(math.radians(self.angle))
            planet_size = planet_data['size'] * self.zoom_factor * 0.5  # Smaller size
            self.canvas.create_oval(x - planet_size, y - planet_size, x + planet_size, y + planet_size, fill=planet_data['color'])

        self.angle += 2  # Increment the angle for rotation
        if self.angle >= 360:
            self.angle = 0  # Reset the angle
        self.after(50, self.animate_planets)

    def animate_exoplanets(self):
        selected_exoplanet = self.exoplanet_var.get()
        if selected_exoplanet in exoplanet_data:
            exoplanet_info = exoplanet_data[selected_exoplanet]
            distance = exoplanet_info['orbital_radius'] * self.zoom_factor

            exoplanet_x = 440 + distance * math.cos(math.radians(self.exoplanet_angle))
            exoplanet_y = 290 + distance * math.sin(math.radians(self.exoplanet_angle))

            # Draw the exoplanet
            self.canvas.create_oval(exoplanet_x - 5 * self.zoom_factor, exoplanet_y - 5 * self.zoom_factor, exoplanet_x + 5 * self.zoom_factor, exoplanet_y + 5 * self.zoom_factor, fill=exoplanet_info['color'])

            # Increment angle for exoplanet
            self.exoplanet_angle += 3  # Rotate faster for visibility
            if self.exoplanet_angle >= 360:
                self.exoplanet_angle = 0  # Reset the angle

        self.after(100, self.animate_exoplanets)

    def zoom(self, event):
        # Zoom functionality
        if event.delta > 0:  # Scroll up
            self.zoom_factor *= 1.1
        else:  # Scroll down
            self.zoom_factor *= 0.9
        self.show_body()  # Refresh to apply zoom factor

    def show_exoplanet_details(self):
        exoplanet_name = self.exoplanet_var.get()
        if exoplanet_name in exoplanet_data:
            details = exoplanet_data[exoplanet_name]['details']
            messagebox.showinfo("Exoplanet Details", f"{exoplanet_name}: {details}")
        else:
            messagebox.showwarning("Warning", "Select a valid exoplanet.")

    def show_constellation_frame(self):
        self.canvas.delete("all")
        self.constellation_points.clear()  # Clear any previous points
        self.create_constellation_ui()

    def create_constellation_ui(self):
        self.label = Label(self.canvas, text="Draw a Constellation:", font=("Helvetica", 14), bg="#1E1E1E", fg="white")
        self.canvas.create_window(450, 30, window=self.label)

        self.constellation_button = Button(self.canvas, text="Add Star", command=self.add_star, bg="#007ACC", fg="white", font=("Helvetica", 10))
        self.canvas.create_window(450, 60, window=self.constellation_button)

        self.clear_constellation_button = Button(self.canvas, text="Clear Constellation", command=self.clear_constellation, bg="#FF4500", fg="white", font=("Helvetica", 10))
        self.canvas.create_window(450, 100, window=self.clear_constellation_button)

        self.canvas.bind("<Button-1>", self.draw_constellation)

    def add_star(self):
        self.constellation_points.append((440, 290))  # Add star at the center for simplicity
        self.redraw_constellation()

    def clear_constellation(self):
        self.canvas.delete("all")
        self.constellation_points.clear()
        self.create_constellation_ui()

    def draw_constellation(self, event):
        if len(self.constellation_points) < 2:
            self.constellation_points.append((event.x, event.y))
        else:
            self.constellation_points.append((event.x, event.y))
            self.redraw_constellation()
            self.constellation_points.clear()  # Reset after drawing

    def redraw_constellation(self):
        for point in self.constellation_points:
            x, y = point
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="white")

        if len(self.constellation_points) > 1:
            self.canvas.create_line(self.constellation_points, fill="white")

if __name__ == "__main__":
    app = ExoplanetExplorerApp()
    app.mainloop()
