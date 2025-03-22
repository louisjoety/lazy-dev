'use client';

import React from 'react';

interface HeaderProps {
  username: string;
}

const Header = ({ username }: HeaderProps) => {
  return (
    <div className="flex justify-end items-center p-4 bg-white shadow-md">
      <div className="flex items-center space-x-2">
        {/* User logo */}
        <img
          width="30"
          height="30"
          src="https://img.icons8.com/ios-glyphs/30/user--v1.png"
          alt="user--v1"
          className="rounded-full"
        />
        <span className="font-bold text-black">{username}</span> {/* Display username */}
      </div>
    </div>
  );
};

export default Header;
