import argparse as args


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
        "-d","--dest", 
        default=None,
        type=str, 
        metavar="Path",
        dest="destination",
        help="optional destination path of the compressed file or files.")

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="enable recursive file search when compressing a directory",
    )

    parser.add_argument(
        "-l",
        "--level",
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
        "-c", "--clear-images",
        action="store_true",
        dest="clear_images",
        help="removes images from compressed files"
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
