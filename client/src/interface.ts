const SERVER_IP: string = "127.0.0.1";

export async function processPipeline(e: object) {
  console.log("Input to Model")
  console.log(e)

  
  try {
    const response = await fetch("http://"+SERVER_IP+":8000/generate-text", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Request-Method': 'POST',
      },
      body: JSON.stringify(e),
    });
    
    // Check if the response is OK (status code 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    updatePipelineStatus();

    // Parse the JSON response
    const data = await response.json();
    
    // Print the JSON object
    console.log('Response JSON:', data);
  } catch (error: any) {
    // Handle errors
    console.error('Error:', error.message);
  }
}

export function updatePipelineStatus() {
  const socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");

  socket.onopen = () => {
      console.log('WebSocket connection established');
  };

  socket.onmessage = (event) => {
     console.log(event)
  };

  socket.onclose = () => {
      console.log('WebSocket connection closed');
  };

  socket.onerror = (error) => {
      console.error('WebSocket error:', error);
  };
}
