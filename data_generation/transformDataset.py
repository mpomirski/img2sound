import pandas as pd
from Extractor import Extractor
from Downloader import download
import os
import keras
import tensorflow as tf


def main() -> None:
    # https://www.kaggle.com/datasets/codebreaker619/vggsound
    size = 10
    df: pd.DataFrame = pd.read_csv('test.csv', header=None)
    df = df.rename(columns={0: 'url', 1: 'label'})
    df['url_new'] = df['url'].str.slice(0, 11).map(
        lambda x: f'https://www.youtube.com/watch?v={x}')
    df['timestamp'] = df['url'].str.slice(12, 18).astype(int)
    df['url'] = df['url_new']
    df = df.drop(columns=['url_new'])

    extractor = Extractor('videos', 'data', duration=5)
    labels: list[str] = []
    i = 0
    for _, row in df.head(size).iterrows():
        try:
            download(row['url'], 'videos', f'{i}.mp4')
            labels.append(row['label'])
            labels.append(row['label'])
            extractor.extract_all_given_time(
                row['timestamp'], f'videos/{i}.mp4', f'{i}')
            os.remove(f'videos/{i}.mp4')
            i += 1
        except Exception as e:
            print(e)
    print(labels)
    split_into_directories(labels)
    im_dataset: tf.data.Dataset = keras.utils.image_dataset_from_directory(
        'dataset/images', labels='inferred', label_mode='categorical', batch_size=32, image_size=(256, 256))  # type: ignore
    sound_dataset: tf.data.Dataset = keras.utils.audio_dataset_from_directory(
        'dataset/sounds', labels='inferred', label_mode='categorical', batch_size=32, sample_rate=22050)  # type: ignore
    im_dataset.save('train_im_dataset')
    sound_dataset.save('train_sound_dataset')


def split_into_directories(labels: list[str]) -> None:
    if not os.path.exists('dataset/images'):
        os.makedirs('dataset/images')

    if not os.path.exists('dataset/sounds'):
        os.makedirs('dataset/sounds')

    for label, filename in zip(labels, os.listdir('data')):
        extension = filename.split('.')[-1]
        if not os.path.exists(f'dataset/images/{label}'):
            os.makedirs(f'dataset/images/{label}')
        if not os.path.exists(f'dataset/sounds/{label}'):
            os.makedirs(f'dataset/sounds/{label}')
        if extension == 'png':
            os.rename(f'data/{filename}',
                      f'dataset/images/{label}/{filename}')
        if extension == 'wav':
            os.rename(f'data/{filename}',
                      f'dataset/sounds/{label}/{filename}')


if __name__ == '__main__':
    main()
