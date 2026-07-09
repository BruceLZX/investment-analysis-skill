#!/usr/bin/env python3
"""
投资分析报告 HTML -> PDF 转换工具
将生成的 HTML 投资分析报告转换为 PDF 格式。

依赖: weasyprint (推荐) 或 pdfkit (备选)
安装: pip install weasyprint
      (weasyprint 需要系统级依赖，详见 https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
备选方案: pip install pdfkit (需要 wkhtmltopdf 系统工具)
"""

import sys
import os
import argparse
from pathlib import Path


def html_to_pdf_weasyprint(html_path: str, pdf_path: str) -> bool:
    """使用 WeasyPrint 将 HTML 转换为 PDF（推荐方案）"""
    try:
        from weasyprint import HTML
        HTML(filename=html_path).write_pdf(pdf_path)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"[WeasyPrint Error] {e}")
        return False


def html_to_pdf_pdfkit(html_path: str, pdf_path: str) -> bool:
    """使用 pdfkit + wkhtmltopdf 将 HTML 转换为 PDF（备选方案）"""
    try:
        import pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
        }
        pdfkit.from_file(html_path, pdf_path, options=options)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"[pdfkit Error] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='将投资分析HTML报告转换为PDF格式'
    )
    parser.add_argument('html_path', help='HTML报告文件路径')
    parser.add_argument('pdf_path', nargs='?', help='PDF输出路径（默认与HTML同目录同名）')
    parser.add_argument('--method', choices=['weasyprint', 'pdfkit', 'auto'],
                        default='auto', help='转换引擎（默认auto自动选择）')

    args = parser.parse_args()

    html_path = Path(args.html_path).resolve()
    if not html_path.exists():
        print(f"❌ HTML文件不存在: {html_path}")
        sys.exit(1)

    if args.pdf_path:
        pdf_path = Path(args.pdf_path).resolve()
    else:
        pdf_path = html_path.with_suffix('.pdf')

    # 确保输出目录存在
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📄 输入文件: {html_path}")
    print(f"📑 输出文件: {pdf_path}")
    print(f"🔧 转换引擎: {args.method}")

    success = False

    if args.method == 'weasyprint':
        success = html_to_pdf_weasyprint(str(html_path), str(pdf_path))
    elif args.method == 'pdfkit':
        success = html_to_pdf_pdfkit(str(html_path), str(pdf_path))
    else:  # auto
        # 优先使用 weasyprint，失败则降级到 pdfkit
        success = html_to_pdf_weasyprint(str(html_path), str(pdf_path))
        if not success:
            print("⚠️  WeasyPrint 不可用，尝试 pdfkit...")
            success = html_to_pdf_pdfkit(str(html_path), str(pdf_path))

    if success:
        file_size_kb = pdf_path.stat().st_size / 1024
        print(f"✅ PDF 生成成功！文件大小: {file_size_kb:.1f} KB")
        print(f"   {pdf_path}")
        sys.exit(0)
    else:
        print("❌ PDF 生成失败！")
        print()
        print("请安装以下任一依赖：")
        print()
        print("方案一（推荐）：")
        print("  pip install weasyprint")
        print("  # macOS 还需要: brew install pango")
        print()
        print("方案二（备选）：")
        print("  pip install pdfkit")
        print("  brew install wkhtmltopdf")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
