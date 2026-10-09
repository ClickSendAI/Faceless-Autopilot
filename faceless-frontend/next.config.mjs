/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

// Base44 sandbox: proxy API calls through the Next.js dev server (single origin)
if (process.env.BASE44_PREVIEW_MODE === '1') {
  nextConfig.rewrites = async () => [
    { source: '/svc/ai-content/:path*', destination: 'http://ai-content:8561/:path*' },
    { source: '/svc/platform-apis/:path*', destination: 'http://platform-apis:8562/:path*' },
    { source: '/svc/analytics/:path*', destination: 'http://analytics:8563/:path*' },
  ]
  if (process.env.BASE44_PUBLIC_HOST_SUFFIX) {
    nextConfig.allowedDevOrigins = ['https://3000-' + process.env.BASE44_PUBLIC_HOST_SUFFIX]
  }
}

export default nextConfig
