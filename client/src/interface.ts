const SERVER_IP: string = "127.0.0.1";

interface WebSocketHandler {
  socket: WebSocket | null;
  setNodes: React.Dispatch<React.SetStateAction<any[]>>;
  connect: (setNodes: React.Dispatch<React.SetStateAction<any[]>>) => void;
  send: (data: any) => void;
  close: () => void;
}

const websocketHandler: WebSocketHandler = {
  socket: null,
  setNodes: ()=>{},

  connect(setNodes: React.Dispatch<React.SetStateAction<any[]>>) {
    this.setNodes = setNodes
    this.socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.socket.onmessage = (event) => {
      console.log('Message from server:', event.data);
      const data = JSON.parse(event.data);
      this.setNodes((nodes: any[]) =>
        nodes.map((node: any) => {
          if (data.step == node.id) {
            return {
              ...node,
              style: { backgroundColor: '#2ecc71' },
            };
          }
          return node;
        })
      )
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  },

  send(data: any) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    } else {
      console.error('WebSocket is not open');
    }
  },

  close() {
    if (this.socket) {
      this.socket.close();
    }
  },
};

export default websocketHandler;




// const useWebSocketHandler = (setNodes: React.Dispatch<React.SetStateAction<any[]>>) => {
//   const socketRef = useRef<WebSocket | null>(null);

//   const openWebSocket = useCallback(() => {
//     const socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");

//     socket.onopen = () => {
//       console.log('WebSocket connection established');
//     };

//     socket.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       console.log(event);

//       setNodes((nodes: any[]) =>
//         nodes.map((node: any) => {
//           if (data.step == node.id) {
//             return {
//               ...node,
//               style: { backgroundColor: '#2ecc71' },
//             };
//           }
//           return node;
//         })
//       );
//     };

//     socket.onclose = () => {
//       console.log('WebSocket connection closed');
//     };

//     socket.onerror = (error) => {
//       console.error('WebSocket error:', error);
//     };

//     socketRef.current = socket;
//   }, [setNodes]);

//   const onSubmitToSocket = (e: any) => {
//     socketRef.current?.send(JSON.stringify(e))
//   }

//   const closeWebSocket = useCallback(() => {
//     if (socketRef.current) {
//       console.log('callback closed the websocket');
//       socketRef.current.close();
//       socketRef.current = null; // Ensure the reference is cleared
//     }
//   }, []);

//   useEffect(() => {
//     return () => {
//       // Ensure the WebSocket connection is closed when the component unmounts
//       closeWebSocket();
//     };
//   }, [closeWebSocket]);

//   return { openWebSocket, onSubmitToSocket, closeWebSocket };
// };

// export default useWebSocketHandler;
