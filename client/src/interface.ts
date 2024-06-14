import { useEffect, useRef, useCallback } from "react";

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
  
  // Parse the JSON response
  const data = await response.json();
  
  // Print the JSON object
  console.log('Response JSON:', data);
} catch (error: any) {
  // Handle errors
  console.error('Error:', error.message);
}
}

const useWebSocketHandler = (setNodes: React.Dispatch<React.SetStateAction<any[]>>) => {
  const socketRef = useRef<WebSocket | null>(null);

  const openWebSocket = useCallback(() => {
    const socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
      console.log(event);

      setNodes((nodes: any[]) =>
        nodes.map((node: any) => {
          if (node.id === "test") {
            return {
              ...node,
              style: { backgroundColor: 'green' },
            };
          }
          return node;
        })
      );
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socketRef.current = socket;
  }, [setNodes]);

  const closeWebSocket = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null; // Ensure the reference is cleared
    }
  }, []);

  useEffect(() => {
    return () => {
      // Ensure the WebSocket connection is closed when the component unmounts
      closeWebSocket();
    };
  }, [closeWebSocket]);

  return { openWebSocket, closeWebSocket };
};

export default useWebSocketHandler;
