import React, { useState } from 'react';

const URLInputForm = ({ onSubmit, loading }) => {
  const [url, setUrl] = useState('');
  const [tonePreset, setTonePreset] = useState('auto');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit(url, tonePreset);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-xl p-8 max-w-3xl mx-auto border border-gray-100">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
          AI Marketing Content Generator
        </h2>
        <p className="text-gray-600 text-lg">
          Transform any website into platform-optimized social media content in seconds
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Website URL
          </label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.example.com"
            className="w-full px-5 py-4 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-lg"
            required
            disabled={loading}
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Brand Tone
          </label>
          <select
            value={tonePreset}
            onChange={(e) => setTonePreset(e.target.value)}
            className="w-full px-5 py-4 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-lg bg-white"
            disabled={loading}
          >
            <option value="auto">🤖 Auto (AI Detects)</option>
            <option value="startup">🚀 Startup (Bold & Innovative)</option>
            <option value="cafe">☕ Cafe (Warm & Friendly)</option>
            <option value="ngo">🌍 NGO (Compassionate & Mission-driven)</option>
            <option value="enterprise">🏢 Enterprise (Professional & Authoritative)</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] shadow-lg text-lg"
        >
          {loading ? 'Generating Content...' : '✨ Generate Marketing Content'}
        </button>
      </form>

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>💡 Try: tesla.com, starbucks.com, stripe.com</p>
      </div>
    </div>
  );
};

export default URLInputForm;
