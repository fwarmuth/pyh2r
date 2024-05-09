# Hear to Read (pyh2r) 🗣️📜
Hear to Read is a Flask server that uses OpenAI Whisper (offline) to transscipe voice messages into readable text.

## 🤔 Why?
I'am a fighting voice messengers for years, they are the wild west of communication. People talking sometimes forget what they were saying halfway through.

"Where is the relevant information!?", i asked! man ey!

Nobody has time to listen to a 3min voice message, just to know that my brother thinks of visiting my parents maybe next weekend and if I want to join, if they mgith go there when the weather is good enought, because the last days it was not that good and the kids like the outside... - Nope sorry - my eyes can scrim through text much faster than my ears can listen to a voice message. So I decided to fight back and created this project.

I've also brewed up a simple Telegram bot implementation, serving as an easy-to-use front end. Simply forward those voice messages to the bot, and voila! It replies with clear text. 🚀

## 💡 How It Works
- Voice messages are sent to the Telegram bot.
- Telegram Bot forwards the voice message to the Flask server.
- Flask server uses OpenAI Whisper to transcribe the voice message.
- And finally, the Flask server sends the transcribed text back to the Telegram bot, which replies to the user.

## 🚀 Quick Start with Docker
```bash
cd <repo>
docker build -f docker/Dockerfile -t pyh2r .
docker run -d \
    --name hear_to_read \
    -e PYH2R_TELEGRAM_BOT_API_TOKEN=YOUR_TELEGRAM_BOT_API_TOKEN \ # required
    -e PYH2R_STORE_AUDIO_FILES=1 \ # Optional, enables storing audio files
    -v ./uploaded_files:/app/uploaded_files \ # Persistent store uploaded files
    pyh2r
```

## Performance
Two things to note:
- OpenAI Whisper is an offline model, depending on your hardware and the length of the voice message, it might some time.
- OpenAI Whisper is not perfect
- OpenAI Whisper comes in differenct flavors, the one used here is the smallest one, so it might not be as accurate as the bigger ones.
- When you got a nvidia GPU, speed will massively increase! just add `--gpus all` to the `docker run` command, make sure you got `nvidia-docker` setup.

### Runtime numbers
| Model    | Subjective quality          | Runtime on Pi-CM4 | Runtime on vServer |
| -------- | --------------------------- | ----------------- | ------------------ |
| tiny     | poor, but enough for me     | 346.94            | 18.08              |
| small    | good                        | 253.89            | 20.12              |
| base     | good                        | 265.60            | 16.65              |
| medium   | better                      | 250.23            | 16.76              |
| large-v3 | best                        | 291.82            | 16.69              |

Notes:
- 30s voice message, while walking fast with background noise
- Pi-CM4: Raspberry Pi Compute Module 4
- vServer: 4c@2.3Ghz old Xeon VM
- Only one experiment, no warmup, no average

