'use client';

import React, { useState, useEffect } from 'react';
import Header from '../components/ui/Headers';

// Define types for our messages and responses
interface CodeSnippet {
  project_name: string;
  matched_files: string[];
  snippets: { [key: string]: string };
}

interface Message {
  user?: string;
  bot?: CodeSnippet[];
  isError?: boolean;
}

const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setMessages([{ bot: [], isError: false }]);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const userMessage = userInput;
    setUserInput(''); // Clear input field
    setIsLoading(true);

    // Add user message immediately
    setMessages(prev => [...prev, { user: userMessage }]);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { bot: data.code_snippets }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        bot: [], 
        isError: true 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header username="John Doe" />
      <div className="flex-grow overflow-auto space-y-4 p-4">
        {messages.map((message, index) => (
          <div key={index} className="flex flex-col gap-4">
            {/* User message */}
            {message.user && (
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <div className="font-bold text-blue-600">You:</div>
                <div className="text-black mt-1">{message.user}</div>
              </div>
            )}

            {/* Bot response */}
            {message.bot && (
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <div className="font-bold text-green-600">Assistant:</div>
                {message.isError ? (
                  <div className="text-red-500 mt-2">
                    Sorry, I encountered an error processing your request. Please try again.
                  </div>
                ) : message.bot.length === 0 ? (
                  <div className="text-gray-600 mt-2">
                    No matching code snippets found.
                  </div>
                ) : (
                  <div className="space-y-4 mt-2">
                    {message.bot.map((snippet, snippetIndex) => (
                      <div key={snippetIndex} className="border rounded-lg p-4">
                        <h2 className="font-bold text-xl mb-2 text-gray-800">
                          Project: {snippet.project_name}
                        </h2>
                        {Object.entries(snippet.snippets).map(([filename, code], codeIndex) => (
                          <div key={codeIndex} className="mt-2">
                            <div className="text-gray-800 mb-1">
                              {filename}
                            </div>
                            <pre className="bg-gray-50 p-3 rounded overflow-x-auto">
                              <code className="text-sm text-gray-800">{code}</code>
                            </pre>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-center">
            <div className="animate-pulse text-gray-500">Processing your request...</div>
          </div>
        )}
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="border-t bg-white p-4">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            className="flex-grow p-2 border rounded-lg text-black"
            placeholder="Ask about your code..."
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className={`px-4 py-2 rounded-lg text-white ${
              isLoading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;