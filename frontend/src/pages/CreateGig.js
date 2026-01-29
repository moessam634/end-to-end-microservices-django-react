import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const CreateGig = () => {
  const { user } = useAuth(); // eslint-disable-line no-unused-vars
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    event_date: '',
    duration_hours: 2,
    setup_time: 30,
    genres: [],
    instruments_needed: [],
    band_size_min: 1,
    band_size_max: 5,
    payment_amount: '',
    payment_type: 'per_gig',
    experience_level: 'intermediate',
    original_music_required: false,
    cover_music_required: true,
    sound_system_provided: true,
    lighting_provided: true,
    backline_provided: false,
    special_requirements: '',
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    is_featured: false,
    is_urgent: false,
    deadline: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const genreOptions = [
    'rock', 'pop', 'jazz', 'blues', 'country', 'electronic',
    'hip_hop', 'classical', 'folk', 'reggae', 'other'
  ];

  const instrumentOptions = [
    'guitar', 'bass', 'drums', 'keyboard', 'piano', 'vocals',
    'saxophone', 'trumpet', 'violin', 'cello', 'flute', 'other'
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleArrayChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Get venue profile ID (assuming user has one venue profile)
      const venueResponse = await axios.get('/venue/profile/');
      const venueId = venueResponse.data.id;

      const gigData = {
        ...formData,
        venue_id: venueId,
        payment_amount: parseFloat(formData.payment_amount),
        band_size_min: parseInt(formData.band_size_min),
        band_size_max: parseInt(formData.band_size_max),
        duration_hours: parseInt(formData.duration_hours),
        setup_time: parseInt(formData.setup_time)
      };

      console.log('Creating gig with data:', gigData);
      const response = await axios.post('/gigs/', gigData);
      console.log('Gig created successfully:', response.data);
      setSuccess('Gig created successfully!');
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        event_date: '',
        duration_hours: 2,
        setup_time: 30,
        genres: [],
        instruments_needed: [],
        band_size_min: 1,
        band_size_max: 5,
        payment_amount: '',
        payment_type: 'per_gig',
        experience_level: 'intermediate',
        original_music_required: false,
        cover_music_required: true,
        sound_system_provided: true,
        lighting_provided: true,
        backline_provided: false,
        special_requirements: '',
        contact_person: '',
        contact_phone: '',
        contact_email: '',
        is_featured: false,
        is_urgent: false,
        deadline: ''
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create gig');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Create New Gig</h1>
        <p className="text-gray-600 mt-2">
          Post a new gig opportunity for musicians to apply to.
        </p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gig Title *
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Jazz Night at Blue Note"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Event Date & Time *
              </label>
              <input
                type="datetime-local"
                name="event_date"
                value={formData.event_date}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                required
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe the gig, atmosphere, audience, etc."
              />
            </div>
          </div>
        </div>

        {/* Musical Requirements */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Musical Requirements</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Genres
              </label>
              <div className="space-y-2 max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2">
                {genreOptions.map(genre => (
                  <label key={genre} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.genres.includes(genre)}
                      onChange={(e) => {
                        const newGenres = e.target.checked
                          ? [...formData.genres, genre]
                          : formData.genres.filter(g => g !== genre);
                        handleArrayChange('genres', newGenres);
                      }}
                      className="mr-2"
                    />
                    <span className="capitalize">{genre}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Instruments Needed
              </label>
              <div className="space-y-2 max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2">
                {instrumentOptions.map(instrument => (
                  <label key={instrument} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.instruments_needed.includes(instrument)}
                      onChange={(e) => {
                        const newInstruments = e.target.checked
                          ? [...formData.instruments_needed, instrument]
                          : formData.instruments_needed.filter(i => i !== instrument);
                        handleArrayChange('instruments_needed', newInstruments);
                      }}
                      className="mr-2"
                    />
                    <span className="capitalize">{instrument}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Band Size (Min)
              </label>
              <input
                type="number"
                name="band_size_min"
                value={formData.band_size_min}
                onChange={handleInputChange}
                min="1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Band Size (Max)
              </label>
              <input
                type="number"
                name="band_size_max"
                value={formData.band_size_max}
                onChange={handleInputChange}
                min="1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experience Level
              </label>
              <select
                name="experience_level"
                value={formData.experience_level}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="professional">Professional</option>
              </select>
            </div>
          </div>
        </div>

        {/* Payment & Duration */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Payment & Duration</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Amount *
              </label>
              <input
                type="number"
                name="payment_amount"
                value={formData.payment_amount}
                onChange={handleInputChange}
                required
                min="0"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0.00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Type
              </label>
              <select
                name="payment_type"
                value={formData.payment_type}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="per_gig">Per Gig</option>
                <option value="per_hour">Per Hour</option>
                <option value="negotiable">Negotiable</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration (Hours)
              </label>
              <input
                type="number"
                name="duration_hours"
                value={formData.duration_hours}
                onChange={handleInputChange}
                min="1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Venue Features */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Venue Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="sound_system_provided"
                  checked={formData.sound_system_provided}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Sound System Provided</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="lighting_provided"
                  checked={formData.lighting_provided}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Lighting Provided</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="backline_provided"
                  checked={formData.backline_provided}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Backline Provided</span>
              </label>
            </div>

            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="original_music_required"
                  checked={formData.original_music_required}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Original Music Required</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="cover_music_required"
                  checked={formData.cover_music_required}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Cover Music Required</span>
              </label>
            </div>

            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_featured"
                  checked={formData.is_featured}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Featured Gig</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_urgent"
                  checked={formData.is_urgent}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>Urgent</span>
              </label>
            </div>
          </div>
        </div>

        {/* Contact Information */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Contact Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contact Person
              </label>
              <input
                type="text"
                name="contact_person"
                value={formData.contact_person}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contact Phone
              </label>
              <input
                type="tel"
                name="contact_phone"
                value={formData.contact_phone}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Phone number"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contact Email
              </label>
              <input
                type="email"
                name="contact_email"
                value={formData.contact_email}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Email address"
              />
            </div>
          </div>

          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Special Requirements
            </label>
            <textarea
              name="special_requirements"
              value={formData.special_requirements}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Any special requirements or notes..."
            />
          </div>

          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Application Deadline (Optional)
            </label>
            <input
              type="datetime-local"
              name="deadline"
              value={formData.deadline}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating...' : 'Create Gig'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateGig;
