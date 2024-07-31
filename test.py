import cv2
import numpy as np
import datetime

overlay_image_file = "videos_and_filters/overlay_image.png"
video_file = "videos_and_filters/input_video1.mp4"
output_video_file = "output/output_video.mp4"

print("==============::->", datetime.datetime.now())

cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print("Error: Couldn't open video file.")
    exit()

# Read the first frame to get the frame size
ret, frame = cap.read()
if not ret:
    print("Error: Couldn't read the first frame.")
    cap.release()
    exit()

frame_height, frame_width = frame.shape[:2]
overlay_img = cv2.imread(overlay_image_file, cv2.IMREAD_UNCHANGED)

# Resize overlay image if needed
if overlay_img.shape[1] != frame_width or overlay_img.shape[0] != frame_height:
    overlay_img = cv2.resize(overlay_img, (frame_width, frame_height))

if overlay_img.shape[2] == 4:  # Has alpha channel
    overlay_rgb = overlay_img[:, :, :3]
    alpha_channel = overlay_img[:, :, 3] / 255.0
else:
    overlay_rgb = overlay_img
    alpha_channel = np.ones((overlay_img.shape[0], overlay_img.shape[1]), dtype=np.float32)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_file, fourcc, 30.0, (frame_width, frame_height))

# Process each frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[:overlay_img.shape[0], :overlay_img.shape[1]]

    mask = alpha_channel
    mask_inv = 1.0 - mask
    frame_bg = roi * mask_inv[:, :, np.newaxis]
    overlay_fg = overlay_rgb * mask[:, :, np.newaxis]
    dst = cv2.add(frame_bg.astype(np.uint8), overlay_fg.astype(np.uint8))

    frame[:overlay_img.shape[0], :overlay_img.shape[1]] = dst
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()

print("==============::->", datetime.datetime.now())
