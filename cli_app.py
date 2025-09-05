# Python env   : Python v3.12.0
# -*- coding: utf-8 -*-        
# @Time    : 2025/4/16 下午3:08   
# @Author  : 李清水            
# @File    : cli_app.py       
# @Description : 命令行工具，统一调用 converter 和 simulator

# ======================================== 导入相关模块 =========================================

import argparse
from ws_converter.converter import convert_image_to_json, convert_video_to_json
from ws_converter.simulator import run_simulator

# ======================================== 全局变量 ============================================

# ======================================== 功能函数 ============================================

def main():
    parser = argparse.ArgumentParser(
        prog="视频图像取模工具平台",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""🎉 欢迎使用『视频图像取模工具平台 v1.0 - Design by FreakStudio Freak嵌入式』🎉

    本工具支持将视频或图像转换为WS2812矩阵点阵数据（JSON格式），并支持播放预览。
    特别需要注意，转换为WS2812点阵数据时，像素点为RGB565格式。

    ✨【使用示例】
    1. 将视频转换为JSON帧：
       python cli_app.py video -i test_gif.mp4 -o output -W 128 -H 64 -f 30

    2. 将图像转换为JSON帧：
       python cli_app.py image -i test_image.png -o out -W 128 -H 64

    3. 播放转换好的帧（支持连播）：
       python cli_app.py play -p "output/test_gif_frame_*.json" -W 128 -H 64 --fps 30

    ⚠️【播放模式说明】
    - 要实现连播，请使用通配符匹配多个JSON文件，例如：
      -p "output/test_gif_frame_*.json"
      否则只加载单帧，空格键无效。

    - 播放控制键：
      空格键   —— 暂停/继续播放
      ← →键   —— 上一帧 / 下一帧
      ESC键   —— 退出播放窗口

    📦【输出命名规则】
    - 每帧JSON文件命名格式为：<输出目录>/<输入文件名>_frame_<编号>.json
      例如：output/test_gif_frame_0000.json、output/test_gif_frame_0001.json

    如需了解更多命令参数，请使用 --help 查看。
    """
    )
    parser.add_argument('--version', action='version', version='视频图像取模工具平台 v1.0.0')
    sub = parser.add_subparsers(dest="mode", required=True)

    # ===== 子命令 convert =====
    conv = sub.add_parser("convert", help="图像或视频转换")
    conv.add_argument("-i", "--input", required=True, help="输入文件路径（图像或视频）")
    conv.add_argument("-o", "--output", required=True, help="输出文件路径（JSON）")
    conv.add_argument("-W", "--width", type=int, required=True, help="输出点阵图像 宽度")
    conv.add_argument("-H", "--height", type=int, required=True, help="输出点阵图像 高度")
    conv.add_argument("-f", "--frames", type=int, default=0, help="输出多少帧数-均匀抽帧（仅视频有效）")
    conv.add_argument("-d", "--desc", default="", help="附加描述信息")

    # ===== 子命令 play =====
    play = sub.add_parser("play", help="播放转换后的 JSON 数据帧")
    play.add_argument("-p", "--path", required=True, help="输入 JSON 数据文件路径")
    play.add_argument("-W", "--width", type=int, required=True, help="LED 屏幕的列数（宽度）")
    play.add_argument("-H", "--height", type=int, required=True, help="LED 屏幕的行数（高度）")
    play.add_argument("--window", type=int, default=1000, help="窗口尺寸（像素），控制播放窗口大小，默认1000")
    play.add_argument("--fps", type=int, default=30, help="播放帧率，默认30帧/秒")

    args = parser.parse_args()

    try:
        if args.mode == "convert":
            if args.frames > 0:
                convert_video_to_json(args.input, args.output, args.width, args.height, args.frames, args.desc)
            else:
                convert_image_to_json(args.input, args.output, args.width, args.height, args.desc)

        elif args.mode == "play":
            run_simulator(args.path, args.width, args.height, args.window, args.fps)
    except Exception as e:
        print(f"[ERROR] {e}")


# ======================================== 自定义类 ============================================

# ======================================== 初始化配置 ==========================================

# ========================================  主程序  ===========================================

if __name__ == "__main__":
    print("🎉 欢迎使用『视频图像取模工具平台 v1.0 - Design by FreakStudio Freak嵌入式』🎉\n如需帮助，请使用 --help 参数")
    main()