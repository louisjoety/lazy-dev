'use client';

import React, { useState, useEffect } from 'react';
import Header from '../components/ui/Headers'; // Import the Header component

const Chatbot = () => {
  const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
  const [userInput, setUserInput] = useState('');

  // Set initial bot message when the component is mounted
  useEffect(() => {
    setMessages([{ user: '', bot: 'How can I help you today?' }]);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (userInput.trim()) {
      // Add user message and bot response
      setMessages((prevMessages) => [
        ...prevMessages,
        { user: userInput, bot: 'OK for now' },
      ]);
      setUserInput(''); // Clear input field
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header Component */}
      <Header username="John Doe" />
      <div className="flex-grow overflow-auto space-y-4 p-4">
        {messages.map((message, index) => (
          <div key={index} className="flex flex-col">
            {/* User's message */}
            {message.user && (
              <div className="text-left text-black">
                <div className="font-bold">User:</div> {/* Name in first line */}
                <div>{message.user}</div> {/* Message in second line */}
              </div>
            )}
            {/* Bot's message */}
            {message.bot && (
              <div className="text-right text-black">
                <div className="font-bold">Bot:</div> {/* Name in first line */}
                <div>{message.bot}</div> {/* Message in second line */}
              </div>
            )}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex items-center space-x-2 mt-4 p-4">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          className="flex-grow p-2 border rounded-lg text-black"
          placeholder="Type a message..."
        />
        <button type="submit" className="p-2 bg-blue-500 text-white rounded-lg">
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
