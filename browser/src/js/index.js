/* eslint-disable no-unused-vars */
// node_modules
import cv from "@techstark/opencv-js";
// custom modules
import Process from "./process.js";
import Setting from "./setting.js";
// css
import "../css/style.css";
// images
import textImg from "../image/sample-text.jpg";

const original = document.querySelector("#original-canvas");
const current = document.querySelector("#current-canvas");

cv.onRuntimeInitialized = main;

function main() {
  const imageElem = new Image();
  imageElem.src = textImg;
  imageElem.onload = processImage;
}

function processImage(e) {
  const imageElem = e.target;
  const image = cv.imread(imageElem);
  const grayImg = Process.gray(image);
  image.delete();
  const cropRect = Setting.crop;
  const cropImg = Process.crop(grayImg, cropRect);
  grayImg.delete();

  const binaryThresh = Setting.binaryThresh;
  const binaryImg = Process.binarization(cropImg, binaryThresh, true);
  cv.imshow(original, cropImg);
  cropImg.delete();
  cv.imshow(current, binaryImg);
  binaryImg.delete();
}
