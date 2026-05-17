"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { Header } from "@/components/header"
import { StatsCards } from "@/components/stats-cards"
import { ContentGrid } from "@/components/content-grid"
import { QuickActions } from "@/components/quick-actions"
import { ContentGenerator } from "@/components/content-generator"
import { AnalyticsDashboard } from "@/components/analytics-dashboard-real"
import { ServicesStatus } from "@/components/services-status"
import { ContentUpload } from "@/components/content-upload"
import { ContentManagement } from "@/components/content-management"

export function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [activeTab, setActiveTab] = useState("overview")
  const [generatedContent, setGeneratedContent] = useState([])
  const [selectedContent, setSelectedContent] = useState(null)

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl space-y-8">
            {/* Welcome Message */}
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl">Welcome back, Alex</h1>
              <p className="mt-2 text-muted-foreground">Here's what's happening with your content today</p>
            </div>

            {/* Tab Navigation */}
            <div className="flex space-x-1 rounded-lg bg-muted p-1">
              <button
                onClick={() => setActiveTab("overview")}
                className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  activeTab === "overview" 
                    ? "bg-background text-foreground shadow-sm" 
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab("generate")}
                className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  activeTab === "generate" 
                    ? "bg-background text-foreground shadow-sm" 
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Generate Content
              </button>
                      <button
                        onClick={() => setActiveTab("analytics")}
                        className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                          activeTab === "analytics" 
                            ? "bg-background text-foreground shadow-sm" 
                            : "text-muted-foreground hover:text-foreground"
                        }`}
                      >
                        Analytics
                      </button>
                      <button
                        onClick={() => setActiveTab("upload")}
                        className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                          activeTab === "upload" 
                            ? "bg-background text-foreground shadow-sm" 
                            : "text-muted-foreground hover:text-foreground"
                        }`}
                      >
                        Upload
                      </button>
                      <button
                        onClick={() => setActiveTab("manage")}
                        className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                          activeTab === "manage" 
                            ? "bg-background text-foreground shadow-sm" 
                            : "text-muted-foreground hover:text-foreground"
                        }`}
                      >
                        Manage
                      </button>
            </div>

            {/* Tab Content */}
                    {activeTab === "overview" && (
                      <>
                        {/* Services Status */}
                        <ServicesStatus />

                        {/* Stats Cards */}
                        <StatsCards />

                        {/* Quick Actions */}
                        <QuickActions />

                        {/* Recent Content */}
                        <ContentGrid />
                      </>
                    )}

            {activeTab === "generate" && (
              <ContentGenerator onGenerate={(content) => setGeneratedContent([...generatedContent, content])} />
            )}

            {activeTab === "analytics" && (
              <AnalyticsDashboard />
            )}

            {activeTab === "upload" && (
              <ContentUpload 
                content={selectedContent} 
                onUploadComplete={(result) => {
                  console.log('Upload completed:', result)
                  // Handle upload completion
                }} 
              />
            )}

            {activeTab === "manage" && (
              <ContentManagement />
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
