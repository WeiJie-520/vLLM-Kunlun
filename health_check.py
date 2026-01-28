#!/usr/bin/env python3
"""
vLLM-Kunlun 项目健康检查脚本
检查项目依赖、配置和基本功能的脚本
"""

import sys
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    print(f"  当前Python版本: {version.major}.{version.minor}.{version.micro}")

    # 检查项目要求的Python版本
    python_version_file = Path(".python-version")
    if python_version_file.exists():
        with open(python_version_file, "r") as f:
            required_version = f.read().strip()
        print(f"  项目要求的Python版本: {required_version}")

    return True


def check_requirements():
    """检查依赖包"""
    print("\n📦 检查依赖包...")

    # 检查requirements.txt是否存在
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("   ❌ requirements.txt 文件不存在")
        return False

    print("   ✅ requirements.txt 存在")

    # 尝试安装核心依赖
    try:
        import torch

        print(f"   ✅ PyTorch 已安装: {torch.__version__}")
    except ImportError:
        print("   ❌ PyTorch 未安装")
        return False

    try:
        import vllm

        print(f"   ✅ vLLM 已安装: {vllm.__version__}")
    except ImportError:
        print("   ❌ vLLM 未安装")
        return False

    return True


def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")

    essential_dirs = ["vllm_kunlun", "docs", "tests"]

    essential_files = ["pyproject.toml", "setup.py", "README.md"]

    all_ok = True

    for dir_name in essential_dirs:
        if Path(dir_name).exists():
            print(f"   ✅ {dir_name}/ 目录存在")
        else:
            print(f"   ❌ {dir_name}/ 目录缺失")
            all_ok = False

    for file_name in essential_files:
        if Path(file_name).exists():
            print(f"   ✅ {file_name} 文件存在")
        else:
            print(f"   ❌ {file_name} 文件缺失")
            all_ok = False

    return all_ok


def check_kunlun_support():
    """检查昆仑芯片支持"""
    print("\n🚀 检查昆仑芯片支持...")

    try:
        # 检查昆仑相关模块
        import torch

        if hasattr(torch, "xpu") and torch.xpu.is_available():
            print("   ✅ 昆仑芯片支持已启用")
            print(f"   可用XPU设备数: {torch.xpu.device_count()}")
        else:
            print("   ⚠️  昆仑芯片支持未启用或不可用")
    except Exception as e:
        print(f"   ❌ 检查昆仑芯片支持时出错: {e}")

    # 检查昆仑相关源码
    kunlun_dirs = [
        "vllm_kunlun/platforms",
        "vllm_kunlun/ops/attention/backends",
        "vllm_kunlun/distributed",
    ]

    for dir_path in kunlun_dirs:

        if Path(dir_path).exists():
            print(f"      ✅ {dir_path} 昆仑相关代码存在")
        else:
            print(f"   ❌ {dir_path} 昆仑相关代码缺失")


def check_build_system():
    """检查构建系统"""
    print("\n🔨 检查构建系统...")

    build_files = ["setup.py", "pyproject.toml", "build.sh"]

    for build_file in build_files:
        if Path(build_file).exists():
            print(f"   ✅ {build_file} 构建文件存在")
        else:
            print(f"   ❌ {build_file} 构建文件缺失")


def run_basic_tests():
    """运行基本测试"""

    print("\n🧪 运行基本测试...")

    # 检查测试目录是否存在
    test_dir = Path("vllm_kunlun/tests")
    if not test_dir.exists():
        print("   ⚠️  测试目录不存在")
        return

    # 尝试运行简单的导入测试
    try:
        # 测试关键模块导入
        test_modules = [
            "vllm_kunlun",
            "vllm_kunlun.platforms",
            "vllm_kunlun.ops.attention.backends.kunlun_attn",
        ]

        for module in test_modules:
            try:
                __import__(module)
                print(f"   ✅ {module} 导入成功")
            except ImportError as e:
                print(f"   ❌ {module} 导入失败: {e}")

    except Exception as e:
        print(f"   ❌ 运行测试时出错: {e}")


def main():
    """主函数"""

    print("=" * 60)
    print("🧬 vLLM-Kunlun 项目健康检查")
    print("=" * 60)

    current_dir = Path.cwd()
    print(f"当前工作目录: {current_dir}")

    # 执行各项检查
    checks = [
        check_python_version,
        check_requirements,
        check_project_structure,
        check_kunlun_support,
        check_build_system,
        run_basic_tests,
    ]

    results = []
    for check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ 检查出错: {e}")
            results.append(False)

    # 总结报告
    print("\n" + "=" * 60)
    print("📊 检查总结")
    print("=" * 60)

    successful_checks = sum(results)
    total_checks = len(results)

    print(f"✅ 通过检查: {successful_checks}/{total_checks}")

    if successful_checks == total_checks:
        print("🎉 所有检查通过！项目状态良好。")
    elif successful_checks >= total_checks * 0.7:
        print("⚠️  大部分检查通过，但存在一些问题需要修复。")
    else:
        print("❌ 多个检查失败，项目可能存在严重问题。")

    print("\n?? 建议:")
    print("   1. 确保安装了所有必要依赖")
    print("   2. 检查昆仑芯片驱动和PyTorch-XPU安装")
    print("   3. 运行完整测试套件验证功能")


if __name__ == "__main__":
    main()
