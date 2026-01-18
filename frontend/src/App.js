import React, { useState } from 'react';
import './App.css';
import URLInputForm from './components/URLInputForm';
import BrandProfileCard from './components/BrandProfileCard';
import PostCard from './components/PostCard';
import LoadingSpinner from './components/LoadingSpinner';
import { analyzeWebsite, downloadJSON, downloadCSV } from './services/api';
import { FaDownload, FaFilter } from 'react-icons/fa';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [filterPlatform, setFilterPlatform] = useState('All');

  const handleSubmit = async (url, tonePreset) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeWebsite(url, tonePreset);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze website. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredPosts = result?.posts?.filter(post => 
    filterPlatform === 'All' || post.platform === filterPlatform
  ) || [];

  const handleDownloadJSON = () => {
    if (result) {
      downloadJSON(result, `${result.brand_profile.brand_name}_content.json`);
    }
  };

  const handleDownloadCSV = () => {
    if (result) {
      downloadCSV(result);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-md border-b-4 border-indigo-600">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-5xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            MarketFlow AI
          </h1>
          <p className="text-gray-600 mt-2 text-lg">URL → Brand Profile → Marketing Content in 30 seconds</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-10">
        {/* Input Form */}
        <URLInputForm onSubmit={handleSubmit} loading={loading} />

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Error State */}
        {error && (
          <div className="mt-10 bg-red-50 border-2 border-red-200 rounded-xl p-6 shadow-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-lg font-semibold text-red-800">Error</h3>
                <p className="text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="mt-12 space-y-8">
            {/* Brand Profile */}
            <BrandProfileCard brandProfile={result.brand_profile} />

            {/* Export Buttons */}
            <div className="flex items-center justify-between bg-white rounded-xl p-6 shadow-lg border border-gray-200">
              <div className="flex items-center space-x-2">
                <FaDownload className="text-indigo-600 text-xl" />
                <span className="font-bold text-gray-800 text-lg">Export Campaign</span>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={handleDownloadCSV}
                  className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg font-semibold transition-all shadow-md"
                >
                  📊 Download CSV
                </button>
                <button
                  onClick={handleDownloadJSON}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg font-semibold transition-all shadow-md"
                >
                  📄 Download JSON
                </button>
              </div>
            </div>

            {/* Platform Filter */}
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
              <div className="flex items-center space-x-4">
                <FaFilter className="text-indigo-600 text-xl" />
                <span className="font-bold text-gray-800 text-lg">Filter by Platform:</span>
                {['All', 'Instagram', 'LinkedIn', 'X'].map((platform) => (
                  <button
                    key={platform}
                    onClick={() => setFilterPlatform(platform)}
                    className={`px-5 py-2 rounded-lg font-semibold transition-all ${
                      filterPlatform === platform
                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {platform}
                  </button>
                ))}
              </div>
            </div>

            {/* Posts Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post, index) => (
                <PostCard key={index} post={post} />
              ))}
            </div>

            {filteredPosts.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No posts found for selected platform.</p>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          <p>Built for hackathon • Powered by Groq + Pollinations AI</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
