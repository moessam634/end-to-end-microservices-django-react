import React from 'react';
import { Link } from 'react-router-dom';
import { 
  MusicalNoteIcon, 
  SparklesIcon, 
  ClockIcon, 
  UserGroupIcon,
  ChartBarIcon,
  BellIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: 'AI-Powered Matching',
      description: 'Our intelligent AI finds the perfect gigs for your style and availability.',
    },
    {
      icon: ClockIcon,
      title: 'Real-time Updates',
      description: 'Get instant notifications about new opportunities and booking confirmations.',
    },
    {
      icon: UserGroupIcon,
      title: 'Smart Networking',
      description: 'Connect with venues and other musicians in your area.',
    },
    {
      icon: ChartBarIcon,
      title: 'Performance Analytics',
      description: 'Track your gig success and earnings over time.',
    },
    {
      icon: BellIcon,
      title: 'Automated Applications',
      description: 'AI helps you apply to gigs with personalized proposals.',
    },
    {
      icon: MusicalNoteIcon,
      title: 'Portfolio Management',
      description: 'Showcase your music and experience to potential venues.',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Find Your Next Gig with
              <span className="text-yellow-300"> AI Intelligence</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100 max-w-3xl mx-auto">
              The smartest way for musicians to discover gigs and for venues to find talent. 
              Powered by artificial intelligence for perfect matches every time.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors duration-200"
              >
                Get Started Free
              </Link>
              <Link
                to="/gigs"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-white hover:text-primary-600 transition-colors duration-200"
              >
                Browse Gigs
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Gig Router?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We combine cutting-edge AI technology with deep understanding of the music industry 
              to create the most efficient gig-finding platform.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 bg-gray-50 rounded-lg hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Transform Your Music Career?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join thousands of musicians and venues who are already using Gig Router 
            to create amazing musical experiences.
          </p>
          <Link
            to="/register"
            className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-colors duration-200"
          >
            Start Your Journey Today
          </Link>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">10,000+</div>
              <div className="text-gray-600">Musicians</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">5,000+</div>
              <div className="text-gray-600">Venues</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">50,000+</div>
              <div className="text-gray-600">Gigs Booked</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
