import argparse as args
import datetime as dt

def get_arguments() -> args.Namespace:
    parser = args.ArgumentParser("compressify", 
                                  description="CLI tool for compressing pdf files locally.",)

    parser.add_argument("source", 
                        type=str,
                        help="source path of the file or directory that should be compressed.")
    
    parser.add_argument("target", 
                        type=str,
                        help="target path of the compressed file or files.")
    
    parser.add_argument("-v", "--verbose", 
                        action="store_true", 
                        dest="verbose", 
                        help="enable verbose output in the console" )
    
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        dest="recursive",
                        help="enable recursive file search when compressing a directory")
    
    parser.add_argument("-t", "--timestamps",
                        action="store_true",
                        dest="timestamps",
                        help="enable timestamps in verbose console output")
    
    parser.add_argument("-l", "--level", 
                        nargs=1, 
                        dest="level", 
                        default=9, 
                        type=int,
                        metavar="VALUE",
                        help="specify the level of compression applied to targeted files")
    
    parser.add_argument("-i", "--imagec",
                        dest="image_compression",
                        default=100,
                        type=int,
                        metavar="VALUE",
                        help="percentual compression of images in targeted files")
    
    return parser.parse_args()


def print_execution_header(arguments: args.Namespace) -> None:
    print("Running compressify with arguments:")
    for ident, value in arguments._get_kwargs():
        print(f"> {ident}: {value}")


def main() -> None:
    arguments = get_arguments()
    print(print_execution_header(arguments))


if __name__ == "__main__":
    main()