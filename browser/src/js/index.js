/* eslint-disable no-unused-vars */
// node_modules
import cv from "@techstark/opencv-js";
// custom modules
import DataProcess from "./data_process.js";
import Extract from "./extract.js";
import Model from "./model.js";
import RandomArray from "./seed_random.js";
// css
import "../css/index.css";
// images
// import textImg from "../image/sample-text.jpg";
import randomAsciiImg from "../image/random-ascii.jpg";

const original = document.querySelector("#original-canvas");
const current = document.querySelector("#current-canvas");

cv.onRuntimeInitialized = main;

function main() {
  const imageElem = new Image();
  imageElem.src = randomAsciiImg;
  imageElem.onload = processImage;
}

async function processImage(e) {
  const rotateImg = Extract.setImageRotation(e.target);
  const textbox = Extract.getTextbox(rotateImg);
  rotateImg.delete();
  const clearTextbox = Extract.enhanceTextbox(textbox);
  textbox.delete();

  const charInfo = Extract.getCharInfo(clearTextbox);
  // 나중에 다른 함수로 분리해서 작성하기
  const imageData = await DataProcess.convertImageToTensor(
    clearTextbox,
    charInfo
  );
  const dataLength = imageData.shape[0];
  const asciiArray = RandomArray.makeArray("ascii");
  const classLength = asciiArray.length;
  const labels = RandomArray.getRandomArray(asciiArray, dataLength);
  const oneHotLabels = await DataProcess.convertLabelToOneHot(
    labels,
    classLength
  );

  Model.ml(imageData, oneHotLabels, charInfo.maxSize, asciiArray);
}
