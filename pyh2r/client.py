import requests

def upload_audio(file_path):
    url = 'http://localhost:5000/upload-audio'
    files = {'file': open(file_path, 'rb')}
    return requests.post(url, files=files)

if __name__ == '__main__':
    audio_file_path = 'tests/female_msgs_0.ogg'  # Replace with the path to your audio file
    result = upload_audio(audio_file_path)
    print("result")