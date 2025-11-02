import argparse
import sys
import datetime

from PIL import Image



def merge_images_horizontally(image_paths, output_path, gap=0, background_color=(250, 250, 250)):
    """
    Merge multiple images horizontally into a single image.
    
    Args:
        image_paths: List of paths to input images
        output_path: Path for the output merged image
        gap: Gap in pixels between images (default: 0)
        background_color: RGB color for background (default: white-ish)
    """
    if not image_paths:
        print("Error: No input images provided", file=sys.stderr)
        return
    
    try:
        images = [Image.open(path) for path in image_paths]
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error opening images: {e}", file=sys.stderr)
        return
    
    if not images:
        print("Error: No valid images loaded", file=sys.stderr)
        return
    
    # Calculate total width and height
    total_width = sum(img.size[0] for img in images) + gap * (len(images) - 1)
    # Use the height of the first image (assuming all have same height)
    height = images[0].size[1]
    
    # Verify all images have the same height
    for i, img in enumerate(images):
        if img.size[1] != height:
            print(f"Warning: Image {image_paths[i]} has different height ({img.size[1]}) than first image ({height})", file=sys.stderr)
    
    # Create new image with background color
    new_image = Image.new('RGB', (total_width, height), background_color)
    
    # Paste images horizontally
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.size[0] + gap
    
    # Save the merged image
    if not output_path:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_path = f"merged-image-{timestamp}.png"
    new_image.save(output_path, "PNG")
    print(f"Merged image saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple images horizontally into a single PNG image"
    )
    parser.add_argument(
        "images",
        nargs="+",
        help="Input image files to merge (e.g., image1.png image2.png)"
    )
    parser.add_argument(
        "-o", "--output",
        default="",
        help="Output file path (default: auto-generated with timestamp)"
    )
    parser.add_argument(
        "-g", "--gap",
        type=int,
        default=0,
        help="Gap in pixels between images (default: 0)"
    )
    
    args = parser.parse_args()
    
    merge_images_horizontally(args.images, args.output, args.gap)


if __name__ == "__main__":
    main()
