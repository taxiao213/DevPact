import os
import argparse
from dotenv import load_dotenv
from workflow import run_collaboration

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="多Agent协同开发系统")
    parser.add_argument("--requirement", "-r", type=str, help="需求描述")
    parser.add_argument("--frontend-path", "-f", type=str, default="", help="前端项目路径")
    parser.add_argument("--backend-path", "-b", type=str, default="", help="后端项目路径")
    parser.add_argument("--max-rounds", "-m", type=int, default=3, help="最大讨论轮次")
    args = parser.parse_args()

    if args.requirement:
        requirement = args.requirement
    else:
        requirement = """
        开发一个用户管理模块，包含以下功能：
        1. 用户注册：用户可以通过邮箱注册账号
        2. 用户登录：支持邮箱密码登录
        3. 用户信息管理：用户可以查看和修改个人信息
        4. 用户列表：管理员可以查看所有用户列表，支持分页和搜索
        """

    print("=" * 60)
    print("多Agent协同开发系统启动")
    print("=" * 60)

    result = run_collaboration(
        requirement=requirement,
        frontend_path=args.frontend_path,
        backend_path=args.backend_path,
        max_rounds=args.max_rounds,
    )

    print("\n" + "=" * 60)
    print("协同开发完成!")
    print("=" * 60)
    print("\n" + result.final_contract)

    print("\n" + "=" * 60)
    print("讨论历史摘要")
    print("=" * 60)
    for i, msg in enumerate(result.discussion_history, 1):
        print(f"\n{i}. [{msg.agent_name}] {msg.message_type}:")
        print(f"   {msg.content}")


if __name__ == "__main__":
    main()
