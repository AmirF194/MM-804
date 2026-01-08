#!/usr/bin/env python3
import sys

# Import VTK modules explicitly
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# These imports are needed to properly initialize the rendering backend on macOS
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballActor
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle

def main():
    # Read STL file
    reader = vtkSTLReader()
    reader.SetFileName("teapot.stl")
    
    # Create mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    # Create actor
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 0)  # Yellow color
    
    # Create renderer
    ren = vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0.1, 0.1, 0.1)
    
    # Create render window
    renWin = vtkRenderWindow()
    renWin.SetSize(800, 800)
    renWin.SetWindowName("Teapot STL Viewer")
    renWin.AddRenderer(ren)
    
    # Create interactor
    iren = vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtkInteractorStyleTrackballActor())
    iren.SetRenderWindow(renWin)
    
    # Initialize and start
    iren.Initialize()
    renWin.Render()
    iren.Start()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())