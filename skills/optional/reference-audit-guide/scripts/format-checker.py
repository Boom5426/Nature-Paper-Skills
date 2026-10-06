#!/usr/bin/env python3
"""
BibTeX and LaTeX Format Checker

独立的格式检查工具,用于验证 BibTeX 和 LaTeX 引用格式。

功能:
1. BibTeX 格式检查 - 验证条目结构、必填字段、字段格式
2. LaTeX 引用检查 - 提取引用、检查一致性
3. 快速格式验证 - 无需 API 调用的快速检查

使用方法:
    python format-checker.py references.bib
    python format-checker.py paper.tex --check-latex
    python format-checker.py references.bib --strict
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from citation_io import load_bibtex, latex_citations, resolve_inputs, fix_common_text


class ErrorLevel(Enum):
    """错误级别"""
    ERROR = "error"      # 严重错误,必须修复
    WARNING = "warning"  # 警告,建议修复
    INFO = "info"        # 信息,可选修复


@dataclass
class FormatError:
    """格式错误数据类"""
    level: ErrorLevel
    location: str        # 文件位置 (如 "entry:smith2020" 或 "line:42")
    field: Optional[str] # 字段名 (如 "author", "year")
    message: str         # 错误描述
    suggestion: Optional[str] = None  # 修复建议


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='检查 BibTeX 和 LaTeX 引用格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s references.bib
  %(prog)s paper.tex --check-latex
  %(prog)s references.bib --strict --output report.txt
  %(prog)s references.bib --fix-common
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='BibTeX 文件(.bib)或 LaTeX 文件(.tex)'
    )

    parser.add_argument(
        '--check-latex',
        action='store_true',
        help='检查 LaTeX 引用(需要提供 .tex 文件)'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='严格模式 - 将警告视为错误'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='输出报告文件路径'
    )

    parser.add_argument(
        '--fix-common',
        action='store_true',
        help='修复单行 DOI URL 和页码分隔符；需 --fixed-output，保留原文件'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )

    parser.add_argument(
        '--entry-type',
        type=str,
        help='只检查特定类型的条目(如 article, inproceedings)'
    )

    parser.add_argument('--bib', action='append', help='明确指定 .bib 文件；可重复')
    parser.add_argument('--tex', help='明确指定一致性检查用的 .tex 文件')
    parser.add_argument('--fixed-output', help='修复后的新 .bib 路径；拒绝覆盖')
    args = parser.parse_args()
    if args.fix_common != bool(args.fixed_output):
        parser.error('--fix-common 必须和 --fixed-output 一起使用')
    return args


def load_bibtex_file(file_path: str) -> List[Dict]:
    """加载 BibTeX 文件

    Args:
        file_path: BibTeX 文件路径

    Returns:
        BibTeX 条目列表

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式错误
    """
    return load_bibtex(file_path)


def load_latex_file(file_path: str) -> str:
    """加载 LaTeX 文件

    Args:
        file_path: LaTeX 文件路径

    Returns:
        文件内容

    Raises:
        FileNotFoundError: 文件不存在
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise ValueError(f"无法读取 LaTeX 文件: {e}")


# ============================================================================
# BibTeX 格式检查函数
# ============================================================================

def get_required_fields(entry_type: str) -> List[str]:
    """获取 BibTeX 条目类型的必填字段

    Args:
        entry_type: 条目类型 (如 'article', 'inproceedings')

    Returns:
        必填字段列表
    """
    required_fields = {
        'article': ['author', 'title', 'journal', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'book': ['title', 'publisher', 'year'],
        'incollection': ['author', 'title', 'booktitle', 'publisher', 'year'],
        'inbook': ['author', 'title', 'chapter', 'publisher', 'year'],
        'proceedings': ['title', 'year'],
        'phdthesis': ['author', 'title', 'school', 'year'],
        'mastersthesis': ['author', 'title', 'school', 'year'],
        'techreport': ['author', 'title', 'institution', 'year'],
        'manual': ['title'],
        'misc': ['title'],
        'unpublished': ['author', 'title', 'note'],
    }
    return required_fields.get(entry_type.lower(), ['title'])


def get_optional_fields(entry_type: str) -> List[str]:
    """获取 BibTeX 条目类型的可选字段

    Args:
        entry_type: 条目类型

    Returns:
        可选字段列表
    """
    optional_fields = {
        'article': ['volume', 'number', 'pages', 'month', 'doi', 'url'],
        'inproceedings': ['editor', 'volume', 'series', 'pages', 'address',
                         'month', 'organization', 'publisher', 'doi', 'url'],
        'book': ['author', 'editor', 'volume', 'series', 'address',
                'edition', 'month', 'isbn', 'doi', 'url'],
    }
    return optional_fields.get(entry_type.lower(), [])


def check_entry_structure(entry: Dict) -> List[FormatError]:
    """检查 BibTeX 条目基本结构

    Args:
        entry: BibTeX 条目字典

    Returns:
        错误列表
    """
    errors = []

    # 检查条目类型
    if 'ENTRYTYPE' not in entry:
        errors.append(FormatError(
            level=ErrorLevel.ERROR,
            location=f"entry:{entry.get('ID', 'unknown')}",
            field='ENTRYTYPE',
            message="缺少条目类型",
            suggestion="添加条目类型,如 @article, @inproceedings"
        ))
        return errors

    # 检查 ID
    if 'ID' not in entry or not entry['ID'].strip():
        errors.append(FormatError(
            level=ErrorLevel.ERROR,
            location="entry:unknown",
            field='ID',
            message="缺少 citation key",
            suggestion="添加唯一的 citation key"
        ))

    # 检查必填字段
    entry_type = entry.get('ENTRYTYPE', '')
    required = get_required_fields(entry_type)
    for field in required:
        if field not in entry or not entry[field].strip():
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry.get('ID', 'unknown')}",
                field=field,
                message=f"缺少必填字段: {field}",
                suggestion=f"添加 {field} 字段"
            ))

    return errors


def check_field_formats(entry: Dict) -> List[FormatError]:
    """检查字段格式

    Args:
        entry: BibTeX 条目字典

    Returns:
        错误列表
    """
    errors = []
    entry_id = entry.get('ID', 'unknown')

    # 年份格式检查
    if 'year' in entry:
        year = entry['year'].strip()
        if not year.isdigit():
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='year',
                message=f"年份格式错误: {year} (应为4位数字)",
                suggestion="使用4位数字年份,如 2023"
            ))
        elif len(year) != 4:
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='year',
                message=f"年份格式错误: {year} (应为4位数字)",
                suggestion="使用4位数字年份,如 2023"
            ))
        else:
            year_int = int(year)
            if year_int < 1900 or year_int > 2030:
                errors.append(FormatError(
                    level=ErrorLevel.WARNING,
                    location=f"entry:{entry_id}",
                    field='year',
                    message=f"年份超出合理范围: {year}",
                    suggestion="检查年份是否正确"
                ))

    # DOI 格式检查
    if 'doi' in entry:
        doi = entry['doi'].strip()
        if not doi.startswith('10.'):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='doi',
                message=f"DOI 格式错误: {doi}",
                suggestion="DOI 应以 '10.' 开头,如 10.1038/nature12345"
            ))
        # 检查是否包含 URL 前缀
        if 'doi.org' in doi or 'dx.doi.org' in doi:
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"entry:{entry_id}",
                field='doi',
                message=f"DOI 包含 URL 前缀: {doi}",
                suggestion="只保留 DOI 本身,移除 https://doi.org/ 前缀"
            ))

    # 作者名格式检查
    if 'author' in entry:
        author = entry['author'].strip()
        # 检查是否为空
        if not author:
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='author',
                message="作者字段为空",
                suggestion="添加作者信息"
            ))
        # 检查格式一致性
        elif ' and ' in author:
            authors = author.split(' and ')
            formats = []
            for a in authors:
                if ',' in a:
                    formats.append('last_first')  # "Last, First"
                else:
                    formats.append('first_last')  # "First Last"

            if len(set(formats)) > 1:
                errors.append(FormatError(
                    level=ErrorLevel.WARNING,
                    location=f"entry:{entry_id}",
                    field='author',
                    message="作者名格式不一致",
                    suggestion="统一使用 'Last, First' 或 'First Last' 格式"
                ))

    # 页码格式检查
    if 'pages' in entry:
        pages = entry['pages'].strip()
        # 检查是否使用了正确的分隔符
        if '-' in pages and '--' not in pages:
            errors.append(FormatError(
                level=ErrorLevel.INFO,
                location=f"entry:{entry_id}",
                field='pages',
                message=f"页码使用单连字符: {pages}",
                suggestion="建议使用双连字符 '--',如 123--145"
            ))

    # URL 格式检查
    if 'url' in entry:
        url = entry['url'].strip()
        if not url.startswith(('http://', 'https://')):
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"entry:{entry_id}",
                field='url',
                message=f"URL 缺少协议前缀: {url}",
                suggestion="添加 http:// 或 https:// 前缀"
            ))

    return errors


def check_consistency(entries: List[Dict]) -> List[FormatError]:
    """检查条目间的一致性

    Args:
        entries: BibTeX 条目列表

    Returns:
        错误列表
    """
    errors = []

    # 检查重复的 citation key
    ids = [e.get('ID', '') for e in entries]
    duplicates = [id for id in ids if ids.count(id) > 1]
    if duplicates:
        for dup_id in set(duplicates):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{dup_id}",
                field='ID',
                message=f"重复的 citation key: {dup_id}",
                suggestion="使用唯一的 citation key"
            ))

    # 检查作者名格式一致性
    author_formats = {}
    for entry in entries:
        if 'author' in entry and ' and ' in entry['author']:
            entry_id = entry.get('ID', 'unknown')
            authors = entry['author'].split(' and ')
            for author in authors:
                if ',' in author:
                    author_formats[entry_id] = 'last_first'
                else:
                    author_formats[entry_id] = 'first_last'
                break

    if len(set(author_formats.values())) > 1:
        errors.append(FormatError(
            level=ErrorLevel.WARNING,
            location="global",
            field='author',
            message="不同条目使用了不同的作者名格式",
            suggestion="统一使用 'Last, First' 或 'First Last' 格式"
        ))

    return errors


# ============================================================================
# LaTeX 引用检查函数
# ============================================================================

def extract_latex_citations(tex_content: str) -> List[str]:
    """从 LaTeX 文件中提取引用

    Args:
        tex_content: LaTeX 文件内容

    Returns:
        引用 key 列表
    """
    return latex_citations(tex_content)


def check_latex_consistency(tex_keys: List[str], bib_keys: List[str]) -> List[FormatError]:
    """检查 LaTeX 引用与 BibTeX 的一致性

    Args:
        tex_keys: LaTeX 中的引用 key 列表
        bib_keys: BibTeX 中的 key 列表

    Returns:
        错误列表
    """
    errors = []

    tex_set = set(tex_keys)
    bib_set = set(bib_keys)

    # 未定义的引用
    undefined = tex_set - bib_set
    if undefined:
        for key in sorted(undefined):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"latex:cite",
                field=key,
                message=f"未定义的引用: {key}",
                suggestion=f"在 BibTeX 文件中添加 {key} 条目"
            ))

    # 未使用的引用
    unused = bib_set - tex_set
    if unused:
        for key in sorted(unused):
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"bibtex:entry",
                field=key,
                message=f"未使用的引用: {key}",
                suggestion=f"在 LaTeX 文件中引用 {key} 或从 BibTeX 中删除"
            ))

    return errors


# ============================================================================
# 报告生成函数
# ============================================================================

def print_errors(errors: List[FormatError], verbose: bool = False):
    """打印错误列表

    Args:
        errors: 错误列表
        verbose: 是否显示详细信息
    """
    if not errors:
        print("✅ 未发现格式错误")
        return

    # 按级别分组
    errors_by_level = {
        ErrorLevel.ERROR: [],
        ErrorLevel.WARNING: [],
        ErrorLevel.INFO: []
    }

    for error in errors:
        errors_by_level[error.level].append(error)

    # 打印统计
    print("\n" + "="*60)
    print("格式检查结果")
    print("="*60)
    print(f"❌ 错误: {len(errors_by_level[ErrorLevel.ERROR])}")
    print(f"⚠️  警告: {len(errors_by_level[ErrorLevel.WARNING])}")
    print(f"ℹ️  信息: {len(errors_by_level[ErrorLevel.INFO])}")
    print("="*60)

    # 打印详细错误
    for level in [ErrorLevel.ERROR, ErrorLevel.WARNING, ErrorLevel.INFO]:
        level_errors = errors_by_level[level]
        if not level_errors:
            continue

        level_symbol = {
            ErrorLevel.ERROR: "❌",
            ErrorLevel.WARNING: "⚠️",
            ErrorLevel.INFO: "ℹ️"
        }[level]

        print(f"\n{level_symbol} {level.value.upper()} ({len(level_errors)}):\n")

        for error in level_errors:
            print(f"  [{error.location}]", end="")
            if error.field:
                print(f" {error.field}:", end="")
            print(f" {error.message}")

            if verbose and error.suggestion:
                print(f"    💡 建议: {error.suggestion}")
            print()


def generate_report(errors: List[FormatError], output_file: str):
    """生成文本格式的检查报告

    Args:
        errors: 错误列表
        output_file: 输出文件路径
    """
    # 按级别分组
    errors_by_level = {
        ErrorLevel.ERROR: [],
        ErrorLevel.WARNING: [],
        ErrorLevel.INFO: []
    }

    for error in errors:
        errors_by_level[error.level].append(error)

    with open(output_file, 'x', encoding='utf-8') as f:
        f.write("# BibTeX/LaTeX 格式检查报告\n\n")

        # 总体统计
        f.write("## 总体统计\n\n")
        f.write(f"- **错误**: {len(errors_by_level[ErrorLevel.ERROR])}\n")
        f.write(f"- **警告**: {len(errors_by_level[ErrorLevel.WARNING])}\n")
        f.write(f"- **信息**: {len(errors_by_level[ErrorLevel.INFO])}\n\n")

        # 详细错误
        for level in [ErrorLevel.ERROR, ErrorLevel.WARNING, ErrorLevel.INFO]:
            level_errors = errors_by_level[level]
            if not level_errors:
                continue

            level_name = {
                ErrorLevel.ERROR: "错误",
                ErrorLevel.WARNING: "警告",
                ErrorLevel.INFO: "信息"
            }[level]

            f.write(f"## {level_name} ({len(level_errors)})\n\n")

            for error in level_errors:
                f.write(f"### [{error.location}]")
                if error.field:
                    f.write(f" {error.field}")
                f.write("\n\n")
                f.write(f"**问题**: {error.message}\n\n")
                if error.suggestion:
                    f.write(f"**建议**: {error.suggestion}\n\n")

    print(f"\n报告已保存到: {output_file}")


def main():
    args = parse_arguments()
    try:
        bib_files, tex_file = resolve_inputs(args.input_file, args.bib, args.tex, args.check_latex)
        entries = [entry for path in bib_files for entry in load_bibtex_file(path)]
        if args.fix_common:
            if len(bib_files) != 1:
                raise ValueError('--fix-common 需要恰好一个 .bib 文件')
            text = fix_common_text(bib_files[0].read_text(encoding='utf-8-sig'))
            with open(args.fixed_output, 'x', encoding='utf-8') as output:
                output.write(text)
            entries = load_bibtex_file(args.fixed_output)
            print(f'修复副本: {args.fixed_output}；原文件保留')
        errors = check_consistency(entries)
        for entry in entries:
            if not args.entry_type or entry.get('ENTRYTYPE') == args.entry_type.lower():
                errors.extend(check_entry_structure(entry))
                errors.extend(check_field_formats(entry))
        if tex_file:
            keys = [entry['ID'] for entry in entries]
            tex_keys = extract_latex_citations(load_latex_file(tex_file))
            if '*' in tex_keys:
                tex_keys = [key for key in tex_keys if key != '*'] + keys
            errors.extend(check_latex_consistency(tex_keys, keys))
        print_errors(errors, args.verbose)
        if args.output:
            generate_report(errors, args.output)
        return int(any(error.level == ErrorLevel.ERROR or
                       (args.strict and error.level == ErrorLevel.WARNING) for error in errors))
    except (OSError, ValueError, ImportError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
