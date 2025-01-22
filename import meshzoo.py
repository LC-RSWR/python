import meshzoo # type: ignore

bary, cells = meshzoo.triangle(8)

# corners = np.array(
#     [
#         [0.0, -0.5 * numpy.sqrt(3.0), +0.5 * numpy.sqrt(3.0)],
#         [1.0, -0.5, -0.5],
#     ]
# )
# points = np.dot(corners, bary).T

# Process the mesh, e.g., write it to a file using meshio
# meshio.write_points_cells("triangle.vtk", points, {"triangle": cells})
# meshio.write_points_cells("triangle.vtk", points, {"triangle": cells})