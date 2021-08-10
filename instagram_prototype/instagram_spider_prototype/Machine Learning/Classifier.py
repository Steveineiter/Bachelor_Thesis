import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
# TODO CNN IS wrong right? is a reinforced learning algho


train_data_generator = ImageDataGenerator(
    rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
)
training_set = train_data_generator.flow_from_directory(
    "/home/stefan/Knowledge/Bachelor-thesis/instagram_prototype/instagram_spider_prototype/images_test",
    target_size=(64, 64),
    batch_size=32,
    class_mode="binary",
)

# TODO we have hard overfit ATM but its just a prototype :3
test_data_generator = ImageDataGenerator(rescale=1.0 / 255)
test_set = test_data_generator.flow_from_directory(
    "/home/stefan/Knowledge/Bachelor-thesis/instagram_prototype/instagram_spider_prototype/images_test",
    target_size=(64, 64),
    batch_size=32,
    class_mode="binary",
)

cnn = tf.keras.models.Sequential()

cnn.add(
    tf.keras.layers.Conv2D(
        filters=32, kernel_size=3, activation="relu", input_shape=[64, 64, 3]
    )
)

cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation="relu"))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Flatten())

cnn.add(tf.keras.layers.Dense(units=128, activation="relu"))

cnn.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

cnn.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
    ],
)

cnn.fit(x=training_set, validation_data=test_set, epochs=25)

# Prediction
import numpy as np
from keras.preprocessing import image

test_image = image.load_img(
    "/home/stefan/Knowledge/Bachelor-thesis/instagram_prototype/instagram_spider_prototype/images_test/Marry - CQ3JltNpzou.jpg",
    target_size=(64, 64),
)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = cnn.predict(test_image)
print(training_set.class_indices)
