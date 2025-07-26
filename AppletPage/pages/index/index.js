Page({
  data: {
    inputValue: '',  // 用户输入的文字
    translatedText: ''  // 翻译后的盲文
  },

  // 监听输入框输入
  onInput: function (e) {
    const value = e.detail.value;
    if (/[a-zA-Z]/.test(value)) {
      wx.showToast({
        title: '目前不支持英文，请重新输入',
        icon: 'none',
        duration: 2000
      });
      this.setData({ inputValue: '', translatedText: '' });  // 清空输入框和翻译结果
    } else {
      this.setData({ inputValue: value });
    }
  },
  // 跳转到拍照翻译页面
  goToCamera() {
    wx.navigateTo({
      url: '/pages/camera/camera'
    });
  },
  // 发送请求到后端进行盲文翻译
  translateText: function () {
    const that = this;
    if (!this.data.inputValue.trim()) {
      wx.showToast({
        title: '请输入文字',
        icon: 'none'
      });
      return;
    }
    
    wx.request({
      url: '/translate', // 确保使用 ngrok 地址
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      data: { text: this.data.inputValue }, // 确保数据格式正确
      success(res) {
        console.log('翻译成功:', res.data);
        if (res.data.braille) {
          that.setData({ translatedText: res.data.braille }); // 确保变量名和 wxml 绑定一致
        } else {
          wx.showToast({ title: '翻译结果为空', icon: 'none' });
        }
      },
      fail(err) {
        console.error('请求失败:', err);
        wx.showToast({
          title: '翻译失败，请检查网络',
          icon: 'none'
        });
      }
    });
  }
});

