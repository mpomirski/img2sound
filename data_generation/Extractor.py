from moviepy.editor import VideoFileClip
import os


class Extractor:
    '''
    This class represents an Extractor object that is used to extract frames and sounds from videos.

    Parameters:
    - videos_path (str): The path to the directory containing the videos.
    - output_path (str): The path to the directory where the extracted frames and sounds will be saved.
    - verbose (bool): Optional. If True, it will print verbose output. Default is False.
    '''

    def __init__(self, videos_path: str, output_path: str, verbose: bool = False) -> None:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_path: str = output_path
        self.videos_path: str = videos_path
        self.verbose: bool = verbose
        if not os.path.exists(videos_path):
            raise FileNotFoundError(f'{videos_path} not found')
        if videos_path == '/':
            raise ValueError(
                'Careful with the path, you are providing the root directory')
        if videos_path.endswith('/'):
            self.videos_path = videos_path[:-1]

    def _extract_frame(self, video_path: str, output_path: str) -> None:
        '''
        Extracts a single frame from a video and saves it as a PNG image.

        Parameters:
        - video_path (str): The path to the video file.
        - output_path (str): The path where the extracted frame will be saved.
        '''
        clip: VideoFileClip = VideoFileClip(video_path)
        clip.save_frame(output_path+'.png', t=1)
        clip.close()
        if self.verbose:
            print(f'MoviePy - Writing frame in {output_path}.png')

    def _extract_sound(self, video_path: str, output_path: str) -> None:
        '''
        Extracts a 10-second audio clip from a video and saves it as a WAV file.

        Parameters:
        - video_path (str): The path to the video file.
        - output_path (str): The path where the extracted audio clip will be saved.
        '''
        clip: VideoFileClip = VideoFileClip(video_path).set_duration(10)
        assert clip.audio is not None
        clip.audio.write_audiofile(
            output_path+'.wav', fps=22050, nbytes=2, bitrate='50k', codec='pcm_s16le', verbose=self.verbose, logger=None if not self.verbose else 'bar')
        clip.close()

    def _extract_sounds(self) -> None:
        '''
        Extracts sounds from all videos in the specified directory and saves them in the output directory.
        '''
        for i, video in enumerate(os.listdir(self.videos_path)):
            video_path: str = f'{self.videos_path}/{video}'
            output_path: str = f'{self.output_path}/{i}'
            self._extract_sound(video_path, output_path)

    def _extract_frames(self) -> None:
        '''
        Extracts frames from all videos in the specified directory and saves them in the output directory.
        '''
        for i, video in enumerate(os.listdir(self.videos_path)):
            video_path: str = f'{self.videos_path}/{video}'
            output_path: str = f'{self.output_path}/{i}'
            self._extract_frame(video_path, output_path)

    def _extract_all(self) -> None:
        '''
        Extracts frames and sounds from all videos in the specified directory and saves them in the output directory.
        '''
        for i, video in enumerate(os.listdir(self.videos_path)):
            video_path: str = f'{self.videos_path}/{video}'
            output_path: str = f'{self.output_path}/{i}'
            self._extract_frame(video_path, output_path)
            self._extract_sound(video_path, output_path)

    def extract_all(self) -> None:
        '''
        Extracts frames and sounds from all videos in the specified directory and saves them in the output directory.
        If an exception occurs during extraction, it prints the error message and performs cleanup.
        '''
        try:
            self._extract_all()
        except Exception as e:
            print(e)
            self.cleanup()

    def extract_frames(self) -> None:
        '''
        Extracts frames from all videos in the specified directory and saves them in the output directory.
        If an exception occurs during extraction, it prints the error message and performs cleanup.
        '''
        try:
            self._extract_frames()
        except Exception as e:
            print(e)
            self.cleanup()

    def extract_sounds(self) -> None:
        '''
        Extracts sounds from all videos in the specified directory and saves them in the output directory.
        If an exception occurs during extraction, it prints the error message and performs cleanup.
        '''
        try:
            self._extract_sounds()
        except Exception as e:
            print(e)
            self.cleanup()

    def cleanup(self) -> None:
        '''
        Cleans up the output directory by removing any partially extracted files.
        '''
        if not os.path.exists(self.output_path):
            raise FileNotFoundError(f'{self.output_path} not found')
        if self.output_path == '/':
            raise ValueError(
                'Careful with the path, you are providing the root directory')
        for file in os.listdir(self.output_path):
            if file.endswith('.png') or file.endswith('.wav'):
                os.remove(f'{self.output_path}/{file}')
                print(f'{file} removed')


def main() -> None:
    extractor: Extractor = Extractor('videos', 'data', verbose=True)
    extractor.extract_all()


if __name__ == '__main__':
    main()
