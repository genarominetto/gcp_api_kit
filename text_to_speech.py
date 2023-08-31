import os
from pydub import AudioSegment
from typing import List

from googleapiclient.discovery import build


from gcp_api_connector.resources.googleapis_auth import get_api_key
APIKEY = get_api_key()

def help():
  #Show aviable voices
  print("""
  english_voices = [
      'en-US-Wavenet-A',
      'en-US-Wavenet-B',
      'en-US-Wavenet-C',
      'en-US-Wavenet-D',
      'en-US-Wavenet-E',
      'en-US-Wavenet-F',
      'en-US-Wavenet-G',
      'en-US-Wavenet-H',
      'en-US-Wavenet-I',
      'en-US-Wavenet-J'
  ]


  spanish_voices = [
      'es-ES-Standard-A',
      'es-ES-Standard-B',
      'es-ES-Standard-C',
      'es-ES-Standard-D'
  ]

  latin_american_voices = [
      'es-US-Standard-A',
      'es-US-Standard-B',
      'es-US-Standard-C'
  ]
  """)

def split_text(text: str, max_bytes: int = 5000) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        if len((current_chunk + " " + word).encode('utf-8')) < max_bytes:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
            
    chunks.append(current_chunk.strip())
    return chunks

def concatenate_audio_files(files: List[str], output_filename: str):
    result = AudioSegment.empty()
    
    for file in files:
        audio = AudioSegment.from_wav(file)
        result += audio
        os.remove(file)
        
    result.export(output_filename, format='wav')

def text_to_speech(text: str, voice: str, output_filename: str):
    chunks = split_text(text)
    audio_files = []

    for i, chunk in enumerate(chunks):
        audio_file = f"chunk_{i}.wav"
        synthesize_speech(chunk, voice, audio_file)
        audio_files.append(audio_file)

    concatenate_audio_files(audio_files, output_filename)

def synthesize_speech(text: str, voice: str, output_filename: str):
    tservice = build('texttospeech', 'v1beta1', developerKey=APIKEY)
    response = tservice.text().synthesize(
        body={
            'input': {
                'text': text
            },
            'voice': {
                'languageCode': voice[:5],
                'name': voice
            },
            'audioConfig': {
                'audioEncoding': 'LINEAR16'
            }
        }).execute()

    import base64
    audio = base64.b64decode(response['audioContent'])

    with open(output_filename, 'wb') as f:
        f.write(audio)

def say(text, model='en-US-Wavenet-A', filename='output.wav'):
  text_to_speech(text, model, filename)

  from IPython.display import Audio, display
  audio = Audio("output.wav", autoplay=True)
  display(audio)
