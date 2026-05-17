/**
 * API Client for Faceless Autopilot AI Backend Services
 */

const API_BASE_URLS = {
  AI_CONTENT: 'http://localhost:8561',
  PLATFORM_APIS: 'http://localhost:8562',
  ANALYTICS: 'http://localhost:8563',
}

// AI Content Service API
export const aiContentAPI = {
  // Generate new content
  generateContent: async (data: {
    topic: string;
    niche: string;
    format: 'short' | 'medium' | 'long';
    duration: number;
    voice_id?: string;
    platforms: string[];
    style?: string;
    tone?: string;
  }) => {
    const response = await fetch(`${API_BASE_URLS.AI_CONTENT}/api/content/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  // Get content status
  getContentStatus: async (contentId: string) => {
    const response = await fetch(`${API_BASE_URLS.AI_CONTENT}/api/content/${contentId}/status`);
    return response.json();
  },

  // Regenerate content
  regenerateContent: async (contentId: string) => {
    const response = await fetch(`${API_BASE_URLS.AI_CONTENT}/api/content/${contentId}/regenerate`, {
      method: 'POST',
    });
    return response.json();
  },

  // Health check
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URLS.AI_CONTENT}/health`);
    return response.json();
  }
};

// Platform APIs Service
export const platformAPI = {
  // Upload content to platforms
  uploadContent: async (data: {
    content_id: string;
    video_url: string;
    title: string;
    description: string;
    platforms: string[];
    tags?: string[];
    category_id?: string;
    privacy_level?: string;
  }) => {
    const response = await fetch(`${API_BASE_URLS.PLATFORM_APIS}/api/platforms/upload`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  // Get upload status
  getUploadStatus: async (uploadId: string) => {
    const response = await fetch(`${API_BASE_URLS.PLATFORM_APIS}/api/platforms/status/${uploadId}`);
    return response.json();
  },

  // Schedule content upload
  scheduleUpload: async (data: {
    content_id: string;
    video_url: string;
    title: string;
    description: string;
    platforms: string[];
    schedule_time: string;
    timezone?: string;
  }) => {
    const response = await fetch(`${API_BASE_URLS.PLATFORM_APIS}/api/platforms/schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  // Health check
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URLS.PLATFORM_APIS}/health`);
    return response.json();
  }
};

// Analytics Service
export const analyticsAPI = {
  // Get analytics overview
  getOverview: async (userId: string, days: number = 30) => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/overview?user_id=${userId}&days=${days}`);
    return response.json();
  },

  // Get content analytics
  getContentAnalytics: async (contentId: string) => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/content/${contentId}`);
    return response.json();
  },

  // Get performance insights
  getInsights: async (userId: string, days: number = 30) => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/insights?user_id=${userId}&days=${days}`);
    return response.json();
  },

  // Sync platform analytics
  syncAnalytics: async (userId: string, platforms: string[]) => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId, platforms }),
    });
    return response.json();
  },

  // Get revenue analytics
  getRevenueAnalytics: async (userId: string, days: number = 30) => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/revenue?user_id=${userId}&days=${days}`);
    return response.json();
  },

  // Get content trends
  getTrends: async (userId: string, niche?: string, days: number = 30) => {
    const params = new URLSearchParams({
      user_id: userId,
      days: days.toString(),
      ...(niche && { niche }),
    });
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/api/analytics/trends?${params}`);
    return response.json();
  },

  // Health check
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URLS.ANALYTICS}/health`);
    return response.json();
  }
};

// Combined API client
export const api = {
  aiContent: aiContentAPI,
  platform: platformAPI,
  analytics: analyticsAPI,
};

// Utility function to check all services health
export const checkAllServicesHealth = async () => {
  try {
    const [aiContent, platform, analytics] = await Promise.all([
      aiContentAPI.healthCheck(),
      platformAPI.healthCheck(),
      analyticsAPI.healthCheck(),
    ]);

    return {
      aiContent,
      platform,
      analytics,
      allHealthy: aiContent.status === 'healthy' && 
                  platform.status === 'healthy' && 
                  analytics.status === 'healthy'
    };
  } catch (error) {
    console.error('Health check failed:', error);
    return {
      aiContent: { status: 'error' },
      platform: { status: 'error' },
      analytics: { status: 'error' },
      allHealthy: false
    };
  }
};



