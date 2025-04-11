import os

def count_images_and_folders(directory: str):
    total_images = 0
    total_folders = 0
    empty_folders = 0

    for root, dirs, files in os.walk(directory):
        # Count image files
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        total_images += len(image_files)

        # Count folders
        total_folders += len(dirs)

        # Check for empty folders
        if not files and not dirs:
            empty_folders += 1

    return total_images, total_folders, empty_folders

if __name__ == "__main__":
    images_directory = "data/images"
    total_images, total_folders, empty_folders = count_images_and_folders(images_directory)
    print(f"Total images: {total_images}")
    print(f"Total folders: {total_folders}")
    print(f"Empty folders: {empty_folders}")