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

  static binarize(image, thresh, doInvert) {
    const invertImg = doInvert ? this.invert(image) : image;
    const binaryImg = new cv.Mat();
    cv.threshold(invertImg, binaryImg, thresh, 255, cv.THRESH_BINARY);
    invertImg.delete();

    return binaryImg;
  }

  static dilate(image, kernelSize) {
    const dilateImg = new cv.Mat();
    const kernel = new cv.Mat.ones(kernelSize[0], kernelSize[1], cv.CV_8U);
    cv.dilate(image, dilateImg, kernel);

    return dilateImg;
  }

  static erode(image, kernelSize) {
    const erodeImg = new cv.Mat();
    const kernel = new cv.Mat.ones(kernelSize[0], kernelSize[1], cv.CV_8U);
    cv.erode(image, erodeImg, kernel);

    return erodeImg;
  }

  static rotate(image, center, angle) {
    const dst = new cv.Mat();
    const dsize = new cv.Size(image.cols, image.rows);
    const matrix = cv.getRotationMatrix2D(center, angle, 1);
    const borderValue = new cv.Scalar(255, 255, 255);
    cv.warpAffine(
      image,
      dst,
      matrix,
      dsize,
      cv.INTER_CUBIC,
      cv.BORDER_CONSTANT,
      borderValue
    );

    matrix.delete();
    return dst;
  }

  static denoise(image, kernelSize, sigmaColor, sigmaSpace) {
    const denoiseImg = new cv.Mat();
    cv.bilateralFilter(image, denoiseImg, kernelSize, sigmaColor, sigmaSpace);

    return denoiseImg;
  }

  static contrast(image, amount) {
    const f = (131 * (amount + 127)) / (127 * (131 - amount));
    const alphaC = f;
    const gammaC = 127 * (1 - f);

    const contrastImg = new cv.Mat();
    cv.addWeighted(image, alphaC, image, 0, gammaC, contrastImg);

    return contrastImg;
  }
}
