# Python env   : Python v3.12.0
# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 上午10:44
# @Author  : 李清水
# @File    : converter.py
# @Description : WS2812矩阵驱动库核心功能文件，可以将图片、视频、文字等转换为对应json文件

# ======================================== 导入相关模块 =========================================

from PIL import Image
import numpy as np
import json
import os
import cv2
from tqdm import tqdm

# ======================================== 全局变量 ============================================

# ======================================== 功能函数 ============================================

# ================ 图像缩放兼容处理 ================
try:
    resample = Image.Resampling.LANCZOS
except AttributeError:
    resample = Image.ANTIALIAS

# ==================== 色彩调整函数 ====================
def apply_color_adjustments(r, g, b, brightness=1.0, contrast=1.0, saturation=1.0):
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    r = gray + (r - gray) * saturation
    g = gray + (g - gray) * saturation
    b = gray + (b - gray) * saturation
    r = (r - 128) * contrast + 128
    g = (g - 128) * contrast + 128
    b = (b - 128) * contrast + 128
    r *= brightness
    g *= brightness
    b *= brightness
    return max(0, min(int(r), 255)), max(0, min(int(g), 255)), max(0, min(int(b), 255))

# ================== RGB888 to RGB565 ===================
def rgb888_to_rgb565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

# ==================== 图片转换函数 ====================
def convert_image_to_json(image_path, output_dir, width, height, description="", brightness=1.0, contrast=1.0, saturation=1.0):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((width * 10, height * 10), resample)
    img_array = np.array(img)
    orig_h, orig_w, _ = img_array.shape
    block_h, block_w = orig_h // height, orig_w // width

    pixels = []
    for y in range(height):
        for x in range(width):
            block = img_array[y*block_h:(y+1)*block_h, x*block_w:(x+1)*block_w]
            avg_color = block.mean(axis=(0, 1))
            r, g, b = map(int, avg_color)
            r, g, b = apply_color_adjustments(r, g, b, brightness, contrast, saturation)
            pixels.append(rgb888_to_rgb565(r, g, b))

    json_data = {
        "pixels": pixels,
        "width": width,
        "height": height,
        "description": description,
        "version": 1.0
    }

    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(image_path))[0]
    with open(os.path.join(output_dir, f"{base}.json"), "w") as f:
        json.dump(json_data, f, indent=2)

# ==================== 视频转换函数 ====================
def convert_video_to_json(video_path, output_dir, width, height, total_frames=30, description="", brightness=1.0, contrast=1.0, saturation=1.0):
    cap = cv2.VideoCapture(video_path)
    total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = min(total_frames, total_video_frames)
    interval = total_video_frames // total_frames
    frame_indices = [min(i * interval, total_video_frames - 1) for i in range(total_frames)]

    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(video_path))[0]

    for idx in tqdm(frame_indices, desc="正在转换视频帧为JSON"):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        img_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = img_array.shape
        block_h, block_w = h // height, w // width

        pixels = []
        for y in range(height):
            for x in range(width):
                block = img_array[y*block_h:(y+1)*block_h, x*block_w:(x+1)*block_w]
                avg_color = block.mean(axis=(0, 1))
                r, g, b = map(int, avg_color)
                r, g, b = apply_color_adjustments(r, g, b, brightness, contrast, saturation)
                pixels.append(rgb888_to_rgb565(r, g, b))

        json_data = {
            "pixels": pixels,
            "width": width,
            "height": height,
            "frame_index": idx,
            "timestamp": round(idx / fps, 2),
            "description": description,
            "version": 1.0
        }

        outpath = os.path.join(output_dir, f"{base}_frame_{idx:04d}.json")
        with open(outpath, "w") as f:
            json.dump(json_data, f, indent=2)

    cap.release()

# ======================================== 自定义类 ============================================

# ======================================== 初始化配置 ==========================================

# ========================================  主程序  ===========================================