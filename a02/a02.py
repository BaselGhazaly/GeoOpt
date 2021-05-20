"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """
        
import Rhino.Geometry as rg

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a


m.FaceNormals.ComputeFaceNormals()
faceNormals = m.FaceNormals

reversedNormals = []



for v in faceNormals:
    r = v.Reverse()
    reversedNormals.append(r)

a = faceNormals


#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

centers = []

for face in range(len(faceNormals)):
    center = m.Faces.GetFaceCenter(face)
    centers.append(center)
    

b = centers

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angleList = []

for i in range(len(faceNormals)):
    ang = rg.Vector3d.VectorAngle(s,faceNormals[i])
    angleList.append(ang)

c = angleList

#print(angleList)

#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

exploded = []
meshcopy = rg.Mesh.Duplicate(m)

for i in range(len(meshcopy.Faces)):
    ex_faces = meshcopy.Faces.ExtractFaces([0])
    exploded.append(ex_faces)

d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

#Boundary of each face's mesh
boundary = []
for i in exploded:
    bound = rg.Mesh.GetNakedEdges(i)
    boundary.append(bound)
#e = boundary #How to shoe polyines

#join boundary
jboundary = []
for i in boundary:
    crvs = []
    for j in i:
        crv = rg.Polyline.ToNurbsCurve(j)
        crvs.append(crv)
    jbound = rg.Curve.JoinCurves(crvs)[0]
    jboundary.append(jbound)

e = jboundary

#Remapangles
reangles = []

for i in angleList:
    re = ( ( (i - min(angleList)) * (max_r - min_r)) / (max(angleList) - min(angleList))  + min_r)
    reangles.append(re)

#print reangles
#re = ( (old value - old min ) / (old max - old min) * (newmax - new min) + new min

# Drawing circles
circles = []
for i in range(len(centers)):
    circle = rg.Circle(centers[i],reangles[i])
    circles.append(circle)

f = circles

#project circle
projCircles = []

for i in range(len(circles)):
    crv = rg.Circle.ToNurbsCurve(circles[i])
    project = rg.Curve.ProjectToMesh(crv,exploded[i], rg.Vector3d.ZAxis,0.01)
    projCircles.append(project)

g = projCircles