#!/usr/bin/env python3
import sys

# Import VTK modules explicitly
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkCommonTransforms import vtkTransform

# These imports are needed to properly initialize the rendering backend on macOS
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle

def main():
    # Create sources
    cube = vtkCubeSource()
    
    cone = vtkConeSource()
    cone.SetResolution(200)
    
    # Create cube mapper and actor
    cubeMapper = vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cube.GetOutputPort())
    
    cubeActor = vtkActor()
    cubeActor.SetMapper(cubeMapper)
    cubeActor.GetProperty().SetColor(1, 0, 0)
    
    # Create cone mapper and actor
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    
    # Transform the cone
    transform = vtkTransform()
    transform.Translate(1, 1, 1)
    coneActor.SetUserTransform(transform)
    
    # Create first renderer (left viewport)
    ren1 = vtkRenderer()
    ren1.SetViewport(0, 0, 0.5, 1)
    ren1.AddActor(cubeActor)
    ren1.AddActor(coneActor)
    ren1.SetBackground(0.1, 0.1, 0.2)
    
    # Create second renderer (right viewport)
    ren2 = vtkRenderer()
    ren2.SetViewport(0.5, 0, 1.0, 1.0)
    ren2.AddActor(cubeActor)
    ren2.SetBackground(0.2, 0.1, 0.1)
    
    # Create render window
    renWin = vtkRenderWindow()
    renWin.SetSize(600, 300)
    renWin.SetWindowName("Multiple Viewports")
    renWin.AddRenderer(ren1)
    renWin.AddRenderer(ren2)
    
    # Create interactor
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    # Set the trackball camera style
    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)
    
    # Initialize and start
    iren.Initialize()
    renWin.Render()
    iren.Start()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
