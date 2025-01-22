import subprocess, json, time
# 定义要运行的可执行文件路径和参数

def run():
    exe_path = r"C:\code\fuison\master\fusiondesigner\trunk\distrib\created_pdf.exe"

    with open(r"t6.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        data["start_time"] = time.time()
    data = json.dumps(data)
    # 使用subprocess模块调用可执行文件并传递参数
    subprocess.call([exe_path, data])



if __name__ == "__main__":
    run()