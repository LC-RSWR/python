import requests
from typing_extensions import Literal


def send_mesh_file(stl_path, file_format='stl', jaw='upper'):
    """
    发送STL文件到预测服务并返回响应。

    :param stl_path: STL文件的路径
    :param file_format: 文件格式，默认值为 'stl'
    :param jaw: 'upper' 或 'lower'，表示上颌或下颌
    :return: 服务器响应的 JSON 数据
    """
    url_path = "http://10.14.29.79:29099/predict"
    
    # 打开 STL 文件并作为文件流发送
    with open(stl_path, 'rb') as file:
        mesh_file = {"files": file}
        format = {
            "file_format": file_format,  # 文件格式，如 'stl'
            "jaw": jaw                   # 'upper' 或 'lower'
        }

        # 发送 POST 请求
        try:
            response = requests.post(url_path, files=mesh_file, data=format)
            
            # 检查响应状态码是否为 200 (成功)
            if response.status_code == 200:
                return response.json()  # 返回 JSON 格式的响应
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

# 示例调用
stl_path = 'u.stl'  # 替换为你自己的 STL 文件路径
result = send_mesh_file(stl_path, file_format='stl', jaw='upper')

# 打印返回的结果
if result:
    print("Prediction Result:", result)
