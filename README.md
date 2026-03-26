# 🚀 Universal Video Downloader

A full-stack web application that allows users to download videos from multiple platforms (like YouTube) in different qualities, including audio (MP3), 
with real-time progress tracking and a modern UI.

---

## 🌟 Features

* 🎥 Download videos in multiple resolutions (144p → 1080p+)
* 🎵 Extract audio as MP3
* ⚡ Real-time download progress (speed, ETA, percentage)
* 🧠 Smart format selection (video + audio merging)
* 🖼️ Video preview (thumbnail + title + duration)
* 📂 Download history with delete options
* 🌐 Supports multiple platforms (YouTube + extendable)
* 💻 Clean and responsive UI

---

## 🏗️ Tech Stack

### Frontend

* Next.js (React)
* TypeScript
* Tailwind CSS
* Axios

### Backend

* FastAPI
* yt-dlp (video extraction & download)
* FFmpeg (audio/video merging)
* SQLite (download history)

---

## 📁 Project Structure

```
universal-video-downloader/
├── frontend/        # Next.js frontend
├── backend/         # FastAPI backend
├── storage/         # Temporary downloaded files
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone Repository

```
git clone https://github.com/atishkamble0504/universal-video-downloader.git
cd universal-video-downloader
```

---

### 🔹 2. Backend Setup (FastAPI)

```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

#### ▶ Run Backend

```
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 🔹 3. Frontend Setup (Next.js)

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🔧 Requirements

Make sure you have installed:

* Python 3.9+
* Node.js (v18+ recommended)
* FFmpeg (must be added to PATH)

---

## 📸 Screenshots

> Add your screenshots here

```
/screenshots/home.png
/screenshots/download.png
```

---

## ⚠️ Disclaimer

This project is for educational purposes only.
Downloading copyrighted content without permission may violate platform terms and local laws. Use responsibly.

---

## 📌 Future Improvements

* Instagram / Twitter support
* Better platform detection
* Cloud deployment
* User authentication
* Queue system for downloads

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Atish Kamble**

---

## ⭐ Support

If you like this project, please ⭐ the repository on GitHub!
