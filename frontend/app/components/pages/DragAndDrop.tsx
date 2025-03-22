'use client';

import React, { useState } from 'react';
import Header from '../ui/Headers'; // Import the Header component

const DragAndDrop = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [dragging, setDragging] = useState(false);
  const [submittedFiles, setSubmittedFiles] = useState<File[]>([]); // Store submitted files

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
    setFiles((prevFiles) => [...prevFiles, ...droppedFiles]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    setFiles((prevFiles) => [...prevFiles, ...selectedFiles]);
  };

  const handleSubmit = () => {
    setSubmittedFiles(files); // Submit the files
    setFiles([]); // Optionally, clear the current files after submission
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Include Header Component */}
      <Header
        username="John Doe"
        className="fixed top-0 left-0 right-0 z-50 bg-white shadow-md" // Fixed header with high z-index
      />

      <div className="flex justify-center items-center flex-grow mt-20"> {/* Add margin-top to avoid overlap with fixed header */}
        <div
          className={`flex justify-center items-center border-2 p-5 border-dashed rounded-lg ${dragging ? 'border-blue-500' : 'border-gray-300'}`}
          style={{ width: '60%' }} // Adjust the width as needed
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
              webkitdirectory="true" // This allows folder uploads
              mozdirectory="true" // This helps with Firefox compatibility
            />
            <label
              htmlFor="file-upload"
              className={`cursor-pointer ${dragging ? 'text-blue-500' : 'text-gray-700'}`} 
            >
              {dragging ? 'Release to drop files' : 'Drag & drop or upload '}
              <span className="text-blue-500 hover:underline">here</span>, or click to select files/folders
            </label>
            <div className="mt-4 text-gray-700">
              <h3>Files Ready to Upload:</h3>
              {files.length > 0 ? (
                <ul>
                  {files.map((file, index) => (
                    <li key={index} className="text-gray-700">{file.name}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-700">No files selected yet.</p>
              )}
            </div>
            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              className="cursor-pointer ${dragging ? 'text-blue-500' : 'text-gray-700'} mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Submit Files
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};


export default DragAndDrop;
