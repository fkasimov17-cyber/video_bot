"""
prompt_engine.py — Core prompt enhancement logic for PromptCraft AI Bot

Transforms raw user ideas (any language) into cinematic, production-grade
text-to-video prompts optimized for modern AI video generation tools.
"""

from __future__ import annotations

import random
import re


# ── Keyword → concept mappings ────────────────────────────────────────────────

GENRE_RULES: list[tuple[list[str], dict]] = [
    # Nature / Landscape
    (
        ["tog", "mountain", "cho'l", "desert", "o'rmon", "forest", "daryo", "river",
         "dengiz", "ocean", "sea", "ko'l", "lake", "vodopat", "waterfall", "nature"],
        {
            "camera": "sweeping drone aerial shot, slow push-in, golden hour",
            "lighting": "volumetric golden hour sunlight, warm amber tones, god rays",
            "style": "hyper-realistic, shot on Arri Alexa Mini LF, 35mm anamorphic lens",
            "generator": "Runway Gen-3 Alpha / Luma Dream Machine",
            "specs": "16:9, 24fps, cinematic",
            "subject_suffix": "in a breathtaking natural landscape",
        },
    ),
    # Cyberpunk / City / Night
    (
        ["shahar", "city", "kecha", "night", "neon", "future", "kelajak", "cyber",
         "robot", "tekhno", "tech", "street", "ko'cha"],
        {
            "camera": "low-angle handheld tracking shot, slow dolly push-in",
            "lighting": "neon cyberpunk glow, deep blue and magenta palette, wet reflections",
            "style": "Blade Runner 2049 aesthetic, anamorphic lens flares, Unreal Engine 5 render",
            "generator": "Runway Gen-3 Alpha / Kling AI",
            "specs": "16:9, 24fps, cinematic",
            "subject_suffix": "in a rain-soaked neon-lit cyberpunk city",
        },
    ),
    # Space / Sci-Fi
    (
        ["kosmos", "space", "yulduz", "star", "sayyora", "planet", "raketa", "rocket",
         "astronaut", "galaxy", "galaktika", "nebula"],
        {
            "camera": "slow floating POV drift, wide-angle deep space pull-back",
            "lighting": "harsh directional solar rays, deep blacks, starfield ambient glow",
            "style": "Interstellar IMAX 70mm look, fine film grain, photorealistic CGI",
            "generator": "Sora / Runway Gen-3 Alpha",
            "specs": "16:9 IMAX, 24fps",
            "subject_suffix": "set against the infinite expanse of deep space",
        },
    ),
    # Action / Battle / Chase
    (
        ["jang", "battle", "fight", "kurash", "harakatli", "action", "chase", "quvish",
         "explosion", "portlash", "war", "urush"],
        {
            "camera": "fast-cut handheld shaky-cam, slow-motion impact moments at 120fps",
            "lighting": "harsh side-lighting, dust particles in backlit beams, practical fire light",
            "style": "gritty realism, 35mm film texture, Saving Private Ryan aesthetic",
            "generator": "Kling AI / Runway Gen-3 Alpha",
            "specs": "16:9, 24fps (with 120fps slow-motion cuts)",
            "subject_suffix": "in an intense high-stakes action sequence",
        },
    ),
    # Romance / Emotional
    (
        ["sevgi", "love", "muhabbat", "romantic", "his", "emotion", "yurak", "heart",
         "yor", "couple", "juft"],
        {
            "camera": "medium close-up, slow rack focus pull, gentle handheld sway",
            "lighting": "soft golden hour bokeh, warm diffused window light, lens flare",
            "style": "dreamy film look, 50mm f/1.2 shallow depth-of-field, muted warm palette",
            "generator": "Luma Dream Machine / Pika Labs",
            "specs": "9:16 vertical, 24fps",
            "subject_suffix": "in a tender, emotionally resonant moment",
        },
    ),
    # Horror / Dark / Mystery
    (
        ["qorong'i", "dark", "dahshat", "horror", "scary", "ghost", "arvoh", "sir",
         "mystery", "abandoned", "tashlab", "creepy"],
        {
            "camera": "slow creeping dolly, low-angle Dutch tilt, handheld tremor",
            "lighting": "chiaroscuro deep shadow, single cold moonlight shaft, atmospheric fog",
            "style": "dark cinematic horror aesthetic, desaturated tones, 35mm film grain",
            "generator": "Runway Gen-3 Alpha / Kling AI",
            "specs": "2.39:1 anamorphic, 24fps",
            "subject_suffix": "shrouded in darkness and dread",
        },
    ),
    # Fantasy / Magic
    (
        ["sehrli", "magic", "fantasy", "ajdaho", "dragon", "pari", "fairy", "sehr",
         "spell", "elf", "orcs", "kingdom", "qirol", "qirollik"],
        {
            "camera": "sweeping cinematic crane shot, slow push-in with orbiting motion",
            "lighting": "ethereal bioluminescent glow, magical particle effects, dramatic rim light",
            "style": "Epic Games Unreal Engine 5 photorealistic fantasy render, rich saturated palette",
            "generator": "Sora / Kling AI",
            "specs": "16:9, 24fps, cinematic",
            "subject_suffix": "in a breathtaking magical fantasy realm",
        },
    ),
    # Animal / Wildlife
    (
        ["hayvon", "animal", "qush", "bird", "bo'ri", "wolf", "sher", "lion", "ot",
         "horse", "fil", "elephant", "wildlife", "tabiat"],
        {
            "camera": "low ground-level tracking shot, telephoto 400mm lens, smooth pan follow",
            "lighting": "golden savanna light, natural ambient, dust particles backlit",
            "style": "BBC Planet Earth II style, hyper-realistic 8K wildlife photography",
            "generator": "Sora / Luma Dream Machine",
            "specs": "16:9, 24fps",
            "subject_suffix": "in their natural wild habitat",
        },
    ),
]

# Fallback (generic cinematic)
FALLBACK_PROFILE = {
    "camera": "medium wide-angle tracking shot, smooth gimbal movement",
    "lighting": "natural cinematic lighting, balanced color grading",
    "style": "hyper-realistic, shot on Arri Alexa Mini, 35mm lens, f/2.0",
    "generator": "Runway Gen-3 Alpha / Kling AI",
    "specs": "16:9, 24fps, cinematic",
    "subject_suffix": "",
}

# Camera movement variety (randomly sampled to avoid repetition)
CAMERA_VARIANTS = [
    "slow-motion dolly push-in",
    "sweeping drone aerial flyover",
    "handheld 35mm lens tracking shot",
    "low-angle crane ascent",
    "smooth gimbal orbit",
    "telephoto compressed pull-back",
]

MOTION_QUALIFIERS = [
    "buttery smooth motion, no camera shake",
    "fluid continuous motion, zero warp artifacts",
    "stable cinematic movement, motion blur at 180° shutter angle",
]


# ── Uzbek → English subject translation (lightweight heuristic) ──────────────

UZ_EN_MAP = {
    "tog": "mountain",
    "tog'": "mountain",
    "qiz": "young woman",
    "bola": "child",
    "yigit": "young man",
    "erkak": "man",
    "ayol": "woman",
    "ot": "horse",
    "bo'ri": "wolf",
    "sher": "lion",
    "fil": "elephant",
    "qush": "bird",
    "shahar": "city",
    "kecha": "night",
    "kunduzi": "daytime",
    "quyosh": "sun",
    "oy": "moon",
    "yulduz": "star",
    "dengiz": "ocean",
    "daryo": "river",
    "o'rmon": "forest",
    "cho'l": "desert",
    "ko'l": "lake",
    "asal": "honey",
    "gul": "flower",
    "bog": "garden",
    "bog'": "garden",
    "qor": "snow",
    "yomg'ir": "rain",
    "shamol": "wind",
    "olov": "fire",
    "suv": "water",
    "osmon": "sky",
    "bulut": "cloud",
    "tepalik": "hill",
    "sahroi": "desert",
    "minayotgan": "riding",
    "yugurmoqda": "running",
    "uchmoqda": "flying",
    "suzmoqda": "swimming",
    "kurashmoqda": "fighting",
    "raqsga": "dancing",
    "tushmoqda": "falling",
    "chiqmoqda": "climbing",
    "turmoqda": "standing",
    "o'tirmoqda": "sitting",
    "yotmoqda": "lying",
    "qarmoqda": "looking",
    "yurmoqda": "walking",
    "chopmoqda": "sprinting",
}


def _translate_uz_words(text: str) -> str:
    """Replace known Uzbek words with their English equivalents (heuristic)."""
    words = re.split(r"(\s+)", text)
    result = []
    for word in words:
        clean = word.strip().lower().rstrip(".,!?;:")
        result.append(UZ_EN_MAP.get(clean, word))
    return " ".join(result).strip()


def _detect_profile(text: str) -> dict:
    """Pick the best genre profile based on keyword matching."""
    lower = text.lower()
    best_score = 0
    best_profile = FALLBACK_PROFILE

    for keywords, profile in GENRE_RULES:
        score = sum(1 for kw in keywords if kw in lower)
        if score > best_score:
            best_score = score
            best_profile = profile

    return best_profile


def _clean_subject(text: str) -> str:
    """Produce a clean English subject phrase from raw user input."""
    translated = _translate_uz_words(text)
    # Capitalize first letter
    return translated[:1].upper() + translated[1:] if translated else text


def enhance_prompt(raw_idea: str) -> dict:
    """
    Transform a raw user idea into a structured cinematic video prompt.

    Returns a dict with keys:
        prompt, subject, camera, lighting, generator, specs
    """
    profile = _detect_profile(raw_idea)
    subject_phrase = _clean_subject(raw_idea)
    suffix = profile.get("subject_suffix", "")

    camera_move = random.choice(CAMERA_VARIANTS)
    motion_qual = random.choice(MOTION_QUALIFIERS)

    # Build the final cinematic prompt
    prompt_parts = [
        f"{subject_phrase}{(' ' + suffix) if suffix else ''},",
        f"{profile['camera']},",
        f"{profile['lighting']},",
        f"{profile['style']},",
        f"{motion_qual}.",
    ]
    full_prompt = " ".join(prompt_parts)

    # Trim to 90 words max while keeping sentence integrity
    words = full_prompt.split()
    if len(words) > 90:
        full_prompt = " ".join(words[:88]) + "..."

    return {
        "prompt": full_prompt,
        "subject": f"{subject_phrase}{(' — ' + suffix) if suffix else ''}",
        "camera": f"{profile['camera']}, {camera_move}",
        "lighting": f"{profile['lighting']} | Style: {profile['style']}",
        "generator": profile["generator"],
        "specs": profile["specs"],
    }
