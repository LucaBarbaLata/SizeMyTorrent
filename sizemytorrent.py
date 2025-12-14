import bencodepy
from tkinter import Tk, filedialog
import os

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
        return info[b"length"]

    # Multi-file torrent
    total = 0
    for file in info[b"files"]:
        total += file[b"length"]
    return total

def main():
    Tk().withdraw()  # Hide main Tk window

    torrent_files = filedialog.askopenfilenames(
        title="Select torrent files",
        filetypes=[("Torrent files", "*.torrent")]
    )

    if not torrent_files:
        print("No torrents selected.")
        return

    grand_total = 0

    print("\nTorrent sizes:\n" + "-" * 30)
    for torrent in torrent_files:
        size = get_torrent_size(torrent)
        grand_total += size
        print(f"{os.path.basename(torrent)} → {format_size(size)}")

    print("\n" + "-" * 30)
    print(f"TOTAL REQUIRED SPACE: {format_size(grand_total)}")

if __name__ == "__main__":
    main()
