import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# 1. 加载数据集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. 数据预处理
x_train = x_train.reshape((60000, 28, 28, 1)).astype('float32') / 255  # 归一化
x_test = x_test.reshape((10000, 28, 28, 1)).astype('float32') / 255  # 归一化
y_train = tf.keras.utils.to_categorical(y_train, 10)  # One-hot 编码
y_test = tf.keras.utils.to_categorical(y_test, 10)  # One-hot 编码

# 3. 构建模型
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

# 4. 编译模型
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 5. 训练模型
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)

# 6. 评估模型
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'\nTest accuracy: {test_acc:.4f}')

# 7. 可视化一些预测结果
predictions = model.predict(x_test)

# 显示前10个测试样本的预测结果
for i in range(10):
    plt.imshow(x_test[i].reshape(28, 28), cmap='gray')
    plt.title(f'Predicted: {predictions[i].argmax()}, Actual: {y_test[i].argmax()}')
    plt.axis('off')
    plt.show()
