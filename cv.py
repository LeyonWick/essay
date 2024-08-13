import cv2
import numpy as np

# 读取图像
image_path = '/home/jinsongxi/dev/storage/2/scene.npy'  # 更新为您的图像路径
data = np.load(image_path, allow_pickle=True).item()

# 获取图像数据
image = data.get('rgb')

if image is None:
    print(f"Failed to load image {image_path}")
else:
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

    if len(contours) > 0:
        # 找到最大的轮廓，假设这是物体
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 计算物体的位置（质心）
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            object_pos = np.array([cX, cY])
            print(f"Object position: {object_pos}")
        else:
            object_pos = np.array([0, 0])
            print("No object detected.")
        
        # 定义货架的位置（假设左货架在左侧，右货架在右侧）
        left_shelf_pos = np.array([0, object_pos[1]])
        right_shelf_pos = np.array([image.shape[1], object_pos[1]])

        # 计算 d1 和 d2
        d1 = np.linalg.norm(object_pos - left_shelf_pos)
        d2 = np.linalg.norm(object_pos - right_shelf_pos)

        print(f"d1 (distance to left shelf): {d1}")
        print(f"d2 (distance to right shelf): {d2}")

        # 这里可以根据 d1 和 d2 进行进一步处理或保存结果
    else:
        print("No contours found.")

    # 显示图像
    cv2.imshow('Original Image', image)
    cv2.imshow('Edged Image', edged)

    # 保存结果图像
    output_path = '/home/jinsongxi/dev/storage/test/out_put_image/image_with_contours.png'  # 更新为您的输出路径
    cv2.imwrite(output_path, edged)
    print(f"Processed image saved as {output_path}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
