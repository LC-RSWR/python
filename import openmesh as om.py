import openmesh as om
import numpy as np


def avg(points, vv_it, vit):
    # 求顶点的重心，python中没有相关函数实现
    return np.average(points[vv_it[vit]][vv_it[vit] != -1], axis=0)


mesh = om.read_polymesh('bunny.ply')
iterations = 10
vv_indices = mesh.vv_indices()  # 获取顶点领域索引
for i in range(iterations):
    laplace = []
    bi_laplace = []
    # 第一次拉普拉斯
    for v_it in range(mesh.n_vertices()):
        laplace.append(avg(mesh.points(), vv_indices, v_it) - mesh.points()[v_it])
    laplace = np.array(laplace)
    # 第二次拉普拉斯
    for v_it in range(mesh.n_vertices()):
        bi_laplace.append(avg(laplace, vv_indices, v_it) - laplace[v_it])
    bi_laplace = np.array(bi_laplace)
    for v_it in range(mesh.n_vertices()):
        mesh.set_point(mesh.vertex_handle(v_it), mesh.points()[v_it] - 0.5 * bi_laplace[v_it])
om.write_mesh('3.ply', mesh)