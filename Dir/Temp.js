// Get the container element where the directory structure will go
const container = document.getElementById('file-tree');

// 1. Create the main "directory" element (e.g., a <div> or <li>)
const newDir = document.createElement('li');
newDir.textContent = '📂 My New Directory';
newDir.classList.add('directory');

// 2. Create the list for its contents (a nested <ul>)
const contentsList = document.createElement('ul');

// 3. Append the contents list to the directory element
newDir.appendChild(contentsList);

// 4. Append the new directory structure to the main container
container.appendChild(newDir);
