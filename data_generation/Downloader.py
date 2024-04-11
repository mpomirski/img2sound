from pytube import YouTube, Stream
import os
from multiprocessing.pool import ThreadPool as Pool


def download(url: str, output_path: str, output_filename: str | None = None) -> None:
    '''
    Downloads a video from the specified URL and saves it in the specified output directory.
    '''

    yt: YouTube = YouTube(url)
    stream: Stream | None = yt.streams.get_by_resolution('360p')
    if stream is not None:
        stream.download(output_path, filename=output_filename)
        print(f'Downloaded video: {url}')
    else:
        raise Exception(f'No stream found for video: {url}')


def download_many(urls: list[str], output_path: str) -> None:
    '''
    Downloads multiple videos from the specified URLs and saves them in the specified output directory.
    '''
    for url in urls:
        try:
            download(url, output_path)
        except Exception as e:
            print(e)


def rename_videos(output_path: str) -> None:
    '''
    Renames all the videos in the specified output directory to a common name format.
    '''
    for i, filename in enumerate(os.listdir(output_path)):
        try:
            os.rename(os.path.join(output_path, filename),
                      os.path.join(output_path, f'{i}.mp4'))
        except Exception as e:
            print(e)


def download_many_async(urls: list[str], output_path: str) -> None:
    '''
    Downloads multiple videos from the specified URLs asynchronously and saves them in the specified output directory.
    '''
    with Pool(len(urls)) as pool:
        pool.starmap(download, [(url, output_path, str(i)+'.mp4')
                     for i, url in enumerate(urls)])


def main() -> None:
    '''
    Downloads a video from the specified URL and saves it in the specified output directory.
    If an exception occurs during download, it prints the error message and performs cleanup.
    '''
    urls: list[str] = ['https://www.youtube.com/watch?v=xp-440CEJqg',
                       'https://www.youtube.com/watch?v=N00STIB2qZ0']
    output_path: str = 'videos'
    download_many_async(urls, output_path)
    rename_videos(output_path)


if __name__ == '__main__':
    main()
