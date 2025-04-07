import cv2
import websockets
import asyncio
import numpy as np


async def send_video(camera_id: str = "camera1"):
    uri = f"ws://localhost:8000/ws/video/{camera_id}"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Уменьшаем разрешение для повышения производительности
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                await websocket.send(buffer.tobytes())
                await asyncio.sleep(0.033)  # ~30 FPS
        finally:
            cap.release()


asyncio.run(send_video())