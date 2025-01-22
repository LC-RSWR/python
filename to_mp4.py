import os
import argparse
from moviepy.editor import ImageSequenceClip, VideoFileClip
from moviepy.video.fx import resize

def create_video(input_folder, output_folder, output_file, thumbnail_name=None, fps=3):
    try:
        # 获取输入文件夹中所有文件的文件名，并按照数字部分排序
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
        images = [os.path.join(input_folder, f) for f in sorted(files, key=lambda x: int(os.path.splitext(x)[0]))]

        # 确保图片列表不为空
        if not images:
            raise ValueError("No images found in the input folder.")

        # 创建视频剪辑
        clip = ImageSequenceClip(images, fps=fps)  # 设置每秒帧数 (FPS)

        # 进行必要的处理，如调整大小等（可选）
        # clip = resize(clip, height=720)  # 如果需要调整大小

        # 写入输出文件
        output_path = os.path.join(output_folder, output_file)
        print(f"Writing video to {output_path}...")
        clip.write_videofile(output_path, codec="libx264", verbose=True)  # 编解码器设置为libx264

        # 如果指定了缩略图名字，则保存视频的中间帧作为缩略图
        if thumbnail_name:
            thumbnail_path = os.path.join(output_folder, thumbnail_name)
            print(f"Saving thumbnail to {thumbnail_path}...")
            video_clip = VideoFileClip(output_path)
            mid_time = video_clip.duration / 2
            video_clip.save_frame(thumbnail_path, t=mid_time)  # 保存视频中间帧作为缩略图

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create video from a sequence of images.")
    parser.add_argument("input_folder", help="Input folder containing images")
    parser.add_argument("output_folder", help="Output folder for the video file")
    parser.add_argument("output_file", help="Output file name for the video")
    parser.add_argument("--thumbnail_name", help="Thumbnail file name")
    parser.add_argument("--fps", type=int, default=3, help="Frames per second (default: 3)")
    args = parser.parse_args()

    create_video(args.input_folder, args.output_folder, args.output_file, args.thumbnail_name, args.fps)
