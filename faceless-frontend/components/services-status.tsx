"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, XCircle, RefreshCw, AlertCircle } from "lucide-react"
import { api } from "@/lib/api"

export function ServicesStatus() {
  const [services, setServices] = useState({
    aiContent: { status: 'unknown', timestamp: null },
    platform: { status: 'unknown', timestamp: null },
    analytics: { status: 'unknown', timestamp: null }
  })
  const [loading, setLoading] = useState(true)
  const [lastChecked, setLastChecked] = useState(new Date())

  const checkServices = async () => {
    setLoading(true)
    try {
      const health = await api.checkAllServicesHealth()
      setServices(health)
      setLastChecked(new Date())
    } catch (error) {
      console.error('Failed to check services health:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    checkServices()
    // Check every 30 seconds
    const interval = setInterval(checkServices, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'healthy':
        return <Badge variant="default" className="bg-green-500">Online</Badge>
      case 'error':
        return <Badge variant="destructive">Offline</Badge>
      default:
        return <Badge variant="secondary">Unknown</Badge>
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <RefreshCw className="h-5 w-5" />
            Services Status
          </CardTitle>
          <Button 
            onClick={checkServices} 
            disabled={loading}
            variant="outline" 
            size="sm"
          >
            {loading ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="h-4 w-4" />
            )}
          </Button>
        </div>
        <p className="text-sm text-muted-foreground">
          Last checked: {lastChecked.toLocaleTimeString()}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* AI Content Service */}
          <div className="flex items-center justify-between p-3 border rounded-lg">
            <div className="flex items-center space-x-3">
              {getStatusIcon(services.aiContent.status)}
              <div>
                <h4 className="font-medium">AI Content Service</h4>
                <p className="text-sm text-muted-foreground">Port 8561</p>
              </div>
            </div>
            {getStatusBadge(services.aiContent.status)}
          </div>

          {/* Platform APIs Service */}
          <div className="flex items-center justify-between p-3 border rounded-lg">
            <div className="flex items-center space-x-3">
              {getStatusIcon(services.platform.status)}
              <div>
                <h4 className="font-medium">Platform APIs Service</h4>
                <p className="text-sm text-muted-foreground">Port 8562</p>
              </div>
            </div>
            {getStatusBadge(services.platform.status)}
          </div>

          {/* Analytics Service */}
          <div className="flex items-center justify-between p-3 border rounded-lg">
            <div className="flex items-center space-x-3">
              {getStatusIcon(services.analytics.status)}
              <div>
                <h4 className="font-medium">Analytics Service</h4>
                <p className="text-sm text-muted-foreground">Port 8563</p>
              </div>
            </div>
            {getStatusBadge(services.analytics.status)}
          </div>

          {/* Overall Status */}
          <div className="pt-4 border-t">
            <div className="flex items-center justify-between">
              <span className="font-medium">Overall Status</span>
              {services.aiContent.status === 'healthy' && 
               services.platform.status === 'healthy' && 
               services.analytics.status === 'healthy' ? (
                <Badge variant="default" className="bg-green-500">All Systems Operational</Badge>
              ) : (
                <Badge variant="destructive">Some Services Down</Badge>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}



