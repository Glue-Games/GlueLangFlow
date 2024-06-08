export async function processPipeline(e: object) {
  console.log("Input to Model")
  console.log(e)

  try {
      const response = await fetch("http://127.0.0.1:8000/generate-text", {
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
    
        // Parse the JSON response
        const data = await response.json();
    
        // Print the JSON object
        console.log('Response JSON:', data);
  } catch (error: any) {
    // Handle errors
    console.error('Error:', error.message);
  }
}