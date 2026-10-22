#!/bin/env python3

import configparser
import glob
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools import merge, ttLib, ttx
from ttfautohint import options, ttfautohint

# 读取 ini 配置
settings = configparser.ConfigParser()
settings.read("build.ini", encoding="utf-8")

FONT_NAME = settings.get("DEFAULT", "FONT_NAME")
SUFFIX = settings.get("DEFAULT", "SUFFIX")
SUFFIX_TC = settings.get("DEFAULT", "SUFFIX_TC")
SUFFIX_TC_ALT = settings.get("DEFAULT", "SUFFIX_TC_ALT")
CH_FONT = settings.get("DEFAULT", "CH_FONT")
CH_FONT_TC = settings.get("DEFAULT", "CH_FONT_TC")
CH_FONT_TC_ALT = settings.get("DEFAULT", "CH_FONT_TC_ALT")
FONTFORGE_PREFIX = settings.get("DEFAULT", "FONTFORGE_PREFIX")
FONTTOOLS_PREFIX = settings.get("DEFAULT", "FONTTOOLS_PREFIX")
BUILD_FONTS_DIR = settings.get("DEFAULT", "BUILD_FONTS_DIR")
HALF_WIDTH_STR = settings.get("DEFAULT", "HALF_WIDTH_STR")
HALF_WIDTH_12 = int(settings.get("DEFAULT", "HALF_WIDTH_12"))
FULL_WIDTH_35 = int(settings.get("DEFAULT", "FULL_WIDTH_35"))


def main():
    # 获取第一个参数
    # 用于指定仅处理特定变体
    specific_variant = sys.argv[1] if len(sys.argv) > 1 else None

    edit_fonts(SUFFIX, specific_variant)
    edit_fonts(SUFFIX_TC, specific_variant)
    edit_fonts(SUFFIX_TC_ALT, specific_variant)


def edit_fonts(suffix: str, specific_variant: str):
    """编辑字体"""

    if specific_variant is None:
        specific_variant = ""

    # 按文件模式指定
    file_pattern = f"{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{specific_variant}*-eng.ttf"
    filenames = glob.glob(f"{BUILD_FONTS_DIR}/{file_pattern}")
    # 找不到文件时报错
    if len(filenames) == 0:
        print(f"Error: {file_pattern} not found")
        return
    paths = [Path(f) for f in filenames]
    for path in paths:
        print(f"edit {str(path)}")
        style = path.stem.split("-")[1]
        variant = path.stem.split("-")[0].replace(
            f"{FONTFORGE_PREFIX}{FONT_NAME}{suffix}", ""
        )
        add_hinting(str(path), str(path).replace(".ttf", "-hinted.ttf"))
        merge_fonts(suffix, style, variant)
        fix_font_tables(suffix, style, variant)

    # 删除临时文件
    # 样式部分后使用通配符指定
    for filename in glob.glob(
        f"{BUILD_FONTS_DIR}/{FONTTOOLS_PREFIX}{FONT_NAME}{suffix}-{specific_variant}*"
    ):
        os.remove(filename)
    for filename in glob.glob(
        f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{specific_variant}*"
    ):
        os.remove(filename)


def add_hinting(input_font_path, output_font_path):
    """为字体增加 hint"""
    args = [
        "-l",
        "6",
        "-r",
        "45",
        "-D",
        "latn",
        "-f",
        "none",
        "-S",
        "-W",
        "-X",
        "",
        "-I",
        input_font_path,
        output_font_path,
    ]
    options_ = options.parse_args(args)
    print("exec hinting", options_)
    ttfautohint(**options_)


def merge_fonts(suffix, style, variant):
    """合并字体"""
    eng_font_path = f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{variant}-{style}-eng-hinted.ttf"
    ch_font_path = f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{suffix}-{variant}-{style}-han.ttf"
    # 删除 vhea, vmtx 表
    ch_font_object = ttLib.TTFont(ch_font_path)
    if "vhea" in ch_font_object:
        del ch_font_object["vhea"]
    if "vmtx" in ch_font_object:
        del ch_font_object["vmtx"]
    ch_font_object.save(ch_font_path)
    # 合并字体文件
    merger = merge.Merger()
    merged_font = merger.merge([eng_font_path, ch_font_path])
    merged_font.save(
        f"{BUILD_FONTS_DIR}/{FONTTOOLS_PREFIX}{FONT_NAME}{suffix}-{variant}-{style}_merged.ttf"
    )


def fix_font_tables(suffix, style, variant):
    """编辑字体文件"""

    input_font_name = (
        f"{FONTTOOLS_PREFIX}{FONT_NAME}{suffix}{variant}-{style}_merged.ttf"
    )
    output_name_base = f"{FONTTOOLS_PREFIX}{FONT_NAME}{suffix}-{variant}-{style}"
    completed_name_base = f"{FONT_NAME}{suffix}-{variant}-{style}"

    # 仅输出含 OS/2, post表的 ttx 文件
    xml = dump_ttx(input_font_name, output_name_base)
    # 编辑 OS/2 表
    fix_os2_table(xml, style, flag_hw=HALF_WIDTH_STR in variant)
    # 编辑 post 表
    fix_post_table(xml, flag_hw=HALF_WIDTH_STR in variant)

    # ttx 文件另存
    xml.write(
        f"{BUILD_FONTS_DIR}/{output_name_base}.ttx",
        encoding="utf-8",
        xml_declaration=True,
    )

    # 将 ttx 文件转换为 ttf 文件
    ttx.main(
        [
            "-o",
            f"{BUILD_FONTS_DIR}/{output_name_base}_os2_post.ttf",
            "-m",
            f"{BUILD_FONTS_DIR}/{input_font_name}",
            f"{BUILD_FONTS_DIR}/{output_name_base}.ttx",
        ]
    )

    # 重命名
    os.rename(
        f"{BUILD_FONTS_DIR}/{output_name_base}_os2_post.ttf",
        f"{BUILD_FONTS_DIR}/{completed_name_base}.ttf",
    )


def dump_ttx(input_name_base, output_name_base) -> ET:
    """仅输出含 OS/2, post 表的 ttx 文件"""
    ttx.main(
        [
            "-t",
            "OS/2",
            "-t",
            "post",
            "-f",
            "-o",
            f"{BUILD_FONTS_DIR}/{output_name_base}.ttx",
            f"{BUILD_FONTS_DIR}/{input_name_base}",
        ]
    )

    return ET.parse(f"{BUILD_FONTS_DIR}/{output_name_base}.ttx")


def fix_os2_table(xml: ET, style: str, flag_hw: bool = False):
    """编辑 OS/2 表"""
    #  xAvgCharWidth
    # 标签格式: <xAvgCharWidth value="1000"/>
    if flag_hw:
        x_avg_char_width = HALF_WIDTH_12
    else:
        x_avg_char_width = FULL_WIDTH_35
    xml.find("OS_2/xAvgCharWidth").set("value", str(x_avg_char_width))

    # 编辑 fsSelection
    # 标签格式: <fsSelection value="00000000 11000000" />
    # 根据样式设置相应位
    fs_selection = None
    if style == "Regular":
        fs_selection = "00000001 01000000"
    elif style == "Italic":
        fs_selection = "00000001 00000001"
    elif style == "Bold":
        fs_selection = "00000001 00100000"
    elif style == "BoldItalic":
        fs_selection = "00000001 00100001"

    if fs_selection is not None:
        xml.find("OS_2/fsSelection").set("value", fs_selection)

    # 编辑 panose
    # 标签格式:
    # <panose>
    #   <bFamilyType value="2" />
    #   <bSerifStyle value="11" />
    #   <bWeight value="6" />
    #   <bProportion value="9" />
    #   <bContrast value="6" />
    #   <bStrokeVariation value="3" />
    #   <bArmStyle value="0" />
    #   <bLetterForm value="2" />
    #   <bMidline value="0" />
    #   <bXHeight value="4" />
    # </panose>
    if style == "Regular" or style == "Italic":
        bWeight = 5
    else:
        bWeight = 8
    if flag_hw:
        panose = {
            "bFamilyType": 2,
            "bSerifStyle": 11,
            "bWeight": bWeight,
            "bProportion": 9,
            "bContrast": 2,
            "bStrokeVariation": 2,
            "bArmStyle": 3,
            "bLetterForm": 2,
            "bMidline": 2,
            "bXHeight": 7,
        }
    else:
        panose = {
            "bFamilyType": 2,
            "bSerifStyle": 11,
            "bWeight": bWeight,
            "bProportion": 3,
            "bContrast": 2,
            "bStrokeVariation": 2,
            "bArmStyle": 3,
            "bLetterForm": 2,
            "bMidline": 2,
            "bXHeight": 7,
        }

    for key, value in panose.items():
        xml.find(f"OS_2/panose/{key}").set("value", str(value))


def fix_post_table(xml: ET, flag_hw: bool = False):
    """编辑 post 表"""
    # 编辑isFixedPitch
    # 标签形式: <isFixedPitch value="0"/>
    is_fixed_pitch = 1 if flag_hw else 0
    xml.find("post/isFixedPitch").set("value", str(is_fixed_pitch))


if __name__ == "__main__":
    main()
