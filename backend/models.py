from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Literal
import uuid

AuthProvider = Literal["phone_sms"]
UserStatus = Literal["active", "blocked"]
SessionStatus = Literal["active", "expired", "revoked"]
SupportedLanguage = Literal["en-US", "ja-JP", "ko-KR"]
AppearanceMode = Literal["ai_generate", "upload_photo"]


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass
class AIAppearanceConfig:
    mode: AppearanceMode
    style_keywords: list[str]
    custom_prompt: str
    uploaded_photo_url: str | None = None
    generated_image_url: str | None = None
    ai_provider: str = "mock-ai-provider"
    ai_model: str = "mock-image-v1"
    final_generation_prompt: str = ""
    generated_at: str = field(default_factory=now_iso)


@dataclass
class AIPersonalityConfig:
    preset_code: str
    preset_name: str
    tone_tags: list[str]
    inner_voice: str
    custom_prompt: str = ""
    final_system_prompt: str = ""
    customized_at: str = field(default_factory=now_iso)


@dataclass
class AICompanionPersona:
    persona_id: str
    language: SupportedLanguage
    language_label: str
    accent: str
    avatar_code: str
    avatar_name: str
    archetype: str
    personality_tags: list[str]
    appearance: AIAppearanceConfig | None = None
    personality_profile: AIPersonalityConfig | None = None
    customized_at: str = field(default_factory=now_iso)
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class UserProfile:
    nickname: str = "Nexis User"
    avatar_url: str | None = None
    locale: str = "zh-CN"
    onboarding_completed: bool = False
    ai_companion: AICompanionPersona | None = None


@dataclass
class UserConsent:
    agreed_user_agreement: bool
    agreed_privacy_policy: bool
    agreed_at: str = field(default_factory=now_iso)


@dataclass
class User:
    user_id: str
    phone: str
    country_code: str = "+86"
    status: UserStatus = "active"
    auth_provider: AuthProvider = "phone_sms"
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    last_login_at: str | None = None
    profile: UserProfile = field(default_factory=UserProfile)
    consent: UserConsent | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class VerificationCode:
    code_id: str
    phone: str
    code: str
    channel: Literal["sms"] = "sms"
    expires_at: str = ""
    is_used: bool = False
    sent_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LoginSession:
    session_id: str
    user_id: str
    access_token: str
    refresh_token: str
    status: SessionStatus = "active"
    created_at: str = field(default_factory=now_iso)
    expires_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AICompanionCustomizationRecord:
    record_id: str
    user_id: str
    persona: AICompanionPersona
    source_page: str = "onboarding_customize_companion"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return asdict(self)
