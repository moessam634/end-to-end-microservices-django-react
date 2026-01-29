import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-2">
          Manage your account and preferences
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Coming Soon</h3>
        <p className="text-gray-600">
          This page will allow you to edit your profile, manage your musician/venue details, 
          upload portfolio materials, and configure AI preferences. Stay tuned!
        </p>
      </div>

      <div className="mt-6 bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Current User Info</h3>
        <div className="space-y-2">
          <p><strong>Name:</strong> {user?.first_name} {user?.last_name}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Type:</strong> {user?.user_type}</p>
          <p><strong>Location:</strong> {user?.city}, {user?.state}, {user?.country}</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
