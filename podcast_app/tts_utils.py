import asyncio
import os
from pydub import AudioSegment
from uuid import uuid4
import edge_tts

HOST_VOICE = "en-US-AndrewNeural"
GUEST_VOICE = "en-US-AvaNeural"

async def synthesize_text(text, voice, filename):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(filename)

async def generate_podcast(script, output_path="podcast.mp3", bg_music_path=None):
    segment_files = []

    for segment in script:
        voice = HOST_VOICE if segment["speaker"] == "Host" else GUEST_VOICE
        temp_file = f"segment_{uuid4().hex}.mp3"
        await synthesize_text(segment["text"], voice, temp_file)
        segment_files.append(temp_file)

    podcast = AudioSegment.empty()
    for file in segment_files:
        audio = AudioSegment.from_mp3(file)
        podcast += audio + AudioSegment.silent(duration=75)

    if bg_music_path:
        background = AudioSegment.from_mp3(bg_music_path)
        if len(background) < len(podcast):
            background *= (len(podcast) // len(background) + 1)
        background = background - 20
        final_mix = podcast.overlay(background)
    else:
        final_mix = podcast

    final_mix.export(output_path, format="mp3")

    for file in segment_files:
        os.remove(file)
    print("output_path: ",output_path)

    return output_path
