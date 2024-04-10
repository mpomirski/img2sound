from Downloader import download_many_async, rename_videos
from Extractor import Extractor
import pandas as pd
import os


def main() -> None:
    set_size = 3
    df: pd.DataFrame = pd.read_csv(
        'ncentroids-500-subset_size-20K.csv', header=None)
    print(df.head(10))
    urls: list[str] = df.iloc[:set_size, 0].tolist()
    start_times: list[float] = df.iloc[:set_size, 1].tolist()
    urls = [f'https://www.youtube.com/watch?v={url}' for url in urls]
    output_path: str = 'videos'
    download_many_async(urls, output_path)
    extractor: Extractor = Extractor(
        output_path, output_path='data', duration=5)
    for start_time, video in zip(start_times, sorted(os.listdir(output_path))):
        extractor.extract_all_given_time(
            start_time, f'{output_path}/{video}', video)


if __name__ == '__main__':
    main()
