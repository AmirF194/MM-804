#!/usr/bin/env python3
"""
PyVista Example - More Pythonic 3D Visualization

PyVista is a high-level wrapper around VTK that makes 3D plotting
much simpler and more intuitive. It provides:
- Cleaner, more Pythonic API
- Built-in mesh operations
- Easy multi-mesh scenes
- Interactive widgets
"""

import pyvista as pv

def main():
    # Create a plotter with a dark theme
    plotter = pv.Plotter(window_size=(1000, 800))
    plotter.set_background("black", top="darkblue")  # Gradient background
    
    # Load the STL file (same teapot as the VTK example)
    mesh = pv.read("teapot.stl")
    
    # Add the mesh with nice rendering properties
    plotter.add_mesh(
        mesh,
        color="gold",
        specular=0.5,       # Shininess
        specular_power=15,
        smooth_shading=True,
        show_edges=False,
    )
    
    # Add some built-in geometric shapes for demonstration
    # Creates a sphere
    sphere = pv.Sphere(radius=10, center=(50, 0, 0))
    plotter.add_mesh(sphere, color="crimson", opacity=0.8)
    
    # Create a cube
    cube = pv.Cube(center=(-50, 0, 0), x_length=15, y_length=15, z_length=15)
    plotter.add_mesh(cube, color="royalblue", opacity=0.8)
    
    # Create a cylinder
    cylinder = pv.Cylinder(center=(0, 50, 0), direction=(0, 1, 0), radius=8, height=20)
    plotter.add_mesh(cylinder, color="forestgreen", opacity=0.8)
    
    # Add a floor plane with grid
    plane = pv.Plane(center=(0, 0, -20), direction=(0, 0, 1), i_size=200, j_size=200)
    plotter.add_mesh(plane, color="gray", opacity=0.3)
    
    # Add axes for orientation
    plotter.add_axes()
    
    # Add a title
    plotter.add_title("PyVista 3D Visualization Demo", font_size=14)
    
    # Enable interactive camera controls
    plotter.enable_trackball_style()
    
    # Show the scene
    plotter.show()


def demo_mesh_operations():
    """Demonstrate PyVista's mesh operations"""
    
    plotter = pv.Plotter(shape=(2, 2), window_size=(1200, 900))
    plotter.set_background("white")
    
    # Panel 1: Boolean operations
    plotter.subplot(0, 0)
    sphere1 = pv.Sphere(radius=1, center=(0, 0, 0))
    sphere2 = pv.Sphere(radius=1, center=(0.5, 0, 0))
    result = sphere1.boolean_difference(sphere2)
    plotter.add_mesh(result, color="coral", show_edges=True)
    plotter.add_title("Boolean Difference")
    
    # Panel 2: Mesh slicing
    plotter.subplot(0, 1)
    mesh = pv.Sphere(radius=1)
    slices = mesh.slice_orthogonal()  # Create X, Y, Z slices
    plotter.add_mesh(mesh, opacity=0.3, color="lightblue")
    plotter.add_mesh(slices, color="red", line_width=3)
    plotter.add_title("Orthogonal Slices")
    
    # Panel 3: Contours
    plotter.subplot(1, 0)
    mesh = pv.Sphere(radius=1)
    mesh["data"] = mesh.points[:, 2]  # Color by Z coordinate
    contours = mesh.contour(isosurfaces=10)
    plotter.add_mesh(mesh, scalars="data", cmap="viridis", opacity=0.5)
    plotter.add_mesh(contours, color="white", line_width=2)
    plotter.add_title("Contours")
    
    # Panel 4: Mesh smoothing
    plotter.subplot(1, 1)
    rough = pv.ParametricRandomHills()
    smooth = rough.smooth(n_iter=100)
    plotter.add_mesh(smooth, color="tan", show_edges=True)
    plotter.add_title("Smoothed Surface")
    
    plotter.link_views()
    plotter.show()


if __name__ == "__main__":
    print("Running PyVista demo...")
    print("Use mouse to rotate, scroll to zoom, shift+drag to pan")
    print("-" * 50)
    
    # Run main demo
    main()
    
    # Uncomment to run mesh operations demo
    # demo_mesh_operations()
