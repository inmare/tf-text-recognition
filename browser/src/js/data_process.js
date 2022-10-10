import cv from "@techstark/opencv-js";
import ImgProcess from "./image_process";
import * as tf from "@tensorflow/tfjs";

export default class DataProcess {
  static async convertImageToTensor(image, charInfo) {
    const cropPointH = charInfo.cropPointH;
    const cropPointV = charInfo.cropPointV;
    const sampleSize = (cropPointH.length - 1) * (cropPointV.length - 1);
    const maxSize = charInfo.maxSize;
    let dataArray = [];
    const previous = performance.now();

    for (let i = 0; i < cropPointV.length - 1; i++) {
      for (let j = 0; j < cropPointH.length - 1; j++) {
        const x = cropPointH[j];
        const y = cropPointV[i];
        const width = cropPointH[j + 1] - cropPointH[j];
        const height = cropPointV[i + 1] - cropPointV[i];
        const charRect = new cv.Rect(x, y, width, height);
        const charImg = image.roi(charRect);
        const paddedImg = ImgProcess.addPadding(
          charImg,
          maxSize.width,
          maxSize.height
        );
        charImg.delete();
        dataArray.push(paddedImg.data);
        paddedImg.delete();

        // const now = performance.now();
        // if (previous) {
        //   console.log(now - previous);
        // }
        // previous = now;
      }
    }

    image.delete();

    const imageData = tf.tidy(() => {
      const imageTensor = tf.tensor(dataArray, [
        sampleSize,
        maxSize.height,
        maxSize.width,
        1,
      ]);
      const maxValue = tf.scalar(255);
      const scaledTensor = tf.div(imageTensor, maxValue);
      tf.dispose([imageTensor, maxValue]);
      return scaledTensor;
    });
    imageData.dispose();
    const now = performance.now();
    console.log(now - previous);
  }

  static async convertLabelToOneHot(labelArray) {
    const labelTensor = tf.tensor1d(labelArray);
    const oneHotLabel = tf.oneHot(labelTensor);

    labelTensor.dispose();
    return oneHotLabel;
  }
}
