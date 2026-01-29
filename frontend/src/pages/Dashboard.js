import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeDropdown, setActiveDropdown] = useState(null);

  const isVenue = user?.user_type === 'venue';
  const isMusician = user?.user_type === 'musician'; // eslint-disable-line no-unused-vars

  const venueFunctions = [
    {
      title: 'Gig Management',
      icon: '🎵',
      items: [
        { name: 'Create New Gig', action: 'create-gig' },
        { name: 'Manage Active Gigs', action: 'manage-gigs' },
        { name: 'View Gig History', action: 'gig-history' },
        { name: 'Gig Analytics', action: 'gig-analytics' }
      ]
    },
    {
      title: 'Applications',
      icon: '📋',
      items: [
        { name: 'Review Applications', action: 'review-applications' },
        { name: 'Pending Reviews', action: 'pending-reviews' },
        { name: 'Accepted Musicians', action: 'accepted-musicians' },
        { name: 'Application Analytics', action: 'app-analytics' }
      ]
    },
    {
      title: 'Venue Profile',
      icon: '🏢',
      items: [
        { name: 'Edit Venue Info', action: 'edit-venue' },
        { name: 'Upload Photos', action: 'upload-photos' },
        { name: 'Manage Features', action: 'manage-features' },
        { name: 'Venue Settings', action: 'venue-settings' }
      ]
    },
    {
      title: 'AI Features',
      icon: '🤖',
      items: [
        { name: 'Generate Gig Descriptions', action: 'ai-descriptions' },
        { name: 'Marketing Content', action: 'ai-marketing' },
        { name: 'Musician Matching', action: 'ai-matching' },
        { name: 'Performance Analytics', action: 'ai-analytics' }
      ]
    },
    {
      title: 'Financial',
      icon: '💰',
      items: [
        { name: 'Payment History', action: 'payment-history' },
        { name: 'Budget Planning', action: 'budget-planning' },
        { name: 'Revenue Reports', action: 'revenue-reports' },
        { name: 'Tax Documents', action: 'tax-documents' }
      ]
    },
    {
      title: 'Communication',
      icon: '💬',
      items: [
        { name: 'Messages', action: 'messages' },
        { name: 'Notifications', action: 'notifications' },
        { name: 'Email Templates', action: 'email-templates' },
        { name: 'Broadcast Messages', action: 'broadcast' }
      ]
    }
  ];

  const musicianFunctions = [
    {
      title: 'Gig Discovery',
      icon: '🔍',
      items: [
        { name: 'Browse Gigs', action: 'browse-gigs' },
        { name: 'AI Recommendations', action: 'ai-recommendations' },
        { name: 'Saved Gigs', action: 'saved-gigs' },
        { name: 'Gig Alerts', action: 'gig-alerts' }
      ]
    },
    {
      title: 'Applications',
      icon: '📝',
      items: [
        { name: 'My Applications', action: 'my-applications' },
        { name: 'Application History', action: 'app-history' },
        { name: 'Pending Applications', action: 'pending-apps' },
        { name: 'Application Templates', action: 'app-templates' }
      ]
    },
    {
      title: 'Profile & Portfolio',
      icon: '👤',
      items: [
        { name: 'Edit Profile', action: 'edit-profile' },
        { name: 'Upload Portfolio', action: 'upload-portfolio' },
        { name: 'Manage Setlists', action: 'manage-setlists' },
        { name: 'Profile Analytics', action: 'profile-analytics' }
      ]
    }
  ];

  const handleFunctionClick = (action) => {
    console.log(`Function clicked: ${action}`);
    setActiveDropdown(null);
    
    // Navigate to specific functions
    switch (action) {
      case 'create-gig':
        navigate('/create-gig');
        break;
      case 'manage-gigs':
        navigate('/gigs');
        break;
      case 'review-applications':
        navigate('/applications');
        break;
      case 'edit-venue':
        navigate('/venue-profile');
        break;
      case 'browse-gigs':
        navigate('/gigs');
        break;
      case 'my-applications':
        navigate('/my-applications');
        break;
      case 'edit-profile':
        navigate('/profile');
        break;
      default:
        console.log(`Function ${action} not implemented yet`);
        break;
    }
  };

  const toggleDropdown = (index) => {
    setActiveDropdown(activeDropdown === index ? null : index);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.first_name || (isVenue ? 'Venue Owner' : 'Musician')}!
        </h1>
        <p className="text-gray-600 mt-2">
          {isVenue 
            ? "Manage your venue, create gigs, and connect with talented musicians."
            : "Here's what's happening with your gigs and opportunities."
          }
        </p>
      </div>

      {/* Function Dropdowns */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {isVenue ? 'Venue Management Functions' : 'Musician Functions'}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {(isVenue ? venueFunctions : musicianFunctions).map((category, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <button
                onClick={() => toggleDropdown(index)}
                className="w-full px-6 py-4 text-left hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition-colors duration-200"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{category.icon}</span>
                    <h3 className="text-lg font-semibold text-gray-900">{category.title}</h3>
                  </div>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform duration-200 ${
                      activeDropdown === index ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>
              
              {activeDropdown === index && (
                <div className="border-t border-gray-200">
                  <div className="py-2">
                    {category.items.map((item, itemIndex) => (
                      <button
                        key={itemIndex}
                        onClick={() => handleFunctionClick(item.action)}
                        className="w-full px-6 py-3 text-left hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition-colors duration-200"
                      >
                        <span className="text-gray-700 hover:text-gray-900">{item.name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isVenue ? 'Active Gigs' : 'My Applications'}
          </h3>
          <div className="text-3xl font-bold text-blue-600">
            {isVenue ? '5' : '8'}
          </div>
          <p className="text-gray-600 text-sm mt-2">
            {isVenue ? 'Currently posted' : 'Pending review'}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isVenue ? 'Applications Received' : 'Confirmed Gigs'}
          </h3>
          <div className="text-3xl font-bold text-green-600">
            {isVenue ? '23' : '3'}
          </div>
          <p className="text-gray-600 text-sm mt-2">
            {isVenue ? 'This month' : 'This month'}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isVenue ? 'Revenue' : 'Earnings'}
          </h3>
          <div className="text-3xl font-bold text-purple-600">
            {isVenue ? '$2,450' : '$1,250'}
          </div>
          <p className="text-gray-600 text-sm mt-2">
            {isVenue ? 'This month' : 'This month'}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isVenue ? 'Musician Network' : 'Profile Views'}
          </h3>
          <div className="text-3xl font-bold text-orange-600">
            {isVenue ? '156' : '89'}
          </div>
          <p className="text-gray-600 text-sm mt-2">
            {isVenue ? 'Connected musicians' : 'This month'}
          </p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {isVenue ? (
            <>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">New application received for "Jazz Night"</p>
                  <p className="text-gray-500 text-sm">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">Gig "Rock Weekend" published successfully</p>
                  <p className="text-gray-500 text-sm">1 day ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">Payment processed for "Acoustic Evening"</p>
                  <p className="text-gray-500 text-sm">3 days ago</p>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">Application accepted for "Jazz Night"</p>
                  <p className="text-gray-500 text-sm">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">New gig posted nearby - "Rock Weekend"</p>
                  <p className="text-gray-500 text-sm">1 day ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <div>
                  <p className="text-gray-900">Payment received for "Acoustic Evening"</p>
                  <p className="text-gray-500 text-sm">3 days ago</p>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
