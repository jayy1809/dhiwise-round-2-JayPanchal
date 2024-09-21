import os

import assemblyai as aai
from moviepy.editor import VideoFileClip

from app.config import ASSEMBLYAI_API_KEY

aai.settings.api_key = ASSEMBLYAI_API_KEY


def process_video_transcription(video_path):
    try:
        audio_path = video_path.replace(".mp4", ".wav")
        video = VideoFileClip(video_path)
        audio = video.audio.subclip(0, 600)
        audio.write_audiofile(audio_path)
        video.close()

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)
        return transcript.text
    
    except Exception as e:
        raise Exception(f"There was an error generating the transcript: {str(e)}")

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
