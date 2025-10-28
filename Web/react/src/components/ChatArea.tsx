
import React, { useState } from 'react';

const ChatArea = () => {
	const [query, setQuery] = useState('');
	const [file, setFile] = useState(null);

	const handleQueryChange = (e: any) => {
		setQuery(e.target.value);
	};

	const handleFileChange = (e: any) => {
		const selectedFile = e.target.files[0];
		if (selectedFile && (selectedFile.type.startsWith('audio/') || selectedFile.type.startsWith('video/'))) {
			setFile(selectedFile);
			// Handle file upload logic here (e.g., send to chatbot API)
			console.log('File selected:', selectedFile.name);
		} else {
			alert('Please select an audio or video file only.');
			e.target.value = ''; // Reset input
		}
	};

	const handleSubmit = (e: any) => {
		e.preventDefault();
		if (query.trim()) {
			// Handle chat query submission (e.g., send to chatbot)
			console.log('Query submitted:', query);
			setQuery('');
		}
	};

	const messages = [
		{ id: 1, text: 'Hello! How can I help you today?', sender: 'bot', time: '10:00 AM' },
		{ id: 2, text: 'I need help with a query.', sender: 'user', time: '10:01 AM' },
	];

	return (
		<div className="max-w-4xl mx-auto w-full">
			<div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-full flex flex-col flex-grow">
				<div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
					<h2 className="text-lg font-semibold text-gray-900 dark:text-white">Active Chat</h2>
					<span className="text-sm text-gray-500 dark:text-gray-400">Online</span>
				</div>

				<div className="flex-1 overflow-y-auto p-4 space-y-4">
					{messages.map((message) => (
						<div
							key={message.id}
							className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
						>
							<div
								className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${message.sender === 'user'
									? 'bg-blue-500 text-white'
									: 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
									}`}
							>
								<p>{message.text}</p>
								<span className="text-xs opacity-70 block mt-1">{message.time}</span>
							</div>
						</div>
					))}
					{messages.length === 0 && (
						<div className="text-center text-gray-500 dark:text-gray-400 py-8">
							Start a conversation...
						</div>
					)}
				</div>
				<div className='flex flex-row w-full '>
					<form onSubmit={handleSubmit} className="flex items-center space-x-2 w-full">
						<input
							type="text"
							value={query}
							onChange={handleQueryChange}
							placeholder="Type your message..."
							className="flex-grow px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white w-64"
						/>
						<label className="flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg cursor-pointer hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
							<span className="mr-2">📎 Upload Audio/Video</span>
							<input
								type="file"
								accept="audio/*,video/*"
								onChange={handleFileChange}
								className="hidden"
							/>
						</label>
						<input
							type="submit"
							disabled={!query.trim()}
							className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500"
							value={'Submit'}
						/>
					</form>
				</div>
			</div>
		</div>
	);
};

export default ChatArea;
