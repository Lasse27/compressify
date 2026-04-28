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
        help="optional destination path of the compressed file or files")

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
        metavar="0-9 [9]",
        help="specify the level of compression applied to targeted files",
    )

    parser.add_argument(
        "-s",
        "--sizekB",
        dest="sizekB",
        default=250,
        type=int,
        metavar="[250]",
        help="pdf documents with less file size (kB) than this will be skipped while compressing",
    )

    parser.add_argument(
        "-i",
        "--imagec",
        dest="image_count",
        default=25,
        type=int,
        metavar="[25]",
        help="pdf pages which have more images than this will be skipped while compressing",
    )
    
    parser.add_argument(
        "-w",
        "--imagew",
        dest="image_max_width",
        default=1280,
        type=int,
        metavar="[1280]",
        help="maximum width of images in target files",
    )
    
    parser.add_argument(
        "-c", "--clear-images",
        action="store_true",
        dest="clear_images",
        help="removes images from compressed files"
    )

    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        type=str,
        default=0,
        metavar="0-5",
        help="specify how verbose the output in the console should be.",
    )

    parser.add_argument(
        "-t",
        "--timestamps",
        action="store_true",
        dest="timestamps",
        help="enable timestamps in verbose console output",
    )

    return parser.parse_args()
