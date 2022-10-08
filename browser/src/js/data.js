import cv from "@techstark/opencv-js";
import * as tf from "@tensorflow/tfjs";
import Setting from "./setting.js";

export default class Data {
  static getMainContour(image) {
    const contours = new cv.MatVector();
    const hier = new cv.Mat();
    cv.findContours(
      image,
      contours,
      hier,
      cv.RETR_TREE,
      cv.CHAIN_APPROX_SIMPLE
    );

    let mainContour;
    for (let i = 0; i < contours.size(); i++) {
      const contour = contours.get(i);
      const currentCntLen = cv.arcLength(contour, true);
      if (!mainContour) {
        mainContour = contour.clone();
      } else {
        const mainCntLen = cv.arcLength(mainContour, true);
        if (currentCntLen > mainCntLen) {
          mainContour.delete();
          mainContour = contour.clone();
        }
      }
      contour.delete();
    }
    contours.delete();
    hier.delete();

    return mainContour;
  }

  static getRotationInfo(contour) {
    const minRect = cv.minAreaRect(contour);
    const verticies = cv.RotatedRect.points(minRect);
    verticies.sort(comparePoints);
    const center = minRect.center;

    const topLeft = verticies[0];
    const topRight = verticies[2];
    const corner = {
      x: topRight.x,
      y: topLeft.y,
    };

    const diagLen = getLength(topRight, topLeft);
    const horiLen = getLength(corner, topLeft);
    const angle = rad2deg(Math.acos(horiLen / diagLen));

    return [center, angle];

    function comparePoints(a, b) {
      if (a.x > b.x) return 1;
      if (a.x == b.x) {
        if (a.y > b.y) return 1;
        if (a.y == b.y) return 0;
        if (a.y < b.y) return -1;
      }
      if (a.x < b.x) return -1;
    }

    function getLength(p1, p2) {
      const xl = Math.pow(Math.abs(p1.x - p2.x), 2);
      const yl = Math.pow(Math.abs(p1.y - p2.y), 2);
      const len = Math.sqrt(xl + yl);

      return len;
    }

    function rad2deg(rad) {
      return rad * (180 / Math.PI);
    }
  }

  static getRectPoint(contour) {
    const contourPoly = new cv.Mat();
    cv.approxPolyDP(contour, contourPoly, 3, true);
    const boundingRect = cv.boundingRect(contourPoly);
    contourPoly.delete();

    return boundingRect;
  }

  static getCharPoint(image) {
    const data = image.data;
    const size = [image.rows, image.cols];
    const imgTensor = tf.tensor(data, size);
    const correction = Setting.lowCorrection;
    // horizontal sum
    const [sum, lowPoint] = tf.tidy(() => {
      const len = tf.scalar(size[0]);
      const sum = tf.sum(imgTensor, 0).div(len);

      const minValue = tf.min(sum).dataSync()[0];
      const minThresh = minValue + correction;
      const threshTensor = tf.fill([sum.size], minThresh);
      const lowPoint = tf.less(sum, threshTensor);
      return [sum, lowPoint.dataSync()];
    });
    imgTensor.dispose();

    let checkStart = null;
    let checkLen = null;
    let cropPoint = [];

    for (let i = 0; i < lowPoint.length - 1; i++) {
      const isLow = lowPoint[i];
      if (isLow) {
        if (checkStart == null) checkStart = i;

        if (!lowPoint[i + 1]) {
          checkLen = i + 1 - checkStart;
          const minIdx = tf.tidy(() => {
            const checkSection = tf.slice(sum, [checkStart], [checkLen]);
            const minIdx = tf.argMin(checkSection).dataSync()[0] + checkStart;
            return minIdx;
          });
          cropPoint.push(minIdx);
          checkStart = null;
          checkLen = null;
        }
      }
    }
    sum.dispose();

    return cropPoint;
  }
}
