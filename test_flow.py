#!/usr/bin/env python3
"""测试脚本：完整开发流程测试"""
import os
import sys

from dotenv import load_dotenv
load_dotenv()

from state import DevelopmentState, ProjectConfig
from agents import SupervisorAgent, FrontendAgent, BackendAgent
from discussion import DiscussionManager
from code_reader import CodeReader

def test_full_flow():
    print("=" * 60)
    print("DevPact - 完整流程测试")
    print("=" * 60)
    
    # 配置
    requirement = """开发一个用户管理模块，包含以下功能：
1. 用户注册：用户可以通过邮箱注册账号
2. 用户登录：支持邮箱密码登录
3. 用户信息管理：用户可以查看和修改个人信息
4. 用户列表：管理员可以查看所有用户列表，支持分页和搜索"""
    
    frontend_path = "/Users/test/Desktop/test2026/TEST-FRONT"
    backend_path = "/Users/test/Desktop/test2026/TEST-BACKEND"
    max_rounds = 4    
    model = "qwen3-coder-plus"
    lang = "zh"
    
    print(f"\n配置信息:")
    print(f"  前端路径: {frontend_path}")
    print(f"  后端路径: {backend_path}")
    print(f"  最大轮次: {max_rounds}")
    print(f"  模型: {model}")
    print(f"  语言: {lang}")
    
    # 初始化
    print("\n" + "=" * 60)
    print("1. 初始化组件")
    print("=" * 60)
    
    code_reader = CodeReader()
    supervisor = SupervisorAgent(model=model, lang=lang)
    frontend = FrontendAgent(model=model, lang=lang)
    backend = BackendAgent(model=model, lang=lang)
    discussion_manager = DiscussionManager(lang=lang)
    
    # 创建状态
    project_config = ProjectConfig(
        frontend_path=frontend_path,
        backend_path=backend_path,
    )
    
    state = DevelopmentState(
        requirement=requirement,
        project_config=project_config,
        max_rounds=max_rounds,
    )
    
    # 读取项目代码
    print("\n" + "=" * 60)
    print("2. 读取项目代码")
    print("=" * 60)
    
    state = code_reader.read_project(state)
    print(f"  前端文件: {len(state.code_context.frontend_files)}")
    print(f"  后端文件: {len(state.code_context.backend_files)}")
    print(f"  现有接口: {len(state.code_context.existing_apis)}")
    
    # 前端任务拆解
    print("\n" + "=" * 60)
    print("3. 前端任务拆解")
    print("=" * 60)
    
    state = frontend.breakdown_tasks(state)
    if state.frontend_breakdown:
        print(f"\n>>> 前端任务数: {len(state.frontend_breakdown.tasks)}")
        print(f">>> 前端接口数: {len(state.frontend_breakdown.endpoints)}")
        if state.frontend_breakdown.endpoints:
            print("\n前端接口:")
            for ep in state.frontend_breakdown.endpoints:
                print(f"  - {ep.method} {ep.path}")
        else:
            print("\n⚠️ 前端接口为空!")
    
    # 后端任务拆解
    print("\n" + "=" * 60)
    print("4. 后端任务拆解")
    print("=" * 60)
    
    state = backend.breakdown_tasks(state)
    if state.backend_breakdown:
        print(f"\n>>> 后端任务数: {len(state.backend_breakdown.tasks)}")
        print(f">>> 后端接口数: {len(state.backend_breakdown.endpoints)}")
        if state.backend_breakdown.endpoints:
            print("\n后端接口:")
            for ep in state.backend_breakdown.endpoints:
                print(f"  - {ep.method} {ep.path}")
        else:
            print("\n⚠️ 后端接口为空!")
    
    # 创建接口提案
    print("\n" + "=" * 60)
    print("5. 创建接口提案")
    print("=" * 60)
    
    state = discussion_manager.create_proposals(state)
    print(f"\n>>> 接口提案数: {len(state.schema_proposals)}")
    
    if len(state.schema_proposals) == 0:
        print("\n⚠️ 警告: 没有创建任何接口提案!")
        print("可能原因:")
        print(f"  1. 前端接口数: {len(state.frontend_breakdown.endpoints) if state.frontend_breakdown else 0}")
        print(f"  2. 后端接口数: {len(state.backend_breakdown.endpoints) if state.backend_breakdown else 0}")
        print("  3. LLM 返回的 JSON 格式不正确")
        
        # 直接跳过讨论，生成契约
        print("\n跳过讨论环节，直接生成契约...")
    else:
        # 讨论
        print("\n" + "=" * 60)
        print("6. 开始讨论")
        print("=" * 60)
        
        while True:
            state.current_round += 1
            print(f"\n--- 第 {state.current_round}/{state.max_rounds} 轮 ---")
            
            # 前端发言
            print("\n[Frontend] 发言中...")
            state, frontend_response = frontend.discuss(state)
            print(f"[Frontend] {frontend_response[:100]}...")
            
            # 后端发言
            print("\n[Backend] 发言中...")
            state, backend_response = backend.discuss(state)
            print(f"[Backend] {backend_response[:100]}...")
            
            # 处理同意
            state = discussion_manager.process_agreements(state)
            
            print(f"\n已同意接口数: {len(state.agreed_schemas)}/{len(state.schema_proposals)}")
            
            # 检查是否完成
            if len(state.agreed_schemas) == len(state.schema_proposals) and len(state.schema_proposals) > 0:
                print("\n✅ 所有接口已达成一致!")
                break
            
            if state.current_round >= state.max_rounds:
                print(f"\n⏱ 达到最大轮次 {state.max_rounds}")
                break
    
    # 生成契约
    print("\n" + "=" * 60)
    print("7. 生成契约文档")
    print("=" * 60)
    
    state = supervisor.generate_contract(state)
    
    print("\n" + "-" * 60)
    print(state.final_contract)
    print("-" * 60)
    
    # 保存契约
    output_path = os.path.join(os.path.dirname(__file__), "test_contract.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(state.final_contract)
    print(f"\n契约已保存到: {output_path}")
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"  前端任务: {len(state.frontend_breakdown.tasks) if state.frontend_breakdown else 0}")
    print(f"  后端任务: {len(state.backend_breakdown.tasks) if state.backend_breakdown else 0}")
    print(f"  前端接口: {len(state.frontend_breakdown.endpoints) if state.frontend_breakdown else 0}")
    print(f"  后端接口: {len(state.backend_breakdown.endpoints) if state.backend_breakdown else 0}")
    print(f"  接口提案: {len(state.schema_proposals)}")
    print(f"  达成一致: {len(state.agreed_schemas)}")
    print(f"  讨论轮次: {state.current_round}")
    print(f"  契约长度: {len(state.final_contract)} 字符")
    
    return state

if __name__ == "__main__":
    test_full_flow()
