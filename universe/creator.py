from PIL import Image, ImageSequence
import os

planet_names = ["Xenat"]
planet_district = "Galaxentre"
planet_system = "Byish"

def extract_frames(gif_path, output_dir):
    # Open the GIF file
    with Image.open(gif_path) as img:
        # Get the title of the GIF without extension
        gif_title = os.path.splitext(os.path.basename(gif_path))[0]
        
        # Create the output directories if they don't exist
        frames_dir = os.path.join(output_dir, gif_title, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        
        first_frame_path = os.path.join(output_dir, gif_title, f"{gif_title}.png")
        
        frame_number = 0
        for frame in ImageSequence.Iterator(img):
            # Calculate the delay
            try:
                delay = frame.info['duration'] / 1000  # Convert ms to seconds
            except KeyError:
                delay = 0.1  # Default delay

            # Save each frame
            frame_path = os.path.join(frames_dir, f"frame_{frame_number:03d}_delay-{delay:.2f}s.png")
            frame.save(frame_path, "PNG")

            # Save the first frame separately
            if frame_number == 0:
                frame.save(first_frame_path, "PNG")

            frame_number += 1

if __name__ == "__main__":
    for planet_name in planet_names:
        gif_path = "universe/"+planet_district+"/"+planet_system+"/"+planet_name+"/"+planet_name+".gif"
        output_dir = "universe/"+planet_district+"/"+planet_system
        extract_frames(gif_path, output_dir)
