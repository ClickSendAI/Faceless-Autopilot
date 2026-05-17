"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Upload, CheckCircle, AlertCircle, Clock } from "lucide-react"
import { api } from "@/lib/api"

interface ContentUploadProps {
  content: any
  onUploadComplete: (result: any) => void
}

export function ContentUpload({ content, onUploadComplete }: ContentUploadProps) {
  const [uploadData, setUploadData] = useState({
    title: content?.title || "",
    description: content?.description || "",
    platforms: [] as string[],
    tags: [] as string[],
    category: "",
    privacy: "public"
  })
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStatus, setUploadStatus] = useState("")
  const [uploadResults, setUploadResults] = useState<any[]>([])

  const platforms = [
    { id: "youtube", name: "YouTube Shorts", icon: "📺" },
    { id: "tiktok", name: "TikTok", icon: "🎵" },
    { id: "instagram", name: "Instagram Reels", icon: "📸" }
  ]

  const categories = [
    "Education",
    "Entertainment", 
    "Howto & Style",
    "Science & Technology",
    "News & Politics",
    "People & Blogs"
  ]

  const handleUpload = async () => {
    if (!uploadData.title || uploadData.platforms.length === 0) {
      alert("Please fill in title and select at least one platform")
      return
    }

    setIsUploading(true)
    setUploadProgress(0)
    setUploadStatus("Starting upload process...")

    try {
      // Call the Platform APIs service
      const response = await api.platform.uploadContent({
        content_id: content.id,
        video_url: content.video_url || "/placeholder-video.mp4",
        title: uploadData.title,
        description: uploadData.description,
        platforms: uploadData.platforms,
        tags: uploadData.tags,
        category_id: uploadData.category,
        privacy_level: uploadData.privacy
      })

      setUploadProgress(50)
      setUploadStatus("Uploading to platforms...")

      // Poll for upload status
      const pollUploadStatus = async () => {
        try {
          const statusResponse = await api.platform.getUploadStatus(response.upload_id)
          setUploadProgress(Math.min(90, uploadProgress + 10))
          
          if (statusResponse.status === 'completed') {
            setUploadProgress(100)
            setUploadStatus("Upload completed successfully!")
            setIsUploading(false)
            
            const results = statusResponse.platform_results || []
            setUploadResults(results)
            onUploadComplete({
              upload_id: response.upload_id,
              status: 'completed',
              platform_results: results
            })
          } else if (statusResponse.status === 'failed') {
            setUploadStatus(`Upload failed: ${statusResponse.error_message}`)
            setIsUploading(false)
          } else {
            // Continue polling
            setTimeout(pollUploadStatus, 3000)
          }
        } catch (error) {
          console.error('Error polling upload status:', error)
          setUploadStatus("Error checking upload status")
          setIsUploading(false)
        }
      }

      // Start polling after a short delay
      setTimeout(pollUploadStatus, 2000)

    } catch (error) {
      console.error('Upload failed:', error)
      setUploadStatus("Failed to start upload")
      setIsUploading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'processing':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload Content to Platforms
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Content Info */}
          <div className="p-4 bg-muted rounded-lg">
            <h4 className="font-medium">Content to Upload</h4>
            <p className="text-sm text-muted-foreground">
              {content?.title || "No content selected"}
            </p>
            {content?.video_url && (
              <p className="text-xs text-muted-foreground mt-1">
                Video: {content.video_url}
              </p>
            )}
          </div>

          {/* Upload Form */}
          <div className="space-y-4">
            <div>
              <Label htmlFor="title">Title *</Label>
              <Input
                id="title"
                value={uploadData.title}
                onChange={(e) => setUploadData({...uploadData, title: e.target.value})}
                placeholder="Enter video title"
              />
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={uploadData.description}
                onChange={(e) => setUploadData({...uploadData, description: e.target.value})}
                placeholder="Enter video description"
                rows={3}
              />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <Label>Category</Label>
                <Select onValueChange={(value) => setUploadData({...uploadData, category: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((category) => (
                      <SelectItem key={category} value={category.toLowerCase()}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Privacy Level</Label>
                <Select onValueChange={(value) => setUploadData({...uploadData, privacy: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select privacy" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="public">Public</SelectItem>
                    <SelectItem value="unlisted">Unlisted</SelectItem>
                    <SelectItem value="private">Private</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Platform Selection */}
            <div>
              <Label>Target Platforms *</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {platforms.map((platform) => (
                  <Button
                    key={platform.id}
                    variant={uploadData.platforms.includes(platform.id) ? "default" : "outline"}
                    size="sm"
                    onClick={() => {
                      const newPlatforms = uploadData.platforms.includes(platform.id)
                        ? uploadData.platforms.filter(p => p !== platform.id)
                        : [...uploadData.platforms, platform.id]
                      setUploadData({...uploadData, platforms: newPlatforms})
                    }}
                  >
                    <span className="mr-2">{platform.icon}</span>
                    {platform.name}
                  </Button>
                ))}
              </div>
            </div>

            {/* Tags */}
            <div>
              <Label htmlFor="tags">Tags (comma-separated)</Label>
              <Input
                id="tags"
                value={uploadData.tags.join(", ")}
                onChange={(e) => setUploadData({...uploadData, tags: e.target.value.split(",").map(t => t.trim()).filter(t => t)})}
                placeholder="Enter tags separated by commas"
              />
            </div>
          </div>

          {/* Upload Progress */}
          {isUploading && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>{uploadStatus}</span>
                <span>{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} className="w-full" />
            </div>
          )}

          {/* Upload Results */}
          {uploadResults.length > 0 && (
            <div className="space-y-2">
              <h4 className="font-medium">Upload Results</h4>
              {uploadResults.map((result, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(result.status)}
                    <span className="font-medium capitalize">{result.platform}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {result.url && (
                      <Button size="sm" variant="outline" asChild>
                        <a href={result.url} target="_blank" rel="noopener noreferrer">
                          View
                        </a>
                      </Button>
                    )}
                    <Badge variant={result.status === 'completed' ? 'default' : 'destructive'}>
                      {result.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Upload Button */}
          <Button 
            onClick={handleUpload}
            disabled={!uploadData.title || uploadData.platforms.length === 0 || isUploading}
            className="w-full"
            size="lg"
          >
            {isUploading ? (
              <>
                <Upload className="mr-2 h-4 w-4 animate-pulse" />
                Uploading...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload to Platforms
              </>
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

