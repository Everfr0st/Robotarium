
import asyncio
import websockets
import json
import cv2
import base64
async def send_data(uri):
	async with websockets.connect(uri) as websocket:
		cap = cv2.VideoCapture(0)
		while True:
			ret, frame = cap.read()
			retval, buffer = cv2.imencode('.jpg', frame)
			jpg_as_text = base64.b64encode(buffer)
			cv2.imshow('live stream',frame)
			
			k = cv2.waitKey(1)
			
			message = {"type": "live_info", "img_data": str(jpg_as_text)}
			message = json.dumps(message)
			await websocket.send(message)
			await websocket.recv()
			if k == 27: 
				break
		cap.release()
		cv2.destroyAllWindows()
asyncio.get_event_loop().run_until_complete(send_data('ws://127.0.0.1:8000/ws/live/main-stream'))
    
    
     



	

