import React, { useState } from 'react';

const Sidebar = () => {
	const [isCollapsed, setIsCollapsed] = useState(false);
	const [activeItem, setActiveItem] = useState('chats');

	const menuItems = [
		{ id: 'chats', label: 'Chat History', icon: '💬' },
		{ id: 'settings', label: 'Settings', icon: '⚙️' },
		{ id: 'help', label: 'Help', icon: '❓' },
	];

	return (
		<aside className={`bg-gray-800 dark:bg-gray-900 text-white transition-all duration-300 ease-in-out overflow-y-auto ${isCollapsed ? 'w-20' : 'w-64'}`}>
			<div className="flex items-center justify-between p-4 border-b border-gray-700">
				{!isCollapsed && (
					<h2 className="text-lg font-semibold">Menu</h2>
				)}
				<button
					onClick={() => setIsCollapsed(!isCollapsed)}
					className="p-2 rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					{isCollapsed ? '→' : '←'}
				</button>
			</div>

			{/* Navigation Items */}
			<nav className="mt-4">
				{menuItems.map((item) => (
					<button
						key={item.id}
						onClick={() => setActiveItem(item.id)}
						className={`w-full flex items-center px-4 py-3 my-0.5 text-left transition-colors ${activeItem === item.id
								? 'bg-blue-600 text-white'
								: 'hover:bg-gray-700 text-gray-300'
							} ${isCollapsed ? 'justify-center' : ''}`}
					>
						<span className={`mr-3 ${isCollapsed ? 'mr-0' : ''}`}>{item.icon}</span>
						{!isCollapsed && <span>{item.label}</span>}
					</button>
				))}
			</nav>

			{/* Additional Content (e.g., Recent Chats when expanded) */}
			{!isCollapsed && (
				<div className="mt-8 p-4 border-t border-gray-700">
					<h3 className="text-sm font-medium text-gray-300 mb-2">Recent Chats</h3>
					<ul className="space-y-1">
						{['Chat 1', 'Chat 2', 'Chat 3'].map((chat) => (
							<li key={chat} className="text-xs text-gray-400 hover:text-white cursor-pointer">
								{chat}
							</li>
						))}
					</ul>
				</div>
			)}
		</aside>
	);
};

export default Sidebar;
