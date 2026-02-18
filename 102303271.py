import os
import sys
import shutil
import subprocess
import imageio_ffmpeg as ffmpeg
from yt_dlp import YoutubeDL

if len(sys.argv) != 5:
    print("Usage: python script.py <Singer> <Videos> <Duration> <Output>")
    sys.exit(1)

singer = sys.argv[1]
num_videos = int(sys.argv[2])       
clip_duration = int(sys.argv[3])          
output_file = sys.argv[4]

if num_videos < 10:
    print("Videos must be 10 or more")
    sys.exit(1)

if clip_duration < 20:
    print("Duration must be 20 seconds or more")
    sys.exit(1)

video_folder = "downloads"
audio_folder = "audio"
trimmed_folder = "cut_audio"
ffmpeg_bin = ffmpeg.get_ffmpeg_exe()

for folder in [video_folder, audio_folder, trimmed_folder]:
    os.makedirs(folder, exist_ok=True)

def cleanup():
    folders = ["downloads", "audio", "cut_audio"]
    for f in folders:
        if os.path.exists(f):
            shutil.rmtree(f)
    if os.path.exists(output_file):
        os.remove(output_file)

def fetch_videos(name, count):
    import time
    import random
    
    query = f"ytsearch{count}:{name}"
    
    strategies = [
        {
            "name": "iOS client",
            "options": {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "quiet": False,
                "ignoreerrors": True,
                "nocheckcertificate": True,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["ios"],
                        "skip": ["hls", "dash"]
                    }
                }
            }
        },
        {
            "name": "Android client", 
            "options": {
                "format": "bestaudio/best",
                "quiet": False,
                "ignoreerrors": True,
                "nocheckcertificate": True,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android"],
                        "skip": ["hls", "dash"]
                    }
                }
            }
        },
        {
            "name": "Simple mode",
            "options": {
                "format": "bestaudio/best",
                "quiet": False,
                "ignoreerrors": True,
                "nocheckcertificate": True
            }
        }
    ]
    
    for strategy in strategies:
        print(f"\n=== Trying {strategy['name']} ===")
        options = strategy['options'].copy()
        options["outtmpl"] = f"{video_folder}/%(title)s.%(ext)s"
        
        try:
            time.sleep(random.uniform(1, 2))
            
            with YoutubeDL(options) as downloader:
                downloader.download([query])
            
            downloaded_files = os.listdir(video_folder) if os.path.exists(video_folder) else []
            print(f"Downloaded {len(downloaded_files)} files")
            
            if len(downloaded_files) >= min(5, count):
                print(f"Success with {strategy['name']}!")
                return
                
        except Exception as e:
            print(f"{strategy['name']} failed: {str(e)}")
            continue
    
    print("\nAll download strategies exhausted")

def extract_audio():
    for item in os.listdir(video_folder):
        src = os.path.join(video_folder, item)
        dest = os.path.join(audio_folder, os.path.splitext(item)[0] + ".mp3")
        subprocess.run(
            [ffmpeg_bin, "-y", "-i", src, "-vn", "-ab", "192k", dest],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def trim_audio():
    audio_files = os.listdir(audio_folder)
    if not audio_files:
        print("No audio files available")
        return
    
    print(f"Trimming {len(audio_files)} files to {clip_duration}s")
    for item in audio_files:
        src = os.path.join(audio_folder, item)
        dest = os.path.join(trimmed_folder, item)
        cmd = [ffmpeg_bin, "-y", "-i", src, "-t", str(clip_duration), "-acodec", "copy", dest]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Trimmed: {item}")
        else:
            print(f"Failed: {item}")

def combine_audio(output):
    audio_list = sorted(os.listdir(trimmed_folder))
    if not audio_list:
        print("No files to merge")
        return
    
    print(f"Merging {len(audio_list)} files")
    temp_file = "list.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        for item in audio_list:
            path = os.path.join(trimmed_folder, item).replace("\\", "/")
            f.write(f"file '{path}'\n")
            print(f"  - {item}")
    
    result = subprocess.run([
        ffmpeg_bin, "-y", "-f", "concat", "-safe", "0",
        "-i", temp_file, "-c", "copy", output
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print("Merge complete")
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

def run():
    cleanup()
    for folder in [video_folder, audio_folder, trimmed_folder]:
        os.makedirs(folder, exist_ok=True)
    
    print(f"Singer: {singer}")
    print(f"Videos: {num_videos}")
    print(f"Duration: {clip_duration}s")
    print(f"Output: {output_file}")
    
    fetch_videos(singer, num_videos)
    extract_audio()
    trim_audio()
    combine_audio(output_file)
    
    if os.path.exists(output_file):
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"SUCCESS: {output_file} created")
        print(f"Size: {size_mb:.2f} MB")
    else:
        print(f"ERROR: Failed to create {output_file}")
        sys.exit(1)

if __name__ == "__main__":
    run()
