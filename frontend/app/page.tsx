"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import Image from "next/image"

type Format = {
  format_id: string
  quality: string
  ext: string
  filesize?: number // already in MB
}

type VideoInfo = {
  title: string
  thumbnail: string
  duration: number
  formats: Format[]
}

type HistoryItem = {
  id: number
  title: string
  filename: string
}

export default function Home() {

  const [url, setUrl] = useState("")
  const [video, setVideo] = useState<VideoInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const [progress, setProgress] = useState("")
  const [speed, setSpeed] = useState("")
  const [eta, setEta] = useState("")
  const [downloaded, setDownloaded] = useState("")

  const [history, setHistory] = useState<HistoryItem[]>([])

  // ==============================
  // Extract Video
  // ==============================

  const extract = async () => {
    if (!url) return

    try {
      setLoading(true)

      const res = await axios.post(
        "http://127.0.0.1:8000/extract",
        { url }
      )

      setVideo(res.data)

    } catch (error) {
      console.error(error)
      alert("Failed to extract video")
    } finally {
      setLoading(false)
    }
  }

  // ==============================
  // Download Video
  // ==============================

  const downloadVideo = async (format_id: string) => {
    try {
      setDownloading(true)

      setProgress("0%")
      setSpeed("")
      setEta("")
      setDownloaded("")

      const res = await axios.post(
        "http://127.0.0.1:8000/download",
        { url, format_id }
      )

      const downloadUrl = res.data.download_url

      const link = document.createElement("a")
      link.href = downloadUrl
      link.setAttribute("download", "")
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      fetchHistory()

    } catch (error) {
      console.error(error)
      alert("Download failed")
    } finally {
      setDownloading(false)
    }
  }

  // ==============================
  // Progress Polling
  // ==============================

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/progress"
        )

        if (res.data) {
          setProgress(res.data.percent || "")
          setSpeed(res.data.speed || "")
          setEta(res.data.eta || "")
          setDownloaded(res.data.downloaded || "")
        }

      } catch {}
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  // ==============================
  // Fetch History
  // ==============================

  const fetchHistory = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/history"
      )
      setHistory(res.data)
    } catch {
      console.error("Failed to load history")
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  // ==============================
  // Delete One History Item
  // ==============================

  const deleteHistoryItem = async (id: number) => {
    if (!confirm("Delete this download from history?")) return

    try {
      await axios.delete(
        `http://127.0.0.1:8000/history/${id}`
      )
      fetchHistory()
    } catch {
      alert("Failed to delete item")
    }
  }

  // ==============================
  // Clear All History
  // ==============================

  const clearHistory = async () => {
    if (!confirm("Delete ALL download history?")) return

    try {
      await axios.delete(
        "http://127.0.0.1:8000/history"
      )
      setHistory([])
    } catch {
      alert("Failed to clear history")
    }
  }

  return (

    <div className="p-10 max-w-3xl mx-auto">

      <h1 className="text-3xl font-bold mb-6">
        Universal Video Downloader
      </h1>

      <input
        className="border p-3 w-full rounded"
        placeholder="Paste video URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button
        onClick={extract}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 mt-4 rounded"
      >
        {loading ? "Extracting..." : "Extract Video"}
      </button>

      {/* Progress */}

      {progress && (
        <div className="mt-6">

          <div className="w-full bg-gray-200 rounded">
            <div
              className="bg-green-600 text-xs text-white p-1 text-center rounded"
              style={{ width: progress }}
            >
              {progress}
            </div>
          </div>

          <div className="mt-2 text-sm text-gray-700">
            {downloaded && <p>Downloaded: {downloaded}</p>}
            {speed && <p>Speed: {speed}</p>}
            {eta && <p>Time remaining: {eta}</p>}
          </div>

        </div>
      )}

      {/* Video Info */}

      {video && (
        <div className="mt-8">

          <div className="bg-white shadow p-4 rounded">

            {/* ✅ FIXED thumbnail error */}
            {video.thumbnail && (
              <Image
                src={video.thumbnail}
                width={400}
                height={220}
                alt="thumbnail"
                className="rounded"
              />
            )}

            <h2 className="text-xl font-semibold mt-4">
              {video.title}
            </h2>

            <p className="text-gray-600 mt-2">
              Duration: {video.duration} seconds
            </p>

          </div>

          <div className="mt-4 flex flex-wrap">

            {video.formats.map((f) => (

              <button
                key={f.format_id}
                disabled={downloading}
                onClick={() => downloadVideo(f.format_id)}
                className="bg-green-600 text-white px-3 py-2 m-1 rounded hover:bg-green-700 disabled:opacity-50"
              >
                {f.quality}

                {/* ✅ FIXED size display */}
                {f.filesize
                  ? ` (${f.filesize} MB)`
                  : " (size unknown)"
                }

              </button>

            ))}

          </div>

        </div>
      )}

      {/* History */}

      <div className="mt-12">

        <div className="flex justify-between items-center mb-4">

          <h2 className="text-2xl font-semibold">
            Recent Downloads
          </h2>

          {history.length > 0 && (
            <button
              onClick={clearHistory}
              className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
            >
              Clear All
            </button>
          )}

        </div>

        {history.length === 0 && (
          <p className="text-gray-500">
            No downloads yet
          </p>
        )}

        {history.map((item) => (

          <div
            key={item.id}
            className="flex justify-between items-center border p-3 rounded mb-2"
          >

            <span className="truncate w-2/3">
              {item.title}
            </span>

            <div className="flex gap-2">

              <a
                href={`http://127.0.0.1:8000/download-file/${item.filename}`}
                className="bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700"
              >
                Download Again
              </a>

              <button
                onClick={() => deleteHistoryItem(item.id)}
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              >
                Delete
              </button>

            </div>

          </div>

        ))}

      </div>

    </div>
  )
}