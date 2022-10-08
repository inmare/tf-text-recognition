/* eslint-disable no-unused-vars */
// node_modules
import cv from "@techstark/opencv-js";
// custom modules
import Extract from "./extract.js";
import Data from "./data.js";
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
  const rotateImg = Extract.setImageRotation(e.target);
  const textbox = Extract.getTextbox(rotateImg);
  const clearTextbox = Extract.enhanceTextbox(textbox);
  textbox.delete();

  Data.getCharPoint(clearTextbox);

  cv.imshow(original, rotateImg);
  cv.imshow(current, clearTextbox);
  rotateImg.delete();
  clearTextbox.delete();
}
