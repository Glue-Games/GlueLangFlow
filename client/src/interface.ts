const SERVER_IP: string = "127.0.0.1";

interface WebSocketHandler {
  socket: WebSocket | null;
  setNodes: React.Dispatch<React.SetStateAction<any[]>>;
  connect: (setNodes: React.Dispatch<React.SetStateAction<any[]>>, data: any) => void;
  send: (data: any) => void;
  close: () => void;
}

function handleData(data: any) {
  const llist = document.getElementById("main-list")
      switch(data.step) {
        case -1:
          if (data.data == "FAILED") {
            alert("failed attempt, refresh and try again...")
          } else {
            alert("Finished!")
          }
          break;
        case 0: /* Not Implemented */
          break;
        case 1: /* Not Implemented */
          break;
        case 2: /* Image Prompt output */
          var imagePromptElement = document.createElement('div')
          imagePromptElement.innerHTML = `
          <h4>Image Prompt <h4>
          <p>${data.data}<p>
          `
          llist?.appendChild(imagePromptElement)
          break;
          case 3: /* Image URL */
          var imageUrlElement = document.createElement('div')
          imageUrlElement.innerHTML = `
          <h4>Image URL (without background)</h4>
          <div><a href="${data.data}" download="gen_image.png">link to download</a></div>
          <img class="image-output" src="${data.data}"></img>
          `
          llist?.appendChild(imageUrlElement)
          break;
        case 4: /* Algo ran */
          break;
        case 5: /* Complete Level */
          var fullImageUrlElement = document.createElement('div')
          fullImageUrlElement.innerHTML = `
          <h4> Full Image URL (with background)</h4>
          <div><a href="${data.data}" download="full_image.png">link to download</a></div>
          <img class="image-output" src="${data.data}"></img>
          `
          llist?.appendChild(fullImageUrlElement)
          break;
      }
}

const websocketHandler: WebSocketHandler = {
  socket: null,
  setNodes: ()=>{},

  connect(setNodes: React.Dispatch<React.SetStateAction<any[]>>, data: any) {
    this.setNodes = setNodes
    this.socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        console.log(data);
        this.socket.send(JSON.stringify(data));
      } else {
        console.error('WebSocket is not open');
      }
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Message from server:', data);
      
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

      handleData(data)
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
      console.log(JSON.stringify(data));
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
