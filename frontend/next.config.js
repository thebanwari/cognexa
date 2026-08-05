/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove experimental appDir for Next.js 16 compatibility
  webpack: (config) => {
    // Mermaid.js compatibility
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
    };
    return config;
  },
  // Enable Turbopack explicitly to avoid conflicts
  experimental: {},
}

module.exports = nextConfig