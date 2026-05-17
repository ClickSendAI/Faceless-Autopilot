"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table"
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select"
import { 
  Play, 
  Pause, 
  Upload, 
  Eye, 
  Edit, 
  Trash2, 
  RefreshCw,
  Filter,
  Search
} from "lucide-react"
import { api } from "@/lib/api"

export function ContentManagement() {
  const [content, setContent] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [platformFilter, setPlatformFilter] = useState("all")

  useEffect(() => {
    loadContent()
  }, [])

  const loadContent = async () => {
    try {
      setLoading(true)
      // In a real app, this would call an API to get user's content
      // For now, we'll use mock data
      const mockContent = [
        {
          id: "content_1",
          title: "5 Money Mistakes That Keep You Poor",
          status: "completed",
          platforms: ["youtube", "tiktok"],
          views: 45000,
          engagement: 12.3,
          created_at: "2024-01-15T10:30:00Z",
          video_url: "/videos/content_1.mp4"
        },
        {
          id: "content_2", 
          title: "Morning Routine of Successful People",
          status: "processing",
          platforms: ["instagram"],
          views: 0,
          engagement: 0,
          created_at: "2024-01-15T14:20:00Z",
          video_url: null
        },
        {
          id: "content_3",
          title: "AI Tools That Will Change Your Life", 
          status: "failed",
          platforms: [],
          views: 0,
          engagement: 0,
          created_at: "2024-01-15T16:45:00Z",
          video_url: null
        }
      ]
      setContent(mockContent)
    } catch (error) {
      console.error('Failed to load content:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRegenerate = async (contentId: string) => {
    try {
      await api.aiContent.regenerateContent(contentId)
      loadContent() // Refresh the list
    } catch (error) {
      console.error('Failed to regenerate content:', error)
    }
  }

  const handleUpload = async (contentId: string) => {
    try {
      const contentItem = content.find(c => c.id === contentId)
      if (!contentItem) return

      await api.platform.uploadContent({
        content_id: contentId,
        video_url: contentItem.video_url,
        title: contentItem.title,
        description: `AI-generated content: ${contentItem.title}`,
        platforms: ["youtube", "tiktok", "instagram"],
        tags: ["ai", "automated"],
        category_id: "education",
        privacy_level: "public"
      })
      
      loadContent() // Refresh the list
    } catch (error) {
      console.error('Failed to upload content:', error)
    }
  }

  const handleDelete = async (contentId: string) => {
    if (confirm('Are you sure you want to delete this content?')) {
      try {
        // In a real app, this would call a delete API
        setContent(content.filter(c => c.id !== contentId))
      } catch (error) {
        console.error('Failed to delete content:', error)
      }
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge variant="default" className="bg-green-500">Completed</Badge>
      case 'processing':
        return <Badge variant="secondary">Processing</Badge>
      case 'failed':
        return <Badge variant="destructive">Failed</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <Play className="h-4 w-4 text-green-500" />
      case 'processing':
        return <RefreshCw className="h-4 w-4 animate-spin text-yellow-500" />
      case 'failed':
        return <Pause className="h-4 w-4 text-red-500" />
      default:
        return <Pause className="h-4 w-4 text-gray-500" />
    }
  }

  const filteredContent = content.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || item.status === statusFilter
    const matchesPlatform = platformFilter === "all" || item.platforms.includes(platformFilter)
    
    return matchesSearch && matchesStatus && matchesPlatform
  })

  if (loading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-center">
              <RefreshCw className="h-6 w-6 animate-spin mr-2" />
              Loading content...
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="h-5 w-5" />
            Content Management
          </CardTitle>
        </CardHeader>
        <CardContent>
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search content..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="processing">Processing</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
              </SelectContent>
            </Select>

            <Select value={platformFilter} onValueChange={setPlatformFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Platform" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="youtube">YouTube</SelectItem>
                <SelectItem value="tiktok">TikTok</SelectItem>
                <SelectItem value="instagram">Instagram</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Content Table */}
          <div className="border rounded-lg">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Content</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Platforms</TableHead>
                  <TableHead>Performance</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredContent.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <div>
                        <h4 className="font-medium">{item.title}</h4>
                        <p className="text-sm text-muted-foreground">
                          {new Date(item.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(item.status)}
                        {getStatusBadge(item.status)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {item.platforms.map((platform) => (
                          <Badge key={platform} variant="outline" className="text-xs">
                            {platform}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">
                        <div>{item.views.toLocaleString()} views</div>
                        <div className="text-muted-foreground">
                          {item.engagement}% engagement
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {item.status === 'completed' && item.video_url && (
                          <Button size="sm" variant="outline" asChild>
                            <a href={item.video_url} target="_blank" rel="noopener noreferrer">
                              <Eye className="h-4 w-4" />
                            </a>
                          </Button>
                        )}
                        
                        {item.status === 'completed' && (
                          <Button 
                            size="sm" 
                            variant="outline"
                            onClick={() => handleUpload(item.id)}
                          >
                            <Upload className="h-4 w-4" />
                          </Button>
                        )}
                        
                        {item.status === 'failed' && (
                          <Button 
                            size="sm" 
                            variant="outline"
                            onClick={() => handleRegenerate(item.id)}
                          >
                            <RefreshCw className="h-4 w-4" />
                          </Button>
                        )}
                        
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => handleDelete(item.id)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {filteredContent.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              No content found matching your filters.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

