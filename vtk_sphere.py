from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# THIS LINE IS CRITICAL
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

sphere = vtkSphereSource()
sphere.SetThetaResolution(40)
sphere.SetPhiResolution(40)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.1)

window = vtkRenderWindow()
window.SetWindowName("VTK Sphere")
window.SetSize(900, 700)
window.AddRenderer(renderer)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

window.Render()
interactor.Initialize()
interactor.Start()
