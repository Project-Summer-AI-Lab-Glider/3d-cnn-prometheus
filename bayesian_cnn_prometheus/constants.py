from pathlib import Path

import bayesian_cnn_prometheus


class DatasetType:
    TRAIN = 'train'
    TEST = 'test'
    VALID = 'valid'


class DatasetTypeTargets:
    TRAIN = 'train_targets'
    TEST = 'test_targets'
    VALID = 'valid_targets'


class Paths:
    PROJECT_DIR = Path(bayesian_cnn_prometheus.__file__).parent
    DATA_DIR = PROJECT_DIR / "data"

    CONFIG_PATH = PROJECT_DIR / 'config.json'

    MASKS_DIR = 'MASKS'
    MASKS_PATH = DATA_DIR / MASKS_DIR
    MASK_FILE_PATTERN = 'MASK_{}.{}'
    MASK_FILE_PATTERN_PATH = MASKS_PATH / MASK_FILE_PATTERN

    IMAGES_DIR = 'IMAGES'
    IMAGES_PATH = DATA_DIR / IMAGES_DIR
    IMAGE_FILE_PATTERN = 'IMG_{}.{}'
    IMAGE_FILE_PATTERN_PATH = IMAGES_PATH / IMAGE_FILE_PATTERN

    REFERENCE_SEGMENTATIONS_DIR = 'REFERENCE_SEGMENTATIONS'
    REFERENCE_SEGMENTATIONS_PATH = DATA_DIR / REFERENCE_SEGMENTATIONS_DIR
    REFERENCE_SEGMENTATION_FILE_PATTERN = 'LUNGS_IMG_{}.{}'
    REFERENCE_SEGMENTATION_FILE_PATTERN_PATH = REFERENCE_SEGMENTATIONS_PATH / REFERENCE_SEGMENTATION_FILE_PATTERN

    RESULTS_DIR = 'RESULTS'
    RESULTS_PATH = DATA_DIR / RESULTS_DIR

    PREDICTIONS_FILE_PATTERN = 'PREDICTIONS_{}.{}'
    PREDICTIONS_FILE_PATTERN_PATH = RESULTS_PATH / PREDICTIONS_FILE_PATTERN

    SUMMARY_FILE_PATTERN = 'SUMMARY_ID_{}_SLICE_{}.{}'
    SUMMARY_FILE_PATTERN_PATH = RESULTS_PATH / SUMMARY_FILE_PATTERN


class Metrics:
    DICE_COEFFICIENT = "dice_coefficient"
    HAUSDORFF_DISTANCE = "hausdorff_distance"
    JACCARD_INDEX = "jaccard_index"
    MEANS = "means"


BATCH_SIZE = 'batch_size'
CHUNK_SIZE = 'chunk_size'
