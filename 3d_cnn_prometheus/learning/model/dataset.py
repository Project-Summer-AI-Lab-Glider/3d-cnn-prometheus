import os
from typing import Tuple

import numpy as np
import tensorflow as tf

from .constants import *
from .experiment_setup import ex


def get_data_generator(dataset_dir_path: str, dataset_targets_dir_path: str, batch_size: int = 1,
                       chunk_size: tuple = (32, 32, 16)):
    """
    Generator for training or validation dataset.
    :param dataset_dir_path: dataset images dir path
    :param dataset_targets_dir_path: dataset targets dir path
    :param batch_size: size of batch for data (default: 1, for validation)
    :param chunk_size: size of chunks
    :return data generator
    """

    def data_generator():
        data_dir_path = os.path.join(dataset_dir_path)
        images_names = os.listdir(data_dir_path)
        batches_num = len(images_names) // batch_size or 1
        images_names = images_names[:batch_size * batches_num]
        images_names_batches = np.array_split(images_names, batches_num)

        for image_file_names in images_names_batches:
            images = []
            targets = []

            for image_file_name in image_file_names:
                image_path = str(os.path.join(data_dir_path, image_file_name))
                target_path = image_path.replace(dataset_dir_path, dataset_targets_dir_path).replace('IMG', 'MASK')

                image = np.load(image_path)
                image = image.reshape((*chunk_size, 1))
                images.append(image)

                target = np.load(target_path)
                target = target.reshape((*chunk_size, 1))
                targets.append(target)

            yield np.asarray(images), np.asarray(targets)

    return data_generator


@ex.capture
def get_train_dataset(batch_size: int, chunk_size: tuple) -> tf.data.Dataset:
    """
    Create training dataset.
    :param batch_size: size of batch for train data
    :param chunk_size: size of chunks use for training
    :return training dataset
    """

    train_data_generator = get_data_generator(str(CHUNKS_TRAIN_PATH), str(CHUNKS_TRAIN_TARGETS_PATH), batch_size, chunk_size)
    train_ds_output_shape = tf.TensorShape([batch_size, *chunk_size, 1])
    train_ds = tf.data.Dataset.from_generator(generator=train_data_generator, output_types=(tf.int64, tf.int64),
                                              output_shapes=(train_ds_output_shape, train_ds_output_shape))
    return train_ds


@ex.capture
def get_valid_dataset(chunk_size: tuple) -> tf.data.Dataset:
    """
    Create validation dataset.
    :param chunk_size: size of chunks use for training
    :return training dataset
    """

    valid_data_generator = get_data_generator(str(CHUNKS_VALID_PATH), str(CHUNKS_VALID_TARGETS_PATH), 1, chunk_size)
    valid_ds_output_shape = tf.TensorShape([1, *chunk_size, 1])
    valid_ds = tf.data.Dataset.from_generator(generator=valid_data_generator, output_types=(tf.int64, tf.int64),
                                              output_shapes=(valid_ds_output_shape, valid_ds_output_shape))
    return valid_ds


@ex.capture
def get_input_shape(dataset: tf.data.Dataset) -> Tuple[int]:
    """
    Get input dataset from tensorflow dataset object.
    :param dataset: tensorflow dataset object
    :return: input shape
    """
    return tuple([int(dim.value) for dim in list(dataset.element_spec[0].shape)])
