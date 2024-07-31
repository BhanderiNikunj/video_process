import cv2
import datetime

print("==============::->",datetime.datetime.now())

cap = cv2.VideoCapture('input_video.mp4')
overlay_img = cv2.imread('overlay_image.png', -1)
overlay_height, overlay_width = overlay_img.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[0:overlay_height, 0:overlay_width]
    overlay_gray = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(overlay_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    overlay_fg = cv2.bitwise_and(overlay_img, overlay_img, mask=mask)
    dst = cv2.add(frame_bg, overlay_fg)
    frame[0:overlay_height, 0:overlay_width] = dst
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
print("==============::->",datetime.datetime.now())
