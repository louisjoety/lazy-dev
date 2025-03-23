'use client';

import React, { useState } from 'react';
import Header from '../components/ui/Headers';
import supabase from '../supabase';

// Define allowed file extensions
const ALLOWED_EXTENSIONS = ['.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.ipynb'];

const DragAndDrop = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [dragging, setDragging] = useState(false);
  const [projectName, setProjectName] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string>('');

  // Helper function to check if file type is allowed
  const isFileAllowed = (file: File): boolean => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    return ALLOWED_EXTENSIONS.includes(extension);
  };

  // Helper function to filter files
  const filterFiles = (newFiles: File[]): File[] => {
    const validFiles: File[] = [];
    const invalidFiles: string[] = [];

    newFiles.forEach(file => {
      if (isFileAllowed(file)) {
        validFiles.push(file);
      } else {
        invalidFiles.push(file.name);
      }
    });

    if (invalidFiles.length > 0) {
      setError(`Invalid file type(s): ${invalidFiles.join(', ')}. Allowed types: ${ALLOWED_EXTENSIONS.join(', ')}`);
      setTimeout(() => setError(''), 5000); // Clear error after 5 seconds
    }

    return validFiles;
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    const validFiles = filterFiles(droppedFiles);
    setFiles((prevFiles) => [...prevFiles, ...validFiles]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const validFiles = filterFiles(selectedFiles);
    setFiles((prevFiles) => [...prevFiles, ...validFiles]);
  };

  const handleSubmit = async () => {
    if (!projectName.trim()) {
      setError('Please enter a project name');
      return;
    }

    if (files.length === 0) {
      setError('Please select files to upload');
      return;
    }

    setIsUploading(true);
    setError('');
    
    try {
      // 1. Upload files to Supabase storage
      const bucketName = 'project-files';
      const uploadPromises = files.map(async (file) => {
        const { error } = await supabase.storage
          .from(bucketName)
          .upload(`${file.name}`, file, { upsert: true });
        
        if (error) {
          throw new Error(`Failed to upload ${file.name}: ${error.message}`);
        }
      });

      await Promise.all(uploadPromises);

      // 2. Call backend to process the uploaded files
      const response = await fetch('http://localhost:8000/upload_project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_name: projectName,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to process project');
      }

      const result = await response.json();
      console.log('Project uploaded successfully:', result);
      
      // Clear the form
      setFiles([]);
      setProjectName('');
      alert('Project uploaded successfully!');

    } catch (error) {
      console.error('Upload failed:', error);
      setError('Failed to upload project. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Header username="John Doe" />

      <div className="flex justify-center items-center flex-grow mt-20">
        <div className="w-full max-w-2xl p-8">
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
          
          <div className="mb-4">
            <label htmlFor="projectName" className="block text-sm font-medium text-gray-700">
              Project Name
            </label>
            <input
              type="text"
              id="projectName"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter project name"
            />
          </div>

          <div
            className={`flex justify-center items-center border-2 p-5 border-dashed rounded-lg ${dragging ? 'border-blue-500' : 'border-gray-300'}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="text-center">
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
                accept={ALLOWED_EXTENSIONS.join(',')}
              />
              <label
                htmlFor="file-upload"
                className={`cursor-pointer ${dragging ? 'text-blue-500' : 'text-gray-700'}`}
              >
                {dragging ? 'Release to drop files' : 'Drag & drop or upload '}
                <span className="text-blue-500 hover:underline">here</span>
              </label>
              <div className="mt-2 text-sm text-gray-500">
                Allowed file types: {ALLOWED_EXTENSIONS.join(', ')}
              </div>
              <div className="mt-4 text-gray-700">
                <h3>Files Ready to Upload:</h3>
                {files.length > 0 ? (
                  <ul className="mt-2">
                    {files.map((file, index) => (
                      <li key={index} className="text-gray-700">{file.name}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-700">No files selected yet.</p>
                )}
              </div>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            disabled={isUploading}
            className={`mt-4 w-full px-4 py-2 rounded-lg ${
              isUploading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-700'
            } text-white font-semibold`}
          >
            {isUploading ? 'Uploading...' : 'Submit Files'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DragAndDrop; 