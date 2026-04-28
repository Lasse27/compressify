from pathlib import Path
import arguments as args
from argparse import Namespace
from pypdf import PageObject, PdfWriter
import shutil
from PIL import Image
import output
import logging
import time

LOGGER = logging.getLogger(__name__)
compressed_amount: int = 0
start_time = time.time_ns()


def main() -> None:
    try:
        # Create output console and read command line arguments
        arguments = args.get_arguments()

        # Configure logging in console
        global LOGGER
        LOGGER = output.init_logger(arguments)
        print_execution_header(arguments)

        # Check paths
        source_path = Path(arguments.source)
        if arguments.destination is None:
            destination_path = source_path
        else:
            destination_path = Path(arguments.destination)

        if not source_path.exists():
            LOGGER.warning(f"Source path '{source_path}' doesn't exist in the filesystem.")
            return

        if source_path.is_dir():
            handle_dir_compression(arguments, source_path, destination_path)

        if source_path.is_file():
            handle_file_compression(arguments, source_path, destination_path)

        process_time = (time.time_ns() - start_time) / 1000.0 / 1000.0 / 1000.0
        LOGGER.info(f"Compressed {compressed_amount} pdf file/s in {process_time:.3f} s.")

    except KeyboardInterrupt:
        LOGGER.warning("Interrupted by user. Exiting program.")
        exit(-1)


def print_execution_header(arguments: Namespace) -> None:
    LOGGER.info("Running compressify with arguments...")
    for ident, value in arguments._get_kwargs():
        LOGGER.debug(f"{ident}: {value}")


def handle_dir_compression(arguments: Namespace, source_path: Path, target_path: Path) -> None:

    # Check path
    if target_path.is_file():
        LOGGER.warning("Target path can't be file path when compressing directory.")
        return

    # Collect files
    paths: list[Path] = []
    LOGGER.info("Collecting files...")
    for path_object in source_path.rglob("*.pdf"):
        if path_object.is_file():
            paths.append(path_object)

    # Logging collection
    paths_count = len(paths)
    if paths_count == 0:
        LOGGER.warning(f"{paths_count} pdf files found.")
    else:
        LOGGER.debug(f"{paths_count} pdf files found.")

    # Compressing all collected files
    LOGGER.info(f"Compressing {paths_count} files... (this may take a while)")
    for i in range(paths_count):
        file_path = paths[i]
        gen_target_path = target_path.joinpath(file_path.with_name(file_path.stem + "-compressed" + file_path.suffix).name)
        LOGGER.info(f"({i+1}/{paths_count}) Compressing {file_path}...")
        handle_file_compression(arguments, file_path.absolute(), gen_target_path)
    return


def handle_file_compression(arguments: Namespace, source_path: Path, target_path: Path):

    # Check path
    if target_path.exists():
        LOGGER.warning(f"Target path '{target_path}' already exists in the filesystem.")

    if target_path.is_dir():
        LOGGER.warning("Target path can't be directory path when compressing file.")
        return
    
    if (source_path.stat().st_size / 1024 < arguments.sizekB):
        shutil.copyfile(source_path, target_path)
        LOGGER.warning(f"Source file below required file size. Copying original file: '{source_path}'.")
        return

    # Remove images
    writer: PdfWriter = PdfWriter(clone_from=source_path)
    if arguments.clear_images:
        writer.remove_images()

    # Compress identical objects
    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    for page in writer.pages:
        if arguments.level > 0:
            page.compress_content_streams(level=arguments.level)
            
    with open(target_path, "wb") as target:
        writer.write(target)
        
    # Compress images after dupliates have been removed
    writer: PdfWriter = PdfWriter(clone_from=target_path)
    for page in writer.pages:
        handle_image_compression(arguments, page)

    with open(target_path, "wb") as target:
        writer.write(target)

    LOGGER.debug(f"Compressed {source_path}")

    # Replace with original if file size is bigger
    if target_path.stat().st_size > source_path.stat().st_size:
        shutil.copyfile(source_path, target_path)
        LOGGER.warning(f"Compressed file was bigger than original file. Copying original file: '{source_path}'.")

    global compressed_amount
    compressed_amount += 1


def handle_image_compression(arguments: Namespace, page):
    try:
        if (len(page.images) > arguments.image_count):
            return
        
        relevant_images = [x for x in page.images if x.image.width > arguments.image_max_width]
        if (len(relevant_images) == 0):
            return
        
        i: int = 1
        LOGGER.debug(f"- Relevant images: {len(relevant_images)}")
        for img in relevant_images:
            LOGGER.debug(f"- - Image {i}/{len(relevant_images)}")
            pil_img = img.image
            ratio = arguments.image_max_width / pil_img.width
            new_size = (arguments.image_max_width, int(pil_img.height * ratio))
            pil_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
            img.replace(pil_img)
            i += 1

    except Exception as ex:
        LOGGER.warning(f"Image compression failed: {ex}")


if __name__ == "__main__":
    main()
