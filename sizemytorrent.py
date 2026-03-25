import re
import sys
import os
import argparse
import bencodepy
from colorama import Fore, Style, init

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
    """Return (total_bytes, internal_name, [(path, size), ...])."""
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

    name = info.get(b"name", b"unknown").decode("utf-8", errors="replace")

    # Single-file torrent
    if b"length" in info:
        return info[b"length"], name, [(name, info[b"length"])]

    # Multi-file torrent
    if b"files" not in info:
        raise ValueError(f"'{torrent_path}' has an unrecognised torrent structure")

    total = 0
    files_list = []
    for file in info[b"files"]:
        file_size = file.get(b"length", 0)
        total += file_size
        path = "/".join(p.decode("utf-8", errors="replace") for p in file[b"path"])
        files_list.append((path, file_size))
    return total, name, files_list


def main():
    parser = argparse.ArgumentParser(description="Calculate torrent disk usage")
    parser.add_argument("torrents", nargs="*", help="Paths to torrent files")
    parser.add_argument("-lA", "--list-all", action="store_true", help="List all files in each torrent")
    parser.add_argument("-s", "--sort", action="store_true", help="Sort torrents by size (largest first)")
    parser.add_argument("-o", "--output", help="Save output to a file")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output (useful for piping)")
    args = parser.parse_args()

    if args.no_color:
        init(strip=True, autoreset=True)
        print(strip_ansi(ascii_art))
    else:
        print(ascii_art)

    # If no torrents provided, open file picker
    if not args.torrents:
        try:
            from tkinter import Tk, filedialog
        except ImportError:
            print(Fore.RED + "tkinter is not available. Pass torrent files as arguments.")
            sys.exit(1)
        root = Tk()
        root.withdraw()
        selected = filedialog.askopenfilenames(
            title="Select torrent files",
            filetypes=[("Torrent files", "*.torrent")]
        )
        root.destroy()
        if not selected:
            print(Fore.RED + "No torrents selected. Exiting.")
            sys.exit(0)
        args.torrents = selected

    # Parse all torrents, separating successes from failures
    results = []
    errors = []
    for torrent_path in args.torrents:
        try:
            size, name, files = get_torrent_size(torrent_path)
            results.append((torrent_path, size, name, files))
        except (OSError, ValueError) as e:
            errors.append(str(e))

    if args.sort:
        results.sort(key=lambda r: r[1], reverse=True)

    grand_total = sum(r[1] for r in results)
    output_lines = []

    def emit(colored_text):
        """Print a colored line and record the plain-text version."""
        print(colored_text)
        output_lines.extend(strip_ansi(colored_text).splitlines())

    emit(Fore.CYAN + "\nTorrent sizes:\n" + "-" * 40)

    for torrent_path, size, name, files in results:
        torrent_filename = os.path.basename(torrent_path)
        emit(f"{Fore.YELLOW}{torrent_filename}{Style.RESET_ALL} → {Fore.GREEN}{format_size(size)}{Style.RESET_ALL}")

        if args.list_all:
            multifile = len(files) > 1
            if multifile:
                emit(Fore.WHITE + f"  └─ {name}/")
                file_indent = "       └─ "
            else:
                file_indent = "  └─ "

            for file_path, file_size in files:
                pct = (file_size / size * 100) if size > 0 else 0
                emit(Fore.WHITE + f"{file_indent}{file_path} : {format_size(file_size)} ({pct:.1f}%)")

    for err in errors:
        emit(Fore.RED + f"  [error] {err}")

    emit(f"\n{Fore.CYAN}TOTAL REQUIRED SPACE: {Fore.MAGENTA}{format_size(grand_total)}{Style.RESET_ALL}")

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines) + "\n")
            print(Fore.BLUE + f"\nOutput saved to {args.output}")
        except OSError as e:
            print(Fore.RED + f"Could not write output file: {e}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
