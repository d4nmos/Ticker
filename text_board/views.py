from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .forms import BoardForm
from .models import Request
from matplotlib import colors
import cv2
import numpy as np
from django.conf import settings
import os

def hex_to_bgr(hex_color):
    rgb_color = colors.hex2color(hex_color)
    bgr_color = tuple(int(c * 255) for c in rgb_color[::-1])
    return bgr_color

def create_text_board(text, color):
    width, height = 100, 100
    duration = 3  
    fps = 20 
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    thickness = 2

    output_file = os.path.join(settings.MEDIA_ROOT, 'output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    text_size = cv2.getTextSize(text, font, font_scale, thickness)
    text_width = (text_size[0])[0]

    text_position = width

    for i in range(duration * fps):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(frame, text, (text_position, 50), font, font_scale, color, thickness)  
        text_position -= 10
    
        if text_position < -text_width - 3:
            text_position = width
    
        out.write(frame)  

    out.release()
    
    return output_file

def board_form(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            picked_color = form.cleaned_data['color']
            
            new_request = Request(description=text, color=picked_color)
            new_request.save()
            
            picked_color_bgr = hex_to_bgr(picked_color)
            
            video_file = create_text_board(text, picked_color_bgr)
            response = FileResponse(open(video_file, 'rb'), as_attachment=True, filename='output.mp4')
            
            return response
    else:
        form = BoardForm()

    return render(request, 'board_form.html', {'form': form})