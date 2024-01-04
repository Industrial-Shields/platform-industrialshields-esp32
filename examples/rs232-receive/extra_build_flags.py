import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse extra build flags.")
    parser.add_argument("-v", "--version", type=int, help="Set version level")
    parser.add_argument("--click1", type=str, help="Specify click1 option")
    parser.add_argument("--click2", type=str, help="Specify click2 option")

    return parser.parse_args()


def click_macros(click: str, number: int) -> str:
    if click == "GPRS":
        return f"-DEXPANSION_MODULE{number}_GPRS "
    else:
        raise(f"Unknown type of click: {click}, only valid"
        "values are: GPRS")

if __name__ == "__main__":
    args = parse_arguments()

    if args.version is not None:
        if args.version == 1:
            print("-DESP32PLC_V1 ")
        elif args.version == 3:
            print("-DESP32PLC_V3 ")
        else:
            raise("You need to specify version 3 or 1 of the ESP32 PLC")

    if args.click1 is not None:
        print(click_macros(args.click1, 1))
    if args.click2 is not None:
        print(click_macros(args.click2, 2))
