import React from 'react';

const Gigs = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Available Gigs</h1>
        <p className="text-gray-600 mt-2">
          Discover amazing opportunities in your area
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Coming Soon</h3>
        <p className="text-gray-600">
          This page will display all available gigs with AI-powered recommendations, 
          filtering options, and quick-apply functionality. Stay tuned!
        </p>
      </div>
    </div>
  );
};

export default Gigs;
