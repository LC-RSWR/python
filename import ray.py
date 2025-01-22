import ray
# 启动Ray
ray.init()
# 定义一个简单的任务
@ray.remote
def sample_task(x):
    return x * x * x * x * x
# 提交任务并获取结果
result_ids = []
for i in range(100000):
    result_ids.append(sample_task.remote(i))
results = ray.get(result_ids)
print(results)
# 关闭Ray
ray.shutdown()