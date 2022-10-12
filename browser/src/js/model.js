import * as tf from "@tensorflow/tfjs";

export default class Model {
  static createConvModel(maxSize, labelArray) {
    const IMAGE_H = maxSize.height;
    const IMAGE_W = maxSize.width;
    const CLASS_NUM = labelArray.length;
    const model = tf.sequential();
    model.add(
      tf.layers.conv2d({
        inputShape: [IMAGE_H, IMAGE_W, 1],
        kernelSize: 3,
        filters: 16,
        activation: "relu",
        padding: "same",
      })
    );
    model.add(tf.layers.maxPooling2d({ poolSize: 2, strides: 2 }));
    model.add(
      tf.layers.conv2d({
        kernelSize: 3,
        filters: 32,
        activation: "relu",
        padding: "same",
      })
    );
    model.add(tf.layers.maxPooling2d({ poolSize: 2, strides: 2 }));
    model.add(
      tf.layers.conv2d({
        kernelSize: 3,
        filters: 32,
        activation: "relu",
        padding: "same",
      })
    );
    model.add(tf.layers.flatten({}));
    model.add(tf.layers.dense({ units: 64, activation: "relu" }));
    model.add(tf.layers.dropout({ rate: 0.5 }));
    model.add(tf.layers.dense({ units: CLASS_NUM, activation: "softmax" }));

    return model;
  }

  static async train(model, imageTrain, labelTrain, imageValid, labelValid) {
    const optimizer = "rmsprop";
    model.compile({
      optimizer,
      loss: "categoricalCrossentropy",
      metrics: ["accuracy"],
    });

    // const batchSize = 640;
    // const validationSplit = 0.15;
    const trainEpochs = 20;
    const logBoard = document.querySelector("#log");

    await model.fit(imageTrain, labelTrain, {
      validationData: [imageValid, labelValid],
      epochs: trainEpochs,
      callbacks: {
        onEpochEnd: async (_, logs) => {
          const p = document.createElement("p");
          p.innerText = `Epoch End. loss:${logs.loss}, acc:${logs.acc}`;
          logBoard.append(p);

          await tf.nextFrame();
        },
      },
    });
  }

  static ml(imageData, labelData, maxSize, labelArray) {
    const SAMPLE_SIZE = imageData.shape[0];
    const VALID_SIZE = 5000;
    const TRAIN_SIZE = SAMPLE_SIZE - VALID_SIZE;
    // const LABEL_SIZE = labelArray.length;
    const imageTrain = tf.slice(imageData, [0], [TRAIN_SIZE]);
    const imageTest = tf.slice(imageData, [TRAIN_SIZE], [VALID_SIZE]);
    const labelTrain = tf.slice(labelData, [0], [TRAIN_SIZE]);
    const labelTest = tf.slice(labelData, [TRAIN_SIZE], [VALID_SIZE]);
    const model = this.createConvModel(maxSize, labelArray);
    model.summary();
    tf.dispose([imageData, labelData]);
    this.train(model, imageTrain, labelTrain, imageTest, labelTest);
  }
}
