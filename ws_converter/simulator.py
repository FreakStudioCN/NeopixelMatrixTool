# Python env   : Python v3.12.0
# -*- coding: utf-8 -*-        
# @Time    : 2025/4/16 下午3:05   
# @Author  : 李清水            
# @File    : simulator.py       
# @Description : WS2812矩阵驱动库仿真功能文件，可以模拟WS2812矩阵驱动库的运行效果

# ======================================== 导入相关模块 =========================================

import pygame
import glob
import json
import natsort
from threading import Event

# ======================================== 全局变量 ============================================

# ======================================== 功能函数 ============================================

def rgb565_to_rgb888(rgb565):
    r = ((rgb565 >> 11) & 0x1F)
    g = ((rgb565 >> 5) & 0x3F)
    b = (rgb565 & 0x1F)
    return (
        (r * 527 + 23) >> 6,
        (g * 259 + 33) >> 6,
        (b * 527 + 23) >> 6
    )

# ======================================== 自定义类 ============================================

class WS2812Simulator:
    def __init__(self, width, height, window_width=1000, fps=30):
        self.width = width
        self.height = height
        self.pixel_size = max(1, window_width // width)
        self.screen_width = width * self.pixel_size
        self.screen_height = height * self.pixel_size
        self.fps = fps
        self.frames = []
        self.current_frame = 0
        self.playing = False
        self.show_numbers = False
        self.stop_event = Event()  # 新增：线程停止控制

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("WS2812 Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)

    def clear_frames(self):  # 新增：清空帧数据
        self.frames.clear()
        self.current_frame = 0

    def load_frames(self, json_pattern):
        self.clear_frames()  # 加载前清空旧数据
        files = natsort.natsorted(glob.glob(json_pattern))
        for path in files:
            with open(path) as f:
                data = json.load(f)
                pixels = [rgb565_to_rgb888(p) for p in data["pixels"]]
                self.frames.append(pixels)

    def draw(self):
        self.screen.fill((0, 0, 0))
        if not self.frames: return  # 无数据时跳过绘制

        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x
                color = self.frames[self.current_frame][i] if i < len(self.frames[self.current_frame]) else (0, 0, 0)
                rect = pygame.Rect(x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        info = self.font.render(f"Frame: {self.current_frame+1}/{len(self.frames)}", True, (255,255,255))
        self.screen.blit(info, (5, 5))

    def run(self):
        self.stop_event.clear()  # 重置停止标志
        while not self.stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_event.set()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.playing = not self.playing
                    elif event.key == pygame.K_RIGHT:
                        self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)
                        self.playing = False
                    elif event.key == pygame.K_LEFT:
                        self.current_frame = max(self.current_frame - 1, 0)
                        self.playing = False

            if self.playing and self.frames:
                self.current_frame = (self.current_frame + 1) % len(self.frames)

            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        # 确保退出时释放资源
        pygame.quit()

def run_simulator(json_pattern, width, height, window_width=1000, fps=30):
    sim = WS2812Simulator(width, height, window_width, fps)
    sim.load_frames(json_pattern)
    sim.run()

# ======================================== 初始化配置 ==========================================

# ========================================  主程序  ===========================================
