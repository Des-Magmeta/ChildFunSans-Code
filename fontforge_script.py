#!fontforge --lang=py -script
# 将中英字体合成一个字体

import configparser
import math
import os
import shutil
import sys
import uuid
from decimal import ROUND_HALF_UP, Decimal

import fontforge
import psMat

# 读取 ini 文件
settings = configparser.ConfigParser()
settings.read("build.ini", encoding="utf-8")

VERSION = settings.get("DEFAULT", "VERSION")
FONT_NAME = settings.get("DEFAULT", "FONT_NAME")
SUFFIX = settings.get("DEFAULT", "SUFFIX")
SUFFIX_TC = settings.get("DEFAULT", "SUFFIX_TC")
SUFFIX_TC_ALT = settings.get("DEFAULT", "SUFFIX_TC_ALT")
CH_FONT = settings.get("DEFAULT", "CH_FONT")
CH_FONT_TC = settings.get("DEFAULT", "CH_FONT_TC")
CH_FONT_TC_ALT = settings.get("DEFAULT", "CH_FONT_TC_ALT")
ENG_FONT = settings.get("DEFAULT", "ENG_FONT")
SOURCE_FONTS_DIR = settings.get("DEFAULT", "SOURCE_FONTS_DIR")
BUILD_FONTS_DIR = settings.get("DEFAULT", "BUILD_FONTS_DIR")
VENDER_NAME = settings.get("DEFAULT", "VENDER_NAME")
FONTFORGE_PREFIX = settings.get("DEFAULT", "FONTFORGE_PREFIX")
IDEOGRAPHIC_SPACE = settings.get("DEFAULT", "IDEOGRAPHIC_SPACE")
HALF_WIDTH_STR = settings.get("DEFAULT", "HALF_WIDTH_STR")
VISIBLE_FULLWIDTH_SPACE_STR = settings.get("DEFAULT", "VISIBLE_FULLWIDTH_SPACE_STR")
CHDOC_STR = settings.get("DEFAULT", "CHDOC_STR")
EM_ASCENT = int(settings.get("DEFAULT", "EM_ASCENT"))
EM_DESCENT = int(settings.get("DEFAULT", "EM_DESCENT"))
OS2_ASCENT = int(settings.get("DEFAULT", "OS2_ASCENT"))
OS2_DESCENT = int(settings.get("DEFAULT", "OS2_DESCENT"))
HALF_WIDTH_12 = int(settings.get("DEFAULT", "HALF_WIDTH_12"))
FULL_WIDTH_35 = int(settings.get("DEFAULT", "FULL_WIDTH_35"))

COPYRIGHT = """[Monaspace]
Copyright (c) 2023, GitHub https://github.com/githubnext/monaspace

[Child Fun Sans]
Copyright 2023-2026 Des-Magmeta (https://github.com/Des-Magmeta/ChildFunSans)

[Child Fun Sans Code]
Copyright 2023-2026 Des-Magmeta
"""

options = {}

def main():
    # 判断选项
    get_options()
    if options.get("unknown-option"):
        usage()
        return

    # 创建 build 目录
    if os.path.exists(BUILD_FONTS_DIR) and not options.get("do-not-delete-build-dir"):
        shutil.rmtree(BUILD_FONTS_DIR)
        os.mkdir(BUILD_FONTS_DIR)
    if not os.path.exists(BUILD_FONTS_DIR):
        os.mkdir(BUILD_FONTS_DIR)

    generate_SC()
    generate_TC()
    #generate_TC_Alt()

def generate_SC():
    """生成 Krypton 系列字体搭配 SC 版"""
    # Regular 样式生成
    generate_font(
        ch_style="Regular",
        eng_style="Regular",
        merged_style="Regular",
        suffix=SUFFIX,
    )
    """
    # debug 模式下仅生成 Regular 样式
    if options.get("debug"):
        return
    """

def generate_TC():
    """生成 Krypton 系列字体搭配 TC 版"""
    # Regular 样式生成
    generate_font(
        ch_style="Regular",
        eng_style="Regular",
        merged_style="Regular",
        suffix=SUFFIX_TC,
    )
    """
    # debug 模式下仅生成 Regular 样式
    if options.get("debug"):
        return
    """

def generate_TC_Alt():
    """生成 Krypton 系列字体搭配 TC Alt 版"""
    # Regular 样式生成
    generate_font(
        ch_style="Regular",
        eng_style="Regular",
        merged_style="Regular",
        suffix=SUFFIX_TC_ALT,
    )
    """
    # debug 模式下仅生成 Regular 样式
    if options.get("debug"):
        return
    """

def usage():
    """非法选项或不明选项时提示用法"""
    print(
        f"Usage: {sys.argv[0]} " "[--visible-fullwidth-space] [--half-width] [--chdoc]"
    )

def get_options():
    """获取选项"""

    global options

    # 没有选项时跳过
    if len(sys.argv) == 1:
        return

    for arg in sys.argv[1:]:
        # 判断选项
        if arg == "--do-not-delete-build-dir":
            options["do-not-delete-build-dir"] = True
        elif arg == "--visible-fullwidth-space":
            options["visible-fullwidth-space"] = True
        elif arg == "--half-width":
            options["half-width"] = True
        elif arg == "--chdoc":
            options["chdoc"] = True
        elif arg == "--debug":
            options["debug"] = True
        else:
            options["unknown-option"] = True
            return

def generate_font(ch_style, eng_style, merged_style, suffix, italic=False):
    print(f"=== Generate {suffix} {merged_style} ===")

    # 打开预合成的字体
    ch_font, eng_font = open_fonts(ch_style, eng_style, suffix)

    # 将英文字体的 EM 度量值转换为 1000
    # ch_font 已经是 1000，因此仅转换 eng_font
    em_1000(eng_font)

    # 从英文字体中删除中文文档中常用的全宽符号
    if options.get("chdoc"):
        remove_chdoc_symbols(eng_font)

    # 删除重复字形
    delete_duplicate_glyphs(ch_font, eng_font)

    # 对一部分字形进行调整
    adjust_some_glyph(ch_font, eng_font)

    # 若为斜体，则对中文字体进行斜体变换
    if italic:
        transform_italic_glyphs(ch_font)

    # 通常将英文字体宽度设置为半角 600
    width_600(eng_font)

    # 使用中文字体将半角宽度（500）的字形宽度调整比例为 3:5 
    width_600_or_1000(ch_font)

    # 在 3:5 比例基础上进一步调整宽度
    if options.get("half-width"):
        # 调整为 1:2
        transform_half_width(ch_font, eng_font)
        # 缩小超出指定宽度的字形大小
        down_scale_redundant_size_glyph(eng_font)

    # 移除 GSUB 表 (针对包含全角字符的行中连字被拆分的解决方案）
    remove_lookups(ch_font)

    # 可见全角空格（酌情使用）
    if options.get("visible-fullwidth-space"):
        visualize_fullwidth_space(ch_font)

    # 为使用选项添加标识符
    variant = HALF_WIDTH_STR if options.get("half-width") else ""
    variant += (
        VISIBLE_FULLWIDTH_SPACE_STR if options.get("visible-fullwidth-space") else ""
    )
    variant += CHDOC_STR if options.get("chdoc") else ""

    # macOS 中处理 post 表可用性错误的解决方案
    # 重命名具有重复字形名称的字形
    delete_glyphs_with_duplicate_glyph_names(eng_font)
    delete_glyphs_with_duplicate_glyph_names(ch_font)

    # 编辑元数据
    cap_height = int(
        Decimal(str(eng_font[0x0048].boundingBox()[3])).quantize(
            Decimal("0"), ROUND_HALF_UP
        )
    )
    x_height = int(
        Decimal(str(eng_font[0x0078].boundingBox()[3])).quantize(
            Decimal("0"), ROUND_HALF_UP
        )
    )
    edit_meta_data(eng_font, merged_style, variant, suffix, cap_height, x_height)
    edit_meta_data(ch_font, merged_style, variant, suffix, cap_height, x_height)

    # 保存为 ttf 文件
    # 注：若设置了某种标记，GSUB 和 GPOS 表将会被删除，进而影响后续生成处理
    eng_font.generate(
        f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{variant}-{merged_style}-eng.ttf",
    )
    ch_font.generate(
        f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{variant}-{merged_style}-han.ttf",
    )

    # 关闭字体文件
    ch_font.close()
    eng_font.close()


def open_fonts(ch_style: str, eng_style: str, suffix: str = ""):
    """打开字体文件"""
    if suffix == SUFFIX:
        ch_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{CH_FONT}{ch_style}.ttf")
        eng_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{ENG_FONT}{eng_style}.otf")
    elif suffix == SUFFIX_TC:
        ch_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{CH_FONT_TC}{ch_style}.ttf")
        eng_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{ENG_FONT}{eng_style}.otf")
    elif suffix == SUFFIX_TC_ALT:
        ch_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{CH_FONT_TC_ALT}{ch_style}.ttf")
        eng_font = fontforge.open(f"{SOURCE_FONTS_DIR}/{ENG_FONT}{eng_style}.otf")
    else:
        print("===Unknown option, please retry! ===")
        return

    # fonttools merge 报错解决方案
    ch_font = altuni_to_entity(ch_font)

    # 解除字体参照
    for glyph in ch_font.glyphs():
        if glyph.isWorthOutputting():
            ch_font.selection.select(("more", None), glyph)
    ch_font.unlinkReferences()
    for glyph in eng_font.glyphs():
        if glyph.isWorthOutputting():
            eng_font.selection.select(("more", None), glyph)
    eng_font.unlinkReferences()

    return ch_font, eng_font


def altuni_to_entity(ch_font):
    """通过“替代Unicode”透明引用并显示的部分转换为具有实体字形的字符"""
    for glyph in ch_font.glyphs():
        if glyph.altuni is not None:
            # 返回以下格式的元组
            # (unicode-value, variation-selector, reserved-field)
            # 第 3 字段始终为 0，可忽略
            altunis = glyph.altuni

            # 若无 variation-selector (-1)，且以透明方式引用字形，则将其转换为实体字形
            before_altuni = ""
            for altuni in altunis:
                # 如果与前一个 altuni 相同，则跳过
                if altuni[1] == -1 and before_altuni != ",".join(map(str, altuni)):
                    glyph.altuni = None
                    copy_target_unicode = altuni[0]
                    try:
                        copy_target_glyph = ch_font.createChar(
                            copy_target_unicode,
                            f"uni{hex(copy_target_unicode).replace('0x', '').upper()}copy",
                        )
                    except Exception:
                        copy_target_glyph = ch_font[copy_target_unicode]
                    copy_target_glyph.clear()
                    copy_target_glyph.width = glyph.width
                    # copy_target_glyph.addReference(glyph.glyphname)
                    ch_font.selection.select(glyph.glyphname)
                    ch_font.copy()
                    ch_font.selection.select(copy_target_glyph.glyphname)
                    ch_font.paste()
                before_altuni = ",".join(map(str, altuni))
    # 重新打开以整理编码
    font_path = f"{BUILD_FONTS_DIR}/{ch_font.fullname}_{uuid.uuid4()}.ttf"
    ch_font.generate(font_path)
    ch_font.close()
    reopen_ch_font = fontforge.open(font_path)
    # 删除临时文件
    os.remove(font_path)
    return reopen_ch_font


def delete_glyphs_with_duplicate_glyph_names(font):
    """重命名具有重复字形名称的字形"""
    glyph_name_set = set()
    for glyph in font.glyphs():
        if glyph.glyphname in glyph_name_set:
            glyph.glyphname = f"{glyph.glyphname}_{glyph.encoding}"
        else:
            glyph_name_set.add(glyph.glyphname)


def adjust_some_glyph(ch_font, eng_font):
    """对一部分字形进行调整"""
    # 当下划线相邻时不调整则会连在一起，此时需缩短
    # 位置略微上移
    underscore = eng_font[0x005F]
    underscore_before_width = underscore.width
    underscore.transform(psMat.scale(0.91, 1))
    underscore.transform(
        psMat.translate((underscore_before_width - underscore.width) / 2, 60)
    )
    underscore.width = underscore_before_width
    # 扩大全角括号的开口
    full_width = ch_font[0x3000].width
    """
    for glyph_name in [0xFF08, 0xFF3B, 0xFF5B]:
        glyph = ch_font[glyph_name]
        glyph.transform(psMat.translate(-180, 0))
        glyph.width = full_width
    for glyph_name in [0xFF09, 0xFF3D, 0xFF5D]:
        glyph = ch_font[glyph_name]
        glyph.transform(psMat.translate(180, 0))
        glyph.width = full_width
    """
    # LEFT SINGLE QUOTATION MARK (U+2018) ～ DOUBLE LOW-9 QUOTATION MARK (U+201E) 设为全角宽度
    for uni in range(0x2018, 0x201E + 1):
        try:
            glyph = ch_font[uni]
            glyph.transform(psMat.translate((full_width - glyph.width) / 2, 0))
            glyph.width = full_width
        except TypeError:
            # 若无字形则继续
            continue
    ch_font.selection.none()

def em_1000(font):
    """将字体 EM 度量值转换为 1000"""
    font.em = EM_ASCENT + EM_DESCENT

def delete_duplicate_glyphs(ch_font, eng_font):
    """比较 ch_font 与 eng_font 字形，并删除重复字形"""
    eng_font.selection.none()
    ch_font.selection.none()

    for glyph in ch_font.glyphs("encoding"):
        try:
            if glyph.isWorthOutputting() and glyph.unicode > 0:
                eng_font.selection.select(("more", "unicode"), glyph.unicode)
        except ValueError:
            # 出现 Encoding is out of range 报错时继续
            continue
    for glyph in eng_font.selection.byGlyphs:
        ch_font.selection.select(("more", "unicode"), glyph.unicode)
    for glyph in ch_font.selection.byGlyphs:
        glyph.clear()

    ch_font.selection.none()
    eng_font.selection.none()

def remove_lookups(font):
    """删除 GSUB, GPOS 表"""
    for lookup in list(font.gsub_lookups) + list(font.gpos_lookups):
        font.removeLookup(lookup)

def transform_italic_glyphs(font):
    # 斜体倾斜度
    ITALIC_SLOPE = 11
    # 设置字体配置中的倾斜角度
    font.italicangle = -ITALIC_SLOPE
    # 对全部字形进行斜体变换
    for glyph in font.glyphs():
        glyph.transform(psMat.skew(ITALIC_SLOPE * math.pi / 180))

def remove_chdoc_symbols(eng_font):
    """从英文字体中删除中文文档中常用的全宽符号"""
    eng_font.selection.none()
    # ⇒ (U+21D2)
    eng_font.selection.select(("more", "unicode"), 0x21D2)
    # ⇔ (U+21D4)
    eng_font.selection.select(("more", "unicode"), 0x21D4)
    """
    # ■-□ (U+25A0-U+25A1)
    eng_font.selection.select(("more", "ranges"), 0x25A0, 0x25A1)
    # ▲-△ (U+25B2-U+25B3)
    eng_font.selection.select(("more", "ranges"), 0x25A0, 0x25B3)
    # ▼-▽ (U+25BC-U+25BD)
    eng_font.selection.select(("more", "ranges"), 0x25BC, 0x25BD)
    # ◆-◇ (U+25C6-U+25C7)
    eng_font.selection.select(("more", "ranges"), 0x25C6, 0x25C7)
    """
    # ○ (U+25CB)
    eng_font.selection.select(("more", "unicode"), 0x25CB)
    # ◎-● (U+25CE-U+25CF)
    eng_font.selection.select(("more", "ranges"), 0x25CE, 0x25CF)
    """
    # ◥ (U+25E5)
    eng_font.selection.select(("more", "unicode"), 0x25E5)
    """
    # ◯ (U+25EF)
    eng_font.selection.select(("more", "unicode"), 0x25EF)
    # ∞ (U+221E)
    eng_font.selection.select(("more", "unicode"), 0x221E)
    # ‐ (U+2010)
    eng_font.selection.select(("more", "unicode"), 0x2010)
    # … (U+2026)
    eng_font.selection.select(("more", "unicode"), 0x2026)
    # ‰ (U+2030)
    eng_font.selection.select(("more", "unicode"), 0x2030)
    # ←-↓ (U+2190-U+2193)
    eng_font.selection.select(("more", "ranges"), 0x2190, 0x2193)
    # ∑ (U+2211)
    eng_font.selection.select(("more", "unicode"), 0x2211)
    # ─-╿ (Box Drawing) (U+2500-U+257F)
    eng_font.selection.select(("more", "ranges"), 0x2500, 0x257F)

    """追加移除部分（原脚本不包括但 Monaspace Krypton 有且可能影响正常区分与排版）"""
    # ①-⑳ (Circled Numbers) (U+2460-U+2473)
    eng_font.selection.select(("more", "ranges"), 0x2460, 0x2473)
    # ⑴-⑼ (Bracket Numbers) (U+2474-U+247C)
    eng_font.selection.select(("more", "ranges"), 0x2474, 0x247C)
    # ⓪ (U+24EA)
    eng_font.selection.select(("more", "unicode"), 0x24EA)
    # ⓿ (U+24FF)
    eng_font.selection.select(("more", "unicode"), 0x24FF)
    # ❶-❿ (Dingbat Negative Circled Numbers) (U+2776-U+277F)
    eng_font.selection.select(("more", "ranges"), 0x2776, 0x277F)
    # ⓫-⓴ (Negative Circled Numbers) (U+24EB-U+24F4)
    eng_font.selection.select(("more", "ranges"), 0x24EB, 0x24F4)
    # ｛ & ｝ (U+FF5B, U+FF5D)
    eng_font.selection.select(("more", "unicode"), 0xFF5B)
    eng_font.selection.select(("more", "unicode"), 0xFF5D)
    # 🄍 (U+1F10D)
    eng_font.selection.select(("more", "unicode"), 0x1F10D)
    # 🄰-🅉 (U+1F130-U+1F149)
    eng_font.selection.select(("more", "ranges"), 0x1F130, 0x1F149)
    # 🅰-🆉 (U+1F170-U+1F189)
    eng_font.selection.select(("more", "ranges"), 0x1F170, 0x1F189)

    for glyph in eng_font.selection.byGlyphs:
        if glyph.isWorthOutputting():
            glyph.clear()
    eng_font.selection.none()

def width_600_or_1000(ch_font):
    """转换为半角或全角宽度"""
    for glyph in ch_font.glyphs():
        if 0 < glyph.width < 600:
            # 调整字形位置后设置宽度
            glyph.transform(psMat.translate((600 - glyph.width) / 2, 0))
            glyph.width = 600
        elif 600 < glyph.width < 1000:
            # 调整字形位置后设置宽度
            glyph.transform(psMat.translate((1000 - glyph.width) / 2, 0))
            glyph.width = 1000
        # 宽度 600 则保持原样

def width_600(eng_font):
    """将英文字体转换为半角宽度"""
    mona_original_half_width = eng_font[0x0030].width
    after_width = 600
    x_scale = after_width / mona_original_half_width
    for glyph in eng_font.glyphs():
        if 0 < glyph.width < after_width:
            # 若宽度小于 after_width，则先对齐位置再设置宽度
            glyph.transform(psMat.translate((after_width - glyph.width) / 2, 0))
            glyph.width = after_width
        elif after_width < glyph.width <= mona_original_half_width:
            # 若宽度大于 after_width，且比原始的半角字符宽度更窄，则先缩小再调宽度
            glyph.transform(psMat.scale(x_scale, 1))
            glyph.width = after_width
        elif mona_original_half_width < glyph.width:
            # 若宽度大于 after_width（可能为连字），则调整至 600 的倍数。
            multiply_number = round(glyph.width / mona_original_half_width)
            glyph.transform(psMat.scale(x_scale, 1))
            glyph.width = after_width * multiply_number

def transform_half_width(ch_font, eng_font):
    """在 3:5 比例基础上进一步调整宽度，使其比例为 1:2"""
    before_width_eng = eng_font[0x0030].width
    after_width_eng = HALF_WIDTH_12
    # 字形本身被缩小至相当于 550 宽，最终设为 HALF_WIDTH_12 宽度
    x_scale = 550 / before_width_eng
    for glyph in eng_font.glyphs():
        if glyph.width > 0:
            # 连字处理
            after_width_eng_multiply = after_width_eng * round(glyph.width / 600)
            # 字形变窄
            glyph.transform(psMat.scale(x_scale, 0.99))
            # 调整宽度
            glyph.transform(
                psMat.translate((after_width_eng_multiply - glyph.width) / 2, 0)
            )
            glyph.width = after_width_eng_multiply

    for glyph in ch_font.glyphs():
        if glyph.width == 600:
            # 与西文字符保持相同宽度
            glyph.transform(psMat.translate((after_width_eng - glyph.width) / 2, 0))
            glyph.width = after_width_eng
        elif glyph.width == 1000:
            # 全角字符宽度应设为 after_width_eng 的 2 倍
            glyph.transform(psMat.translate((after_width_eng * 2 - glyph.width) / 2, 0))
            glyph.width = after_width_eng * 2

def down_scale_redundant_size_glyph(eng_font):
    """缩小超出规定宽度的字形大小"""

    # 原本 x=0 位置在字形缩小后、超出边界的位置
    x_zero_pos_after_reduction = -10

    for glyph in eng_font.glyphs():
        bounding_x_min = glyph.boundingBox()[0]
        if (
            glyph.width > 0
            and bounding_x_min < 0
            and not (
                0x0020 <= glyph.unicode <= 0x02AF
            )  # 基本拉丁文 0x0020 - 0x0192 跳过
            and not (
                0xE0B0 <= glyph.unicode <= 0xE0D4
            )  # Powerline 符号 0xE0B0 - 0xE0D4 跳过
            and not (
                0x2500 <= glyph.unicode <= 0x257F
            )  # 制表符 0x2500 - 0x257F 跳过
            and not (
                0x2591 <= glyph.unicode <= 0x2593
            )  # 几何图形 0x2591 - 0x2593 跳过
        ):
            before_width = glyph.width
            if bounding_x_min > x_zero_pos_after_reduction:
                x_scale = 1 + (bounding_x_min * 2) / glyph.width
            else:
                # 若突出部分的宽度超过特定值，则固定缩小比例
                x_scale = 1 + (x_zero_pos_after_reduction * 2) / glyph.width
            glyph.transform(psMat.scale(x_scale, 1))
            glyph.transform(psMat.translate((before_width - glyph.width) / 2, 0))
            glyph.width = before_width

def visualize_fullwidth_space(ch_font):
    """可见全角空格"""
    # 替换全角空格
    glyph = ch_font[0x3000]
    width_to = glyph.width
    glyph.clear()
    ch_font.mergeFonts(fontforge.open(f"{SOURCE_FONTS_DIR}/{IDEOGRAPHIC_SPACE}"))
    # 设置宽度并调整位置
    ch_font.selection.select("U+3000")
    for glyph in ch_font.selection.byGlyphs:
        width_from = glyph.width
        glyph.transform(psMat.translate((width_to - width_from) / 2, 0))
        glyph.width = width_to
    ch_font.selection.none()

def edit_meta_data(
    font, weight: str, variant: str, suffix: str, cap_height: int, x_height: int
):
    """编辑字体内的元数据"""
    font.ascent = EM_ASCENT
    font.descent = EM_DESCENT

    os2_ascent = OS2_ASCENT
    os2_descent = OS2_DESCENT

    font.os2_winascent = os2_ascent
    font.os2_windescent = os2_descent

    font.os2_typoascent = os2_ascent
    font.os2_typodescent = -os2_descent
    font.os2_typolinegap = 0

    font.hhea_ascent = os2_ascent
    font.hhea_descent = -os2_descent
    font.hhea_linegap = 0

    font.os2_xheight = x_height
    font.os2_capheight = cap_height

    # 解决 VSCode 内底部位置显示时 g、j 等字符被截断的问题
    # 删除水平基线
    font.horizontalBaseline = None

    font.sfnt_names = (
        (
            "English (US)",
            "License",
            """This Font Software is licensed under the SIL Open Font License,
Version 1.1. This license is available with a FAQ
at: http://scripts.sil.org/OFL""",
        ),
        ("English (US)", "License URL", "http://scripts.sil.org/OFL"),
        ("English (US)", "Version", VERSION),
    )
    font.familyname = f"{FONT_NAME} {suffix} {variant}".strip()
    font.fontname = f"{FONT_NAME}{suffix}{variant}-{weight}"
    font.fullname = f"{FONT_NAME} {suffix} {variant}".strip() + f" {weight}"
    font.os2_vendor = VENDER_NAME
    font.copyright = COPYRIGHT

if __name__ == "__main__":
    main()
