from moviepy.editor import VideoFileClip, concatenate_videoclips
import glob
import os
import config
import random
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
date_string = now.strftime("%d-%m-%Y-%H-%M-%S")


instascraper_folder = "C:\\Projects\\Instascraper_and_vidomaker\\"
keyword = config.keyword
videos_add = "videos"
final_add = f"AAA-{keyword}-final-video-{date_string}.mp4"

PATH_TO_VIDEO_FOLDER = os.path.join(instascraper_folder, keyword, videos_add)
OUTPUT_VIDEO_FILE = os.path.join(instascraper_folder, keyword, videos_add, final_add)
print(PATH_TO_VIDEO_FOLDER)
print(OUTPUT_VIDEO_FILE)


# merge multiple video files
def merge_videos(video_files, output_file):
    clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", ffmpeg_params=['-lavfi', '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16']) 
    # blur '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16'
    #alternatywny blur "[0:v]scale=1920*2:1080*2,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[0:v]scale=-1:1080[ov];[bg][ov]overlay=(W-w)/2:(H-h)/2,crop=w=1920:h=1080"
    # alternatywny blur ponoć szybki 'scale=1280:720:force_original_aspect_ratio=decrease:flags=fast_bilinear,split[original][copy];[copy]scale=32:18:force_original_aspect_ratio=increase:flags= fast_bilinear,gblur=sigma=2,scale=1280:720:flags=fast_bilinear[blurred];[blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2,setsar=1'
 
# list of files in dir path
def get_dir_files(dir_path, patterns=None):
    """Get all absolute paths for pattern matched files in a directory.

    Args:
        dir_path (str): The path to of the directory containing media assets.
        patterns (list of str): The list of patterns/file extensions to match.

    Returns:
        (list of str): A list of all pattern-matched files in a directory.
    """
    if not patterns or type(patterns) != list:
        print('No patterns list passed to get_dir_files, defaulting to some video types.')
        patterns = ['*.mp4', '*.avi', '*.mov', '*.flv']

    video_files_list = []
    for pattern in patterns:
        dir_path = os.path.abspath(dir_path) + '/' + pattern
        video_files_list.extend(glob.glob(dir_path))

    return video_files_list


video_files_list = []
video_files_list = get_dir_files(PATH_TO_VIDEO_FOLDER)
print(f"video list:  {video_files_list}")
# to do - ograniczenie liczby plików filmów do połączenia config.max_video_files_to_concanate
random.shuffle(video_files_list)
print(f"shuffle video list:  {video_files_list}")

# Replace with the desired output file path

merge_videos(video_files_list, OUTPUT_VIDEO_FILE)