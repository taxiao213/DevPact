from state import DevelopmentState, SchemaProposal, APIEndpoint


LANGUAGES = {
    "zh": {
        "created_proposals": "创建了接口提案",
        "interface_agreed": "接口已达成一致!",
    },
    "en": {
        "created_proposals": "Created interface proposals",
        "interface_agreed": "Interface agreed!",
    }
}


class DiscussionManager:
    def __init__(self, lang: str = "zh"):
        self.current_endpoint_index = 0
        self.lang = lang
        self.t = LANGUAGES.get(lang, LANGUAGES["zh"])

    def create_proposals(self, state: DevelopmentState) -> DevelopmentState:
        frontend_endpoints = state.frontend_breakdown.endpoints if state.frontend_breakdown else []
        backend_endpoints = state.backend_breakdown.endpoints if state.backend_breakdown else []

        print(f"[Discussion] Frontend endpoints: {len(frontend_endpoints)}")
        print(f"[Discussion] Backend endpoints: {len(backend_endpoints)}")
        
        if frontend_endpoints:
            print(f"[Discussion] Frontend paths: {[ep.path for ep in frontend_endpoints]}")
        if backend_endpoints:
            print(f"[Discussion] Backend paths: {[ep.path for ep in backend_endpoints]}")

        merged_endpoints = self._merge_endpoints(frontend_endpoints, backend_endpoints)

        for endpoint in merged_endpoints:
            proposal = SchemaProposal(
                endpoint=endpoint,
                proposed_by="Supervisor",
                agreed_by=[],
            )
            state.schema_proposals.append(proposal)

        print(f"\n[Discussion] {self.t['created_proposals']}: {len(state.schema_proposals)}")
        return state

    def _merge_endpoints(
        self, frontend_endpoints: list[APIEndpoint], backend_endpoints: list[APIEndpoint]
    ) -> list[APIEndpoint]:
        merged = {}
        for ep in frontend_endpoints:
            key = f"{ep.method}:{ep.path}"
            if key not in merged:
                merged[key] = ep
            else:
                merged[key] = self._combine_fields(merged[key], ep)

        for ep in backend_endpoints:
            key = f"{ep.method}:{ep.path}"
            if key not in merged:
                merged[key] = ep
            else:
                merged[key] = self._combine_fields(merged[key], ep)

        return list(merged.values())

    def _combine_fields(self, ep1: APIEndpoint, ep2: APIEndpoint) -> APIEndpoint:
        request_fields = {f.name: f for f in ep1.request_fields}
        for f in ep2.request_fields:
            if f.name not in request_fields:
                request_fields[f.name] = f

        response_fields = {f.name: f for f in ep1.response_fields}
        for f in ep2.response_fields:
            if f.name not in response_fields:
                response_fields[f.name] = f

        return APIEndpoint(
            path=ep1.path,
            method=ep1.method,
            description=ep1.description or ep2.description,
            request_fields=list(request_fields.values()),
            response_fields=list(response_fields.values()),
        )

    def process_agreements(self, state: DevelopmentState) -> DevelopmentState:
        recent_messages = state.discussion_history[-2:] if len(state.discussion_history) >= 2 else state.discussion_history

        for msg in recent_messages:
            if msg.message_type == "agreement":
                for proposal in state.schema_proposals:
                    if msg.agent_name not in proposal.agreed_by:
                        proposal.agreed_by.append(msg.agent_name)

        for proposal in state.schema_proposals:
            if "Frontend" in proposal.agreed_by and "Backend" in proposal.agreed_by:
                if proposal.endpoint not in state.agreed_schemas:
                    state.agreed_schemas.append(proposal.endpoint)
                    print(f"\n[Discussion] {proposal.endpoint.path} {self.t['interface_agreed']}")

        return state

    def check_round_complete(self, state: DevelopmentState) -> bool:
        return len(state.agreed_schemas) == len(state.schema_proposals)
