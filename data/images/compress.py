import os
from PIL import Image

def compress_images_in_place(directory, quality=85):
    """
    Compresses and overwrites images in the given directory.

    Parameters:
        directory (str): Path to the directory containing the images.
        quality (int): Compression quality (1-100). Higher is better quality.
    """
    # Supported image formats
    supported_formats = [".jpg", ".jpeg", ".png"]

    total_original_size = 0
    total_compressed_size = 0
    processed_files = 0

    # Debug: Print the directory being processed
    print(f"Processing directory: {directory}")

    for root, _, files in os.walk(directory):
        # Debug: Print the current root directory and files
        print(f"Current root: {root}")
        print(f"Files in root: {files}")

        for file in files:
            # Check if the file is an image
            if any(file.lower().endswith(ext) for ext in supported_formats):
                input_path = os.path.join(root, file)

                print(f"Starting compression for: {input_path}")
                try:
                    # Open the image
                    with Image.open(input_path) as img:
                        original_size = os.path.getsize(input_path)
                        total_original_size += original_size

                        # Convert PNGs to RGB if necessary (JPEG does not support alpha)
                        if img.mode in ("RGBA", "P") and file.lower().endswith(".png"):
                            img = img.convert("RGB")

                        # Save the image back to the same path with compression
                        img.save(input_path, optimize=True, quality=quality)

                        compressed_size = os.path.getsize(input_path)
                        total_compressed_size += compressed_size
                        processed_files += 1

                        print(f"Compressed and replaced: {input_path} | Original size: {original_size} bytes | Compressed size: {compressed_size} bytes")

                except Exception as e:
                    print(f"Failed to compress {input_path}: {e}")

    # Generate final report
    print("\n--- Compression Report ---")
    print(f"Total files processed: {processed_files}")
    print(f"Total original size: {total_original_size} bytes")
    print(f"Total compressed size: {total_compressed_size} bytes")
    if processed_files > 0:
        compression_ratio = (total_original_size - total_compressed_size) / total_original_size * 100
        print(f"Total space saved: {total_original_size - total_compressed_size} bytes ({compression_ratio:.2f}%)")
    else:
        print("No files were processed. Please check the directory for supported formats.")
    print("--------------------------")

if __name__ == "__main__":
    # Directory containing images
    image_directory = "./images"  # Update to match your actual directory

    # Set the compression quality (e.g., 85 for good quality with compression)
    compression_quality = 85

    compress_images_in_place(image_directory, compression_quality)
