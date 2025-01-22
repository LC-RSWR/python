import numpy as np
import trimesh

def crop_one_mesh(dental_mesh_name,crown_mesh_name):
    mesh = trimesh.load (dental_mesh_name )
    crown = trimesh.load (crown_mesh_name )
    fdi_vertices = crown.vertices
    bbx_min, bbx_max = np.min ( fdi_vertices, axis=0 ), np.max ( fdi_vertices, axis=0 )
    #添加中心的随机偏移
    y_off = np.random.rand()-0.2
    x_off= np.random.rand()-0.2
    bbx_center = (bbx_min + bbx_max) / 2  # 包围盒中心
    bbx_radius = (bbx_max - bbx_min) / 2 # 包围盒半径
    # print('offset: ',x_off, y_off)
    bbx_radius = bbx_radius * np.array([1.3,1.3,1.8])+ np.array([x_off,y_off,0]) # 扩大半径

    # 包围盒6个面的原点
    plane_origin = np.array ( [ [ -bbx_radius[ 0 ], 0, 0 ],
                                        [ 0, -bbx_radius[ 1 ], 0 ],
                                        [ 0, 0, -bbx_radius[ 2 ] ],
                                        [ 0, 0, bbx_radius[ 2 ] ],
                                        [ 0, bbx_radius[ 1 ], 0 ],
                                        [ bbx_radius[ 0 ], 0, 0 ] ], dtype='float32' )

    # 包围盒6个面的法线
    plane_normal = np.array ( [ [ -1., 0., 0. ],
                                        [ 0., -1., 0. ],
                                        [ 0., 0., -1. ],
                                        [ 0., 0., 1. ],
                                        [ 0., 1., 0. ],
                                        [ 1., 0., 0. ] ] )

    patch_mesh = mesh.slice_plane ( plane_origin=bbx_center + plane_origin, plane_normal=-plane_normal )
    trimesh.exchange.export.export_mesh( patch_mesh,'patch_'+crown_mesh_name,'stl')

    if False:
        patch_pointcloud_number = 4096
        mesh_o3d_patch = patch_mesh.as_open3d
        sample_point = mesh_o3d_patch.sample_points_poisson_disk ( patch_pointcloud_number )
        sample_point.estimate_normals()
        points = np.asarray(sample_point.points)


if __name__=='__main__':
    crop_one_mesh(dental_mesh_name= 'U.stl',crown_mesh_name = '17.stl')