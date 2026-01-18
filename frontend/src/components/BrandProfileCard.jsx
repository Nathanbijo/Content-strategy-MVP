import React from 'react';
import { FaBuilding, FaBullseye, FaTag, FaPalette, FaQuoteLeft } from 'react-icons/fa';

const BrandProfileCard = ({ brandProfile }) => {
  return (
    <div className="bg-gradient-to-br from-white to-indigo-50 rounded-xl shadow-xl p-8 mb-10 border border-indigo-100">
      <div className="flex items-center mb-6">
        <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-3 rounded-lg mr-4">
          <FaBuilding className="text-white text-2xl" />
        </div>
        <div>
          <h2 className="text-3xl font-bold text-gray-800">{brandProfile.brand_name}</h2>
          <span className="inline-block mt-2 bg-indigo-100 text-indigo-800 text-sm font-semibold px-4 py-1 rounded-full">
            {brandProfile.tone}
          </span>
        </div>
      </div>

      <div className="mb-6 p-4 bg-white rounded-lg border-l-4 border-indigo-600">
        <div className="flex items-start">
          <FaQuoteLeft className="text-indigo-400 text-xl mr-3 mt-1" />
          <p className="text-gray-700 leading-relaxed">{brandProfile.description}</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <div className="flex items-center mb-3">
            <FaTag className="text-indigo-600 mr-2" />
            <h3 className="font-bold text-gray-800">Products & Services</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {brandProfile.products_services.map((item, index) => (
              <span key={index} className="bg-white border border-indigo-200 text-gray-700 text-sm px-3 py-1 rounded-lg hover:bg-indigo-50 transition-colors">
                {item}
              </span>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center mb-3">
            <FaBullseye className="text-purple-600 mr-2" />
            <h3 className="font-bold text-gray-800">Target Audience</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {brandProfile.target_audience.map((audience, index) => (
              <span key={index} className="bg-purple-100 text-purple-800 text-sm px-3 py-1 rounded-lg font-medium">
                {audience}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-indigo-200">
        <div className="flex items-center mb-3">
          <FaPalette className="text-pink-600 mr-2" />
          <h3 className="font-bold text-gray-800">Brand Colors</h3>
        </div>
        <div className="flex gap-3">
          {brandProfile.colors.map((color, index) => (
            <div key={index} className="flex items-center space-x-2 bg-white px-4 py-2 rounded-lg border border-gray-200">
              <div 
                className="w-8 h-8 rounded-md border-2 border-gray-300 shadow-sm" 
                style={{ backgroundColor: color }}
              ></div>
              <span className="text-sm font-mono text-gray-600">{color}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BrandProfileCard;
