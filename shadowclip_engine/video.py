import subprocess
import json
import os
from typing import Tuple

def get_video_dimensions(input_path: str) -> Tuple[int, int]:
    """Get video width and height using ffprobe"""
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        input_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to probe video: {result.stderr}")
    
    data = json.loads(result.stdout)
    
    # Find video stream
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            return int(stream['width']), int(stream['height'])
    
    raise RuntimeError("No video stream found")

def convert_to_vertical(input_path: str, output_path: str) -> None:
    """
    Convert video to vertical 9:16 format (1080x1920)
    
    - If video is horizontal (16:9), center crop to 9:16
    - If video is already vertical, scale to 1080x1920
    - Preserves audio with AAC codec
    """
    # Get original dimensions
    width, height = get_video_dimensions(input_path)
    
    # Determine aspect ratio and processing needed
    aspect_ratio = width / height
    
    # Target dimensions
    target_width = 1080
    target_height = 1920
    
    if abs(aspect_ratio - 16/9) < 0.1:  # 16:9 video
        # Calculate crop width for 9:16 aspect ratio
        crop_height = height
        crop_width = int(height * 9 / 16)
        
        if crop_width > width:
            # Fallback: scale if crop width exceeds original
            crop_width = width
            crop_height = int(width * 16 / 9)
        
        # Center crop
        x_offset = (width - crop_width) // 2
        y_offset = (height - crop_height) // 2
        
        filter_complex = (
            f"crop={crop_width}:{crop_height}:{x_offset}:{y_offset},"
            f"scale={target_width}:{target_height}"
        )
    else:  # Already vertical or other aspect
        filter_complex = f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2"
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', filter_complex,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y',  # Overwrite output
        output_path
    ]
    
    # Execute conversion
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg conversion failed: {result.stderr}")
    
    # Verify output was created
    if not os.path.exists(output_path):
        raise RuntimeError("Output file was not created")