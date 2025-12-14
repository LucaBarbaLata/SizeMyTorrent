# SizeMyTorrent

**SizeMyTorrent** is a lightweight Python utility that lets you select multiple `.torrent` files and instantly calculate how much disk space is required **before** you start downloading.

It works both from the command line or via a file picker when no torrents are specified.

No trackers. No clients. No surprises. Open Source!

---

## ✨ Features

* 📂 Select **multiple torrent files** at once, via CLI or file picker
* 📏 Calculates **exact required disk space**
* 📦 Supports **single-file** and **multi-file** torrents
* 🧮 Human-readable output (B / KB / MB / GB / TB, auto-adjusted)
* 🌈 Colored terminal output
* 🗂️ Optional `-lA` flag to list all files inside each torrent in a tree view
* 💾 Optional `-o FILE` flag to save results to a file
* ⚡ Works **offline** (reads torrent metadata only)
* 🐍 Simple, clean Python code

---

## 📸 Example Output

```text
Torrent sizes:
----------------------------------------
Ubuntu.iso.torrent → 4.56 GB
Anime.Pack.torrent → 38.21 GB
Movie.Collection.torrent → 92.03 GB

TOTAL REQUIRED SPACE: 134.80 GB

With -lA:
Ubuntu.iso.torrent → 4.56 GB
  └─ Ubuntu.iso : 4.56 GB
Anime.Pack.torrent → 38.21 GB
  └─ Anime/Show1.mkv : 22.00 GB
  └─ Anime/Show2.mkv : 16.21 GB
```

---

## 🔧 Requirements

* Python **3.9+**
* `bencodepy`
* `colorama`

Install dependencies:

```bash
pip install bencodepy colorama
```

> `tkinter` is included by default with most Python installations.

---

## 🚀 Usage

1. Clone the repository:

```bash
git clone https://github.com/LucaBarbaLata/SizeMyTorrent.git
cd SizeMyTorrent
```

2. Run the script (CLI or file picker mode):

```bash
# Use file picker if no arguments provided
python sizemytorrent.py

# Or provide torrent files as arguments
python sizemytorrent.py *.torrent

# List all files inside torrents
python sizemytorrent.py *.torrent -lA

# Save output to a file
python sizemytorrent.py *.torrent -lA -o report.txt
```

---

## 🧠 How It Works

* Opens and decodes `.torrent` files using **bencode**
* Reads the `info` dictionary
* Sums file sizes:

  * `length` for single-file torrents
  * `files[].length` for multi-file torrents
* Supports optional listing of all files in a tree view

No network access is required.

---

## 🛠️ Project Structure

```text
SizeMyTorrent/
├── sizemytorrent.py
└── README.md
```

---

## 💡 Possible Future Improvements

* 📊 Export results to CSV / JSON
* 🖥️ Full GUI application
* 🧲 Magnet link support (metadata fetch)
* 📁 Custom output directory size estimation
* 🌳 Prettier folder tree display

---

## 🤝 Contributing

Pull requests are welcome!
Feel free to open an issue for ideas, bugs, or improvements.

---

## 📜 License

MIT License – do whatever you want, just give credit.
