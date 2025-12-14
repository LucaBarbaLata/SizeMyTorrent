# SizeMyTorrent

**SizeMyTorrent** is a lightweight Python utility that lets you select multiple `.torrent` files and instantly calculate how much disk space is required **before** you start downloading.

No trackers. No clients. No surprises.

---

## ✨ Features

* 📂 Select **multiple torrent files** at once
* 📏 Calculates **exact required disk space**
* 📦 Supports **single-file** and **multi-file** torrents
* 🧮 Human-readable output (MB / GB / TB)
* ⚡ Works **offline** (reads torrent metadata only)
* 🐍 Simple, clean Python code

---

## 📸 Example Output

```text
Torrent sizes:
------------------------------
Ubuntu.iso.torrent → 4.56 GB
Anime.Pack.torrent → 38.21 GB
Movie.Collection.torrent → 92.03 GB

------------------------------
TOTAL REQUIRED SPACE: 134.80 GB
```

---

## 🔧 Requirements

* Python **3.9+**
* `bencodepy`

Install dependency:

```bash
pip install bencodepy
```

> `tkinter` is included by default with most Python installations.

---

## 🚀 Usage

1. Clone the repository:

```bash
git clone https://github.com/lucabarbalata/SizeMyTorrent.git
cd SizeMyTorrent
```

2. Run the script:

```bash
python sizemytorrent.py
```

3. Select one or more `.torrent` files when the file picker opens

4. View the calculated disk space in the terminal

---

## 🧠 How It Works

* Opens and decodes `.torrent` files using **bencode**
* Reads the `info` dictionary
* Sums file sizes:

  * `length` for single-file torrents
  * `files[].length` for multi-file torrents

No network access is required.

---

## 🛠️ Project Structure

```text
SizeMyTorrent/
├── sizemytorrent.py
└──README.md
```

---

## 💡 Possible Future Improvements

* 📊 Export results to CSV / JSON
* 🧠 Detect duplicate files across torrents
* 🖥️ Full GUI application
* 🧲 Magnet link support (metadata fetch)
* 📁 Custom output directory size estimation

---

## 🤝 Contributing

Pull requests are welcome!
Feel free to open an issue for ideas, bugs, or improvements.

---