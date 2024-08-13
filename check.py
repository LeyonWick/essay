import numpy as np

# 加载一个示例的 .npy 文件
data = np.load('/home/jinsongxi/dev/storage/output_data/data_1.npy', allow_pickle=True).item()

# 打印内容以检查数据
print(data)
