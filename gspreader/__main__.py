from gspreader import get_sheet


def main():
    sheet = get_sheet("Language", "phrases")
    print(sheet)


if __name__ == "__main__":
    main()
