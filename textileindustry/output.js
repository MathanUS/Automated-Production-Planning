document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch output data from the server
    function fetchOutputData() {
        fetch('/output-data') // Replace with your server route
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update HTML elements with the received data
                document.getElementById('makespan').textContent = data.makespan;
                const sequenceList = document.getElementById('sequence');
                sequenceList.innerHTML = ''; // Clear existing list items
                data.sequence.forEach(taskId => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `Task ID: ${taskId}`;
                    sequenceList.appendChild(listItem);
                });
            })
            .catch(error => {
                console.error('Error fetching output data:', error);
            });
    }

    // Call the function to fetch output data when the page loads
    fetchOutputData();
});
