"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Play, Pause, Download, RefreshCw } from "lucide-react"

interface ContentGeneratorProps {
  onGenerate: (content: any) => void
}

export function ContentGenerator({ onGenerate }: ContentGeneratorProps) {
  const [step, setStep] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [formData, setFormData] = useState({
    topic: "",
    niche: "",
    format: "",
    voice: "",
    duration: "",
    platforms: [] as string[]
  })

  const niches = [
    "Personal Finance",
    "Health & Fitness", 
    "Technology",
    "Business",
    "Motivation",
    "Education"
  ]

  const formats = [
    "Tips & Tricks",
    "Educational",
    "Motivational",
    "Entertainment",
    "News & Updates"
  ]

  const voices = [
    "Professional Male",
    "Professional Female", 
    "Casual Male",
    "Casual Female",
    "Energetic"
  ]

  const platforms = [
    { id: "youtube", name: "YouTube Shorts", icon: "📺" },
    { id: "tiktok", name: "TikTok", icon: "🎵" },
    { id: "instagram", name: "Instagram Reels", icon: "📸" }
  ]

  const handleGenerate = async () => {
    if (!formData.topic || !formData.niche || formData.platforms.length === 0) {
      alert("Please fill in all required fields")
      return
    }

    setIsGenerating(true)
    setProgress(0)
    
    try {
      // Call the real AI Content API
      const response = await api.aiContent.generateContent({
        topic: formData.topic,
        niche: formData.niche,
        format: formData.format as 'short' | 'medium' | 'long' || 'short',
        duration: formData.format === 'tips & tricks' ? 60 : formData.format === 'educational' ? 180 : 300,
        voice_id: formData.voice || 'default',
        platforms: formData.platforms,
        style: 'educational',
        tone: 'professional'
      })

      setProgress(50)
      
      // Poll for status updates
      const pollStatus = async () => {
        try {
          const statusResponse = await api.aiContent.getContentStatus(response.content_id)
          setProgress(Math.min(90, progress + 10))
          
          if (statusResponse.status === 'completed') {
            setProgress(100)
            setIsGenerating(false)
            
            const generatedContent = {
              id: response.content_id,
              title: `AI-Generated: ${formData.topic}`,
              description: `Automatically generated content about ${formData.topic}`,
              platform: formData.platforms[0] || "youtube",
              thumbnail: "/placeholder.svg",
              video_url: statusResponse.video_url,
              views: "0",
              engagement: "0%",
              status: "generated"
            }
            
            onGenerate(generatedContent)
          } else if (statusResponse.status === 'failed') {
            alert(`Generation failed: ${statusResponse.error_message}`)
            setIsGenerating(false)
          } else {
            // Continue polling
            setTimeout(pollStatus, 2000)
          }
        } catch (error) {
          console.error('Error polling status:', error)
          alert("Error checking generation status")
          setIsGenerating(false)
        }
      }

      // Start polling after a short delay
      setTimeout(pollStatus, 2000)

    } catch (error) {
      console.error('Content generation failed:', error)
      alert("Failed to start content generation")
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <RefreshCw className="h-5 w-5" />
            AI Content Generator
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Step 1: Topic & Niche */}
          <div className="space-y-4">
            <div>
              <Label htmlFor="topic">Topic or Keyword</Label>
              <Input
                id="topic"
                placeholder="e.g., '5 Money Mistakes That Keep You Poor'"
                value={formData.topic}
                onChange={(e) => setFormData({...formData, topic: e.target.value})}
              />
            </div>
            
            <div>
              <Label>Content Niche</Label>
              <Select onValueChange={(value) => setFormData({...formData, niche: value})}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a niche" />
                </SelectTrigger>
                <SelectContent>
                  {niches.map((niche) => (
                    <SelectItem key={niche} value={niche.toLowerCase()}>
                      {niche}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Step 2: Format & Voice */}
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label>Content Format</Label>
              <Select onValueChange={(value) => setFormData({...formData, format: value})}>
                <SelectTrigger>
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent>
                  {formats.map((format) => (
                    <SelectItem key={format} value={format.toLowerCase()}>
                      {format}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Voice Style</Label>
              <Select onValueChange={(value) => setFormData({...formData, voice: value})}>
                <SelectTrigger>
                  <SelectValue placeholder="Select voice" />
                </SelectTrigger>
                <SelectContent>
                  {voices.map((voice) => (
                    <SelectItem key={voice} value={voice.toLowerCase()}>
                      {voice}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Step 3: Platform Selection */}
          <div>
            <Label>Target Platforms</Label>
            <div className="flex flex-wrap gap-2 mt-2">
              {platforms.map((platform) => (
                <Button
                  key={platform.id}
                  variant={formData.platforms.includes(platform.id) ? "default" : "outline"}
                  size="sm"
                  onClick={() => {
                    const newPlatforms = formData.platforms.includes(platform.id)
                      ? formData.platforms.filter(p => p !== platform.id)
                      : [...formData.platforms, platform.id]
                    setFormData({...formData, platforms: newPlatforms})
                  }}
                >
                  <span className="mr-2">{platform.icon}</span>
                  {platform.name}
                </Button>
              ))}
            </div>
          </div>

          {/* Generation Progress */}
          {isGenerating && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Generating content...</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} className="w-full" />
            </div>
          )}

          {/* Generate Button */}
          <Button 
            onClick={handleGenerate}
            disabled={!formData.topic || !formData.niche || isGenerating}
            className="w-full"
            size="lg"
          >
            {isGenerating ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Play className="mr-2 h-4 w-4" />
                Generate Content
              </>
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
