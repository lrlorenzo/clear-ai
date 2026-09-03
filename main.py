from dotenv import load_dotenv

from enhancer.audio_enhancer import AudioEnhancer

load_dotenv()

import argparse
import logging
import logging.config
import yaml
from settings import settings
from html import parser

_logger = logging.getLogger(__name__)

def main():

    with open("logging.yaml") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)

    parser = argparse.ArgumentParser(description="Clean background noise and chatter from interview audio using ClearVoice AI.")
    parser.add_argument("-f", "--file", type=str, help="Path to a single input audio file.")
    parser.add_argument("-d", "--dir", type=str, help="Path to an input directory containing audio files.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path for the output file or output directory.")    

    args = parser.parse_args()

    if not args.file and not args.dir:
            parser.error("You must specify either --file (-f) or --dir (-d).")
    if args.file and args.dir:
        parser.error("Please specify either --file or --dir, not both.")

    _logger.info(f"Using model: {settings.MODEL}")
    _logger.info(f"Supported file extensions: {settings.SUPPORTED_EXTENSIONS}")
    enhancer = AudioEnhancer(settings)
    enhancer.enhance_video(args.file, args.output)

if __name__ == "__main__":
    main()