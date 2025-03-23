'use client';

import React from 'react';
import Link from 'next/link';
import Header from '../components/ui/Headers';

interface DashboardProps {
  files?: File[];
}

const Dashboard: React.FC<DashboardProps> = ({ files = [] }) => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header username="John Doe" />
      
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Navigation Cards */}
          <Link href="/upload" 
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition duration-200 ease-in-out transform hover:-translate-y-1">
            <h2 className="text-xl font-semibold text-blue-600 mb-2">Upload Project</h2>
            <p className="text-gray-600">Upload and store your project files for future reference.</p>
          </Link>
          
          <Link href="/chatbot"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition duration-200 ease-in-out transform hover:-translate-y-1">
            <h2 className="text-xl font-semibold text-purple-600 mb-2">Chat Assistant</h2>
            <p className="text-gray-600">Search and explore your project codebase using natural language.</p>
          </Link>
        </div>

        {/* Recent Projects Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">Recent Projects</h2>
          <div className="border rounded-lg">
            {files && files.length > 0 ? (
              <ul className="divide-y">
                {files.map((file, index) => (
                  <li key={index} className="p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-500">{file.size} bytes</p>
                      </div>
                      <button className="text-blue-500 hover:text-blue-700">
                        View Details
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="p-4 text-center text-gray-500">
                No projects uploaded yet. Start by uploading your first project!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 