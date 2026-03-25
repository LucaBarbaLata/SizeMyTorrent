import re
import bencodepy
import os
import argparse
from colorama import Fore, Style, init
from tkinter import Tk, filedialog

init(autoreset=True)  # enable color output

# ASCII Art
ascii_art = f"""{Fore.CYAN}
 $$$$$$\  $$\                           $$\      $$\                 $$$$$$$$\                                                 $$\
$$  __$$\ \__|                          $$$\    $$$ |                \__$$  __|                                                $$ |
$$ /  \__|$$\ $$$$$$$$\  $$$$$$\        $$$$\  $$$$ |$$\   $$\          $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$\ $$$$$$\
\$$$$$$\  $$ |\____$$  |$$  __$$\       $$\$$\$$ $$ |$$ |  $$ |         $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\\_$$  _|
 \____$$\ $$ |  $$$$ _/ $$$$$$$$ |      $$ \$$$  $$ |$$ |  $$ |         $$ |$$ /  $$ |$$ |  \__|$$ |  \__|$$$$$$$$ |$$ |  $$ | $$ |
$$\   $$ |$$ | $$  _/   $$   ____|      $$ |\$  /$$ |$$ |  $$ |         $$ |$$ |  $$ |$$ |      $$ |      $$   ____|$$ |  $$ | $$ |$$\
\$$$$$$  |$$ |$$$$$$$$\ \$$$$$$$\       $$ | \_/ $$ |\$$$$$$$ |         $$ |\$$$$$$  |$$ |      $$ |      \$$$$$$$\ $$ |  $$ | \$$$$  |
 \______/ \__|\________| \_______|      \__|     \__| \____$$ |         \__| \______/ \__|      \__|       \_______|\__|  \__|  \____/
                                                     $$\   $$ |
                                                     \$$$$$$  |
                                                      \______/
{Style.RESET_ALL}"""

ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text):
    return ANSI_ESCAPE.sub("", text)


def format_size(bytes_size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"


def get_torrent_size(torrent_path):
    try:
        with open(torrent_path, "rb") as f:
            torrent = bencodepy.decode(f.read())
    except OSError as e:
        raise OSError(f"Could not read '{torrent_path}': {e}") from e
    except Exception as e:
        raise ValueError(f"Could not parse '{torrent_path}': {e}") from e

    try:
        info = torrent[b"info"]
    except (KeyError, TypeError) as e:
        raise ValueError(f"'{torrent_path}' is not a valid torrent file (missing info dict)") from e

    # Single-file torrent
    if b"length" in info:
        name = info[b"name"].decode("utf-8", errors="replace")
        return info[b"length"], [(name, info[b"length"])]

    # Multi-file torrent
    if b"files" not in info:
        raise ValueError(f"'{torrent_path}' has an unrecognised torrent structure")

    total = 0
    files_list = []
    for file in info[b"files"]:
        file_size = file[b"length"]
        total += file_size
        path = "/".join(p.decode("utf-8", errors="replace") for p in file[b"path"])
        files_list.append((path, file_size))
    return total, files_list


def main():
    parser = argparse.ArgumentParser(description="Calculate torrent disk usage")
    parser.add_argument("torrents", nargs="*", help="Paths to torrent files")
    parser.add_argument("-lA", "--list-all", action="store_true", help="List all files in each torrent")
    parser.add_argument("-o", "--output", help="Save output to a file")
    args = parser.parse_args()

    # If no torrents provided, open file picker
    if not args.torrents:
        Tk().withdraw()  # hide main window
        args.torrents = filedialog.askopenfilenames(
            title="Select torrent files",
            filetypes=[("Torrent files", "*.torrent")]
        )
        if not args.torrents:
            print(Fore.RED + "No torrents selected. Exiting.")
            return

    grand_total = 0
    output_lines = []

    def emit(colored_text):
        """Print a colored line and record the plain-text version."""
        print(colored_text)
        output_lines.append(strip_ansi(colored_text))

    emit(Fore.CYAN + "\nTorrent sizes:\n" + "-" * 40)

    for torrent in args.torrents:
        try:
            size, files = get_torrent_size(torrent)
        except (OSError, ValueError) as e:
            emit(Fore.RED + f"  [error] {e}")
            continue

        grand_total += size
        torrent_name = os.path.basename(torrent)
        emit(f"{Fore.YELLOW}{torrent_name}{Style.RESET_ALL} → {Fore.GREEN}{format_size(size)}{Style.RESET_ALL}")

        if args.list_all:
            for file_path, file_size in files:
                emit(Fore.WHITE + f"  └─ {file_path} : {format_size(file_size)}")

    emit(f"\n{Fore.CYAN}TOTAL REQUIRED SPACE: {Fore.MAGENTA}{format_size(grand_total)}{Style.RESET_ALL}")

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines) + "\n")
            print(Fore.BLUE + f"\nOutput saved to {args.output}")
        except OSError as e:
            print(Fore.RED + f"Could not write output file: {e}")


if __name__ == "__main__":
    print(ascii_art)
    main()
