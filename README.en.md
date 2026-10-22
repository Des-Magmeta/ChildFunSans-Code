# Child Fun Sans Code
A hybrid font mixed [Child Fun Sans](https://github.com/Des-Magmeta/ChildFunSans) and [Monaspace Krypton](https://github.com/githubnext/monaspace), with CJK ideographs and some symbol using Child Fun Sans, suitable for coding.

## Make and Adjustment
- Latin, Greek, Cyrillic (LGC) characters based on Monaspace Krypton:
  - Modified punctuations `‛` and `‟`;
  - Replaced some symbols (Circled numebrs, tabular symbols) using Child Fun Sans;
  - Completed glyphs & symbols used in Hanyu Pinyin, Pe̍h-ōe-jī (POJ), and Taiwanese Hokkien Romanization;
  - Added ligature character `U+FB00`ﬀ - `U+FB04`ﬄ;
  - Removed all symbols in Private Use Area except PowerLine symbols, superiors, and inferiors;
  - Removed fullwidth punctuation `｛` and `｝`.

- CJK ideographs and symbols based on Child Fun Sans:
  - Replaced fullwidth punctuation `｛`and`｝`, and completes fullwidth glyphs;
  - Removed feature `dlig` (Discretionary Ligatures) to show codes correctly in terminal and IDE;
  - Removed glyphs using Monaspace Krypton from feature `vert` (Vertical Forms), mainly for CJK.

- Added Standardized Variation Sequences (SVS) according to Unicode 16.0.

## Variation
### Before We Begin

Term           | Meaning                                                    |
--------------:|:-----------------------------------------------------------|
LGC            | Latin, Greek and Cyrillic letters (punctuations included). |
CJK Ideograph  | Including Hanzi (ZH), Kanji (JP) and Hanja (KR) (Hangul in Korea excluded). |
Halfwidth (HW) | The width that LGC letters and punctuations used in monospaced fonts. |
Fullwidth (FW) | The width that CJK Ideograph and symbols used in monospaced fonts. |
\- (Post Script)| In monospaced fonts, width of hangul is equal to CJK ideograph.    |

### Detail

Variation | Detail | Name |
----------|--------|------|
Halfwidth : Fullwidth = 1:2 | Width of 2 LGC characters is equal to that of 1 CJK ideograph. | `ChildFunSansCode-*W50.ttf` |
Halfwidth : Fullwidth = 3:5 | Width of 5 LGC characters is equal to that of 3 CJK ideographs, using original width in Monaspace Krypton. | `ChildFunSansCode-*W60.ttf` |
Simplified Chinese (SC) | Use Child Fun Sans **SC** to show ideograph, mainly for China Mainland users. | `ChildFunSansCode-SC*.ttf`
Traditional Chinese (TC) | Use Child Fun Sans **TC** to show ideograph, suitable for TW/HK/MO users. | `ChildFunSansCode-TC*.ttf`

> For Japanese users, it's suitable to use [Moralerspace](https://github.com/yuru7/moralerspace) Krypton, mixed Monaspace Krypton and Stick.

## How to Get Fonts
Download `.ttf` files in release and install it/them.

## Notes
- In some IDE, they only show English name `Child Fun Sans Code SC/TC W50/W60`.  
- There may be something wrong with `W60` Variation (HW ∶ FW = 3:5), especially both appears CJK and LGC in texts.
  - Not consistent widths with 3:5;  
  - Not recognized as monospaced fonts in terminals or IDEs.

## Build
Tools and Runtime to build:
- Fontforge `20230101` [Windows](https://fontforge.org/en-US/downloads/windows/) | [Linux](https://fontforge.org/en-US/downloads/gnulinux/)
- Python: `>=3.8`

### Windows (PowerShell)
```
# Install required tools
pip install -r requirements.txt
# Build Fonts
& "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" .\fontforge_script.py && python fonttools_script.py
```

<!-- 

### Linux
```
docker build -t font/ChildFunSans-Code .
docker run -it --rm -v $PWD:/workspace font/ChildFunSans-Code:latest
```

-->

## Authorization
Child Fun Sans code is derived from [Moralerspace](https://github.com/yuru7/moralerspace), which is licensed under the SIL Open Font License 1.1.

### License

- Free use, including commercial use, without payment, notification, or identification of the original author.
- Share font files freely and install them on any software or device.
- On this basis, the work shall be modified or re-created. The second modified version shall also be published in [SIL Open Font Licenses 1.1](https://scripts.sil.org/OFL).

### Limit

- When making a derived font, the font name cannot use the “reserved name” of the original font.
- The reserved name “<span lang="zh-cn">游趣体 Code</span>”, “<span lang="zh-tw">遊趣體 Code</span>”, and “Child Fun Sans Code” shall not be used for the second modified work. Without modifying the font source code, the recompiled font can continue to use its reserved name.
  
- According to the provisions of Article 1 in the license and terms of [SIL Open Font License 1.1](https://scripts.sil.org/OFL), **Selling this font by itself is banned.**
- This font can't be distributed in a license other than the [SIL Open Font License 1.1](https://scripts.sil.org/OFL).

## Reference  
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
