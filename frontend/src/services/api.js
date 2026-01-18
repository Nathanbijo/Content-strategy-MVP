import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const analyzeWebsite = async (url, tonePreset = 'auto') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
      url: url,
      tonePreset: tonePreset
    }, {
      timeout: 90000
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    if (error.response) {
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      throw new Error('No response from server. Check your connection.');
    } else {
      throw new Error('Failed to make request');
    }
  }
};

export const downloadJSON = (data, filename) => {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

export const downloadCSV = (data) => {
  const brandProfile = data.brand_profile;
  const posts = data.posts;
  
  let csvContent = `Brand Name,${brandProfile.brand_name}\n`;
  csvContent += `Description,"${brandProfile.description}"\n`;
  csvContent += `Tone,${brandProfile.tone}\n`;
  csvContent += `\n`;
  csvContent += `Platform,Caption,Hashtags,CTA,Engagement Score\n`;
  
  posts.forEach(post => {
    const hashtags = post.hashtags.join(' ');
    const caption = post.caption.replace(/"/g, '""');
    csvContent += `${post.platform},"${caption}","${hashtags}",${post.cta},${post.engagement_score_label}\n`;
  });
  
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${brandProfile.brand_name}_marketing_content.csv`;
  a.click();
  URL.revokeObjectURL(url);
};
