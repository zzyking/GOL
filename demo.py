import numpy as np
from PIL import Image

def cellular_automaton(rule_number, n=256, t=256, seed=42):
    np.random.seed(seed)
    rule = np.array([int(bit) for bit in f"{rule_number:08b}"[::-1]], dtype=np.int8)

    states = np.zeros((t, n), dtype=np.int8)
    # states[0] = np.random.choice([0, 1], size=n, p=[0.9, 0.1])
    states[0] = np.zeros(256)
    states[0][128]=1

    for step in range(1, t):
        for i in range(n):
            left = (i-1) % n
            right = (i+1) % n
            key = 4 * states[step-1, left] + 2 * states[step-1, i] + states[step-1, right]
            states[step, i] = rule[key]
    return states

# 创建4096x4096的大图像数组
big_image = np.zeros((4096, 4096), dtype=np.uint8)

for rule in range(256):
    # 生成当前规则的演化状态
    states = cellular_automaton(rule)
    # 将状态转换为0和255的灰度值，并调整数据类型
    block = ((1 - states) * 255).astype(np.uint8)
    
    # 计算在大图中的位置
    row = rule // 16  # 行号（0-15）
    col = rule % 16   # 列号（0-15）
    
    # 计算像素起始坐标
    y_start = row * 256
    x_start = col * 256
    
    # 将当前块填充到大图像中
    big_image[y_start:y_start+256, x_start:x_start+256] = block

# 使用PIL保存为PNG图像
img = Image.fromarray(big_image, mode='L')
img.save('cellular_automata_combined_1activate.png')