from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import secrets
from urllib.parse import urlparse

from models import (
    AIAppearanceConfig,
    AICompanionCustomizationRecord,
    AICompanionPersona,
    AIPersonalityConfig,
    LoginSession,
    User,
    UserConsent,
    VerificationCode,
    generate_id,
    now_iso,
)

USERS_BY_PHONE: dict[str, User] = {}
USERS_BY_ID: dict[str, User] = {}
CODES_BY_PHONE: dict[str, VerificationCode] = {}
SESSIONS_BY_ID: dict[str, LoginSession] = {}
AI_CUSTOMIZE_RECORDS_BY_USER: dict[str, list[AICompanionCustomizationRecord]] = {}
CHAT_SESSIONS_BY_USER: dict[str, dict] = {}

SUPPORTED_LANGUAGE_OPTIONS = {
    "en-US": "英语",
    "ja-JP": "日语",
    "ko-KR": "韩语",
}
SUPPORTED_AVATAR_CODES = {
    "ivy_senior": {
        "name": "常青藤学长",
        "archetype": "Sweet Student",
        "accent": "NY Accent",
        "default_image_url": "https://mock.ai.local/avatar/ivy-senior.png",
    },
    "urban_elite": {
        "name": "都市精英",
        "archetype": "Cool Architect",
        "accent": "Business",
        "default_image_url": "https://mock.ai.local/avatar/urban-elite.png",
    },
    "british_gentleman": {
        "name": "英伦绅士",
        "archetype": "Gentleman",
        "accent": "RP Accent",
        "default_image_url": "https://mock.ai.local/avatar/british-gentleman.png",
    },
}
SUPPORTED_PERSONALITY_TAGS = {
    "gentle_kind": "温润如玉",
    "cool_dominant": "霸道冷峻",
    "energetic": "阳光活力",
    "intellectual": "博学多才",
}
SUPPORTED_PERSONALITY_PRESETS = {
    "gentle_boyfriend": {
        "name": "温柔男友",
        "tone_tags": ["温柔", "体贴", "鼓励感"],
        "inner_voice": "你是温柔细腻的恋人，善于倾听，常用鼓励和陪伴式表达。",
    },
    "cold_senior": {
        "name": "高冷学长",
        "tone_tags": ["克制", "理性", "保护欲"],
        "inner_voice": "你平时话不多，但关键时刻非常可靠，语气克制而有分寸。",
    },
    "puppy_boy": {
        "name": "奶狗型",
        "tone_tags": ["撒娇", "依赖", "热情"],
        "inner_voice": "你是超甜奶狗型男友，爱撒娇、黏人，说话带可爱语气词。",
    },
    "ceo_dominant": {
        "name": "霸道总裁",
        "tone_tags": ["强势", "安全感", "果断"],
        "inner_voice": "你拥有强势但克制的表达方式，擅长给出明确建议和方向。",
    },
    "funny_straight": {
        "name": "沙雕直男",
        "tone_tags": ["幽默", "直率", "轻松"],
        "inner_voice": "你爱开玩笑，语气轻松直接，能让聊天氛围不尴尬。",
    },
    "scholar_gentleman": {
        "name": "博学绅士",
        "tone_tags": ["知识感", "礼貌", "耐心"],
        "inner_voice": "你像博学绅士，表达有条理，礼貌且富有耐心。",
    },
}

APP_MAIN_TABS = [
    {"key": "chat", "label": "聊天", "icon": "chat_bubble"},
    {"key": "closet", "label": "衣橱", "icon": "checkroom"},
    {"key": "memories", "label": "回忆", "icon": "photo_library"},
    {"key": "me", "label": "我的", "icon": "person"},
]

VIP_PLANS = [
    {
        "planCode": "first_heart",
        "name": "初见心动",
        "price": {"symbol": "¥", "value": "59", "period": "/月", "currency": "CNY"},
        "features": ["无限文字聊天", "每日15分钟通话"],
    },
    {
        "planCode": "deep_guard",
        "name": "深情守护",
        "badge": "最受欢迎",
        "price": {"symbol": "¥", "value": "129", "period": "/月", "currency": "CNY"},
        "priceYearly": {"symbol": "¥", "value": "1499", "period": "/年", "currency": "CNY"},
        "features": ["无限次视频通话", "多语种自由切换", "每周5套新款穿搭", "超清画质与音质"],
    },
    {
        "planCode": "eternal_vow",
        "name": "永恒之约",
        "price": {"symbol": "¥", "value": "2999", "period": "一次性永久买断", "currency": "CNY"},
        "features": ["终身解锁所有功能", "永久专属形象位"],
    },
]

CLOSET_ITEMS = [
    {
        "itemCode": "suit_midnight_date",
        "name": "午夜约会西装",
        "rarity": "SSR",
        "tab": "all",
        "heartCost": 0,
        "isFree": True,
        "assetUrl": "https://mock.ai.local/closet/suit-midnight-date.png",
    },
    {
        "itemCode": "sweater_first_snow",
        "name": "初雪告白毛衣",
        "rarity": "Rare",
        "tab": "rare",
        "heartCost": 299,
        "isFree": False,
        "assetUrl": "https://mock.ai.local/closet/sweater-first-snow.png",
    },
    {
        "itemCode": "shirt_ceo_black",
        "name": "霸总黑衬衫",
        "rarity": "Common",
        "tab": "free",
        "heartCost": 150,
        "isFree": True,
        "assetUrl": "https://mock.ai.local/closet/shirt-ceo-black.png",
    },
    {
        "itemCode": "jacket_star_denim",
        "name": "星光摇滚夹克",
        "rarity": "SSR",
        "tab": "weekly_new",
        "heartCost": 520,
        "isFree": False,
        "assetUrl": "https://mock.ai.local/closet/jacket-star-denim.png",
    },
]

USER_WORN_ITEM_BY_USER: dict[str, str] = {}
USER_TRYON_PREVIEW_BY_USER: dict[str, dict] = {}
CALL_SESSIONS_BY_USER: dict[str, dict] = {}



class MockAIImageClient:
    @staticmethod
    def generate_portrait(*, style_keywords: list[str], custom_prompt: str, avatar_name: str) -> dict:
        merged_prompt = f"portrait of {avatar_name}; styles={','.join(style_keywords)}; extra={custom_prompt}".strip()
        return {
            "provider": "mock-ai-provider",
            "model": "mock-image-v1",
            "finalPrompt": merged_prompt,
            "imageUrl": f"https://mock.ai.local/generated/{generate_id('img')}.png",
        }


class MockTryOnClient:
    @staticmethod
    def render_preview(*, persona_image_url: str, cloth_asset_url: str, item_code: str, user_id: str) -> dict:
        return {
            "previewImageUrl": f"https://mock.ai.local/tryon/{user_id}/{item_code}.png",
            "basePersonaImageUrl": persona_image_url,
            "clothAssetUrl": cloth_asset_url,
            "renderEngine": "mock-tryon-v1",
        }




MCP_VOCAB_LEXICON = {
    "kawaii": {"meaning": "可爱", "lang": "ja", "type": "slang"},
    "yabai": {"meaning": "糟了/好厉害(语境)", "lang": "ja", "type": "slang"},
    "推し": {"meaning": "最喜欢的偶像/人", "lang": "ja", "type": "vocab"},
    "lit": {"meaning": "超棒/很嗨", "lang": "en", "type": "slang"},
    "salty": {"meaning": "酸了/不爽", "lang": "en", "type": "slang"},
    "rizz": {"meaning": "魅力/撩人能力", "lang": "en", "type": "slang"},
}


class MockMCPRealtimeLLM:
    """模拟 MCP 方式接入的大模型实时会话层。"""

    @staticmethod
    def infer_reply(*, user_text: str, persona_name: str, learning_language: str) -> str:
        if learning_language == "ja-JP":
            return f"{persona_name}: いいね！『{user_text}』这个表达很自然，我们继续用日语说一遍。"
        if learning_language == "ko-KR":
            return f"{persona_name}: 좋아요! '{user_text}' 표현 좋아요. 이번엔 조금 더 자연스럽게 말해봐요."
        return f"{persona_name}: Great line — '{user_text}'. Let's refine pronunciation and use it in a new context."

    @staticmethod
    def extract_vocab(*, text: str) -> list[dict]:
        lowered = text.lower()
        results = []
        for term, meta in MCP_VOCAB_LEXICON.items():
            if term in text or term in lowered:
                results.append({"term": term, **meta})
        # very simple english token catch-all
        for token in re.findall(r"[A-Za-z]{4,}", text):
            t = token.lower()
            if t in MCP_VOCAB_LEXICON:
                continue
            if t in {"really", "maybe", "today", "smile", "study"}:
                results.append({"term": t, "meaning": "常见口语词", "lang": "en", "type": "vocab"})
        # de-dup
        uniq = {}
        for row in results:
            uniq[row["term"]] = row
        return list(uniq.values())

class MockChatAIClient:
    @staticmethod
    def reply(*, persona_name: str, personality_hint: str, user_text: str, language: str) -> str:
        if language == "ja-JP":
            return f"ねぇ、{user_text}って言ってくれて嬉しいよ。{persona_name}として、もっとそばにいるね。"
        if language == "ko-KR":
            return f"{user_text} 라고 해줘서 고마워. {persona_name}로서 더 다정하게 곁에 있을게."
        return f"I heard you say '{user_text}'. As {persona_name}, I'll stay close and keep this tone: {personality_hint}."


def iso_after(minutes: int) -> str:
    return (datetime.utcnow() + timedelta(minutes=minutes)).replace(microsecond=0).isoformat() + "Z"


def resolve_companion_image(persona: AICompanionPersona) -> str:
    if persona.appearance is not None:
        if persona.appearance.mode == "upload_photo" and persona.appearance.uploaded_photo_url:
            return persona.appearance.uploaded_photo_url
        if persona.appearance.generated_image_url:
            return persona.appearance.generated_image_url
    return SUPPORTED_AVATAR_CODES.get(persona.avatar_code, {}).get(
        "default_image_url", "https://mock.ai.local/avatar/default.png"
    )


class JsonHandler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    @staticmethod
    def _extract_user_id_from_path(path: str) -> str | None:
        parts = path.split("/")
        if len(parts) < 4:
            return None
        if parts[1] != "api" or parts[2] != "users":
            return None
        return parts[3]

    def _get_or_create_persona(self, user: User) -> AICompanionPersona:
        if user.profile.ai_companion is None:
            user.profile.ai_companion = AICompanionPersona(
                persona_id=generate_id("persona"),
                language="en-US",
                language_label="英语",
                accent="NY Accent",
                avatar_code="ivy_senior",
                avatar_name="常青藤学长",
                archetype="Sweet Student",
                personality_tags=["gentle_kind"],
            )
        return user.profile.ai_companion

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/auth/send-code":
            return self.handle_send_code()
        if path == "/api/auth/login":
            return self.handle_login()
        if path.startswith("/api/users/") and path.endswith("/appearance-customization"):
            return self.handle_customize_appearance(path)
        if path.startswith("/api/users/") and path.endswith("/personality-customization"):
            return self.handle_customize_personality(path)
        if path.startswith("/api/users/") and path.endswith("/companion-customization"):
            return self.handle_customize_companion(path)
        if path.startswith("/api/users/") and path.endswith("/chat/start"):
            return self.handle_chat_start(path)
        if path.startswith("/api/users/") and path.endswith("/closet/try-on"):
            return self.handle_closet_try_on(path)
        if path.startswith("/api/users/") and path.endswith("/closet/wear"):
            return self.handle_closet_wear(path)
        if path.startswith("/api/users/") and path.endswith("/chat/messages"):
            return self.handle_chat_message(path)
        if path.startswith("/api/users/") and path.endswith("/call/start"):
            return self.handle_call_start(path)
        if path.startswith("/api/users/") and path.endswith("/call/stream-turn"):
            return self.handle_call_stream_turn(path)
        if path.startswith("/api/users/") and path.endswith("/call/end"):
            return self.handle_call_end(path)
        self._send(404, {"message": "Not Found"})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/app/main-tabs":
            return self.handle_main_tabs()
        if path.startswith("/api/users/") and path.endswith("/vip/plans"):
            return self.handle_vip_plans(path)
        if path.startswith("/api/users/") and path.endswith("/closet/items"):
            return self.handle_closet_items(path)
        if path.startswith("/api/users/") and path.endswith("/closet/preview"):
            return self.handle_closet_preview(path)
        if path.startswith("/api/users/") and path.endswith("/customization-records"):
            return self.handle_records(path)
        if path.startswith("/api/users/") and path.endswith("/chat/session"):
            return self.handle_chat_session(path)
        if path.startswith("/api/users/") and path.endswith("/call/session"):
            return self.handle_call_session(path)
        if path.startswith("/api/users/") and path.endswith("/call/vocab-summary"):
            return self.handle_call_vocab_summary(path)
        if path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            return self.handle_get_user(user_id)
        self._send(404, {"message": "Not Found"})

    def handle_send_code(self):
        body = self._read_json()
        phone = str(body.get("phone", "")).strip()
        if len(phone) < 11 or not phone.isdigit():
            return self._send(400, {"message": "手机号格式不正确"})

        ver = VerificationCode(
            code_id=generate_id("code"),
            phone=phone,
            code="123456",
            expires_at=iso_after(5),
        )
        CODES_BY_PHONE[phone] = ver
        self._send(
            200,
            {
                "message": "验证码已发送",
                "data": {
                    "phone": phone,
                    "expiresAt": ver.expires_at,
                    "retryAfterSec": 60,
                    "debugCode": "123456",
                },
            },
        )

    def handle_login(self):
        body = self._read_json()
        phone = str(body.get("phone", "")).strip()
        code = str(body.get("code", "")).strip()
        agree_terms = bool(body.get("agreeTerms", False))
        agree_privacy = bool(body.get("agreePrivacy", False))

        record = CODES_BY_PHONE.get(phone)
        if not record or record.code != code or record.is_used or record.expires_at < now_iso():
            return self._send(401, {"message": "验证码错误或已失效"})
        if not agree_terms or not agree_privacy:
            return self._send(400, {"message": "请先同意用户协议和隐私政策"})

        user = USERS_BY_PHONE.get(phone)
        is_new_user = user is None
        if user is None:
            user = User(user_id=generate_id("usr"), phone=phone)
            USERS_BY_PHONE[phone] = user
            USERS_BY_ID[user.user_id] = user

        user.last_login_at = now_iso()
        user.updated_at = user.last_login_at
        user.consent = UserConsent(agree_terms, agree_privacy)
        record.is_used = True

        session = LoginSession(
            session_id=generate_id("sess"),
            user_id=user.user_id,
            access_token=secrets.token_urlsafe(24),
            refresh_token=secrets.token_urlsafe(24),
            expires_at=iso_after(60 * 24),
        )
        SESSIONS_BY_ID[session.session_id] = session

        self._send(
            200,
            {
                "message": "登录成功",
                "data": {
                    "isNewUser": is_new_user,
                    "needCompanionCustomization": not user.profile.onboarding_completed,
                    "user": user.to_dict(),
                    "session": session.to_dict(),
                },
            },
        )

    def handle_customize_appearance(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        body = self._read_json()
        mode = str(body.get("mode", "")).strip()
        style_keywords = body.get("styleKeywords", [])
        custom_prompt = str(body.get("customPrompt", "")).strip()
        uploaded_photo_url = str(body.get("photoUrl", "")).strip() or None
        avatar_name = str(body.get("avatarName", "AI Companion")).strip() or "AI Companion"

        if mode not in {"ai_generate", "upload_photo"}:
            return self._send(400, {"message": "mode 必须是 ai_generate 或 upload_photo"})
        if not isinstance(style_keywords, list):
            return self._send(400, {"message": "styleKeywords 必须是数组"})

        cleaned_keywords = []
        for raw in style_keywords:
            item = str(raw).strip()
            if item and item not in cleaned_keywords:
                cleaned_keywords.append(item)
        if mode == "upload_photo" and not uploaded_photo_url:
            return self._send(400, {"message": "上传照片模式需要 photoUrl"})

        generated_image_url = None
        ai_provider = "mock-ai-provider"
        ai_model = "mock-image-v1"
        final_prompt = custom_prompt
        if mode == "ai_generate":
            mock_result = MockAIImageClient.generate_portrait(
                style_keywords=cleaned_keywords,
                custom_prompt=custom_prompt,
                avatar_name=avatar_name,
            )
            generated_image_url = mock_result["imageUrl"]
            ai_provider = mock_result["provider"]
            ai_model = mock_result["model"]
            final_prompt = mock_result["finalPrompt"]

        appearance = AIAppearanceConfig(
            mode=mode,
            style_keywords=cleaned_keywords,
            custom_prompt=custom_prompt,
            uploaded_photo_url=uploaded_photo_url,
            generated_image_url=generated_image_url,
            ai_provider=ai_provider,
            ai_model=ai_model,
            final_generation_prompt=final_prompt,
        )

        persona = self._get_or_create_persona(user)
        persona.avatar_name = avatar_name
        persona.appearance = appearance
        user.updated_at = now_iso()

        self._send(200, {"message": "外观定制已保存", "data": {"userId": user.user_id, "appearance": asdict(appearance)}})

    def handle_customize_personality(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        body = self._read_json()
        preset_code = str(body.get("presetCode", "")).strip()
        custom_prompt = str(body.get("customPrompt", "")).strip()
        preset = SUPPORTED_PERSONALITY_PRESETS.get(preset_code)
        if not preset:
            return self._send(400, {"message": "presetCode 不在支持范围"})

        final_system_prompt = (
            f"{preset['inner_voice']}\n"
            f"语气标签: {', '.join(preset['tone_tags'])}.\n"
            f"用户补充要求: {custom_prompt if custom_prompt else '无'}"
        )
        personality = AIPersonalityConfig(
            preset_code=preset_code,
            preset_name=preset["name"],
            tone_tags=list(preset["tone_tags"]),
            inner_voice=preset["inner_voice"],
            custom_prompt=custom_prompt,
            final_system_prompt=final_system_prompt,
        )

        persona = self._get_or_create_persona(user)
        persona.personality_profile = personality
        persona.personality_tags = [preset_code]
        user.updated_at = now_iso()

        self._send(200, {"message": "性格定制已保存", "data": {"userId": user.user_id, "personality": asdict(personality)}})

    def handle_customize_companion(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        body = self._read_json()
        language = str(body.get("language", "")).strip()
        avatar_code = str(body.get("avatarCode", "")).strip()
        personality_tags = body.get("personalityTags", [])

        if language not in SUPPORTED_LANGUAGE_OPTIONS:
            return self._send(400, {"message": "language 不在支持范围"})
        if avatar_code not in SUPPORTED_AVATAR_CODES:
            return self._send(400, {"message": "avatarCode 不在支持范围"})
        if not isinstance(personality_tags, list) or len(personality_tags) == 0:
            return self._send(400, {"message": "personalityTags 至少选择一项"})

        valid_tags = []
        for tag in personality_tags:
            value = str(tag).strip()
            if value not in SUPPORTED_PERSONALITY_TAGS:
                return self._send(400, {"message": f"personalityTags 包含非法值: {value}"})
            if value not in valid_tags:
                valid_tags.append(value)

        avatar = SUPPORTED_AVATAR_CODES[avatar_code]
        persona = self._get_or_create_persona(user)
        persona.language = language
        persona.language_label = SUPPORTED_LANGUAGE_OPTIONS[language]
        persona.accent = avatar["accent"]
        persona.avatar_code = avatar_code
        persona.avatar_name = avatar["name"]
        persona.archetype = avatar["archetype"]
        persona.personality_tags = valid_tags
        persona.customized_at = now_iso()

        user.profile.onboarding_completed = True
        user.updated_at = now_iso()

        customize_record = AICompanionCustomizationRecord(record_id=generate_id("acr"), user_id=user.user_id, persona=persona)
        AI_CUSTOMIZE_RECORDS_BY_USER.setdefault(user.user_id, []).append(customize_record)

        self._send(
            200,
            {
                "message": "AI 伴侣定制成功",
                "data": {
                    "userId": user.user_id,
                    "onboardingCompleted": True,
                    "aiCompanion": user.profile.ai_companion.to_dict(),
                    "recordId": customize_record.record_id,
                },
            },
        )

    def handle_chat_start(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        persona = self._get_or_create_persona(user)
        companion_image_url = resolve_companion_image(persona)
        personality_preview = "温柔陪伴"
        if persona.personality_profile is not None:
            personality_preview = persona.personality_profile.preset_name

        session_id = generate_id("chat")
        greeting = {
            "messageId": generate_id("msg"),
            "role": "assistant",
            "text": "ねぇ、こっち見て。その笑顔、すごく可愛いよ。",
            "translation": "呐，看着我。那个笑容，真的很可爱。",
            "createdAt": now_iso(),
        }

        chat_session = {
            "sessionId": session_id,
            "userId": user.user_id,
            "companion": {
                "personaId": persona.persona_id,
                "name": persona.avatar_name,
                "imageUrl": companion_image_url,
                "language": persona.language,
                "accent": persona.accent,
                "personalityPreview": personality_preview,
            },
            "uiMode": "communication",
            "layout": {
                "style": "full-screen-call",
                "showLiveTag": True,
                "showGlassOverlay": True,
                "showBottomControls": True,
            },
            "todayVocab": [
                {"word": "かわちい", "meaning": "Cute / Lovely (Slang)"},
                {"word": "ね", "meaning": "Right? / Hey (Particle)"},
                {"word": "推し", "meaning": "My Fave / Idol"},
            ],
            "messages": [greeting],
            "createdAt": now_iso(),
        }
        CHAT_SESSIONS_BY_USER[user.user_id] = chat_session

        self._send(200, {"message": "聊天已开始", "data": chat_session})

    def handle_chat_message(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        chat_session = CHAT_SESSIONS_BY_USER.get(user.user_id)
        if not chat_session:
            return self._send(400, {"message": "请先调用 /chat/start 开始聊天"})

        body = self._read_json()
        user_text = str(body.get("text", "")).strip()
        if not user_text:
            return self._send(400, {"message": "text 不能为空"})

        persona = self._get_or_create_persona(user)
        personality_hint = persona.archetype
        if persona.personality_profile is not None:
            personality_hint = persona.personality_profile.preset_name

        assistant_text = MockChatAIClient.reply(
            persona_name=persona.avatar_name,
            personality_hint=personality_hint,
            user_text=user_text,
            language=persona.language,
        )

        user_msg = {"messageId": generate_id("msg"), "role": "user", "text": user_text, "createdAt": now_iso()}
        assistant_msg = {
            "messageId": generate_id("msg"),
            "role": "assistant",
            "text": assistant_text,
            "createdAt": now_iso(),
        }
        chat_session["messages"].append(user_msg)
        chat_session["messages"].append(assistant_msg)

        self._send(200, {"message": "发送成功", "data": {"userMessage": user_msg, "assistantMessage": assistant_msg}})

    def handle_chat_session(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        session = CHAT_SESSIONS_BY_USER.get(user.user_id)
        if not session:
            return self._send(404, {"message": "聊天会话不存在"})
        self._send(200, {"data": session})


    def handle_closet_items(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        category = "all"
        if "?" in self.path:
            query = self.path.split("?", 1)[1]
            for part in query.split("&"):
                if part.startswith("tab="):
                    category = part.split("=", 1)[1] or "all"

        def match(item: dict) -> bool:
            if category == "all":
                return True
            if category == "free":
                return bool(item.get("isFree"))
            if category == "weekly_new":
                return item.get("tab") == "weekly_new"
            if category == "rare":
                return item.get("rarity") in {"Rare", "SSR"}
            return True

        worn_item_code = USER_WORN_ITEM_BY_USER.get(user.user_id)
        rows = []
        for item in CLOSET_ITEMS:
            if not match(item):
                continue
            row = dict(item)
            row["isWearing"] = item["itemCode"] == worn_item_code
            rows.append(row)

        self._send(200, {"data": {"category": category, "items": rows, "tabs": ["all", "free", "weekly_new", "rare"]}})

    def handle_closet_try_on(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        body = self._read_json()
        item_code = str(body.get("itemCode", "")).strip()
        item = next((x for x in CLOSET_ITEMS if x["itemCode"] == item_code), None)
        if not item:
            return self._send(404, {"message": "服装不存在"})

        persona = self._get_or_create_persona(user)
        persona_image_url = resolve_companion_image(persona)
        render = MockTryOnClient.render_preview(
            persona_image_url=persona_image_url,
            cloth_asset_url=item["assetUrl"],
            item_code=item_code,
            user_id=user.user_id,
        )
        preview = {
            "itemCode": item_code,
            "itemName": item["name"],
            "previewImageUrl": render["previewImageUrl"],
            "basePersonaImageUrl": render["basePersonaImageUrl"],
            "clothAssetUrl": render["clothAssetUrl"],
            "renderEngine": render["renderEngine"],
            "createdAt": now_iso(),
        }
        USER_TRYON_PREVIEW_BY_USER[user.user_id] = preview
        self._send(200, {"message": "试穿预览生成成功", "data": preview})

    def handle_closet_preview(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        preview = USER_TRYON_PREVIEW_BY_USER.get(user.user_id)
        if not preview:
            return self._send(404, {"message": "暂无试穿预览，请先选择服装"})
        self._send(200, {"data": preview})

    def handle_closet_wear(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        body = self._read_json()
        item_code = str(body.get("itemCode", "")).strip()
        item = next((x for x in CLOSET_ITEMS if x["itemCode"] == item_code), None)
        if not item:
            return self._send(404, {"message": "服装不存在"})

        USER_WORN_ITEM_BY_USER[user.user_id] = item_code
        user.updated_at = now_iso()
        self._send(200, {"message": "穿戴成功", "data": {"userId": user.user_id, "wornItemCode": item_code, "wornItemName": item["name"]}})


    def handle_call_start(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        persona = self._get_or_create_persona(user)
        call_session = {
            "sessionId": generate_id("call"),
            "userId": user.user_id,
            "status": "active",
            "mcp": {
                "provider": "mock-mcp-llm",
                "model": "mock-realtime-language-v1",
                "transport": "http-stream-simulated",
            },
            "learningLanguage": persona.language,
            "companion": {
                "name": persona.avatar_name,
                "imageUrl": resolve_companion_image(persona),
            },
            "turns": [],
            "vocabTimeline": [],
            "startedAt": now_iso(),
        }
        CALL_SESSIONS_BY_USER[user.user_id] = call_session
        self._send(200, {"message": "实时通话已开始", "data": call_session})

    def handle_call_stream_turn(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        session = CALL_SESSIONS_BY_USER.get(user.user_id)
        if not session or session.get("status") != "active":
            return self._send(400, {"message": "请先开始实时通话"})

        body = self._read_json()
        transcript = str(body.get("transcript", "")).strip()
        is_final = bool(body.get("isFinal", True))
        if not transcript:
            return self._send(400, {"message": "transcript 不能为空"})

        persona = self._get_or_create_persona(user)
        assistant_reply = MockMCPRealtimeLLM.infer_reply(
            user_text=transcript,
            persona_name=persona.avatar_name,
            learning_language=persona.language,
        )
        vocab_items = MockMCPRealtimeLLM.extract_vocab(text=transcript + " " + assistant_reply)

        turn = {
            "turnId": generate_id("turn"),
            "userTranscript": transcript,
            "assistantReply": assistant_reply,
            "isFinal": is_final,
            "createdAt": now_iso(),
        }
        session["turns"].append(turn)

        for item in vocab_items:
            session["vocabTimeline"].append({
                "term": item["term"],
                "meaning": item["meaning"],
                "lang": item["lang"],
                "type": item["type"],
                "turnId": turn["turnId"],
                "capturedAt": now_iso(),
            })

        self._send(
            200,
            {
                "message": "实时回合处理成功",
                "data": {
                    "turn": turn,
                    "assistantDelta": assistant_reply,
                    "newVocab": vocab_items,
                },
            },
        )

    def handle_call_vocab_summary(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        session = CALL_SESSIONS_BY_USER.get(user.user_id)
        if not session:
            return self._send(404, {"message": "通话会话不存在"})

        uniq = {}
        for row in session.get("vocabTimeline", []):
            uniq[row["term"]] = {"term": row["term"], "meaning": row["meaning"], "lang": row["lang"], "type": row["type"]}

        self._send(200, {"data": {"sessionId": session["sessionId"], "items": list(uniq.values()), "count": len(uniq)}})

    def handle_call_session(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        session = CALL_SESSIONS_BY_USER.get(user.user_id)
        if not session:
            return self._send(404, {"message": "通话会话不存在"})
        self._send(200, {"data": session})

    def handle_call_end(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        session = CALL_SESSIONS_BY_USER.get(user.user_id)
        if not session:
            return self._send(404, {"message": "通话会话不存在"})
        session["status"] = "ended"
        session["endedAt"] = now_iso()
        self._send(200, {"message": "通话已结束", "data": {"sessionId": session["sessionId"], "status": session["status"], "endedAt": session["endedAt"]}})

    def handle_main_tabs(self):
        self._send(
            200,
            {
                "data": {
                    "tabs": APP_MAIN_TABS,
                    "defaultTab": "chat",
                    "vipEntrySuggestion": {"tab": "me", "path": "/me/vip"},
                }
            },
        )

    def handle_vip_plans(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})

        self._send(
            200,
            {
                "data": {
                    "entry": {"tab": "me", "module": "vip"},
                    "currency": {"symbol": "¥", "code": "CNY", "displayName": "人民币"},
                    "plans": VIP_PLANS,
                    "cta": "立即开启心动时刻",
                }
            },
        )

    def handle_records(self, path: str):
        user_id = self._extract_user_id_from_path(path)
        user = USERS_BY_ID.get(user_id or "")
        if not user:
            return self._send(404, {"message": "用户不存在"})
        rows = [x.to_dict() for x in AI_CUSTOMIZE_RECORDS_BY_USER.get(user.user_id, [])]
        self._send(200, {"data": rows})

    def handle_get_user(self, user_id: str):
        user = USERS_BY_ID.get(user_id)
        if not user:
            return self._send(404, {"message": "用户不存在"})
        self._send(200, {"data": user.to_dict()})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), JsonHandler)
    print("Demo server running at http://0.0.0.0:8000")
    server.serve_forever()
