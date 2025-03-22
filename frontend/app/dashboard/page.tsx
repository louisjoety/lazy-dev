'use client'

import React from 'react';
import Header from '../components/ui/Headers'; // Import Header component

interface DashboardProps {
  files?: File[];
}

const Dashboard: React.FC<DashboardProps> = ({ files = [] }) => {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Include the Header component */}
      <Header
        username="John Doe" // Pass any necessary props to Header
      />

      <div className="flex justify-center items-center flex-grow mt-20 text-black"> {/* Add text-black here */}
        <div className="w-full max-w-4xl p-5">
          <h1 className="text-xl font-semibold mb-4">Uploaded Files Dashboard</h1>
          <div className="border p-4 rounded-lg">
            {files && files.length > 0 ? (
              <ul>
                {files.map((file, index) => (
                  <li key={index} className="py-2">
                    <strong>{file.name}</strong> - {file.size} bytes
                  </li>
                ))}
              </ul>
            ) : (
              <p>No files uploaded yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
