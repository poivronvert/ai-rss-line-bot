// 將 Next.js 應用部署到 Firebase Cloud Functions 上，並且透過 HTTP 請求來運行
const { onRequest } = require('firebase-functions/v2/https'); //Firebase 提供的 HTTP 觸發器
const next = require('next');
const { setGlobalOptions } = require("firebase-functions/v2");

setGlobalOptions({ 
  region: "asia-east1", // 配置Cloud Functions伺服器區域運行
  memory: "1GB"
});


const app = next({
  dev: false,
  conf: { 
    distDir: '.next' // Next.js編譯後的輸出目錄，讓 Firebase Cloud Functions 能夠存取 Next.js 的完整應用功能
  }
});

//Next.js 應用的請求處理函數，所有進入的 HTTP 請求（包括 API 和頁面請求）都會由 handle 處理。
const handle = app.getRequestHandler(); 

//將 Next.js 應用程式部署成名為 nextServer 的 Firebase Function
exports.nextServer = onRequest(async (req, res) => { 
    try {
    await app.prepare(); //初始化 Next.js 應用程式
    return handle(req, res);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Internal Server Error');
  }
});
