import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-primary"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="h-12 w-12 bg-gradient-to-br from-primary to-secondary rounded-full opacity-20"></div>
        </div>
      </div>
      <div className="mt-6 space-y-2 text-center">
        <p className="text-gray-700 font-semibold text-lg">Analyzing website...</p>
        <p className="text-gray-500 text-sm">Generating brand profile and marketing content</p>
        <div className="flex items-center justify-center space-x-2 mt-4">
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
