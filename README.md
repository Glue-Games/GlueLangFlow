# PicWiz Level Generator


# Server

## Run Server

Will run both the compilation of the typescript into js and also load the fastAPI server 
```
npm run start
```

Changes to run on server: basically client should address the correct ws address
```
diff --git a/client/src/interface.ts b/client/src/interface.ts
index a7eb597..75f38da 100644
--- a/client/src/interface.ts
+++ b/client/src/interface.ts
@@ -1,4 +1,4 @@
-const SERVER_IP: string = "127.0.0.1";
+const SERVER_IP: string = "65.0.149.192";
 
 interface WebSocketHandler {
   socket: WebSocket | null;
@@ -59,7 +59,7 @@ const websocketHandler: WebSocketHandler = {
 
   connect(setNodes: React.Dispatch<React.SetStateAction<any[]>>, data: any) {
     this.setNodes = setNodes
-    this.socket = new WebSocket("ws://"+SERVER_IP+":8000/ws");
+    this.socket = new WebSocket("ws://"+SERVER_IP+"/ws");
 
     this.socket.onopen = () => {
       console.log('WebSocket connection established');
```

Running the benchmark:
(Make sure the folder structure is as expected with the paths in benchmark.py)
```
python benchmark.py
```