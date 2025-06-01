import boto3
import os

def polly_speak(
    text,
    voice_id="Joanna",
    output_format="mp3",
    play=True,
    engine="neural",
    use_ssml=False
):
    """
    Converts text to speech using Amazon Polly and saves it to /tmp/polly.mp3

    Args:
        text (str): Text or SSML to convert to speech
        voice_id (str): Polly voice (e.g., Joanna, Amy, Kendra)
        output_format (str): Audio format, usually 'mp3'
        play (bool): If True, plays the audio
        engine (str): 'standard' or 'neural'
        use_ssml (bool): If True, treats text as SSML
    """
    output_path = "/tmp/polly.mp3"
    # Wrap the prompt in SSML

    polly = boto3.client("polly")

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine=engine,
        TextType="ssml" if use_ssml else "text"
    )

    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())

    print(f"✅ [{voice_id}] Audio saved to: {output_path}")

    if play:
        os.system(f"mpg123 {output_path} > /dev/null 2>&1")

    return output_path


