from typing import Annotated
from pydantic import BaseModel, Field
from operator import add


class APIField(BaseModel):
    name: str = Field(description="字段名称")
    type: str = Field(description="字段类型")
    required: bool = Field(default=True, description="是否必填")
    description: str = Field(default="", description="字段描述")


class APIEndpoint(BaseModel):
    path: str = Field(description="接口路径")
    method: str = Field(description="HTTP方法")
    description: str = Field(description="接口描述")
    request_fields: list[APIField] = Field(default_factory=list, description="请求字段")
    response_fields: list[APIField] = Field(default_factory=list, description="响应字段")


class TaskBreakdown(BaseModel):
    agent_name: str = Field(description="Agent名称")
    tasks: list[str] = Field(description="拆解的任务列表")
    endpoints: list[APIEndpoint] = Field(default_factory=list, description="涉及的接口")


class DiscussionMessage(BaseModel):
    agent_name: str = Field(description="发言的Agent")
    content: str = Field(description="发言内容")
    message_type: str = Field(default="comment", description="消息类型: comment/proposal/agreement/disagreement")


class SchemaProposal(BaseModel):
    endpoint: APIEndpoint = Field(description="接口定义")
    proposed_by: str = Field(description="提议者")
    agreed_by: list[str] = Field(default_factory=list, description="同意的Agent列表")


class ProjectConfig(BaseModel):
    frontend_path: str = Field(default="", description="前端项目路径")
    backend_path: str = Field(default="", description="后端项目路径")
    frontend_tech: str = Field(default="", description="前端技术栈")
    backend_tech: str = Field(default="", description="后端技术栈")


class CodeContext(BaseModel):
    frontend_files: dict[str, str] = Field(default_factory=dict, description="前端关键文件内容")
    backend_files: dict[str, str] = Field(default_factory=dict, description="后端关键文件内容")
    existing_apis: list[APIEndpoint] = Field(default_factory=list, description="现有接口列表")
    db_models: list[str] = Field(default_factory=list, description="数据库模型")


class DevelopmentState(BaseModel):
    requirement: str = Field(default="", description="原始需求")
    project_config: ProjectConfig = Field(default_factory=ProjectConfig, description="项目配置")
    code_context: CodeContext = Field(default_factory=CodeContext, description="代码上下文")
    frontend_breakdown: TaskBreakdown | None = Field(default=None, description="前端任务拆解")
    backend_breakdown: TaskBreakdown | None = Field(default=None, description="后端任务拆解")
    discussion_history: Annotated[list[DiscussionMessage], add] = Field(default_factory=list, description="讨论历史")
    schema_proposals: list[SchemaProposal] = Field(default_factory=list, description="接口提案")
    agreed_schemas: list[APIEndpoint] = Field(default_factory=list, description="达成一致的接口定义")
    current_round: int = Field(default=0, description="当前讨论轮次")
    max_rounds: int = Field(default=3, description="最大讨论轮次")
    is_complete: bool = Field(default=False, description="是否完成协商")
    final_contract: str = Field(default="", description="最终契约文档")
