function saveTask() {
    // Get form input values
    const taskId = document.getElementById('taskId').value;
    const machineId = document.getElementById('machineId').value;
    const duration = document.getElementById('duration').value;

    // Create JSON object with the collected data
    const taskData = {
        "taskId": taskId,
        "machineId": machineId,
        "duration": duration
    };

    // Convert JSON object to a string for storage or transmission
    const jsonData = JSON.stringify(taskData);

    // For demonstration purposes, you can log the JSON data
    console.log(jsonData);

    // You can send this data to a server, save it locally, or perform other operations
    // For example, you could use fetch() to send this data to a server endpoint
}


