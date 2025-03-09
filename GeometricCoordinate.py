import tkinter as tk
from tkinter import ttk, messagebox
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_cuboid(ax, cuboid):
    (x_min, y_min, z_min, x_max, y_max, z_max) = cuboid
    r = [[x_min, x_max], [y_min, y_max], [z_min, z_max]]
    
    vertices = np.array([[x, y, z] for x in r[0] for y in r[1] for z in r[2]])
    
    faces = [
        [vertices[j] for j in [0, 1, 3, 2]],
        [vertices[j] for j in [4, 5, 7, 6]],
        [vertices[j] for j in [0, 1, 5, 4]],
        [vertices[j] for j in [2, 3, 7, 6]],
        [vertices[j] for j in [0, 2, 6, 4]],
        [vertices[j] for j in [1, 3, 7, 5]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

def plot_sphere(ax, sphere):
    (cx, cy, cz, r) = sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = cx + r * np.outer(np.cos(u), np.sin(v))
    y = cy + r * np.outer(np.sin(u), np.sin(v))
    z = cz + r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color='r', alpha=0.3)

def plot_pyramid(ax, pyramid):
    (apex_x, apex_y, apex_z, base1_x, base1_y, base1_z, base2_x, base2_y, base2_z, base3_x, base3_y, base3_z, base4_x, base4_y, base4_z) = pyramid
    apex = (apex_x, apex_y, apex_z)
    base1 = (base1_x, base1_y, base1_z)
    base2 = (base2_x, base2_y, base2_z)
    base3 = (base3_x, base3_y, base3_z)
    base4 = (base4_x, base4_y, base4_z)

    vertices = [apex, base1, base2, base3, base4]
    
    faces = [
        [apex, base1, base2],
        [apex, base2, base3],
        [apex, base3, base4],
        [apex, base4, base1],
        [base1, base2, base3, base4]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors='yellow', linewidths=1, edgecolors='black', alpha=.25))


def calculate_intersection(shapes):
    # Function to calculate intersection points
    # Logic to calculate intersection points between shapes
    # Return intersection points as a list of tuples (x, y, z)
    return [(0, 1, 0), (0, 2, 0), (-1, -1, 0)]  # Placeholder example points


def create_plot(cuboid, sphere, pyramid, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the shapes
    if cuboid:
        plot_cuboid(ax, cuboid)
    if sphere:
        plot_sphere(ax, sphere)
    if pyramid:
        plot_pyramid(ax, pyramid)

    # Plot intersection points
    if points:
        xs, ys, zs = zip(*points)
        ax.scatter(xs, ys, zs, c='r', marker='o')
    
    # Set labels and display options
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Shapes Display')

    return fig



def create_input_window():
    global cuboid_entry, sphere_entry, pyramid_entry, cuboid_input, sphere_input, pyramid_input

    def open_type_selection_window():
        cuboid_coords = cuboid_entry.get().split(',')
        sphere_coords = sphere_entry.get().split(',')
        pyramid_coords = pyramid_entry.get().split(',')
        
        # Convert input coordinates to tuples
        cuboid_input = tuple(map(float, cuboid_coords)) if cuboid_coords != [''] else None
        sphere_input = tuple(map(float, sphere_coords)) if sphere_coords != [''] else None
        pyramid_input = tuple(map(float, pyramid_coords)) if pyramid_coords != [''] else None
        
        root.destroy()
        create_type_selection_window(cuboid_input, sphere_input, pyramid_input)
    
    root = tk.Tk()
    root.title("Shape Coordinates Input")
    
    # Labels and entry fields for inputting coordinates
    ttk.Label(root, text="Cuboid Coordinates (x_min, y_min, z_min, x_max, y_max, z_max):").grid(row=0, column=0, sticky=tk.W)
    cuboid_entry = ttk.Entry(root)
    cuboid_entry.grid(row=1, column=0, sticky=tk.W)
    
    ttk.Label(root, text="Sphere Coordinates (cx, cy, cz, r):").grid(row=2, column=0, sticky=tk.W)
    sphere_entry = ttk.Entry(root)
    sphere_entry.grid(row=3, column=0, sticky=tk.W)

    ttk.Label(root, text="Pyramid Apex Coordinates (apex_x, apex_y, apex_z):").grid(row=4, column=0, sticky=tk.W)
    pyramid_entry = ttk.Entry(root)
    pyramid_entry.grid(row=5, column=0, sticky=tk.W)
    
    # Button to proceed to shape selection window
    ttk.Button(root, text="Next", command=open_type_selection_window).grid(row=6, column=0, sticky=tk.W)
    
    root.mainloop()




def create_type_selection_window(cuboid_input, sphere_input, pyramid_input):
    def open_plot_window():
        selected_shapes = [shape for shape, var in shape_vars.items() if var.get()]

        if not selected_shapes:
            messagebox.showerror("Error", "Please select at least one shape.")
            return

        shapes = {
            "cuboid": cuboid_input if "cuboid" in selected_shapes else None,
            "sphere": sphere_input if "sphere" in selected_shapes else None,
            "pyramid": pyramid_input if "pyramid" in selected_shapes else None
        }

        intersection_points = calculate_intersection(shapes)

        create_plot_window(shapes, intersection_points)
    
    root = tk.Tk()
    root.title("Shape Type Selection")

    shape_vars = {
        "cuboid": tk.BooleanVar(),
        "sphere": tk.BooleanVar(),
        "pyramid": tk.BooleanVar()
    }

    # Checkboxes for selecting shapes
    ttk.Label(root, text="Select shapes to plot:").grid(row=0, column=0, sticky=tk.W)

    row = 1
    for shape in shape_vars:
        ttk.Checkbutton(root, text=shape.capitalize(), variable=shape_vars[shape]).grid(row=row, column=0, sticky=tk.W)
        row += 1

    # Button to proceed to plot window
    ttk.Button(root, text="Plot", command=open_plot_window).grid(row=row, column=0, sticky=tk.W)

    root.mainloop()


def create_plot_window(shapes, points):
    root = tk.Tk()
    root.title("3D Shapes Display")

    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create 3D plot
    fig = create_plot(shapes.get("cuboid"), shapes.get("sphere"), shapes.get("pyramid"), points)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    root.mainloop()


def main():
    # Initialize input variables
    cuboid_input = None
    sphere_input = None
    pyramid_input = None
    
    # Create input window
    create_input_window()

if _name_ == "_main_":
    main()
