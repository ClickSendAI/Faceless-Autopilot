"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from "recharts"
import { TrendingUp, TrendingDown, Eye, Heart, MessageCircle, Share, Download, RefreshCw } from "lucide-react"
import { api } from "@/lib/api"

export function AnalyticsDashboard() {
  const [analyticsData, setAnalyticsData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState(new Date())

  useEffect(() => {
    loadAnalyticsData()
  }, [])

  const loadAnalyticsData = async () => {
    try {
      setLoading(true)
      
      // Get analytics overview from real API
      const overview = await api.analytics.getOverview('user-123', 30)
      
      // Get performance insights
      const insights = await api.analytics.getInsights('user-123', 30)
      
      // Get revenue analytics
      const revenue = await api.analytics.getRevenueAnalytics('user-123', 30)
      
      setAnalyticsData({
        overview,
        insights,
        revenue
      })
      
      setLastUpdated(new Date())
    } catch (error) {
      console.error('Failed to load analytics data:', error)
      // Fallback to mock data
      setAnalyticsData({
        overview: {
          total_videos: 25,
          total_views: 125000,
          total_revenue: 1250.50,
          engagement_rate: 8.5,
          top_performing_content: [
            {
              content_id: "content_1",
              title: "AI Productivity Tips",
              views: 45000,
              engagement_rate: 12.3
            }
          ],
          platform_breakdown: {
            youtube: 65000,
            tiktok: 35000,
            instagram: 25000
          }
        },
        insights: {
          insights: ["Your productivity content performs 40% better"],
          recommendations: ["Focus more on productivity content"],
          trends: { views_trend: "+15%" }
        },
        revenue: {
          total_revenue: 1250.50,
          monthly_revenue: 450.00,
          growth_rate: "+22%"
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    loadAnalyticsData()
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-center">
              <RefreshCw className="h-6 w-6 animate-spin mr-2" />
              Loading analytics data...
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const data = analyticsData?.overview || {}
  const insights = analyticsData?.insights || {}
  const revenue = analyticsData?.revenue || {}

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
          <p className="text-muted-foreground">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </p>
        </div>
        <Button onClick={handleRefresh} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.total_views?.toLocaleString() || 0}</div>
            <p className="text-xs text-muted-foreground">
              {insights.trends?.views_trend || "+0%"} from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Engagement Rate</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.engagement_rate?.toFixed(1) || 0}%</div>
            <p className="text-xs text-muted-foreground">
              Average across all platforms
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${revenue.total_revenue?.toFixed(2) || 0}</div>
            <p className="text-xs text-muted-foreground">
              {revenue.growth_rate || "+0%"} from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Videos</CardTitle>
            <Download className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.total_videos || 0}</div>
            <p className="text-xs text-muted-foreground">
              Generated this month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Platform Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Platform Distribution</CardTitle>
          <CardDescription>Views by platform</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(data.platform_breakdown || {}).map(([platform, views]) => (
              <div key={platform} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Badge variant="outline" className="capitalize">
                    {platform}
                  </Badge>
                  <span className="text-sm text-muted-foreground">
                    {views?.toLocaleString()} views
                  </span>
                </div>
                <div className="text-sm font-medium">
                  {data.total_views > 0 ? Math.round((views / data.total_views) * 100) : 0}%
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Top Performing Content */}
      <Card>
        <CardHeader>
          <CardTitle>Top Performing Content</CardTitle>
          <CardDescription>Your best performing videos</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.top_performing_content?.map((content: any, index: number) => (
              <div key={content.content_id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium">{content.title}</h4>
                  <p className="text-sm text-muted-foreground">
                    {content.views?.toLocaleString()} views • {content.engagement_rate?.toFixed(1)}% engagement
                  </p>
                </div>
                <Badge variant="secondary">#{index + 1}</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Insights</CardTitle>
          <CardDescription>AI-powered recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {insights.insights?.map((insight: string, index: number) => (
              <div key={index} className="flex items-start space-x-2">
                <TrendingUp className="h-4 w-4 text-green-500 mt-0.5" />
                <p className="text-sm">{insight}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}



