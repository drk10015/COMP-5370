from nosj_parser import NOSJ_Parser
import argparse, sys, os



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse NOSJ data")
    parser.add_argument("--file-name", "-f", type=str, help="File name to parse")
    args = parser.parse_args()
    if (not os.path.exists(args.file_name)):
        print(f"ERROR -- File does not exist. ({args.file_name})", file=sys.stderr)
        sys.exit(66)
    with open(args.file_name, 'r') as file:
        data = file.read()
    parser = NOSJ_Parser(data)
    parsed_data = parser.parse()
    parser.print_parsed_data(parsed_data)
    sys.exit(0)



    