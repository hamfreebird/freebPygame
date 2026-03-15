"""
测试运行脚本
用于运行 freepygame 库的所有测试
"""

import argparse
import os
import subprocess
import sys


def run_tests(test_path=None, quick=False, verbose=False, coverage=False):
    """
    运行测试

    Args:
        test_path: 测试路径，如果为 None 则运行所有测试
        quick: 是否使用快速测试模式（跳过慢速测试）
        verbose: 是否显示详细输出
        coverage: 是否生成测试覆盖率报告
    """
    # 确保当前目录是项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # 构建 pytest 命令
    cmd = [sys.executable, "-m", "pytest"]

    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")

    if quick:
        cmd.append("--quick")

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=freepygame", "--cov-report=term", "--cov-report=html"])

    # 添加额外的参数
    cmd.extend(
        [
            "--tb=short",  # 简短的 traceback
            "--durations=10",  # 显示最慢的10个测试
        ]
    )

    print(f"运行命令: {' '.join(cmd)}")
    print("=" * 80)

    # 运行测试
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return 130
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return 1


def run_specific_test_pattern(pattern, quick=False, verbose=False):
    """运行特定模式的测试"""
    cmd = [sys.executable, "-m", "pytest", "-k", pattern]

    if quick:
        cmd.append("--quick")

    if verbose:
        cmd.append("-v")

    print(f"运行测试模式: {pattern}")
    print(f"命令: {' '.join(cmd)}")
    print("=" * 80)

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return 130


def run_example(example_name):
    """运行示例程序"""
    example_path = os.path.join("examples", example_name)

    if not os.path.exists(example_path):
        print(f"错误: 示例文件 '{example_name}' 不存在")
        print(f"可用的示例: {', '.join(os.listdir('examples'))}")
        return 1

    print(f"运行示例: {example_name}")
    print("=" * 80)

    try:
        result = subprocess.run([sys.executable, example_path], check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n示例程序被用户中断")
        return 130
    except Exception as e:
        print(f"运行示例时出错: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="运行 freepygame 测试")
    parser.add_argument(
        "path", nargs="?", default=None, help="测试文件或目录路径（默认为所有测试）"
    )
    parser.add_argument(
        "--quick", action="store_true", help="快速测试模式（跳过慢速测试）"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细输出")
    parser.add_argument("--coverage", action="store_true", help="生成测试覆盖率报告")
    parser.add_argument(
        "--pattern", help="运行匹配特定模式的测试（使用 pytest -k 语法）"
    )
    parser.add_argument("--example", help="运行示例程序（例如：basic_demo.py）")
    parser.add_argument(
        "--list-examples", action="store_true", help="列出所有可用的示例"
    )

    args = parser.parse_args()

    # 列出示例
    if args.list_examples:
        examples_dir = "examples"
        if os.path.exists(examples_dir):
            examples = os.listdir(examples_dir)
            if examples:
                print("可用的示例:")
                for example in examples:
                    if example.endswith(".py"):
                        print(f"  {example}")
            else:
                print("没有找到示例文件")
        else:
            print(f"示例目录 '{examples_dir}' 不存在")
        return 0

    # 运行示例
    if args.example:
        return run_example(args.example)

    # 运行特定模式的测试
    if args.pattern:
        return run_specific_test_pattern(args.pattern, args.quick, args.verbose)

    # 运行普通测试
    return run_tests(args.path, args.quick, args.verbose, args.coverage)


if __name__ == "__main__":
    sys.exit(main())
