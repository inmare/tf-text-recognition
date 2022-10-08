const Setting = {
  // 위쪽부터 시계방향으로 얼만큼 자르고 싶은지를 나타냄
  // 하지만 현재는 테스트용으로 임의로 숫자를 설정한 상태
  crop: [50, 400, 350, 300],
  binaryThresh: 100,
  dilationKernel: {
    rotate: [15, 10],
    findRect: [25, 10],
  },
  erosionKernel: {
    findRect: [15, 1],
  },
  angleThresh: 0.1,
  denoise: {
    kernelSize: 3,
    sigmaColor: 75,
    sigmaStrength: 75,
  },
  contrastAmount: 16,
  lowCorrection: 10,
  charImage: {
    width: 0,
    height: 0,
  },
};

export default Setting;
