import React from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';

function App() {
	return (
		<div className="flex h-screen w-screen bg-gray-100 dark:bg-gray-900 w-full">

			<div className="flex flex-col w-full">
				<Navbar />
				<main className="flex flex-row p-6 w-full h-full">
					<Sidebar />
					<ChatArea />
				</main>
			</div>
		</div>
	);
}

export default App;