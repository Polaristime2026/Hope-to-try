Page({
  data: {
    scanning: false,
    photoPath: '',
    photoTaken: false,
    timedOut: false // 是否超时标记
  },

  goBack() {
    wx.navigateBack();
  },
  retakePhoto() {
    this.setData({
      photoTaken: false,
      photoPath: '',
      scanning: false,
      timedOut: false
    });
  },
  
  confirmPhoto() {
    const path = this.data.photoPath;
    const that = this;
  
    this.setData({ scanning: true });
  
    setTimeout(() => {
      if (!that.data.timedOut) {
        that.uploadWithTimeout(path, 2500);
      }
    }, 2500);
  }
  ,
  takePhoto() {
    // 防止用户扫描中点击拍照按钮
    if (this.data.scanning) {
      console.log('[拍照中...] 禁止重复点击');
      return;
    }

    const ctx = wx.createCameraContext();
    const that = this;

    ctx.takePhoto({
      quality: 'high',
      success(res) {
        const path = res.tempImagePath;

        // 锁图 & 启动扫描
        that.setData({
          photoPath: path,
          photoTaken: true,
          timedOut: false
        });

      }
    });
  },

  uploadWithTimeout(filePath, timeout = 2500) {
    const that = this;

    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('timeout')), timeout);
    });

    const uploadPromise = new Promise((resolve, reject) => {
      wx.uploadFile({
        url: 'https://example.com/ocr',
        filePath,
        name: 'file',
        success(res) {
          try {
            const result = JSON.parse(res.data || '{}');
            resolve(result);
          } catch (e) {
            reject(e);
          }
        },
        fail(err) {
          reject(err);
        }
      });
    });

    Promise.race([uploadPromise, timeoutPromise])
      .then(result => {
        that.setData({ scanning: false });
        if (result.text) {
          wx.navigateTo({
            url: `/pages/result/result?text=${encodeURIComponent(result.text)}`
          });
        } else {
          wx.showToast({ title: '识别失败', icon: 'none' });
        }
      })
      .catch(err => {
        that.setData({
          scanning: false,
          timedOut: true, // 标记为已超时
          photoTaken: false, //  解锁图像，允许重新拍
          photoPath: ''      // 可选：清空图像路径
        });

        if (err.message === 'timeout') {
          wx.showToast({ title: '网络超时，请重试', icon: 'none' });
        } else {
          wx.showToast({ title: '识别失败', icon: 'none' });
        }

        console.error('[上传错误]', err);
      });
  }
});
