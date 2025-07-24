import os
import sys
import numpy as np
from tkinter import Tk, filedialog
from moviepy.editor import VideoFileClip
from PIL import Image, ImageEnhance, ImageFilter

def select_video_files():
    try:
        root = Tk()
        root.withdraw()
        return filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
        )
    except Exception as e:
        print(f"Error selecting files: {str(e)}")
        return []

def remove_metadata(input_path, output_path):
    try:
        video = VideoFileClip(input_path)
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            ffmpeg_params=['-map_metadata', '-1'],
            threads=4,
            preset='fast'
        )
        video.close()
        return True
    except Exception as e:
        print(f"Metadata removal failed: {str(e)}")
        return False

def pitch_down_audio(input_path, output_path, pitch_factor=1.03):
    try:
        cmd = (
            f'ffmpeg -y -i "{input_path}" '
            f'-filter_complex "[0:a]rubberband=pitch={1/pitch_factor}[a]" '
            f'-map 0:v -map "[a]" -c:v copy -shortest "{output_path}"'
        )
        result = os.system(cmd)
        return result == 0
    except Exception as e:
        print(f"Audio pitch down failed: {str(e)}")
        return False

def apply_video_filter(input_path, output_path):
    try:
        clip = VideoFileClip(input_path)

        watermark_path = 'watermark.png'
        watermark = Image.open(watermark_path).convert("RGBA")

        wm_width = 250
        aspect_ratio = watermark.size[1] / watermark.size[0]
        watermark = watermark.resize((wm_width, int(wm_width * aspect_ratio)), Image.LANCZOS)
        watermark_np = np.array(watermark)

        def apply_filters(frame):
            try:
                img = Image.fromarray(frame).convert("RGBA")

                img = ImageEnhance.Contrast(img).enhance(1.2)
                img = ImageEnhance.Color(img).enhance(0.9)
                img = img.filter(ImageFilter.GaussianBlur(radius=0.7))

                x = 20
                y = img.size[1] - watermark_np.shape[0] - 20
                img.paste(watermark, (x, y), watermark)

                return np.array(img.convert("RGB"))
            except Exception as e:
                print(f"Frame processing error: {str(e)}")
                return frame

        filtered_clip = clip.fl_image(apply_filters)
        filtered_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='fast'
        )

        clip.close()
        filtered_clip.close()
        return True
    except Exception as e:
        print(f"Video filter application failed: {str(e)}")
        return False

def process_video_file(input_path, output_path):
    temp_files = []

    try:
        print(f"\n>>> Processing: {os.path.basename(input_path)}")

        no_meta_path = "temp_no_meta.mp4"
        if not remove_metadata(input_path, no_meta_path):
            return False
        temp_files.append(no_meta_path)

        pitched_path = "temp_pitched.mp4"
        if not pitch_down_audio(no_meta_path, pitched_path):
            return False
        temp_files.append(pitched_path)

        if not apply_video_filter(pitched_path, output_path):
            return False

        print(f"✔ Finished: {output_path}")
        return True

    except Exception as e:
        print(f"✖ Failed: {str(e)}")
        return False
    finally:
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try: os.remove(temp_file)
                except: pass

if __name__ == "__main__":
    print("=== Instagram Video Processor ===")

    input_files = select_video_files()

    if not input_files:
        print("No files selected. Exiting.")
        sys.exit()

    for input_path in input_files:
        output_path = os.path.splitext(input_path)[0] + "_processed.mp4"

        if os.path.exists(output_path):
            print(f"Output already exists: {output_path} — skipping.")
            continue

        process_video_file(input_path, output_path)

    input("\nAll done! Press Enter to exit...")
