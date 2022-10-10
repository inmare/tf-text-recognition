import cv from "@techstark/opencv-js";
import * as tf from "@tensorflow/tfjs";

export default class ImgData {
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

  static getCropPoint(image, correction, mode) {
    const data = image.data;
    const size = [image.rows, image.cols];
    const imgTensor = tf.tensor(data, size);
    // horizontal sum
    const [sum, lowPoint] = tf.tidy(() => {
      let len;
      let sum;
      if (mode == "h") {
        len = tf.scalar(size[0]);
        sum = tf.sum(imgTensor, 0).div(len);
      } else if (mode == "v") {
        len = tf.scalar(size[1]);
        sum = tf.sum(imgTensor, 1).div(len);
      }

      const minValue = tf.min(sum).dataSync()[0];
      const minThresh = minValue + correction;
      const threshTensor = tf.fill([sum.size], minThresh);
      const lowPoint = tf.less(sum, threshTensor);

      tf.dispose([len, threshTensor]);
      return [sum, lowPoint.dataSync()];
    });
    imgTensor.dispose();

    let checkStart = null;
    let checkLen = null;
    let cropPoint = [];

    for (let i = 0; i < lowPoint.length; i++) {
      const isLow = lowPoint[i];
      if (isLow) {
        if (checkStart == null) checkStart = i;

        if (i == lowPoint.length - 1 || !lowPoint[i + 1]) {
          checkLen =
            i == lowPoint.length - 1 ? i - checkStart : i + 1 - checkStart;
          const minIdx = tf.tidy(() => {
            const checkSection = tf.slice(sum, [checkStart], [checkLen]);
            const minIdx = tf.argMin(checkSection).dataSync()[0] + checkStart;
            tf.dispose(checkSection);

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

  static getMaxSize(cropPoint) {
    const cropPointTensor = tf.tensor1d(cropPoint);
    const maxSize = tf.tidy(() => {
      const tensorSize = cropPointTensor.size - 1;
      const tensorA = tf.slice(cropPointTensor, [1], [tensorSize]);
      const tensorB = tf.slice(cropPointTensor, [0], [tensorSize]);
      const diff = tf.sub(tensorA, tensorB);
      const maxSize = tf.max(diff);
      tf.dispose([tensorSize, tensorA, tensorB, diff]);

      return maxSize.dataSync()[0];
    });
    cropPointTensor.dispose();

    return maxSize;
  }
}
