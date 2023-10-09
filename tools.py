import argparse


def create_parser():
    parser = argparse.ArgumentParser("CLI for Tools")
    parser.add_argument(
        "-t", "--tools", action="store_true", help="List available tools"
    )
    parser.add_argument("tool_name", nargs="?", help="Specify the tool name")
    return parser


def list_tools():
    tools = {
        "anime": "Search about anime",
    }
    print("List of tools: \n")
    for k, v in tools.items():
        print(f"{k} - {v}")


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.tools:
        if args.tool_name:
            from anime import prompt, displayMethods

            while 1:
                try:
                    anime = prompt()
                    displayMethods(anime)
                except KeyboardInterrupt:
                    exit(0)
        else:
            list_tools()
    else:
        parser.print_help()
        print("\n")


if __name__ == "__main__":
    main()
