# AI Coding Session Transcript
- Task: Forecast Bitcoin price 240 minutes ahead using 72 hours of 1-minute closes.
- Approach: Linear regression on the last 240 minutes with a 0.15 shrinkage factor to beat the persistence baseline safely.
- Output: main.py (Python 3.13, reads /input, writes /output, no external dependencies).
