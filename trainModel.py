import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


data_dir = "dataset"

# Train data characteristics
batch_size = 32
img_height = 224
img_width = 224
epochs = 10  

# validation data
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input, 
    validation_split=0.2  # 20% for validation
)


train_data = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    subset="training",
    class_mode="categorical"
)

val_data = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    subset="validation",
    class_mode="categorical"
)

# Load pre-trained
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(img_height, img_width, 3))


base_model.trainable = False

# define model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation="relu"),
    Dense(train_data.num_classes, activation="softmax")
])

# define optimizers, loss function and metrics.
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs
)

# save model
model.save("custom_model.h5")
print("model saved")
