import os
import re
from pathlib import Path
from state import DevelopmentState, CodeContext, APIEndpoint, APIField


class CodeReader:
    FRONTEND_PATTERNS = {
        "api": ["**/api/**/*.{ts,tsx,js,jsx}", "**/services/**/*.{ts,tsx,js,jsx}"],
        "types": ["**/types/**/*.{ts,tsx}", "**/interfaces/**/*.{ts,tsx}"],
        "components": ["**/components/**/*.{tsx,jsx,vue}"],
        "pages": ["**/pages/**/*.{tsx,jsx,vue}", "**/views/**/*.{tsx,jsx,vue}"],
        "store": ["**/store/**/*.{ts,js}", "**/redux/**/*.{ts,js}", "**/vuex/**/*.{ts,js}"],
    }

    BACKEND_PATTERNS = {
        "controllers": ["**/controllers/**/*.{py,js,ts,go,java}"],
        "routes": ["**/routes/**/*.{py,js,ts,go,java}", "**/routers/**/*.{py,js,ts,go,java}"],
        "models": ["**/models/**/*.{py,js,ts,go,java}", "**/entities/**/*.{py,js,ts,go,java}"],
        "services": ["**/services/**/*.{py,js,ts,go,java}"],
        "schemas": ["**/schemas/**/*.{py,js,ts}", "**/dto/**/*.{py,js,ts}"],
    }

    MAX_FILE_SIZE = 50000
    MAX_FILES_PER_CATEGORY = 5

    def read_project(self, state: DevelopmentState) -> DevelopmentState:
        if state.project_config.frontend_path:
            state.code_context.frontend_files = self._read_frontend(state.project_config.frontend_path)
            state.code_context.frontend_files.update(
                self._detect_tech_stack(state.project_config.frontend_path, "frontend", state)
            )

        if state.project_config.backend_path:
            state.code_context.backend_files = self._read_backend(state.project_config.backend_path)
            state.code_context.existing_apis = self._extract_existing_apis(state.project_config.backend_path)
            state.code_context.db_models = self._extract_db_models(state.project_config.backend_path)
            self._detect_tech_stack(state.project_config.backend_path, "backend", state)

        return state

    def _read_frontend(self, path: str) -> dict[str, str]:
        files = {}
        project_path = Path(path)
        if not project_path.exists():
            print(f"[CodeReader] 前端路径不存在: {path}")
            return files

        for category, patterns in self.FRONTEND_PATTERNS.items():
            count = 0
            for pattern in patterns:
                for file_path in project_path.glob(pattern):
                    if count >= self.MAX_FILES_PER_CATEGORY:
                        break
                    content = self._read_file(file_path)
                    if content:
                        key = f"frontend/{category}/{file_path.name}"
                        files[key] = content
                        count += 1
                if count >= self.MAX_FILES_PER_CATEGORY:
                    break

        config_files = ["package.json", "tsconfig.json", "vite.config.*", "vue.config.*"]
        for pattern in config_files:
            for file_path in project_path.glob(pattern):
                content = self._read_file(file_path)
                if content:
                    files[f"frontend/config/{file_path.name}"] = content

        return files

    def _read_backend(self, path: str) -> dict[str, str]:
        files = {}
        project_path = Path(path)
        if not project_path.exists():
            print(f"[CodeReader] 后端路径不存在: {path}")
            return files

        for category, patterns in self.BACKEND_PATTERNS.items():
            count = 0
            for pattern in patterns:
                for file_path in project_path.glob(pattern):
                    if count >= self.MAX_FILES_PER_CATEGORY:
                        break
                    content = self._read_file(file_path)
                    if content:
                        key = f"backend/{category}/{file_path.name}"
                        files[key] = content
                        count += 1
                if count >= self.MAX_FILES_PER_CATEGORY:
                    break

        config_files = ["requirements.txt", "pyproject.toml", "go.mod", "package.json", "pom.xml"]
        for config_file in config_files:
            file_path = project_path / config_file
            if file_path.exists():
                content = self._read_file(file_path)
                if content:
                    files[f"backend/config/{config_file}"] = content

        return files

    def _read_file(self, file_path: Path) -> str | None:
        try:
            if file_path.stat().st_size > self.MAX_FILE_SIZE:
                return None
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[CodeReader] 读取文件失败 {file_path}: {e}")
            return None

    def _detect_tech_stack(self, path: str, project_type: str, state: DevelopmentState) -> dict[str, str]:
        project_path = Path(path)
        tech_info = {}

        package_json = project_path / "package.json"
        if package_json.exists():
            content = self._read_file(package_json)
            if content:
                tech_info["package.json"] = content
                if project_type == "frontend":
                    if "react" in content.lower():
                        state.project_config.frontend_tech = "React"
                    elif "vue" in content.lower():
                        state.project_config.frontend_tech = "Vue"
                    elif "angular" in content.lower():
                        state.project_config.frontend_tech = "Angular"
                elif project_type == "backend":
                    if "express" in content.lower():
                        state.project_config.backend_tech = "Node.js/Express"
                    elif "nestjs" in content.lower() or "@nestjs" in content.lower():
                        state.project_config.backend_tech = "NestJS"

        pyproject = project_path / "pyproject.toml"
        requirements = project_path / "requirements.txt"
        if pyproject.exists() or requirements.exists():
            content = self._read_file(pyproject if pyproject.exists() else requirements)
            if content:
                tech_info["python_config"] = content
                if project_type == "backend":
                    if "fastapi" in content.lower():
                        state.project_config.backend_tech = "Python/FastAPI"
                    elif "django" in content.lower():
                        state.project_config.backend_tech = "Python/Django"
                    elif "flask" in content.lower():
                        state.project_config.backend_tech = "Python/Flask"

        go_mod = project_path / "go.mod"
        if go_mod.exists():
            state.project_config.backend_tech = "Go"

        return tech_info

    def _extract_existing_apis(self, path: str) -> list[APIEndpoint]:
        apis = []
        project_path = Path(path)
        if not project_path.exists():
            return apis

        for file_path in project_path.glob("**/*.py"):
            content = self._read_file(file_path)
            if not content:
                continue

            fastapi_routes = re.findall(
                r'@(?:router|app)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                content,
                re.IGNORECASE,
            )
            for method, route in fastapi_routes:
                apis.append(APIEndpoint(path=route, method=method.upper(), description=f"现有接口: {file_path.name}"))

            flask_routes = re.findall(
                r'@app\.route\s*\(\s*["\']([^"\']+)["\'].*?methods\s*=\s*\[([^\]]+)\]',
                content,
                re.IGNORECASE,
            )
            for route, methods in flask_routes:
                method = "GET" if "GET" in methods.upper() else "POST"
                apis.append(APIEndpoint(path=route, method=method, description=f"Flask路由: {file_path.name}"))

        return apis[:20]

    def _extract_db_models(self, path: str) -> list[str]:
        models = []
        project_path = Path(path)
        if not project_path.exists():
            return models

        for file_path in project_path.glob("**/models/**/*.py"):
            content = self._read_file(file_path)
            if not content:
                continue

            class_names = re.findall(r'class\s+(\w+)\s*\([^)]*(?:Model|Base|Table)[^)]*\)', content, re.IGNORECASE)
            models.extend(class_names)

        return list(set(models))[:10]

    def build_context_prompt(self, state: DevelopmentState, agent_type: str) -> str:
        context_parts = []

        if agent_type == "frontend":
            if state.project_config.frontend_tech:
                context_parts.append(f"前端技术栈: {state.project_config.frontend_tech}")

            if state.code_context.frontend_files:
                context_parts.append("\n现有前端代码结构:")
                for file_key, content in list(state.code_context.frontend_files.items())[:5]:
                    context_parts.append(f"\n--- {file_key} ---")
                    context_parts.append(content[:2000])

            if state.code_context.existing_apis:
                context_parts.append("\n后端现有接口:")
                for api in state.code_context.existing_apis[:10]:
                    context_parts.append(f"  {api.method} {api.path}")

        elif agent_type == "backend":
            if state.project_config.backend_tech:
                context_parts.append(f"后端技术栈: {state.project_config.backend_tech}")

            if state.code_context.backend_files:
                context_parts.append("\n现有后端代码结构:")
                for file_key, content in list(state.code_context.backend_files.items())[:5]:
                    context_parts.append(f"\n--- {file_key} ---")
                    context_parts.append(content[:2000])

            if state.code_context.existing_apis:
                context_parts.append("\n现有接口:")
                for api in state.code_context.existing_apis[:10]:
                    context_parts.append(f"  {api.method} {api.path}")

            if state.code_context.db_models:
                context_parts.append(f"\n现有数据库模型: {', '.join(state.code_context.db_models)}")

        return "\n".join(context_parts)
