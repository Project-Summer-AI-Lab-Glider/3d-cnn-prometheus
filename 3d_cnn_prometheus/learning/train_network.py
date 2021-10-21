import math
import os

from tensorflow.keras.callbacks import Callback, LearningRateScheduler, ModelCheckpoint

from model.dataset import get_train_data
from model.model import get_model
from model.utils import AnnealingCallback, ex

# Ignores TensorFlow CPU messages.
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


@ex.capture
def schedule(epoch: int, initial_learning_rate: float, lr_decay_start_epoch: int) -> float:
    """
    Defines exponentially decaying learning rate.
    :param epoch: actual epoch number (int)
    :param initial_learning_rate: initial learning rate (float)
    :param lr_decay_start_epoch: epoch number since the learning rate is decaying (int)
    :return: updated value of the learning rate (float)
    """
    if epoch < lr_decay_start_epoch:
        return initial_learning_rate
    else:
        return initial_learning_rate * math.exp((10 * initial_learning_rate) * (lr_decay_start_epoch - epoch))


@ex.automain
def train(weights_path: str, epochs: int, batch_size: int, initial_epoch: int, kl_start_epoch: int,
          kl_alpha_increase_per_epoch: float, data_dir: str) -> None:
    """
    Trains a model.
    :param weights_path: path to save updated weights (or path to trained before weights if they exist) (str)
    :param epochs: number of epochs to train the model (int)
    :param batch_size: number of samples in one batch (samples participating in training during one epoch) (int)
    :param initial_epoch: epoch at which to start training (useful for resuming a previous training run) (int)
    :param kl_start_epoch: epoch at which to start increasing KL weight (article: s) (int)
    :param kl_alpha_increase_per_epoch: step value to obtain the KL weight for the current epoch (article: k_1) (float)
    """
    print('Loading data...')
    input_shape, train_ds, valid_ds = get_train_data()
    train_len = len(os.listdir((os.path.join(data_dir, 'train'))))

    print('Getting the model...')
    # Loads or creates model.
    model, checkpoint_path, kl_alpha = get_model(input_shape, scale_factor=train_len / batch_size,
                                                 weights_path=weights_path)

    # Sets callbacks.
    checkpointer = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, save_best_only=True)

    scheduler = LearningRateScheduler(schedule)
    annealer = Callback() if kl_alpha is None else AnnealingCallback(kl_alpha, kl_start_epoch,
                                                                     kl_alpha_increase_per_epoch)

    print('Fitting the model...')
    # Trains model.
    model.fit(x=train_ds, epochs=epochs,
              initial_epoch=initial_epoch,
              callbacks=[checkpointer, scheduler, annealer],
              validation_data=valid_ds,
              steps_per_epoch=1, validation_steps=1)


if __name__ == '__main__':
    train()
