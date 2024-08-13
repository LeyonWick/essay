import cv2
import numpy as np
import os

# 定义文件夹路径
root_dir = '/home/jinsongxi/dev/storage/'  # 更新为您的根目录
output_dir = '/home/jinsongxi/dev/storage/test/out_put_image/'  # 更新为您的输出目录

# 检查输出目录是否存在，不存在则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历所有300个场景
for i in range(1, 301):
    scene_path = os.path.join(root_dir, str(i), 'scene.npy')  # 构建每个场景的路径
    data = np.load(scene_path, allow_pickle=True).item()
    
    # 读取图像数据
    image = data.get('rgb')
    
    if image is None:
        print(f"Failed to load image {scene_path}")
        continue
    
    # 检查图像是否为三通道，如果不是则转换为三通道
    if len(image.shape) == 2:  # 如果是灰度图像
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 1:  # 如果是单通道图像
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用Canny边缘检测
    edged = cv2.Canny(blurred, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

    # 计算 d1 和 d2 （你需要根据实际需求定义计算方式）
    # 示例：假设左货架在图像的左侧，右货架在图像的右侧
    object_pos = data.get('label', [0, 0])  # 假设 'label' 键存储了物体的位置
    left_shelf_pos = np.array([50, image.shape[0] // 2])  # 假设左货架在距离左边缘50像素的位置
    right_shelf_pos = np.array([image.shape[1] - 50, image.shape[0] // 2])  # 右货架在右边缘50像素的位置

    d1 = np.linalg.norm(object_pos - left_shelf_pos)
    d2 = np.linalg.norm(object_pos - right_shelf_pos)

    # 保存每个场景的处理结果
    output_image_path = os.path.join(output_dir, f'image_{i}.png')
    cv2.imwrite(output_image_path, image_with_contours)
    
    # 将 d1, d2 和其他相关数据保存为字典并保存为 .npy 文件
    output_data = {
        'image_path': output_image_path,
        'object_pos': object_pos,
        'd1': d1,
        'd2': d2
    }
    output_data_path = os.path.join(output_dir, f'data_{i}.npy')
    np.save(output_data_path, output_data)
    
    print(f"Processed scene {i}, saved image and data.")

print("All scenes processed.")
