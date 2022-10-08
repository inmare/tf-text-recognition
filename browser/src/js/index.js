/* eslint-disable no-unused-vars */
// node_modules
import cv, { rotate } from "@techstark/opencv-js";
// custom modules
import Extract from "./extract.js";
// css
import "../css/style.css";
// images
import textImg from "../image/sample-text.jpg";
import randomAsciiImg from "../image/random-ascii.jpg";

const original = document.querySelector("#original-canvas");
const current = document.querySelector("#current-canvas");

cv.onRuntimeInitialized = main;

function main() {
  const imageElem = new Image();
  imageElem.src = randomAsciiImg;
  imageElem.onload = processImage;
}

function processImage(e) {
  const rotateImg = Extract.setImageRotation(e.target);
  const textbox = Extract.getTextbox(rotateImg);
  // rotateImg.delete();
  const clearTextbox = Extract.enhanceTextbox(textbox);
  textbox.delete();

  const charInfo = Extract.getCharInfo(clearTextbox);
  console.log(charInfo);

  // cv.imshow(original, rotateImg);
  cv.imshow(current, rotateImg);
  // rotateImg.delete();
  rotateImg.delete();
  clearTextbox.delete();
}
