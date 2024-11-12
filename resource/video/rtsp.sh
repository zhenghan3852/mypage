#!/bin/bash
#/root/rtsp-simple-server/mediamtx
for((;;)); do
    ffmpeg -re -i "/root/data/resource/video/output.h264" -c copy -f rtsp rtsp://127.0.0.1:8554/stream
done
# sudo nohup ffmpeg -re -stream_loop -1 -i /root/data/resource/video/output.h264 -c copy -f rtsp rtsp://127.0.0.1:8554/stream 2>&1 &
# sudo nohup ffmpeg -re -stream_loop -1 -i /root/data/resource/video/output.h264 -c copy -f rtsp rtsp://127.0.0.1:8554/stream &