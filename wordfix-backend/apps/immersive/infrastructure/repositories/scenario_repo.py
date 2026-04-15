"""
Concrete scenario repository implementation using Django ORM.
"""

from uuid import UUID

from apps.immersive.domain.entities import ImmersiveScenarioEntity, NPCCharacterEntity
from apps.immersive.domain.repositories import AbstractScenarioRepository
from apps.immersive.infrastructure.models import ImmersiveScenario, NPCCharacter


class DjangoScenarioRepository(AbstractScenarioRepository):
    """Django ORM implementation of scenario repository."""

    def _to_scenario_entity(self, obj: ImmersiveScenario) -> ImmersiveScenarioEntity:
        return ImmersiveScenarioEntity(
            id=obj.id,
            name=obj.name,
            name_uz=obj.name_uz,
            description=obj.description,
            description_uz=obj.description_uz,
            location=obj.location,
            difficulty=obj.difficulty,
            scene_config=obj.scene_config,
            target_vocabulary=obj.target_vocabulary,
            expected_phrases=obj.expected_phrases,
            max_turns=obj.max_turns,
            time_limit_seconds=obj.time_limit_seconds,
            xp_reward=obj.xp_reward,
            order=obj.order,
            is_active=obj.is_active,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    def _to_npc_entity(self, obj: NPCCharacter) -> NPCCharacterEntity:
        return NPCCharacterEntity(
            id=obj.id,
            scenario_id=obj.scenario_id,
            name=obj.name,
            role=obj.role,
            role_uz=obj.role_uz,
            personality=obj.personality,
            avatar_config=obj.avatar_config,
            initial_greeting=obj.initial_greeting,
            system_prompt=obj.system_prompt,
            voice_config=obj.voice_config,
            is_active=obj.is_active,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    def list_all(self, difficulty: str | None = None, location: str | None = None) -> list[ImmersiveScenarioEntity]:
        qs = ImmersiveScenario.objects.filter(is_active=True)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if location:
            qs = qs.filter(location=location)
        return [self._to_scenario_entity(obj) for obj in qs]

    def get_by_id(self, scenario_id: UUID) -> ImmersiveScenarioEntity:
        obj = ImmersiveScenario.objects.get(id=scenario_id, is_active=True)
        return self._to_scenario_entity(obj)

    def get_npcs(self, scenario_id: UUID) -> list[NPCCharacterEntity]:
        qs = NPCCharacter.objects.filter(scenario_id=scenario_id, is_active=True)
        return [self._to_npc_entity(obj) for obj in qs]

    def get_npc_by_id(self, npc_id: UUID) -> NPCCharacterEntity:
        obj = NPCCharacter.objects.get(id=npc_id, is_active=True)
        return self._to_npc_entity(obj)
