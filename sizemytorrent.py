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

def format_size(bytes_size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"

def get_torrent_size(torrent_path):
    with open(torrent_path, "rb") as f:
        torrent = bencodepy.decode(f.read())

    info = torrent[b"info"]

    # Single-file torrent
    if b"length" in info:
        return info[b"length"], [(info[b"name"].decode(), info[b"length"])]

    # Multi-file torrent
    total = 0
    files_list = []
    for file in info[b"files"]:
        file_size = file[b"length"]
        total += file_size
        path = "/".join([p.decode() for p in file[b"path"]])
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

    print(Fore.CYAN + "\nTorrent sizes:\n" + "-"*40)
    output_lines.append("Torrent sizes:\n" + "-"*40)

    for torrent in args.torrents:
        size, files = get_torrent_size(torrent)
        grand_total += size
        torrent_name = os.path.basename(torrent)
        line = f"{Fore.YELLOW}{torrent_name}{Style.RESET_ALL} → {Fore.GREEN}{format_size(size)}{Style.RESET_ALL}"
        print(line)
        output_lines.append(f"{torrent_name} → {format_size(size)}")

        if args.list_all:
            for file_path, file_size in files:
                tree_line = f"  └─ {file_path} : {format_size(file_size)}"
                print(Fore.WHITE + tree_line)
                output_lines.append(f"  {file_path} : {format_size(file_size)}")

    total_line = f"\n{Fore.CYAN}TOTAL REQUIRED SPACE: {Fore.MAGENTA}{format_size(grand_total)}{Style.RESET_ALL}"
    print(total_line)
    output_lines.append(f"TOTAL REQUIRED SPACE: {format_size(grand_total)}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for line in output_lines:
                # Remove color codes for the file
                clean_line = ''.join(c for c in line if c not in (Fore.CYAN, Fore.YELLOW, Fore.GREEN, Fore.WHITE, Fore.MAGENTA, Style.RESET_ALL))
                f.write(clean_line + "\n")
        print(Fore.BLUE + f"\nOutput saved to {args.output}")

if __name__ == "__main__":
    print(ascii_art)
    main()
