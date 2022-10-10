import cv from "@techstark/opencv-js";
import ImgProcess from "./image_process.js";
import Setting from "./setting.js";
import ImgData from "./image_data.js";

// 상황에 따라서 이미지를 삭제하거나 유지해야 하는 상황이 발생했고,
// 그에 따라 일괄적인 이미지 삭제가 어려운 상황임.
// 따라서 이미지를 반환하면 그 이미지를 동일한 함수내에서 삭제하는 방법 사용
export default class Extract {
  static setImageRotation(imageElem) {
    const image = cv.imread(imageElem);
    const grayImg = ImgProcess.gray(image);
    image.delete();
    const cropRect = Setting.crop;
    const cropImg = ImgProcess.crop(grayImg, cropRect);
    grayImg.delete();
    const binaryThresh = Setting.binaryThresh;
    const binaryImg = ImgProcess.binarize(cropImg, binaryThresh, true);
    const rotationKernel = Setting.dilationKernel.rotate;
    const dilateImg = ImgProcess.dilate(binaryImg, rotationKernel);
    binaryImg.delete();

    const mainContour = ImgData.getMainContour(dilateImg);
    dilateImg.delete();
    const [center, angle] = ImgData.getRotationInfo(mainContour);
    mainContour.delete();

    const rotateImg = ImgProcess.rotate(cropImg, center, -angle);
    cropImg.delete();
    return rotateImg;
  }

  static getTextbox(image) {
    const binaryThresh = Setting.binaryThresh;
    const binaryImg = ImgProcess.binarize(image, binaryThresh, true);
    const dilationKernel = Setting.dilationKernel.findRect;
    const dilateImg = ImgProcess.dilate(binaryImg, dilationKernel);
    binaryImg.delete();
    const erosionKernel = Setting.erosionKernel.findRect;
    const erodeImg = ImgProcess.erode(dilateImg, erosionKernel);
    dilateImg.delete();

    const mainContour = ImgData.getMainContour(erodeImg);
    erodeImg.delete();

    const rect = ImgData.getRectPoint(mainContour);
    mainContour.delete();

    const textbox = image.roi(rect);

    return textbox;
  }

  static enhanceTextbox(image) {
    const invertImg = ImgProcess.invert(image);
    const kernelSize = Setting.denoise.kernelSize;
    const sigmaColor = Setting.denoise.sigmaColor;
    const sigmaStrength = Setting.denoise.sigmaStrength;
    const denoiseImg = ImgProcess.denoise(
      invertImg,
      kernelSize,
      sigmaColor,
      sigmaStrength
    );
    invertImg.delete();
    const amount = Setting.contrastAmount;
    const contrastImg = ImgProcess.contrast(denoiseImg, amount);
    denoiseImg.delete();

    return contrastImg;
  }

  static getCharInfo(image) {
    const correction = Setting.lowCorrection;
    const cropPointH = ImgData.getCropPoint(image, correction, "h");
    const maxWidth = ImgData.getMaxSize(cropPointH);
    const cropPointV = ImgData.getCropPoint(image, correction, "v");
    const maxHeight = ImgData.getMaxSize(cropPointV);

    const charInfo = {
      cropPointH: cropPointH,
      cropPointV: cropPointV,
      maxSize: {
        width: maxWidth,
        height: maxHeight,
      },
    };

    return charInfo;
  }
}
