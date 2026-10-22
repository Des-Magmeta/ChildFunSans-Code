<div align="center">
 
<span lang="zh-hans">简体中文</span> | <span lang="zh-hant">[繁體中文](README.zh-hant.md)</span>
</div>

# 游趣体 Code | Child Fun Sans Code
「游趣体」与 Monaspace Krypton 的合并字体，可用于编程用途。

## 字体简介
本字体是「[游趣体](https://github.com/Des-Magmeta/ChildFunSans)」和 [Monaspace Krypton](https://github.com/githubnext/monaspace) 的合并字体，将汉字、部分符号部分更换为「游趣体」并作出其他调整，可作为「游趣体」用于编程用途的等宽版本。

## 制作与调整
- 西文部分在 Monaspace Krypton 基础上调整：
  - 修改`‛`、`‟`等标点符号，使字形与其他字符风格设计一致；
  - 将部分与西文同宽的字符（如带圈数字序号、制表符）替换作「游趣体」样式；
  - 补全汉语拼音、台罗拼音、白话字等相关字符及其所需组合变音符号；
  - 增加连字字符 `U+FB00`「ﬀ」-`U+FB04`「ﬄ」；
  - 移除私用区 Powerline 和上下标外的所有符号；
  - 移除原有全宽标点`｛`、`｝`。

- 汉字、符号部分在「游趣体」基础上调整：
  - 将全宽标点`｛`、`｝`替换为「游趣体」，并补充部分全宽字符；
  - 移除 `dlig`「自由连字」特性，防止部分终端／IDE 下字形无法正确显示；
  - 将使用 Monaspace Krypton 的字符移出 `vert` 特性。

- 根据 Unicode 16.0 标准化变体序列（Standardized Variation Sequences, SVS），新增弯引号 `“‘’”` `“︁‘︁’︁”︁` 宽度选择。

## 变体版本

种类 | 说明 | 命名方式 |
-----|------|----------|
半角∶全角 = 1:2 | 2 个半角字符与 1 个全角字符宽度相等的版本。如果您希望以 2 倍宽度显示半角和全角字符，请选用此版本。 | `ChildFunSansCode-*W50.ttf` |
半角∶全角 = 3:5 | 5 个半角字符与 3 个全角字符宽度相等的版本。由于半角字母数字以原始宽度显示，因此易于阅读。 | `ChildFunSansCode-*W60.ttf` |
简体版 | 汉字部分采用「游趣体」简体版字形，适合简体中文用户使用。 | `ChildFunSansCode-SC*.ttf`
繁体版 | 汉字部分采用「游趣体 TC」字形，适合繁体中文用户使用。 | `ChildFunSansCode-TC*.ttf`

## 获取字体
请从发布（Release）页面下载 `.ttf` 文件，并按照各操作系统的方法进行安装。

## 注意事项
- 部分环境中可能会显示英文名称 Child Fun Sans Code SC/TC W50/W60，敬请留意；  
- 由于技术原因，`W60`版本（半角∶全角 = 3:5）可能出现以下问题之一，敬请留意：
  - 在部分终端下的显示宽度可能出现异常；  
  - 宽度无异常，但可能无法被正确识别为等宽字体，如将 PANOSE 强制设定为 `9` Monospaced，将出现上一条问题；
- 本字体有部分排版特性缺失，如介意，请移步[此处](https://github.com/Des-Magmeta/ChildFunSans)使用完整版。

## 构建
用于构建的工具和运行环境：
- Fontforge `20230101` [Windows](https://fontforge.org/en-US/downloads/windows/) | [Linux](https://fontforge.org/en-US/downloads/gnulinux/)
- Python: `>=3.8`

### Windows (PowerShell)
```
# 安装必要文件
pip install -r requirements.txt
# 构建字体
& "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" .\fontforge_script.py && python fonttools_script.py
```

<!-- 
### Linux
```
docker build -t font/ChildFunSans-Code .
docker run -it --rm -v $PWD:/workspace font/ChildFunSans-Code:latest
```
-->

## 授权信息 
 本字体是基于 SIL Open Font License 1.1 改造的 FONTWORKS 开发并发布的 [Stick](https://github.com/fontworks-fonts/Stick) 开源项目。
 
 ### 许可 
  - 这款字体无论是个人还是企业都可以自由商用，无需付费，也无需知会或者标明原作者； 
  - 这款字体可以自由传播、分享，或者将字体安装于系统、软件或APP中也是允许的，可以与任何软件捆绑再分发以及／或一并销售； 
  - 这款字体可以自由修改、改造，制作衍生字体。修改或改造后的字体也必须同样以 [SIL OFL 1.1](https://openfontlicense.org) 公开。 
 ### 限制 
  - 在制作衍生字体时，字体名称不可使用原有字体的「保留名称」。本字体保留名称「游趣体 Code」「遊趣體 Code」「Child Fun Sans Code」，基于本字体二次衍生的字体，名称不可出现「游趣体 Code」「遊趣體 Code」「Child Fun Sans Code」字样；而在没有对字体源代码进行修改的情况下，重新编译出来的字体，可以继续使用本字体的保留名称。 
  - 根据 [SIL Open Font License 1.1](https://openfontlicense.org)「许可与条件」中第 1 条的规定， **禁止单独出售字体文件(OTF/TTF文件)的行为。** 
  - 该字体不可在 [SIL Open Font License 1.1](https://openfontlicense.org) 以外的授权许可下发行。

## 参考资料  
  - [Stick](https://github.com/fontworks-fonts/Stick) by [FONTWORKS K.K.](ttps://github.com/fontworks-fonts/)  
  - [Moralerspace](https://github.com/yuru7/moralerspace)  
  - [Monaspace](https://github.com/githubnext/monaspace)  
  - [Child Fun Sans](https://github.com/Des-Magmeta/ChildFunSans)

## Star History

<a href="https://www.star-history.com/?repos=Des%2DMagmeta%2FChildFunSans%2DCode&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans%2DCode&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans%2DCode&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Des%2DMagmeta/ChildFunSans%2DCode&type=date&legend=top-left" />
 </picture>
</a>
