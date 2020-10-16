"""
Author: Giebisch
ATR checks periodically if specified streamer
is streaming and automatically downloads the stream if possible
"""

import argparse
import time
import os
import youtube_dl

class AutomaticTwitchRecorder:
    """ATR monitors a Twitch channel and downloads the stream
    """
    def __init__(self, channel, output_dir, check_rate):
        self.channel = channel
        self.output_dir = os.path.join(output_dir, '')
        self.check_rate = check_rate

    def check_if_online(self):
        """Checks if channel is currently streaming

        Returns:
            [bool]: [1 if streaming, 0 else]
        """
        ydl = youtube_dl.YoutubeDL()
        try:
            _ = ydl.extract_info(f"http://www.twitch.tv/{self.channel}", download=False)
            return 1
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as _:
            return 0

    def start_loop(self):
        """
        Main loop for Automatic Twitch Recorder
        Downloads stream if channel is currently online and saves it to output_dir

        Returns:
            None
        """
        while True:
            if self.check_if_online():
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': f'{self.output_dir}%(title)s'+'.mp4',
                    'noplaylist': True,
                    'extract-audio': True,
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"http://www.twitch.tv/{self.channel}"])
            else:
                time.sleep(self.check_rate)

def main(args):
    """Starts AutomaticTwitchRecorder

    Args:
        args ([args]): [CLI Arguments]
    """
    atr = AutomaticTwitchRecorder(args.channel, args.output, args.check_rate)
    atr.start_loop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatic Twitch Recorder")
    parser.add_argument("channel", type=str, help="Specify which Twitch Channel you \
        want to observe and download")
    parser.add_argument("--output", type=str, default=os.getcwd(), help="Specfiy desired output \
        directory, if blank current directory will be set")
    parser.add_argument("--check-rate", type=int, default=45, help="Specify how often you want to \
        check if specified channel is streaming. Standard: 45 secs")

    args = parser.parse_args()

    main(args)
