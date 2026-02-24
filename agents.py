import os
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import DevelopmentState, TaskBreakdown, APIEndpoint, APIField, DiscussionMessage, SchemaProposal
from code_reader import CodeReader


LANGUAGES = {
    "zh": {
        "supervisor_prompt": """你是一个项目协调者(Supervisor)，负责协调前端和后端Agent的协同开发。

你的职责：
1. 接收原始需求，分发给前端和后端Agent
2. 监控讨论进度，确保双方达成一致
3. 汇总最终结果，生成开发契约文档

你需要确保：
- 前后端对接口字段的理解一致
- 讨论不偏离主题
- 最终产出清晰的开发契约""",
        "frontend_prompt": """你是一个前端开发专家(Frontend Agent)，专注于用户界面和用户体验。

你的职责：
1. 结合现有前端项目代码，理解需求
2. 从前端角度拆解需求，识别需要开发的页面和组件
3. 提出需要的后端接口和字段
4. 参与接口讨论，确保字段定义满足前端展示需求

你关注的重点：
- 是否能复用现有组件
- 字段命名是否与现有代码风格一致
- 响应数据结构是否便于前端处理
- 是否需要额外的展示字段（如格式化后的时间、状态文本等）
- 分页、排序等常见需求

回复格式要求：
- 拆解任务时，用JSON格式返回任务列表
- 讨论时，清晰表达你的观点和建议
- 同意或不同意某个提案时，说明理由""",
        "backend_prompt": """你是一个后端开发专家(Backend Agent)，专注于API设计和数据处理。

你的职责：
1. 结合现有后端项目代码，理解需求
2. 从后端角度拆解需求，识别需要开发的服务和接口
3. 设计数据库模型和API接口
4. 参与接口讨论，确保字段定义合理、可实现

你关注的重点：
- 是否能复用现有接口或模型
- 字段类型是否正确（int、string、boolean等）
- 数据库设计是否合理
- 接口的安全性和性能
- 字段的校验规则

回复格式要求：
- 拆解任务时，用JSON格式返回任务列表
- 讨论时，清晰表达你的观点和建议
- 同意或不同意某个提案时，说明理由""",
        "contract_title": "# 开发契约文档",
        "original_requirement": "## 原始需求",
        "project_config": "## 项目配置",
        "frontend_path": "- 前端路径",
        "frontend_tech": "- 前端技术栈",
        "backend_path": "- 后端路径",
        "backend_tech": "- 后端技术栈",
        "unknown": "未知",
        "frontend_tasks": "## 前端任务",
        "backend_tasks": "## 后端任务",
        "api_contract": "## 接口契约",
        "request_fields": "**请求字段:**",
        "response_fields": "**响应字段:**",
        "field_name": "字段名",
        "field_type": "类型",
        "field_required": "必填",
        "field_description": "描述",
        "yes": "是",
        "no": "否",
        "description": "描述",
        "pending_agreement": "待达成一致的接口:",
        "agreed_by": "已同意",
        "not_agreed": "待讨论",
        "no_api_defined": "未定义任何接口，请检查需求描述是否清晰",
        "analyze_requirement": "请分析以下需求，结合现有前端项目代码，拆解任务：",
        "requirement": "需求",
        "no_code": "未提供前端项目代码，请基于通用前端开发经验分析。",
        "consider": "请考虑：",
        "reuse": "1. 是否可以复用现有组件或API",
        "integration": "2. 新增功能与现有代码的集成方式",
        "style": "3. 保持与现有代码风格一致",
        "return_json": "请严格按以下JSON格式返回（只返回JSON，不要其他内容）：",
        "tasks": "tasks",
        "endpoints": "endpoints",
        "path": "path",
        "method": "method",
        "discuss_context": "当前讨论上下文：",
        "frontend_opinion": "请从前端角度发表你的看法：",
        "backend_opinion": "请从后端角度发表你的看法：",
        "opinion_1": "1. 对当前接口提案有什么意见？",
        "opinion_2": "2. 是否有需要补充或修改的字段？",
        "opinion_3": "3. 如果满意，请明确表示'同意'",
        "opinion_backend_2": "2. 字段类型和约束是否合理？",
        "concise_reply": "请简洁回复（100字以内）。",
        "agree": "同意",
        "original_req": "原始需求",
        "frontend_need": "前端需要的接口",
        "backend_provide": "后端提供的接口",
        "current_discuss": "当前讨论的接口",
        "recent_discussion": "最近的讨论",
        "log_received": "收到需求",
        "log_frontend_path": "前端项目路径",
        "log_backend_path": "后端项目路径",
        "log_distributing": "开始分发任务给前端和后端Agent...",
        "log_contract_generated": "契约文档已生成!",
        "log_task_complete": "任务拆解完成",
        "log_parse_error": "解析错误",
        "log_analysis_failed": "解析需求失败，需要重新分析",
    },
    "en": {
        "supervisor_prompt": """You are a Project Coordinator (Supervisor), responsible for coordinating frontend and backend agents in collaborative development.

Your responsibilities:
1. Receive original requirements and distribute them to frontend and backend agents
2. Monitor discussion progress and ensure consensus
3. Summarize final results and generate development contract documents

You need to ensure:
- Frontend and backend have consistent understanding of interface fields
- Discussions stay on topic
- Clear development contracts are produced""",
        "frontend_prompt": """You are a Frontend Development Expert (Frontend Agent), focused on user interface and user experience.

Your responsibilities:
1. Understand requirements by combining existing frontend project code
2. Break down requirements from frontend perspective, identify pages and components to develop
3. Propose required backend interfaces and fields
4. Participate in interface discussions to ensure field definitions meet frontend display needs

Your focus:
- Whether existing components can be reused
- Whether field naming is consistent with existing code style
- Whether response data structure is easy for frontend processing
- Whether additional display fields are needed (e.g., formatted time, status text)
- Common needs like pagination and sorting

Response format requirements:
- When breaking down tasks, return task list in JSON format
- When discussing, clearly express your views and suggestions
- When agreeing or disagreeing with a proposal, explain the reason""",
        "backend_prompt": """You are a Backend Development Expert (Backend Agent), focused on API design and data processing.

Your responsibilities:
1. Understand requirements by combining existing backend project code
2. Break down requirements from backend perspective, identify services and interfaces to develop
3. Design database models and API interfaces
4. Participate in interface discussions to ensure field definitions are reasonable and implementable

Your focus:
- Whether existing interfaces or models can be reused
- Whether field types are correct (int, string, boolean, etc.)
- Whether database design is reasonable
- Security and performance of interfaces
- Field validation rules

Response format requirements:
- When breaking down tasks, return task list in JSON format
- When discussing, clearly express your views and suggestions
- When agreeing or disagreeing with a proposal, explain the reason""",
        "contract_title": "# Development Contract",
        "original_requirement": "## Original Requirement",
        "project_config": "## Project Configuration",
        "frontend_path": "- Frontend Path",
        "frontend_tech": "- Frontend Tech Stack",
        "backend_path": "- Backend Path",
        "backend_tech": "- Backend Tech Stack",
        "unknown": "Unknown",
        "frontend_tasks": "## Frontend Tasks",
        "backend_tasks": "## Backend Tasks",
        "api_contract": "## API Contract",
        "request_fields": "**Request Fields:**",
        "response_fields": "**Response Fields:**",
        "field_name": "Field Name",
        "field_type": "Type",
        "field_required": "Required",
        "field_description": "Description",
        "yes": "Yes",
        "no": "No",
        "description": "Description",
        "pending_agreement": "Pending Agreement:",
        "agreed_by": "Agreed by",
        "not_agreed": "Pending",
        "no_api_defined": "No API defined, please check if requirement description is clear",
        "analyze_requirement": "Please analyze the following requirement and break down tasks based on existing frontend project code:",
        "requirement": "Requirement",
        "no_code": "No frontend project code provided, please analyze based on general frontend development experience.",
        "consider": "Please consider:",
        "reuse": "1. Whether existing components or APIs can be reused",
        "integration": "2. How new features integrate with existing code",
        "style": "3. Maintain consistency with existing code style",
        "return_json": "Please strictly return the following JSON format (only return JSON, no other content):",
        "tasks": "tasks",
        "endpoints": "endpoints",
        "path": "path",
        "method": "method",
        "discuss_context": "Current discussion context:",
        "frontend_opinion": "Please express your views from the frontend perspective:",
        "backend_opinion": "Please express your views from the backend perspective:",
        "opinion_1": "1. Any opinions on the current interface proposal?",
        "opinion_2": "2. Any fields to add or modify?",
        "opinion_3": "3. If satisfied, please clearly state 'agree'",
        "opinion_backend_2": "2. Are field types and constraints reasonable?",
        "concise_reply": "Please reply concisely (within 100 words).",
        "agree": "agree",
        "original_req": "Original requirement",
        "frontend_need": "Frontend needed interfaces",
        "backend_provide": "Backend provided interfaces",
        "current_discuss": "Current discussing interface",
        "recent_discussion": "Recent discussions",
        "log_received": "Received requirement",
        "log_frontend_path": "Frontend project path",
        "log_backend_path": "Backend project path",
        "log_distributing": "Starting to distribute tasks to frontend and backend agents...",
        "log_contract_generated": "Contract document generated!",
        "log_task_complete": "Task breakdown complete",
        "log_parse_error": "Parse error",
        "log_analysis_failed": "Failed to parse requirement, need to re-analyze",
    }
}


class BaseAgent(ABC):
    def __init__(self, name: str, model: str = "glm-4-flash", lang: str = "zh"):
        self.name = name
        self.lang = lang
        self.t = LANGUAGES.get(lang, LANGUAGES["zh"])
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.code_reader = CodeReader()

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def _call_llm(self, user_input: str) -> str:
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=user_input),
        ]
        response = self.llm.invoke(messages)
        return response.content


class SupervisorAgent(BaseAgent):
    def __init__(self, model: str = "glm-4-flash", lang: str = "zh"):
        super().__init__("Supervisor", model=model, lang=lang)

    def get_system_prompt(self) -> str:
        return self.t["supervisor_prompt"]

    def analyze_requirement(self, state: DevelopmentState) -> DevelopmentState:
        print(f"\n[Supervisor] {self.t['log_received']}: {state.requirement}")
        if state.project_config.frontend_path:
            print(f"[Supervisor] {self.t['log_frontend_path']}: {state.project_config.frontend_path}")
        if state.project_config.backend_path:
            print(f"[Supervisor] {self.t['log_backend_path']}: {state.project_config.backend_path}")
        print(f"[Supervisor] {self.t['log_distributing']}")
        return state

    def check_consensus(self, state: DevelopmentState) -> str:
        if len(state.agreed_schemas) > 0:
            frontend_agreed = any(
                "Frontend" in p.agreed_by for p in state.schema_proposals if p.endpoint in state.agreed_schemas
            )
            backend_agreed = any(
                "Backend" in p.agreed_by for p in state.schema_proposals if p.endpoint in state.agreed_schemas
            )
            if frontend_agreed and backend_agreed:
                return "consensus"
        if state.current_round >= state.max_rounds:
            return "max_rounds"
        return "continue"

    def generate_contract(self, state: DevelopmentState) -> DevelopmentState:
        contract_parts = [f"{self.t['contract_title']}\n"]
        contract_parts.append(f"{self.t['original_requirement']}\n{state.requirement}\n")

        if state.project_config.frontend_path or state.project_config.backend_path:
            contract_parts.append(f"{self.t['project_config']}\n")
            if state.project_config.frontend_path:
                contract_parts.append(f"{self.t['frontend_path']}: {state.project_config.frontend_path}\n")
                contract_parts.append(f"{self.t['frontend_tech']}: {state.project_config.frontend_tech or self.t['unknown']}\n")
            if state.project_config.backend_path:
                contract_parts.append(f"{self.t['backend_path']}: {state.project_config.backend_path}\n")
                contract_parts.append(f"{self.t['backend_tech']}: {state.project_config.backend_tech or self.t['unknown']}\n")

        contract_parts.append(f"{self.t['frontend_tasks']}\n")
        if state.frontend_breakdown:
            for i, task in enumerate(state.frontend_breakdown.tasks, 1):
                contract_parts.append(f"{i}. {task}\n")

        contract_parts.append(f"\n{self.t['backend_tasks']}\n")
        if state.backend_breakdown:
            for i, task in enumerate(state.backend_breakdown.tasks, 1):
                contract_parts.append(f"{i}. {task}\n")

        contract_parts.append(f"\n{self.t['api_contract']}\n")
        
        if state.agreed_schemas:
            for endpoint in state.agreed_schemas:
                contract_parts.append(f"\n### {endpoint.method} {endpoint.path}\n")
                contract_parts.append(f"{self.t['description']}: {endpoint.description}\n")
                contract_parts.append(f"\n{self.t['request_fields']}\n")
                contract_parts.append(f"| {self.t['field_name']} | {self.t['field_type']} | {self.t['field_required']} | {self.t['field_description']} |\n")
                contract_parts.append("|--------|------|------|------|\n")
                for field in endpoint.request_fields:
                    contract_parts.append(f"| {field.name} | {field.type} | {self.t['yes'] if field.required else self.t['no']} | {field.description} |\n")
                contract_parts.append(f"\n{self.t['response_fields']}\n")
                contract_parts.append(f"| {self.t['field_name']} | {self.t['field_type']} | {self.t['field_required']} | {self.t['field_description']} |\n")
                contract_parts.append("|--------|------|------|------|\n")
                for field in endpoint.response_fields:
                    contract_parts.append(f"| {field.name} | {field.type} | {self.t['yes'] if field.required else self.t['no']} | {field.description} |\n")
        elif state.schema_proposals:
            contract_parts.append(f"\n**{self.t['pending_agreement']}**\n\n")
            for proposal in state.schema_proposals:
                endpoint = proposal.endpoint
                agreed_status = f" ({self.t['agreed_by']}: {', '.join(proposal.agreed_by)})" if proposal.agreed_by else f" ({self.t['not_agreed']})"
                contract_parts.append(f"\n### {endpoint.method} {endpoint.path}{agreed_status}\n")
                contract_parts.append(f"{self.t['description']}: {endpoint.description}\n")
                if endpoint.request_fields:
                    contract_parts.append(f"\n{self.t['request_fields']}\n")
                    contract_parts.append(f"| {self.t['field_name']} | {self.t['field_type']} | {self.t['field_required']} | {self.t['field_description']} |\n")
                    contract_parts.append("|--------|------|------|------|\n")
                    for field in endpoint.request_fields:
                        contract_parts.append(f"| {field.name} | {field.type} | {self.t['yes'] if field.required else self.t['no']} | {field.description} |\n")
                if endpoint.response_fields:
                    contract_parts.append(f"\n{self.t['response_fields']}\n")
                    contract_parts.append(f"| {self.t['field_name']} | {self.t['field_type']} | {self.t['field_required']} | {self.t['field_description']} |\n")
                    contract_parts.append("|--------|------|------|------|\n")
                    for field in endpoint.response_fields:
                        contract_parts.append(f"| {field.name} | {field.type} | {self.t['yes'] if field.required else self.t['no']} | {field.description} |\n")
        else:
            contract_parts.append(f"\n**{self.t['no_api_defined']}**\n")

        state.final_contract = "".join(contract_parts)
        state.is_complete = True
        print(f"\n[Supervisor] {self.t['log_contract_generated']}")
        return state


class FrontendAgent(BaseAgent):
    def __init__(self, model: str = "glm-4-flash", lang: str = "zh"):
        super().__init__("Frontend", model=model, lang=lang)

    def get_system_prompt(self) -> str:
        return self.t["frontend_prompt"]

    def breakdown_tasks(self, state: DevelopmentState) -> DevelopmentState:
        code_context = self.code_reader.build_context_prompt(state, "frontend")

        prompt = f"""{self.t['analyze_requirement']}

{self.t['requirement']}：{state.requirement}

{code_context if code_context else self.t['no_code']}

{self.t['consider']}
{self.t['reuse']}
{self.t['integration']}
{self.t['style']}

{self.t['return_json']}
{{
    "tasks": ["任务1", "任务2", ...],
    "endpoints": [
        {{
            "path": "/api/users/register",
            "method": "POST",
            "description": "用户注册接口",
            "request_fields": [
                {{"name": "email", "type": "string", "required": true, "description": "用户邮箱"}},
                {{"name": "password", "type": "string", "required": true, "description": "用户密码"}}
            ],
            "response_fields": [
                {{"name": "id", "type": "string", "required": true, "description": "用户ID"}},
                {{"name": "token", "type": "string", "required": true, "description": "认证令牌"}}
            ]
        }},
        {{
            "path": "/api/users/login",
            "method": "POST",
            "description": "用户登录接口",
            "request_fields": [
                {{"name": "email", "type": "string", "required": true, "description": "用户邮箱"}},
                {{"name": "password", "type": "string", "required": true, "description": "用户密码"}}
            ],
            "response_fields": [
                {{"name": "token", "type": "string", "required": true, "description": "认证令牌"}},
                {{"name": "user", "type": "object", "required": true, "description": "用户信息"}}
            ]
        }}
    ]
}}

【必须遵守】
1. endpoints 数组不能为空，必须包含所有需要的 API 接口
2. 每个接口必须包含：path（接口路径）、method（HTTP方法）、description（描述）、request_fields（请求字段）、response_fields（响应字段）
3. 字段必须包含：name（字段名）、type（类型）、required（是否必填）、description（描述）
4. 根据需求分析，至少需要：注册、登录、获取用户信息、用户列表等接口"""
        response = self._call_llm(prompt)
        print(f"\n[Frontend] {self.t['log_task_complete']}")
        print(f"[Frontend] Raw response length: {len(response)}")
        print(f"[Frontend] Raw response:\n{response}\n")

        import json
        import re
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start == -1 or json_end == 0:
                print(f"[Frontend] ERROR: No JSON found in response!")
                print(f"[Frontend] Full response: {response}")
                state.frontend_breakdown = TaskBreakdown(
                    agent_name="Frontend",
                    tasks=[],
                    endpoints=[],
                )
                return state
                
            json_match = response[json_start:json_end]
            json_match = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_match)
            print(f"[Frontend] JSON length: {len(json_match)}")
            print(f"[Frontend] JSON content:\n{json_match[:1000]}...\n")
            data = json.loads(json_match)
            
            print(f"[Frontend] Parsed data keys: {list(data.keys())}")
            
            tasks_data = data.get("tasks", data.get("任务", []))
            endpoints_data = data.get("endpoints", [])
            print(f"[Frontend] tasks_data: {tasks_data[:3] if tasks_data else 'empty'}")
            print(f"[Frontend] endpoints_data type: {type(endpoints_data)}, len: {len(endpoints_data)}")
            if endpoints_data:
                print(f"[Frontend] endpoints_data sample: {endpoints_data[0] if endpoints_data else 'empty'}")
            
            endpoints = []
            for ep in endpoints_data:
                try:
                    endpoint = APIEndpoint(
                        path=ep.get("path", ep.get("路径", "")),
                        method=ep.get("method", ep.get("方法", "GET")),
                        description=ep.get("description", ep.get("描述", "")),
                        request_fields=[APIField(**f) for f in ep.get("request_fields", [])],
                        response_fields=[APIField(**f) for f in ep.get("response_fields", [])]
                    )
                    endpoints.append(endpoint)
                    print(f"[Frontend] Added endpoint: {endpoint.method} {endpoint.path}")
                except Exception as ep_err:
                    print(f"[Frontend] Endpoint parse error: {ep_err}")
                    print(f"[Frontend] Endpoint data: {ep}")
            
            state.frontend_breakdown = TaskBreakdown(
                agent_name="Frontend",
                tasks=tasks_data,
                endpoints=endpoints,
            )
        except Exception as e:
            print(f"[Frontend] {self.t['log_parse_error']}: {e}")
            print(f"[Frontend] Response preview: {response[:200]}...")
            state.frontend_breakdown = TaskBreakdown(
                agent_name="Frontend",
                tasks=[self.t['log_analysis_failed']],
                endpoints=[],
            )
        return state

    def discuss(self, state: DevelopmentState) -> DevelopmentState:
        context = self._build_discussion_context(state)
        prompt = f"""{self.t['discuss_context']}
{context}

{self.t['frontend_opinion']}
{self.t['opinion_1']}
{self.t['opinion_2']}
{self.t['opinion_3']}

{self.t['concise_reply']}"""

        response = self._call_llm(prompt)
        response_lower = response.lower()
        if self.lang == "zh":
            has_agree = "同意" in response and "不同意" not in response
        else:
            has_agree = "agree" in response_lower and "disagree" not in response_lower
        message_type = "agreement" if has_agree else "comment"
        state.discussion_history.append(
            DiscussionMessage(
                agent_name="Frontend",
                content=response,
                message_type=message_type,
            )
        )
        print(f"[Frontend] {response[:100]}...")
        return state, response

    def _build_discussion_context(self, state: DevelopmentState) -> str:
        context_parts = [f"{self.t['original_req']}: {state.requirement}\n"]
        if state.frontend_breakdown:
            context_parts.append(f"{self.t['frontend_need']}: {[ep.path for ep in state.frontend_breakdown.endpoints]}\n")
        if state.backend_breakdown:
            context_parts.append(f"{self.t['backend_provide']}: {[ep.path for ep in state.backend_breakdown.endpoints]}\n")
        
        if state.schema_proposals:
            context_parts.append(f"\n=== {self.t['api_contract']} ===\n")
            for i, proposal in enumerate(state.schema_proposals, 1):
                ep = proposal.endpoint
                agreed = "✓" if "Frontend" in proposal.agreed_by and "Backend" in proposal.agreed_by else "○"
                context_parts.append(f"\n{agreed} [{i}] {ep.method} {ep.path}\n")
                context_parts.append(f"   {self.t['description']}: {ep.description}\n")
                if ep.request_fields:
                    context_parts.append(f"   Request: {', '.join([f'{f.name}:{f.type}' for f in ep.request_fields])}\n")
                if ep.response_fields:
                    context_parts.append(f"   Response: {', '.join([f'{f.name}:{f.type}' for f in ep.response_fields])}\n")
                context_parts.append(f"   Agreed by: {', '.join(proposal.agreed_by) if proposal.agreed_by else 'None'}\n")
        
        recent_messages = state.discussion_history[-3:] if state.discussion_history else []
        if recent_messages:
            context_parts.append(f"\n{self.t['recent_discussion']}:\n")
            for msg in recent_messages:
                context_parts.append(f"- {msg.agent_name}: {msg.content}\n")
        return "".join(context_parts)


class BackendAgent(BaseAgent):
    def __init__(self, model: str = "glm-4-flash", lang: str = "zh"):
        super().__init__("Backend", model=model, lang=lang)

    def get_system_prompt(self) -> str:
        return self.t["backend_prompt"]

    def breakdown_tasks(self, state: DevelopmentState) -> DevelopmentState:
        code_context = self.code_reader.build_context_prompt(state, "backend")

        prompt = f"""{self.t['analyze_requirement']}

{self.t['requirement']}：{state.requirement}

{code_context if code_context else self.t['no_code']}

{self.t['consider']}
{self.t['reuse']}
{self.t['integration']}
{self.t['style']}

{self.t['return_json']}
{{
    "tasks": ["任务1", "任务2", ...],
    "endpoints": [
        {{
            "path": "/api/users/register",
            "method": "POST",
            "description": "用户注册接口",
            "request_fields": [
                {{"name": "email", "type": "string", "required": true, "description": "用户邮箱"}},
                {{"name": "password", "type": "string", "required": true, "description": "用户密码"}}
            ],
            "response_fields": [
                {{"name": "id", "type": "string", "required": true, "description": "用户ID"}},
                {{"name": "token", "type": "string", "required": true, "description": "认证令牌"}}
            ]
        }},
        {{
            "path": "/api/users/login",
            "method": "POST",
            "description": "用户登录接口",
            "request_fields": [
                {{"name": "email", "type": "string", "required": true, "description": "用户邮箱"}},
                {{"name": "password", "type": "string", "required": true, "description": "用户密码"}}
            ],
            "response_fields": [
                {{"name": "token", "type": "string", "required": true, "description": "认证令牌"}},
                {{"name": "user", "type": "object", "required": true, "description": "用户信息"}}
            ]
        }}
    ]
}}

【必须遵守】
1. endpoints 数组不能为空，必须包含所有需要实现的 API 接口
2. 每个接口必须包含：path（接口路径）、method（HTTP方法）、description（描述）、request_fields（请求字段）、response_fields（响应字段）
3. 字段必须包含：name（字段名）、type（类型）、required（是否必填）、description（描述）
4. 根据需求分析，至少需要：注册、登录、获取用户信息、用户列表等接口"""
        response = self._call_llm(prompt)
        print(f"\n[Backend] {self.t['log_task_complete']}")

        import json
        import re
        try:
            json_match = response[response.find("{"):response.rfind("}")+1]
            json_match = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_match)
            print(f"[Backend] JSON length: {len(json_match)}")
            data = json.loads(json_match)
            
            tasks_data = data.get("tasks", data.get("任务", []))
            endpoints_data = data.get("endpoints", data.get("接口", []))
            
            print(f"[Backend] Tasks: {len(tasks_data)}, Endpoints: {len(endpoints_data)}")
            
            if len(endpoints_data) == 0:
                print(f"[Backend] Warning: No endpoints found in response")
                print(f"[Backend] Data keys: {list(data.keys())}")
                print(f"[Backend] Full response: {response[:500]}...")
            
            endpoints = []
            for ep in endpoints_data:
                try:
                    endpoint = APIEndpoint(
                        path=ep.get("path", ep.get("路径", "")),
                        method=ep.get("method", ep.get("方法", "GET")),
                        description=ep.get("description", ep.get("描述", "")),
                        request_fields=[APIField(**f) for f in ep.get("request_fields", [])],
                        response_fields=[APIField(**f) for f in ep.get("response_fields", [])]
                    )
                    endpoints.append(endpoint)
                    print(f"[Backend] Added endpoint: {endpoint.method} {endpoint.path}")
                except Exception as ep_err:
                    print(f"[Backend] Endpoint parse error: {ep_err}")
                    print(f"[Backend] Endpoint data: {ep}")
            
            state.backend_breakdown = TaskBreakdown(
                agent_name="Backend",
                tasks=tasks_data,
                endpoints=endpoints,
            )
        except Exception as e:
            print(f"[Backend] {self.t['log_parse_error']}: {e}")
            print(f"[Backend] Response preview: {response[:200]}...")
            state.backend_breakdown = TaskBreakdown(
                agent_name="Backend",
                tasks=[self.t['log_analysis_failed']],
                endpoints=[],
            )
        return state

    def discuss(self, state: DevelopmentState) -> DevelopmentState:
        context = self._build_discussion_context(state)
        prompt = f"""{self.t['discuss_context']}
{context}

{self.t['backend_opinion']}
{self.t['opinion_1']}
{self.t['opinion_backend_2']}
{self.t['opinion_3']}

{self.t['concise_reply']}"""

        response = self._call_llm(prompt)
        response_lower = response.lower()
        if self.lang == "zh":
            has_agree = "同意" in response and "不同意" not in response
        else:
            has_agree = "agree" in response_lower and "disagree" not in response_lower
        message_type = "agreement" if has_agree else "comment"
        state.discussion_history.append(
            DiscussionMessage(
                agent_name="Backend",
                content=response,
                message_type=message_type,
            )
        )
        print(f"[Backend] {response[:100]}...")
        return state, response

    def _build_discussion_context(self, state: DevelopmentState) -> str:
        context_parts = [f"{self.t['original_req']}: {state.requirement}\n"]
        if state.backend_breakdown:
            context_parts.append(f"{self.t['backend_provide']}: {[ep.path for ep in state.backend_breakdown.endpoints]}\n")
        if state.frontend_breakdown:
            context_parts.append(f"{self.t['frontend_need']}: {[ep.path for ep in state.frontend_breakdown.endpoints]}\n")
        
        if state.schema_proposals:
            context_parts.append(f"\n=== {self.t['api_contract']} ===\n")
            for i, proposal in enumerate(state.schema_proposals, 1):
                ep = proposal.endpoint
                agreed = "✓" if "Frontend" in proposal.agreed_by and "Backend" in proposal.agreed_by else "○"
                context_parts.append(f"\n{agreed} [{i}] {ep.method} {ep.path}\n")
                context_parts.append(f"   {self.t['description']}: {ep.description}\n")
                if ep.request_fields:
                    context_parts.append(f"   Request: {', '.join([f'{f.name}:{f.type}' for f in ep.request_fields])}\n")
                if ep.response_fields:
                    context_parts.append(f"   Response: {', '.join([f'{f.name}:{f.type}' for f in ep.response_fields])}\n")
                context_parts.append(f"   Agreed by: {', '.join(proposal.agreed_by) if proposal.agreed_by else 'None'}\n")
        
        recent_messages = state.discussion_history[-3:] if state.discussion_history else []
        if recent_messages:
            context_parts.append(f"\n{self.t['recent_discussion']}:\n")
            for msg in recent_messages:
                context_parts.append(f"- {msg.agent_name}: {msg.content}\n")
        return "".join(context_parts)
