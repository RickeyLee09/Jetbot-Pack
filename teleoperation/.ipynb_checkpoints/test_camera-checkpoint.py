from jetbot import Camera
import cv2

camera = Camera()

camera.start()

print(camera.value.shape)

cv2.imshow('image',camera.value)

cv2.imwrite('snapshots/1.png',camera.value, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
cv2.waitKey(0)


camera.stop()

