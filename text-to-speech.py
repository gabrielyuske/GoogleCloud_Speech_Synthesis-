import os
from google.cloud import texttospeech
#API_KEY
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret.json"

def synthesize_speech(text,lang="日本語",gender="default"):
    gender_type={
        "default":texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        "male": texttospeech.SsmlVoiceGender.MALE,
        "female": texttospeech.SsmlVoiceGender.FEMALE,
        "neutral": texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_code = {
        "英語": "en-US",
        "日本語": "ja-JP"
    }
    # lang = "日本語"
    # gender = "default"
    # text="こんにちは初めてのgoogle-cloud"
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender= gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    #return response

    filename = "test.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f"音声データを{filename}に書き出しました")

    #JUPITERの場合でいちいち保存したくない時に音声を出力する
    # from IPython.display import Audio
    # Audio(response.audio_content)

lang = "日本語"
gender = "default"
text="こんにちは初めてのgoogle-cloud"
text2="my first workout with google cloud"

synthesize_speech(text2,lang="英語",gender="male")

#response = synthesize_speech(text,gender="male")
#Audio(response.audio_content)

# SSLも使用することができるSSMLは細かい休止や頭文字、日付,時刻,略語,検査すべきテキストに対するオーディオ形式を指定できる。