import os
from google.cloud import texttospeech
import io
import streamlit as st

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
        "日本語": "ja-JP",
        "ポルトガル語":"pt-BR"
    }

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

    return response

st.title("音声出力アプリ")

st.markdown("### データ準備")

input_option = st.selectbox(
    "入力データの選択",
    ("直接入力","テキストファイル")
)

input_data = None

if input_option == "直接入力":
    input_data = st.text_area("こちらにテキストを入力してください","Cloud Speech-to-Text用もサンプル文です。")
else:
    upload_file = st.file_uploader("テキストファイルをアップロードしてください",["txt"])#txt形式
    if upload_file is not None:
        content = upload_file.read()
        #テキストとして読み込むためにdecodeをする
        input_data = content.decode()

if input_data is not None:
    st.write("入力データ")
    st.write(input_data)
    st.markdown("### パラメータ設定")
    st.subheader("言語の話者の性別選択")

    lang = st.selectbox(
        "言語を指定してください",
        ("日本語","英語","ポルトガル語")
    )
    gender = st.selectbox(
        "話者の性別を指定してください",
        ("default", "male","female","neutral")
    )
    st.markdown("### 音声合成")
    st.write("こちらの文章で音声ファイルの生成を行いますか？")
    if st.button("開始"):
        comment = st.empty()
        comment.write("音声出力を開始します")
        response = synthesize_speech(input_data,lang=lang,gender=gender)
        st.audio(response.audio_content)
        comment.write("完了しました")