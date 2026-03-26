import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "img.youtube.com", // ✅ ADD THIS (CRITICAL FIX)
      },
      {
        protocol: "https",
        hostname: "**.ytimg.com",
      },
      {
        protocol: "https",
        hostname: "**.fbcdn.net",
      },
      {
        protocol: "https",
        hostname: "**.cdninstagram.com",
      },
      {
        protocol: "https",
        hostname: "**.twimg.com",
      },
      {
        protocol: "https",
        hostname: "**.vimeocdn.com",
      },
      {
        protocol: "https",
        hostname: "**.redd.it",
      },
      {
        protocol: "https",
        hostname: "**.redditmedia.com",
      },
      {
        protocol: "https",
        hostname: "via.placeholder.com", // ✅ for fallback image
      },
    ],
  },
};

export default nextConfig;