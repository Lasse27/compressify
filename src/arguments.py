import argparse

def argparse_init() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("level", help="Specifies the level of the compression applied to targeted files.")
    args = parser.parse_args()
    print(args)
    
    
if __name__ == "__main__":
    argparse_init()