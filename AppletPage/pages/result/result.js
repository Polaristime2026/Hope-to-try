Page({
  data: {
    resultText: ''
  },
  onLoad(options) {
    this.setData({
      resultText: decodeURIComponent(options.text || '')
    });
  }
});
