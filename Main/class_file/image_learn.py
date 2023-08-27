import os
import numpy as np
import cv2 as cv
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import LearningRateScheduler
import matplotlib.pyplot as plt

class ImageLearn:
    def __init__(self):

        self.IMG_SIZE = (80, 80)
        self.channels = 1
        self.char_path = r'../../img/face'

        # 데이터 로드
        self.data = []
        self.labels = []
        self.class_names = self.list_directories(self.char_path)

        self.train_model()

    def list_directories(self, path):
        """
        지정된 경로의 폴더를 출력합니다.
        """
        class_names = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                class_names.append(name)
        return class_names

    def train_model(self):

        for name in self.class_names:
            path = os.path.join(self.char_path, name)
            for image_name in os.listdir(path):
                image_path = os.path.join(path, image_name)
                img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)  # 회색조 이미지로 읽기
                img = cv.resize(img, self.IMG_SIZE)
                self.data.append(img)
                self.labels.append(self.class_names.index(name))

        data = np.array(self.data, dtype=np.float32) / 255.0  # 정규화
        labels = to_categorical(np.array(self.labels))

        x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2)
        x_train = x_train.reshape(x_train.shape[0], self.IMG_SIZE[0], self.IMG_SIZE[1], self.channels)
        x_val = x_val.reshape(x_val.shape[0], self.IMG_SIZE[0], self.IMG_SIZE[1], self.channels)

        BATCH_SIZE = 32
        EPOCHS = 10

        datagen = ImageDataGenerator()
        train_gen = datagen.flow(x_train, y_train, batch_size=BATCH_SIZE)

        # 모델 생성
        model_shape = (self.IMG_SIZE[0], self.IMG_SIZE[1], self.channels)
        model = self.custom_model(model_shape, len(self.class_names))

        # SGD optimizer 사용해서 모델 컴파일
        optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        model.summary()

        lr_sched = self.step_decay_schedule(initial_lr=0.001, decay_factor=0.75, step_size=10)
        callbacks_list = [lr_sched]

        training = model.fit(train_gen,
                             steps_per_epoch=len(x_train) // BATCH_SIZE,
                             epochs=EPOCHS,
                             validation_data=(x_val, y_val),
                             validation_steps=len(y_val) // BATCH_SIZE,
                             callbacks=callbacks_list)

        # model.save("face_model.h5")
        model.save("face_model.keras")

    def custom_model(self, input_shape, num_classes):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))

        return model


    def step_decay_schedule(self, initial_lr=1e-3, decay_factor=0.75, step_size=10):

        def schedule(epoch):
            return initial_lr * (decay_factor ** np.floor(epoch / step_size))

        return LearningRateScheduler(schedule)




    # 테스트
    # 테스트 경로
    # test_path = 'uu_img.png'
    # img = cv.imread(test_path)
    # plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))  # OpenCV는 BGR 형식으로 이미지를 읽으므로 RGB로 변환합니다.
    # plt.show()
    #
    #
    # def prepare(image):
    #     image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # 회색조로 변경
    #     image = cv.resize(image, IMG_SIZE)  # 이미지 크기 조절
    #     image = image.reshape(1, IMG_SIZE[0], IMG_SIZE[1], 1)  # 모델 예측을 위한 형태로 변환
    #     image = image / 255.0  # 데이터 정규화
    #     return image
    #
    #
    # prepared_img = prepare(img)
    # predictions = model.predict(prepared_img)
    #
    # # Getting class with the highest probability
    # print(class_names[np.argmax(predictions[0])])

if __name__ == '__main__':
    image_learn = ImageLearn()
