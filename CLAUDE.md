# DxSxT Network — 投資者簡報網頁（Claude Code 專案說明）

呢個 repo 係 **DxSxT Network**（正式名稱 De Stijl Technology Network International）嘅
單頁投資者簡報網站：一個 RWA（Real World Assets）× GameFi 項目，基於原始 PDF pitch deck
改造成網頁版。呢份文件係俾 Claude Code（或者任何接手嘅開發者/AI）快速理解項目結構同
編輯規則用嘅。

## 專案結構

```
.
├── src/
│   └── index_template.html   ← 源文件，帶 __TOKEN__ placeholder，呢個先係應該編輯嘅文件
├── assets/                   ← 所有圖片素材（jpg/png），build.py 會讀呢度嘅圖做 base64 內嵌
│   ├── hero.jpg / roadmap.jpg          （原 PDF 抽出嘅 AI 渲染圖）
│   ├── pillar.jpg / bank.jpg / engine.jpg / contract.jpg   （之後生成補充嘅機制配圖）
│   ├── logo/mark_crop.png / logo/wordmark_white_crop.png   （官方 logo，已去透明邊）
│   ├── logo/destijl_logo.png / destijl_mark.png   （De Stijl「形品科技」官方 logo 原圖，
│   │                           同由佢自動裁出嘅左邊幾何 mark；mark 係 render_icons.py 生成）
│   └── icons/                （web app icon：favicon、apple-touch-icon 180、192/512、maskable，白底；
│                               由 tools/render_icons.py 用 destijl_logo.png 裁出嘅 mark 渲染，
│                               唔用「de stijl」字同「形品科技」；build.py 淨係複製 png/ico）
├── tools/
│   └── render_icons.py       ← 重新生成 assets/icons（需要 Pillow；build.py 本身唔需要）
├── build.py                  ← 建置腳本：讀 src/ + assets/，輸出 dist/index.html + icons/ + manifest.json
├── dist/
│   ├── index.html            ← 建置產出，呢個先係最終部署/發布嘅檔案，唔好手動改
│   ├── icons/                ← 由 assets/icons 複製
│   └── manifest.json      ← build.py 生成（PWA manifest，主畫面 icon / 名稱 / 主題色）
└── docs/
    └── video-storyboard.md   ← 120秒宣傳片分鏡腳本（另一份周邊產出，唔屬於網頁本身）
```

**編輯流程：只改 `src/index_template.html`，然後跑 `python3 build.py` 重新生成
`dist/index.html`。千祈唔好直接改 `dist/index.html`——下次 build 會覆蓋晒。**

## 建置

```bash
python3 build.py
```

冇任何第三方 dependency，淨係用 Python 標準庫（`base64`、`pathlib`）。跑完會喺
`dist/index.html` 生成一個完全 self-contained 嘅 HTML（所有圖片已經 base64 內嵌，
唔需要額外靜態資源），可以直接開喺瀏覽器，或者部署去任何靜態網站託管（GitHub Pages、
Netlify、Vercel 等等）。

`src/index_template.html` 本身係一個冇 `<html>/<head>/<body>` 嘅 fragment；`build.py`
會將佢包成完整文件，並加上 `<html lang="zh-Hans" translate="no">`、charset、viewport
同 `notranslate` meta。**呢層 wrapper 唔可以刪**：之前部署去 Render 時因為冇 `lang`
宣告，iOS Safari 自動將簡體翻譯成繁體，出現「間歇調用引擎」「慷慨 × 商人 × 玩家」呢類
亂譯（2026-09-03 用戶截圖反映）。如果用戶再報告網頁文案「變咗」但 repo 入面係啱嘅，
先檢查係咪瀏覽器翻譯功能所致。

## 部署

而家實際上線嘅網址係 **https://dxsxt-intro.onrender.com**（Render 靜態網站，伺服
`dist/index.html`）。push 去 GitHub `main` 後 Render 會重新部署；Cloudflare 有 5 分鐘
cache（`s-maxage=300`），改完可能要等幾分鐘先見到。

## 呢個網頁嘅背景

- 呢份簡報係俾投資者睇嘅募資材料，唔係一般 marketing landing page，所以文案風格要
  「專業直接、去 AI 腔」，但**唔可以變得太口語化／隨便**（呢一點喺項目過程入面同用戶
  確認過：「去 AI 腔，但保持專業」）。
- 視覺風格：深色主題（無 light mode，設計上刻意 commit 單一深色視覺），深藍太空感 +
  AI 渲染建築/城市 + 深色數據圖表。分類色板（RWA=藍 `#4f8dff`、資本=金
  `#bf8016`/`#e3ac35`、GameFi=綠 `#1fae82`）經過 colorblind-safe 驗證，改色板前請重新
  跑驗證（詳見 `dataviz` skill 嘅 `validate_palette.js`，如果冇裝呢個 skill 就用其他
  contrast checker 驗證代替）。
- 字體：Unbounded（display）、Noto Sans TC（中英文內文）、IBM Plex Mono（數據/圖表）。

## 內容編輯規則（已經同用戶確認落嚟嘅規矩，改文案前一定要留意）

1. **項目名一律「DxSxT Network」**，唔可以寫做「DxST」（呢個係之前改漏過嘅錯字，成個
   repo 搜索一次「DxST」確保冇漏網之魚）。
2. **「國債」唔好寫做「美國國債」**——除咗 Market Opportunity 嗰兩個引用第三方數據嘅
   stat tile（「代幣化美國國債產品總值增長 +380%」、「代幣化美國國債平均年化回報
   4.14%」）本身就係精確引述第三方統計，呢兩處要保留「美國」。其他所有 DxSxT 自己嘅
   敘述文字一律淨係講「國債」。
3. **文案唔用 AI 腔/大廠黑話**：不僅、更是、正如、毋庸置疑、值得一提、深入探討、完美
   融合、維度、矩陣、賦能、破圈、下半場、閉環，呢啲詞一律唔用；亦都唔用浮誇讚美詞
   （「饕餮盛宴」、「震撼來襲」之類）。但**唔好行去另一個極端變成口語化大白話**（唔用
   啦/嘛/哈呢類語氣詞），要維持專業投資簡報嘅語域。
4. **唔可以出現未經證實嘅回報數字承諾**（例如帶暗示性嘅「~500%回報」）。代幣解鎖時間
   表（vesting schedule）只可以描述做「紀律性、漸進式釋放」機制，唔可以暗示係回報保
   證。所有市場數據／回報相關文字，如果引用第三方研究（BCG、渣打銀行、BlackRock、FMI
   等），要清楚標明「呢個係第三方預測，唔代表 DxSxT Network 自己嘅預期表現或回報保
   證」——網頁 Market Opportunity 同 Ask 章節已經有呢類免責聲明，加新數據時要跟返呢個
   格式。
5. 風險聲明入面嘅中英文措辭要保持對齊（例如而家中文淨係講「風險」、英文都對應淨係講
   "risk"，冇加強度形容詞如「重大/高度/significant」——如果之後要改風險聲明嘅語氣，
   記得中英文一齊改，唔好淨改一邊）。
6. 網頁已經移除咗原本 PDF 入面嘅 Team 同 CTA/Contact 兩個章節（用戶明確話唔要），
   如果要加返，需要用戶重新確認先好加。

## Artifact 發布（呢個 repo 之外嘅發布流程）

呢個網頁除咗可以部署做靜態網站，之前一直都係透過 Claude 嘅 Artifact 工具發布緊喺
`https://claude.ai/code/artifact/123bb26c-89b2-45a5-a615-a8414c86b737`（呢個 URL 淨係
喺果邊 Claude 對話入面先用得到，同呢個 GitHub repo 係兩條獨立線——呢度淨係做代碼/版本
管理用）。如果之後想繼續用 Claude 嗰邊嘅 Artifact 流程同步更新，記得對應嘅 build 產出
（`dist/index.html`）內容要一致。

## 其他文件

- `docs/video-storyboard.md`：120 秒宣傳片分鏡腳本（10 個鏡頭，投資者 Pitch 式敘事，
  每鏡有 image/video prompt，其中鏡頭 1/4/8/10 有虛擬主持人出鏡），同網頁本身內容
  相關但係獨立產出，唔會被 `build.py` 用到。
