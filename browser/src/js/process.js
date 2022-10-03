/* eslint-disable no-unused-vars */
import cv from "@techstark/opencv-js";

export default class Process {
  static gray(image) {
    const grayImg = new cv.Mat();
    cv.cvtColor(image, grayImg, cv.COLOR_BGR2GRAY);

    return grayImg;
  }

  static crop(image, cropRect) {
    // 후에 setting.js에 적힌 설명대로 변수를 수정하기
    const [x, y, width, height] = cropRect;
    const rect = new cv.Rect(x, y, width, height);
    const cropImg = image.roi(rect);

    return cropImg;
  }

  static invert(image) {
    const invertImg = new cv.Mat();
    cv.bitwise_not(image, invertImg);

    return invertImg;
  }

  static binarization(image, thresh, doInvert) {
    const invertImg = doInvert ? this.invert(image) : image;
    const binaryImg = new cv.Mat();
    cv.threshold(invertImg, binaryImg, thresh, 255, cv.THRESH_BINARY);
    invertImg.delete();

    return binaryImg;
  }
}
