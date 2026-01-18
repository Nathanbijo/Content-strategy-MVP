import React, { useState } from 'react';
import { FaInstagram, FaLinkedin, FaTwitter, FaCopy, FaCheck, FaExternalLinkAlt } from 'react-icons/fa';

const PostCard = ({ post }) => {
  const [copied, setCopied] = useState(false);

  const getPlatformIcon = () => {
    switch (post.platform) {
      case 'Instagram':
        return <FaInstagram className="text-pink-600" />;
      case 'LinkedIn':
        return <FaLinkedin className="text-blue-600" />;
      case 'X':
        return <FaTwitter className="text-blue-400" />;
      default:
        return null;
    }
  };

  const getPlatformColor = () => {
    switch (post.platform) {
      case 'Instagram':
        return 'border-pink-400 bg-gradient-to-br from-pink-50 to-purple-50';
      case 'LinkedIn':
        return 'border-blue-400 bg-gradient-to-br from-blue-50 to-indigo-50';
      case 'X':
        return 'border-blue-300 bg-gradient-to-br from-blue-50 to-sky-50';
      default:
        return 'border-gray-300 bg-white';
    }
  };

  const getScoreBadgeColor = () => {
    switch (post.engagement_score_label) {
      case 'High':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const handleCopy = () => {
    const textToCopy = `${post.caption}\n\n${post.hashtags.join(' ')}\n\n${post.cta}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getHeadline = () => {
    return post.caption.split('.')[0] + (post.caption.includes('.') ? '.' : '');
  };

  return (
    <div className={`rounded-xl shadow-lg border-2 ${getPlatformColor()} hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] overflow-hidden`}>
      {/* Image with Text Overlay */}
      {post.image_url && (
        <div className="relative h-64 overflow-hidden">
          <img
            src={post.image_url}
            alt={`${post.platform} creative`}
            className="w-full h-full object-cover"
            loading="lazy"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          {/* Text Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent flex flex-col justify-end p-6">
            <h3 className="text-white text-xl font-bold mb-2 drop-shadow-lg leading-tight">
              {getHeadline()}
            </h3>
            <button className="bg-white text-gray-900 px-5 py-2 rounded-full font-semibold text-sm hover:bg-gray-100 transition-colors w-fit shadow-lg">
              {post.cta}
            </button>
          </div>
        </div>
      )}

      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="text-2xl">{getPlatformIcon()}</div>
            <span className="font-bold text-gray-800 text-lg">{post.platform}</span>
          </div>
          
          <span className={`text-xs font-bold px-3 py-1 rounded-full border ${getScoreBadgeColor()}`}>
            {post.engagement_score_label}
          </span>
        </div>

        {/* Caption */}
        <p className="text-gray-700 mb-4 leading-relaxed text-sm">{post.caption}</p>

        {/* Hashtags */}
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {post.hashtags.map((hashtag, index) => (
              <span key={index} className="text-indigo-600 text-sm font-semibold hover:text-indigo-800 cursor-pointer">
                {hashtag}
              </span>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleCopy}
              className="flex items-center space-x-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-4 py-2 rounded-lg transition-all font-medium text-sm"
            >
              {copied ? <FaCheck className="text-green-600" /> : <FaCopy />}
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
            
            {post.image_url && (
              <a
                href={post.image_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 text-sm font-medium"
              >
                <FaExternalLinkAlt />
                <span>View Image</span>
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
