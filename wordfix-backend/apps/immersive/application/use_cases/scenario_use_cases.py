"""Scenario listing use cases."""

from uuid import UUID


class ListScenariosUseCase:
    """List available immersive scenarios."""

    def __init__(self, scenario_repo):
        self.scenario_repo = scenario_repo

    def execute(self, difficulty: str | None = None, location: str | None = None) -> list[dict]:
        scenarios = self.scenario_repo.list_all(difficulty=difficulty, location=location)
        return [
            {
                "id": str(s.id),
                "name": s.name,
                "name_uz": s.name_uz,
                "description": s.description,
                "description_uz": s.description_uz,
                "location": s.location,
                "difficulty": s.difficulty,
                "max_turns": s.max_turns,
                "time_limit_seconds": s.time_limit_seconds,
                "xp_reward": s.xp_reward,
                "scene_config": s.scene_config,
            }
            for s in scenarios
        ]


class GetScenarioDetailUseCase:
    """Get scenario detail with NPCs."""

    def __init__(self, scenario_repo):
        self.scenario_repo = scenario_repo

    def execute(self, scenario_id: str) -> dict:
        scenario_id = UUID(str(scenario_id))
        scenario = self.scenario_repo.get_by_id(scenario_id)
        npcs = self.scenario_repo.get_npcs(scenario_id)
        return {
            "id": str(scenario.id),
            "name": scenario.name,
            "name_uz": scenario.name_uz,
            "description": scenario.description,
            "description_uz": scenario.description_uz,
            "location": scenario.location,
            "difficulty": scenario.difficulty,
            "scene_config": scenario.scene_config,
            "target_vocabulary": scenario.target_vocabulary,
            "max_turns": scenario.max_turns,
            "time_limit_seconds": scenario.time_limit_seconds,
            "xp_reward": scenario.xp_reward,
            "npcs": [
                {
                    "id": str(npc.id),
                    "name": npc.name,
                    "role": npc.role,
                    "role_uz": npc.role_uz,
                    "avatar_config": npc.avatar_config,
                    "initial_greeting": npc.initial_greeting,
                }
                for npc in npcs
            ],
        }
