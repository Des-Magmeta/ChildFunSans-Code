<span lang="zh-hant">

# 遊趣體 Code | Child Fun Sans Code
「遊趣體」與 Monaspace Krypton 的合併字型，可用於程式設計用途。

## 字型簡介
本字型是「[遊趣體](https://github.com/Des-Magmeta/ChildFunSans)」和 [Moralerspace](https://github.com/yuru7/moralerspace) 的合併字型，將漢字、部分符號部分更換為「遊趣體」並作出其他調整，可作為「遊趣體」用於程式設計用途的等寬版本。

## 製作與調整
- 西文部分在 Monaspace Krypton 基礎上調整：
  - 修改`‛`、`‟`等標點符號，使字形與其他字元風格設計一致；
  - 將部分與西文同寬的字元（如帶圈數位序號、定位字元）替換作「遊趣體」樣式；
  - 補全漢語拼音、台羅拼音、白話字等相關字元及其所需組合變音符號；
  - 增加連字字元 `U+FB00`「ﬀ」-`U+FB04`「ﬄ」；
  - 移除私用區 Powerline 和上下標外的所有符號；
  - 移除原有全寬標點`｛`、`｝`。

- 漢字、符號部分在「遊趣體」基礎上調整：
  - 將全形標點`｛`、`｝`替換為「遊趣體 TC」，並補充部分全寬字元；
  - 移除 `dlig`「自由連字」特性，防止部分終端／IDE 下字形無法正確顯示；
  - 將使用 Monaspace Krypton 的字元移出 `vert` 特性。

- 根據 Unicode 16.0 標準化變體序列（Standardized Variation Sequences, SVS），新增彎引號 `“‘’”` `“︁‘︁’︁”︁` 寬度選擇。

## 變體版本

種類 | 說明 | 命名方式 |
-----|------|----------|
半形∶全形 = 1:2 | 2 個半形字元與 1 個全形字符寬度相等的版本。如果您希望以 2 倍寬度顯示半形和全形字符，請選用此版本。 | `ChildFunSansCode-*W50.ttf` |
半形∶全形 = 3:5 | 5 個半形字元與 3 個全形字符寬度相等的版本。由於半形英数以原始寬度顯示，因此易於閱讀。 | `ChildFunSansCode-*W60.ttf` |
簡體版 | 漢字部分採用「遊趣體」簡體版字形，適合簡體中文使用者使用。 | `ChildFunSansCode-SC*.ttf`
繁體版 | 漢字部分採用「遊趣體 TC」字形，適合繁體中文使用者使用。 | `ChildFunSansCode-TC*.ttf`

## 獲取字型
請從發佈（Release）頁面下載 `.ttf` 檔，並按照各作業系統的方法進行安裝。

## 注意事項
- 部分環境中可能會顯示英文名稱 Child Fun Sans Code SC/TC W50/W60，敬請留意；  
- 由於技術原因，`W60`版本（半形∶全形 = 3:5）可能出現以下問題之一，敬請留意：
  - 在部分終端下的顯示寬度可能出現異常；  
  - 寬度無異常，但可能無法被正確識別為等寬字型，如將 PANOSE 強制設定為 `9` Monospaced，將出現上一條問題；
- 本字型有部分排版特性缺失，如介意，請移步[此處](https://github.com/Des-Magmeta/ChildFunSans-TC)使用完整版。

## 構建
用於構建的工具和運行環境：
- Fontforge `20230101` [Windows](https://fontforge.org/en-US/downloads/windows/) | [Linux](https://fontforge.org/en-US/downloads/gnulinux/)
- Python: `>=3.8`

### Windows (PowerShell)
```
# 安裝必要檔
pip install -r requirements.txt
# 構建字型
& "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" .\fontforge_script.py && python fonttools_script.py
```

<!-- 

### Linux
```
docker build -t font/ChildFunSans-Code .
docker run -it --rm -v $PWD:/workspace font/ChildFunSans-Code:latest
```

-->

## 授權資訊 
 本字型是基於 SIL Open Font License 1.1 改造的 FONTWORKS 開發並發佈的 [Stick](https://github.com/fontworks-fonts/Stick) 開源項目。
 
 ### 許可 
  - 這款字型無論是個人還是企業都可以自由商用，無需付費，也無需知會或者標明原作者； 
  - 這款字型可以自由傳播、分享，或者將字型安裝於系統、軟體或APP中也是允許的，可以與任何軟體捆綁再分發以及／或一併銷售； 
  - 這款字型可以自由修改、改造，製作衍生字型。修改或改造後的字型也必須同樣以 [SIL OFL 1.1](https://openfontlicense.org) 公開。 
 ### 限制 
  - 在製作衍生字型時，字型名稱不可使用原有字型的「保留名稱」。本字型保留名稱「<span lang="zh-hans">游趣体 Code</span>」「遊趣體 Code」「Child Fun Sans Code」，基於本字型二次衍生的字型，名稱不可出現「<span lang="zh-hans">游趣体 Code</span>」「遊趣體 Code」「Child Fun Sans Code」字樣；而在沒有對字型原始程式碼進行修改的情況下，重新編譯出來的字型，可以繼續使用本字型的保留名稱。 
  - 根據 [SIL Open Font License 1.1](https://openfontlicense.org)「許可與條件」中第 1 條的規定， **禁止單獨出售字型檔(OTF/TTF檔)的行為。** 
  - 該字型不可在 [SIL Open Font License 1.1](https://openfontlicense.org) 以外的授權許可下發行。

## 參考資料  
  - [Stick](https://github.com/fontworks-fonts/Stick) by [FONTWORKS K.K.](ttps://github.com/fontworks-fonts/)  
  - [Moralerspace](https://github.com/yuru7/moralerspace)  
  - [Monaspace](https://github.com/githubnext/monaspace)  
  - [Child Fun Sans](https://github.com/Des-Magmeta/ChildFunSans)

## Star History

<a href="https://www.star-history.com/?repos=Des%2DMagmeta%2FChildFunSans&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans&type=date&legend=top-left" />
 </picture>
</a>

</span>
