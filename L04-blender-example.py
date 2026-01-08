#!/usr/bin/env python3
"""
Blender Python Script Example

This script demonstrates Blender's Python API (bpy) for 3D visualization.
Unlike VTK/PyVista which are primarily for visualization, Blender is a 
full 3D content creation suite with powerful modeling, rendering, 
and animation capabilities.

HOW TO RUN:
-----------
Option 1 - From Blender's UI:
    1. Open Blender
    2. Go to Scripting workspace
    3. Open this file or paste the code
    4. Click "Run Script"

Option 2 - From command line (headless):
    blender --background --python L04-blender-example.py

Option 3 - From command line (with UI):
    blender --python L04-blender-example.py
"""

import bpy
import math
import os


def clear_scene():
    """Remove all objects from the current scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def setup_world():
    """Configure world settings with a nice gradient background"""
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    # Clear existing nodes
    nodes.clear()
    
    # Create gradient background
    background = nodes.new(type='ShaderNodeBackground')
    background.inputs[0].default_value = (0.02, 0.02, 0.08, 1)  # Dark blue
    background.inputs[1].default_value = 1.0  # Strength
    
    output = nodes.new(type='ShaderNodeOutputWorld')
    links.new(background.outputs[0], output.inputs[0])


def create_material(name, color, metallic=0.0, roughness=0.5):
    """Create a PBR material with the given properties"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    
    return mat


def import_stl(filepath):
    """Import an STL file and return the imported object"""
    # Get current objects before import
    before = set(bpy.data.objects)
    
    # Import STL
    bpy.ops.wm.stl_import(filepath=filepath)
    
    # Find the newly imported object
    after = set(bpy.data.objects)
    new_objects = after - before
    
    if new_objects:
        return list(new_objects)[0]
    return None


def add_primitive_shapes():
    """Add various primitive shapes to demonstrate Blender's capabilities"""
    shapes = []
    
    # Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(5, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Demo_Sphere"
    mat = create_material("Crimson", (0.86, 0.08, 0.24), metallic=0.3, roughness=0.2)
    sphere.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    shapes.append(sphere)
    
    # Cube
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-5, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Demo_Cube"
    mat = create_material("RoyalBlue", (0.25, 0.41, 0.88), metallic=0.5, roughness=0.3)
    cube.data.materials.append(mat)
    shapes.append(cube)
    
    # Cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=2, location=(0, 5, 0))
    cylinder = bpy.context.active_object
    cylinder.name = "Demo_Cylinder"
    mat = create_material("ForestGreen", (0.13, 0.55, 0.13), metallic=0.4, roughness=0.4)
    cylinder.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    shapes.append(cylinder)
    
    # Torus (Blender-specific shape)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.5,
        minor_radius=0.5,
        location=(0, -5, 0)
    )
    torus = bpy.context.active_object
    torus.name = "Demo_Torus"
    mat = create_material("Purple", (0.58, 0.0, 0.83), metallic=0.6, roughness=0.15)
    torus.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    shapes.append(torus)
    
    # Floor plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -2))
    floor = bpy.context.active_object
    floor.name = "Floor"
    mat = create_material("Floor", (0.3, 0.3, 0.3), metallic=0.0, roughness=0.8)
    floor.data.materials.append(mat)
    shapes.append(floor)
    
    return shapes


def setup_lighting():
    """Create a three-point lighting setup"""
    # Key light (main light)
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 500
    key_light.data.size = 5
    key_light.data.color = (1, 0.95, 0.9)  # Warm white
    
    # Fill light (softer, from opposite side)
    bpy.ops.object.light_add(type='AREA', location=(-6, 4, 5))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 200
    fill_light.data.size = 8
    fill_light.data.color = (0.9, 0.95, 1)  # Cool white
    
    # Rim light (backlight for edge definition)
    bpy.ops.object.light_add(type='SPOT', location=(0, 8, 6))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 800
    rim_light.data.spot_size = math.radians(45)
    rim_light.rotation_euler = (math.radians(60), 0, math.radians(180))


def setup_camera():
    """Position camera for a nice view of the scene"""
    bpy.ops.object.camera_add(location=(12, -12, 8))
    camera = bpy.context.active_object
    camera.name = "Main_Camera"
    
    # Point camera at origin
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Set camera properties
    camera.data.lens = 35  # Focal length
    camera.data.clip_end = 1000
    
    return camera


def configure_render_settings():
    """Configure render settings for high quality output"""
    scene = bpy.context.scene
    
    # Use Cycles for better quality - check using try/except for compatibility
    try:
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128
        scene.cycles.use_denoising = True
    except Exception:
        # Fall back to EEVEE if Cycles not available
        try:
            scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Blender 4.2+
        except Exception:
            scene.render.engine = 'BLENDER_EEVEE'  # Older versions
    
    # Output settings
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'


def main():
    """Main function to set up the Blender scene"""
    print("=" * 50)
    print("Blender Python Script Demo")
    print("=" * 50)
    
    # Clear existing scene
    clear_scene()
    
    # Setup environment
    setup_world()
    
    # Try to import the teapot STL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stl_path = os.path.join(script_dir, "teapot.stl")
    
    if os.path.exists(stl_path):
        print(f"Importing STL: {stl_path}")
        teapot = import_stl(stl_path)
        if teapot:
            teapot.name = "Teapot"
            # Scale to fit the scene
            teapot.scale = (0.1, 0.1, 0.1)
            # Apply gold material
            mat = create_material("Gold", (1, 0.84, 0), metallic=0.9, roughness=0.2)
            teapot.data.materials.append(mat)
            bpy.ops.object.shade_smooth()
            print("Teapot imported successfully!")
    else:
        print(f"STL not found at {stl_path}, creating demo cube instead")
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        demo = bpy.context.active_object
        demo.name = "Demo_Object"
        mat = create_material("Gold", (1, 0.84, 0), metallic=0.9, roughness=0.2)
        demo.data.materials.append(mat)
    
    # Add primitive shapes
    add_primitive_shapes()
    
    # Setup lighting
    setup_lighting()
    
    # Setup camera
    setup_camera()
    
    # Configure render settings
    configure_render_settings()
    
    print("Scene setup complete!")
    print("Press F12 to render, or use viewport shading to preview")


# Run the script
if __name__ == "__main__":
    main()
