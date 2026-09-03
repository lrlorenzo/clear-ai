import logging
from pathlib import Path
from clearvoice import ClearVoice
from pydub import AudioSegment
from moviepy import VideoFileClip, AudioFileClip

import settings

_logger = logging.getLogger(__name__)

class AudioEnhancer:

    def __init__(self, settings):
        self.clearvoice = ClearVoice(task='speech_enhancement', model_names=[settings.MODEL])

    def enhance_video(self, input_path: str | Path, output_path: str | Path) -> None:
        input_file = Path(input_path)
        output_file = Path(output_path)

        if not input_file.exists():
            raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

        _logger.info(f"Enhancing audio file: {input_file}")

        temp_clean_wav = None
        temp_raw_wav = None
        
        try:
            _logger.info("Extracting audio and converting to WAV format...")
            video, temp_raw_wav = self.export_wav_format(input_file)
            temp_clean_wav = self.clean_background_noise(input_file, temp_raw_wav)
            self.merge_audio_video(video, temp_clean_wav, output_file)

        except Exception as e:
            _logger.error(f"Error occurred while enhancing audio file: {e}")
            raise

        finally:
            if temp_raw_wav and temp_raw_wav.exists():
                temp_raw_wav.unlink()
            if temp_clean_wav and temp_clean_wav.exists():
                temp_clean_wav.unlink()

    def export_wav_format(self, input_file: str | Path) -> Path:
            temp_raw_wav = input_file.parent / f"_temp_raw_{input_file.stem}.wav"        
            video = VideoFileClip(str(input_file))
            video.audio.write_audiofile(str(temp_raw_wav))

            return video, temp_raw_wav

    def clean_background_noise(self, input_file: str | Path, temp_raw_wav: str | Path) -> Path:
        temp_clean_wav = input_file.parent / f"_temp_clean_{input_file.stem}.wav"
        enhanced_audio = self.clearvoice(input_path=str(temp_raw_wav), online_write=False)
        self.clearvoice.write(enhanced_audio, output_path=str(temp_clean_wav))
        return temp_clean_wav

    def merge_audio_video(self, video: VideoFileClip, temp_clean_wav: str | Path, output_file: str | Path) -> None:
        _logger.info("Merging enhanced audio with original video...")

        clean_audio = AudioFileClip(str(temp_clean_wav))
        final_video = video.with_audio(clean_audio)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        final_video.write_videofile(str(output_file), codec="libx264", audio_codec="aac")

        clean_audio.close()
        video.close()

        _logger.info(f"Enhanced video saved to: {output_file}")


