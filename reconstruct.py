import cv2
import numpy as np
import os
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim

# ---------- STEP 1: Extract frames from jumbled video ----------
input_video = "jumbled_video.mp4"
frames_dir = "frames"
os.makedirs(frames_dir, exist_ok=True)

print("[1/4] Extracting frames from jumbled video...")
cap = cv2.VideoCapture(input_video)
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imwrite(f"{frames_dir}/frame_{count:04d}.jpg", frame)
    count += 1
cap.release()
print(f"Extracted {count} frames to '{frames_dir}' folder.")

# ---------- STEP 2: Compute visual similarity ----------
print("[2/4] Computing frame similarities (this may take several minutes)...")

def read_gray(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (160, 120))  # smaller size for faster processing
    return img

frame_files = sorted(os.listdir(frames_dir))
frames = [read_gray(os.path.join(frames_dir, f)) for f in frame_files]
n = len(frames)

similarity = np.zeros((n, n))
for i in tqdm(range(n)):
    for j in range(i + 1, n):
        score = ssim(frames[i], frames[j])
        similarity[i, j] = similarity[j, i] = score

# ---------- STEP 3: Determine frame order ----------
print("[3/4] Determining correct frame order...")

visited = [False] * n
order = []

# Start with frame least similar to others (likely first)
start = np.argmin(similarity.mean(axis=1))
order.append(start)
visited[start] = True

for _ in tqdm(range(n - 1)):
    last = order[-1]
    next_idx = np.argmax(similarity[last] * (~np.array(visited)))
    visited[next_idx] = True
    order.append(next_idx)

print("Frame order determined.")

# ---------- STEP 4: Rebuild ordered video ----------
ordered_dir = "ordered_frames"
os.makedirs(ordered_dir, exist_ok=True)

print("[4/4] Rebuilding ordered video...")

# Copy frames in new order
for idx, frame_idx in enumerate(order):
    src = os.path.join(frames_dir, frame_files[frame_idx])
    dst = os.path.join(ordered_dir, f"frame_{idx:04d}.jpg")
    os.system(f"copy \"{src}\" \"{dst}\" >nul" if os.name == 'nt' else f"cp \"{src}\" \"{dst}\"")

# Create video at 30 fps
output_video = "reconstructed_video.mp4"
sample_frame = cv2.imread(os.path.join(ordered_dir, "frame_0000.jpg"))
h, w, _ = sample_frame.shape
out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))

fade_frames = 10  # number of frames to fade out (adjust if needed)
for i in range(len(order)):
    frame = cv2.imread(os.path.join(ordered_dir, f"frame_{i:04d}.jpg"))

    # Apply fade-out on last few frames
    if i >= len(order) - fade_frames:
        alpha = ((len(order) - i) / fade_frames)**1.5  # fades from 1 → 0
        frame = (frame * alpha).astype(np.uint8)

    out.write(frame)


out.release()
print("Reconstructed video saved as 'reconstructed_video.mp4'")

print("\nAll steps completed successfully!")
print("Check 'reconstructed_video.mp4' for your final output.")
