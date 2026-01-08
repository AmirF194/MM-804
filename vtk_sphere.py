#!/usr/bin/env python3
import sys

# Import VTK modules
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# THIS LINE IS CRITICAL for mouse interaction
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

# These imports are needed to properly initialize the rendering backend
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle

def main():
    # Create the sphere source
    sphere = vtkSphereSource()
    sphere.SetThetaResolution(40)
    sphere.SetPhiResolution(40)

    # Create mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())

    # Create actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    # Create renderer
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)

    # Create render window
    window = vtkRenderWindow()
    window.SetWindowName("VTK Sphere")
    window.SetSize(900, 700)
    window.AddRenderer(renderer)

    # Create interactor
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    
    # Set the trackball camera style
    style = vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    # Initialize and start
    interactor.Initialize()
    window.Render()
    
    # Start the event loop - this should keep the window open
    interactor.Start()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
