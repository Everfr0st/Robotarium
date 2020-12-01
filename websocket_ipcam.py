
import asyncio
import websockets
import json
import cv2
import base64
import time
from datetime import datetime, timedelta
import sys

async def send_data(uri):
	async with websockets.connect(uri) as websocket:
		time_start = time.time()
		cap = cv2.VideoCapture("http://192.168.1.3:8080/videofeed")

		_pause = 0.05
		while True:
			ret, frame = cap.read()
			time_end = time.time()
			delta_time = timedelta(seconds= int(time_end - time_start)) 

			retval, buffer = cv2.imencode('.jpg', frame)
					
			jpg_as_text = base64.b64encode(buffer).decode('utf-8')

			cv2.imshow('live stream',frame)
			
			k = cv2.waitKey(1)
			
			message = {
				"type": "live_info", 
				"img_data": jpg_as_text, 
				'time_elapsed': str(delta_time),
				"started": True,
				"finished": False,
			}
			message = json.dumps(message)
			await websocket.send(message)
			await websocket.recv()
			time.sleep(_pause)
			
			if k == 27: 
				message = {
					"type": "live_info", 
					'time_elapsed': '',
					"started": False,
					"finished": True,
				}
				message = json.dumps(message)
				await websocket.send(message)
				await websocket.recv()
				break
		cap.release()
		cv2.destroyAllWindows()

print('conectando a :')
print('ws://127.0.0.1:8000/ws/live-main-stream/{}/'.format(sys.argv[1]))
asyncio.get_event_loop().run_until_complete(send_data('ws://127.0.0.1:8000/ws/live-main-stream/{}/'.format(sys.argv[1])))
    
    
     



	

