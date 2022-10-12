class SeedRandom {
  constructor() {
    this.seed = 1;
  }

  random() {
    // 난수 생성 알고리즘
    // 출처 : https://blog.naver.com/pmw9440/221877712774
    this.seed = (1013904223 + 1664525 * this.seed) % 4294967296;
    return this.seed / 4294967296;
  }

  choice(array) {
    const idx = Math.round(this.random() * array.length - 0.5);
    return array[idx];
  }
}

export default class RandomArray {
  static makeArray(mode) {
    let array = [];
    if (mode == "ascii") {
      for (let i = 0x21; i < 0x7f; i++) {
        array.push(i - 0x21);
      }
    }
    return array;
  }

  static getRandomArray(array, length) {
    let randomArray = [];
    const seedRandom = new SeedRandom();
    seedRandom.random();
    for (let i = 0; i < length; i++) {
      const item = seedRandom.choice(array);
      randomArray.push(item);
    }

    return randomArray;
  }
}
