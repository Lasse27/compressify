import argparse as args
import datetime as dt
from output import Console
from pathlib import Path


def get_arguments() -> args.Namespace:
    parser = args.ArgumentParser(
        "compressify",
        description="CLI tool for compressing pdf files locally.",
    )

    parser.add_argument(
        "source",
        type=str,
        help="source path of the file or directory that should be compressed.",
    )

    parser.add_argument(
        "target", type=str, help="target path of the compressed file or files."
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="enable recursive file search when compressing a directory",
    )

    parser.add_argument(
        "-f",
        "--filter",
        nargs=1,
        dest="filter",
        default=None,
        type=str,
        metavar="REGEX",
        help="specify a filter expression for the targeted files.",
    )

    parser.add_argument(
        "-l",
        "--level",
        nargs=1,
        dest="level",
        default=9,
        type=int,
        metavar="0-9",
        help="specify the level of compression applied to targeted files",
    )

    parser.add_argument(
        "-i",
        "--imagec",
        dest="image_compression",
        default=100,
        type=int,
        metavar="0-100",
        help="percentual compression of images in targeted files",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="enable verbose output in the console",
    )

    parser.add_argument(
        "-t",
        "--timestamps",
        action="store_true",
        dest="timestamps",
        help="enable timestamps in verbose console output",
    )

    parser.add_argument(
        "-n",
        "--no-color",
        action="store_true",
        dest="no_color",
        help="enable colorized text in verbose console output",
    )

    return parser.parse_args()


def print_execution_header(console: Console, arguments: args.Namespace) -> None:
    console.log_info(f"Running compressify with arguments:")
    for ident, value in arguments._get_kwargs():
        console.log_raw(f"> {ident}: {value}")


def main() -> None:
    console: Console = Console()
    arguments = get_arguments()

    # Configure logging in console
    console.toggle_output(arguments.verbose)
    console.toggle_colorized(not arguments.no_color)
    console.toggle_timestamps(arguments.timestamps)
    print_execution_header(console, arguments)

    # Collect files
    console.log_info("Collecting files")

    # compress at level

    # compress images


if __name__ == "__main__":
    main()
