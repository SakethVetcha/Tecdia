# 🧩 Jumbled Frames Reconstruction Challenge

### 🎯 Objective  
Reconstruct the correct order of frames from a jumbled 5-second, 1080p, 60 FPS video and output the reconstructed video in `.mp4` format.

---

## ⚙️ Project Overview  
This solution:  
- Extracts all frames from the input jumbled video.  
- Computes pairwise **Structural Similarity (SSIM)** between frames.  
- Builds a **frame similarity matrix** to estimate visual continuity.  
- Determines the correct sequential order using a **greedy nearest-neighbor algorithm**.  
- Reassembles the ordered frames into a smooth video output.  
- Logs total execution time for benchmarking.

---

## 🧱 Folder Structure  
JumbledFramesReconstruction/
│
├── reconstruct.py
├── README.md
├── requirements.txt
└── execution_time_log.txt

yaml
Copy code

---

## 💾 Requirements  
Create a Python 3.8+ environment and install dependencies.

### Option 1: Clone and Install via `requirements.txt`  
```bash
git clone https://github.com/SakethVetcha/Tecdia.git
cd Tecdia
pip install -r requirements.txt
Option 2: Manual Installation
bash
Copy code
pip install opencv-python scikit-image tqdm numpy
▶️ How to Run
Place your jumbled video (e.g., jumbled_video.mp4) in the same folder as reconstruct.py.

Run the script:

bash
Copy code
python reconstruct.py
Outputs:

Extracted frames → frames/

Ordered frames → ordered_frames/

Final video → reconstructed_video.mp4

Execution time → execution_time_log.txt

🧠 Algorithm Explanation
Step 1: Frame Extraction
Each frame is extracted and saved as an image using OpenCV.

Step 2: Visual Similarity (SSIM)
Each frame is converted to grayscale (160×120) for speed, and SSIM scores are computed between pairs to measure visual closeness.

Step 3: Frame Order Reconstruction
A greedy approach:

Start with the frame least similar to all others (likely the first frame).

Repeatedly pick the most similar unvisited frame.

Continue until all frames are ordered.

Step 4: Video Reconstruction
Frames are reordered and written into an .mp4 video.
A subtle fade-out is applied to the final few frames to smooth the transition.

⚡ Performance and Optimization
Feature	Description
Metric	SSIM (Structural Similarity Index)
Processing Size	160×120 grayscale
Algorithm Type	Greedy frame similarity chaining
Parallelism	Optional — can be parallelized for large datasets
Runtime	~2–3 minutes (300 frames on i7-12650H)
Memory Usage	~500–700 MB

📊 Output Files
File / Folder	Description
frames/	Extracted raw frames
ordered_frames/	Frames in predicted correct order
reconstructed_video.mp4	Final output video
execution_time_log.txt	Total runtime log

🏁 Example
bash
Copy code
python reconstruct.py
Output video will be saved as reconstructed_video.mp4 in the project folder.

Author: SakethVetcha
Repository: https://github.com/SakethVetcha/Tecdia
Version: 1.0
License: MIT

makefile
Copy code
