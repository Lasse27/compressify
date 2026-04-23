from output import Console
from pathlib import Path
import arguments as args
from argparse import Namespace
from pypdf import PdfWriter


def main() -> None:

    # Create output console and read command line arguments
    console: Console = Console()
    arguments = args.get_arguments()

    # Configure logging in console
    console.toggle_output(arguments.verbose)
    console.toggle_colorized(not arguments.no_color)
    console.toggle_timestamps(arguments.timestamps)
    print_execution_header(console, arguments)

    # Check paths
    source_path = Path(arguments.source)
    if arguments.destination is None:
        destination_path = source_path
    else:
        destination_path = Path(arguments.destination)

    if not source_path.exists():
        console.log_warn(f"Source path '{source_path}' doesn't exist in the filesystem.")
        return

    if source_path.is_dir():
        handle_dir_compression(console, arguments, source_path, destination_path)

    if source_path.is_file():
        handle_file_compression(console, arguments, source_path, destination_path)


def print_execution_header(console: Console, arguments: Namespace) -> None:
    console.log_info("Running compressify with arguments:")
    for ident, value in arguments._get_kwargs():
        console.log_raw(f"> {ident}: {value}")


def handle_dir_compression(console: Console, arguments: Namespace, source_path: Path, target_path: Path) -> None:

    # Check path
    if target_path.is_file():
        console.log_warn("Target path can't be file path when compressing directory.")
        return

    # Collect files
    paths: list[Path] = []
    console.log_info("Collecting files...'")
    for path_object in source_path.rglob("*.pdf"):
        if path_object.is_file():
            paths.append(path_object)

    # Logging collection
    paths_count = len(paths)
    if paths_count == 0:
        console.log_warn(f"{paths_count} pdf files found.")
    else:
        console.log_raw(f"> {paths_count} pdf files found.")

    # Compressing all collected files
    console.log_info("Compressing files...")
    for file_path in paths:
        gen_target_path = target_path.joinpath(file_path.with_name(file_path.stem + "-compressed" + file_path.suffix).name)
        handle_file_compression(console, arguments, file_path.absolute(), gen_target_path)
    return


def handle_file_compression(console: Console, arguments: Namespace, source_path: Path, target_path: Path):

    # Check path
    if target_path.exists():
        console.log_warn(f"Target path '{target_path}' already exists in the filesystem.")
        if not console.simple_prompt("Overwrite existing file?"):
            return

    if target_path.is_dir():
        console.log_warn("Target path can't be directory path when compressing file.")
        return

    writer: PdfWriter = PdfWriter(clone_from=source_path)
    if arguments.clear_images:
        writer.remove_images()

    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    
    # Lossless compression
    for page in writer.pages:
        if arguments.level > 0:
            page.compress_content_streams(level=arguments.level)
        if arguments.image_compression < 100:
            for img in page.images:
                img.replace(img.image, quality=arguments.image_compression)

    writer.write(target_path)
    console.log_raw(f"> Compressed {source_path}")


if __name__ == "__main__":
    main()
