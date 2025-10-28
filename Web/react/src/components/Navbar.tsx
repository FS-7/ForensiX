import React from 'react';

const PROJECT_NAME: string = "NAME"

const Navbar = () => {
	return (
		<nav className="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
			<div className=" mx-auto px-2 ">
				<div className="flex justify-between items-center h-16">
					<div className="flex items-center">
						<h1 className="text-xl font-bold text-gray-900 dark:text-white">{PROJECT_NAME}</h1>
					</div>

					<div className="flex items-center space-x-4">
						<div className="flex items-center space-x-2">
							<i className='w-8 h-8 rounded-full bi bi-person-circle text-xl'></i>
						</div>
					</div>
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
