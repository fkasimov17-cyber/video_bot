# 🎬 PromptCraft AI Bot

> **[@PromptCraft_AI_bot](https://t.me/PromptCraft_AI_bot)** — World-Class AI Video Prompt Engineer

Transform simple ideas into **cinematic, production-grade text-to-video prompts** optimized for modern AI video generators.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌍 Multilingual | Accepts Uzbek and English input |
| 🎭 Genre detection | Auto-detects Nature, Cyberpunk, Space, Action, Romance, Horror, Fantasy, Wildlife |
| 🎥 Cinematographic | Generates real camera angles, lenses, FPS, and lighting specs |
| 🤖 Multi-platform | Optimized for Runway Gen-3, Sora, Kling AI, Luma, Pika, MidJourney |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/video_bot.git
cd video_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your token
Create a `.env` file in the project root:
```
BOT_TOKEN=your_telegram_bot_token_here
```
> ⚠️ **Never commit your `.env` file!** It is already in `.gitignore`.

### 4. Run the bot
```bash
python bot.py
```

---

## 📁 Project Structure

```
video_bot/
├── bot.py            # Telegram bot — commands & message handlers
├── prompt_engine.py  # Core prompt engineering logic
├── requirements.txt  # Python dependencies
├── .env              # 🔒 Secret token (gitignored)
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Launch the bot |
| `/help` | Show all commands |
| `/example` | View sample prompts |
| `/about` | About the bot |

---

## 🎯 Supported AI Video Generators

- **Runway Gen-3 Alpha**
- **OpenAI Sora**
- **Kling AI**
- **Luma Dream Machine**
- **Pika Labs**
- **MidJourney Video**

---

## 📊 Output Format

Each generated prompt includes:

```
🎬 Enhanced Video Prompt (Copy-Paste Ready):
`[cinematic prompt here]`

📊 Prompt Breakdown:
• Subject & Motion: ...
• Cinematography & Camera: ...
• Lighting & Style: ...

💡 Recommended AI Generator: Runway Gen-3 Alpha / Kling AI
⚙️ Aspect Ratio / FPS: 16:9, 24fps, cinematic
```

---

## 📜 License

MIT License — feel free to fork and build on top!
