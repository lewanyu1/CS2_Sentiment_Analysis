import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import sys
import platform
import numpy as np
from PIL import Image

# ============================
# 0. 路径配置
# ============================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config

# ============================
# 1. 变量绑定
# ============================
INPUT_FILE = os.path.join(config.PROCESSED_DATA_DIR, 'top_keywords_report.csv')
IMG_DIR = os.path.join(root_dir, '5_visualization', 'images')
MASK_IMAGE_PATH = os.path.join(IMG_DIR, 'cs2_mask.png')  # 确保图片在这里！
OUTPUT_IMG = os.path.join(IMG_DIR, 'wordcloud_cs2_masked.png')


# ============================
# 2. 辅助函数
# ============================
def get_font_path():
    """寻找中文字体"""
    system_name = platform.system()
    if system_name == "Darwin":  # Mac
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        ]
    elif system_name == "Windows":  # Windows
        candidates = [
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc"
        ]
    else:
        candidates = ["/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"]

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def process_mask_image(img_path):
    """
    【核心修复】专治 JPG 噪点
    """
    if not os.path.exists(img_path):
        print(f"[WARN] 找不到图片: {img_path}")
        return None

    print(f"🖼️ 正在深度清洗蒙版图片: {img_path}")

    # 1. 强制转为灰度图，扔掉彩色噪点
    img = Image.open(img_path).convert("L")

    # 2. 二值化处理：把浅灰色背景强行变白
    # 阈值设为 200，凡是大于 200 的亮色都变成纯白(255)
    mask = img.point(lambda p: 255 if p > 200 else 0)

    mask_array = np.array(mask)

    # 3. 检查一下黑白占比
    black_ratio = np.sum(mask_array == 0) / mask_array.size
    print(f"   -> 清洗后黑色填词区占比: {black_ratio:.2%}")

    return mask_array


# ============================
# 3. 主逻辑
# ============================
def generate_cs2_wordcloud():
    print("☁️ [CS2 最终版词云] 任务启动...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到关键词数据: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)
    keywords_dict = dict(zip(df['keyword'], df['weight']))

    # 获取处理好的蒙版
    mask_image = process_mask_image(MASK_IMAGE_PATH)

    # WordCloud 配置
    wc_kwargs = {
        'font_path': get_font_path(),
        'background_color': 'white',  # 背景必须是白
        'max_words': 600,  # AK47 比较细长，多放点词才填得满
        'random_state': 42,
        'prefer_horizontal': 0.9,
        'width': 1600,
        'height': 900,
        'colormap': 'viridis',
        # 🔴 关键修改：针对 AK47，把轮廓线关掉！
        # 因为枪的边缘很碎，画线会显得脏。关掉后就是纯文字组成的枪。
        'contour_width': 0,
        'contour_color': 'steelblue'
    }

    if mask_image is not None:
        wc_kwargs['mask'] = mask_image
        print("✅ 成功加载并清洗蒙版图片！")
    else:
        print("⚠️ 未加载蒙版，将生成默认矩形词云。")

    wc = WordCloud(**wc_kwargs)

    print("🎨 正在渲染 (请稍候)...")
    wc.generate_from_frequencies(keywords_dict)

    plt.figure(figsize=(16, 9), dpi=300)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)

    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

    plt.savefig(OUTPUT_IMG, bbox_inches='tight')
    print(f"🎉 完美版词云已保存: {OUTPUT_IMG}")
    plt.close()


if __name__ == '__main__':
    generate_cs2_wordcloud()