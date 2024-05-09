from tensorflow.keras.metrics import MeanIoU
import tensorflow as tf

app_model = None


# CONFIG CLASS CUSTOM
@tf.keras.utils.register_keras_serializable()
class UpdatedMeanIoU(MeanIoU):
    def __init__(self,
                 y_true=None,
                 y_pred=None,
                 num_classes=None,
                 name=None,
                 dtype=None):
        super(UpdatedMeanIoU, self).__init__(num_classes=num_classes, name=name, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)

    @classmethod
    def from_config(cls, config):
        return cls(num_classes=config['num_classes'], name=config['name'], dtype=config['dtype'])


# INITIAL MODEL
def init_model():
    segment_model = tf.keras.models.load_model('.model/model_segmentation_latest.keras')
    segment_model.summary()
    global app_model
    app_model = segment_model
    return app_model
