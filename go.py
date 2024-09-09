import os
import subprocess
from pathlib import Path
from tqdm import tqdm

def convert_flac_to_mp3(flac_file):
    mp3_file = flac_file.with_suffix('.mp3')
    
    # Construct the ffmpeg command with overwrite option
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without prompting
        '-i', str(flac_file),
        '-qscale:a', '0',
        str(mp3_file)
    ]
    
    # Run the ffmpeg command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        os.remove(flac_file)
        return True
    else:
        print(f"\nError converting {flac_file}:")
        print(result.stderr)
        return False

def main():
    # Get the current working directory
    root_dir = Path.cwd()
    
    # Find all FLAC files in the current directory and subdirectories
    flac_files = list(root_dir.rglob('*.flac'))
    
    total_files = len(flac_files)
    print(f"Found {total_files} FLAC files")
    
    # Convert each FLAC file to MP3 with progress bar
    successful_conversions = 0
    with tqdm(total=total_files, desc="Converting", unit="file") as pbar:
        for flac_file in flac_files:
            if convert_flac_to_mp3(flac_file):
                successful_conversions += 1
            pbar.update(1)
    
    print(f"\nConverted {successful_conversions} out of {total_files} files successfully.")

if __name__ == "__main__":
    main()
