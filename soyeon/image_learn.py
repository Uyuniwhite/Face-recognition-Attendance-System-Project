import cv2
import os


input_folder = "face/우현"
# output_folder = ""

# 이미지 학습시키기
# if not os.path.exists(output_folder):
#     os.mkdir(output_folder)
#
# for img_name in os.listdir(input_folder):
#     img_path = os.path.join(input_folder, img_name)
#     img = cv2.imread(img_path)
#
#     # Resize the image to 128x128
#     resized_img = cv2.resize(img, (128, 128))
#
#     output_path = os.path.join(output_folder, img_name)
#     cv2.imwrite(output_path, resized_img)

# 이미지 전처리(정규화)
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
#
# datagen = ImageDataGenerator(rescale=1./255.) # 이를 통해 이미지는 0과 1 사이의 값을 가지게 됩니다.
#
# generator = datagen.flow_from_directory(
#     output_folder,
#     target_size=(128, 128),
#     batch_size=32,
#     class_mode='binary' # binary or categorical depending on your dataset
# )

# 이미지 전처리(정규화)

output_folder = "face"
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1. / 255.)

generator = datagen.flow_from_directory(
    output_folder,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical'  # 다중 클래스 분류를 위해 'categorical'로 변경
)

# 모델 설계
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(512, activation='relu'),
    # tf.keras.layers.Dense(1, activation='sigmoid'),  # 이진 분류를 위한 sigmoid 활성화 함수
    tf.keras.layers.Dense(len(generator.class_indices), activation='softmax')  # 다중 클래스 분류를 위한 softmax 활성화 함수
])

# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 훈련
model.fit(generator, epochs=25)

# 모델 저장
model.save('people.h5')

import json

# Save class indices
with open('class_indices.json', 'w') as f:
    json.dump(generator.class_indices, f)
