'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Header from '../components/ui/Headers';

interface Project {
  project_name: string;
  tags: string[];
}

const Dashboard = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await fetch('http://localhost:8000/get_all_projects');
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        const data = await response.json();
        setProjects(data.projects);
      } catch (err) {
        setError('Failed to load projects. Please try again later.');
        console.error('Error fetching projects:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

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

        {/* Projects Section */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">Your Projects</h2>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-2 text-gray-600">Loading projects...</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {projects.length > 0 ? (
                projects.map((project, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{project.project_name}</h3>
                    <div className="flex flex-wrap gap-2">
                      {project.tags.map((tag, tagIndex) => (
                        <span
                          key={tagIndex}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 bg-white rounded-lg shadow-md">
                  <p className="text-gray-500">No projects uploaded yet. Start by uploading your first project!</p>
                  <Link 
                    href="/upload"
                    className="mt-4 inline-block px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-200"
                  >
                    Upload Project
                  </Link>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 