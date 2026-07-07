"""
Smart Bharat - Gemini AI Service
Central wrapper around the Gemini API. All AI calls in the app go through
this module so the API key stays server-side and never reaches the client.
"""

from google import genai
from google.genai import types
from config import Config

_client = None


def _get_client():
    """Lazily create and cache the Gemini client using the API key from environment."""
    global _client
    if _client is None:
        if not Config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Please add it to your .env file."
            )
        _client = genai.Client(api_key=Config.GEMINI_API_KEY)
    return _client


def generate_text(prompt, system_instruction=None, temperature=0.7):
    """
    Generic text generation call to Gemini.
    Returns plain text response. Raises on failure (caller should catch).
    """
    client = _get_client()
    response = client.models.generate_content(
        model=Config.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=1024,
        ),
    )
    return (response.text or "").strip()


def chat_with_assistant(user_message, language="en", history=None):
    """
    Handles the AI Civic Assistant chatbot conversation.
    `history` is a list of {"role": "user"/"model", "text": "..."} dicts.
    """
    lang_instruction = (
        "Reply in Hindi (Devanagari script)."
        if language == "hi"
        else "Reply in simple, clear English."
    )

    system_instruction = f"""You are 'Smart Bharat AI', a helpful, friendly civic assistant for
Indian citizens. You help people understand:
- Government schemes and welfare programs
- Public services (municipal, state, central)
- Citizen rights and duties
- Taxes (Income Tax, GST)
- Passport, Driving License, PAN, Aadhaar processes
- Health schemes (Ayushman Bharat, etc.)
- Education schemes and scholarships
- Agriculture schemes (PM-KISAN, etc.)
- Welfare and social security schemes

Rules:
- Keep answers concise, structured, and easy to understand (use short paragraphs or bullet points).
- Use simple language, avoid excessive jargon.
- If unsure of an exact rule/fee, mention it may vary and advise checking the official government portal.
- Be warm, respectful, and encouraging.
- {lang_instruction}
"""

    client = _get_client()

    chat_history = []
    if history:
        for turn in history[-10:]:  # keep last 10 turns for context
            role = "user" if turn.get("role") == "user" else "model"
            chat_history.append(
                types.Content(role=role, parts=[types.Part(text=turn.get("text", ""))])
            )

    chat = client.chats.create(
        model=Config.GEMINI_MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            max_output_tokens=1024,
        ),
        history=chat_history,
    )
    response = chat.send_message(user_message)
    return (response.text or "").strip()


def recommend_service(category, sub_query=""):
    """
    Uses Gemini to recommend a government service based on a selected category.
    Returns structured text covering: service, eligibility, documents, process, time.
    """
    lang_note = ""
    prompt = f"""A citizen is looking for government services related to: "{category}".
Additional details from the citizen: "{sub_query if sub_query else 'None provided'}"

Provide a clear, structured recommendation with these exact sections:
1. Recommended Service
2. Eligibility
3. Required Documents
4. Process (step by step)
5. Estimated Time

Keep it concise, practical, and India-specific (mention relevant ministries/portals like india.gov.in, umang app, etc. where relevant).
Format using Markdown with headers (###) for each section and bullet points for lists.
"""
    system_instruction = "You are a Government Service Finder assistant for Indian citizens named Smart Bharat AI."
    return generate_text(prompt, system_instruction=system_instruction, temperature=0.5)


def generate_complaint_draft(complaint_type, location, description):
    """
    Generates a professional, formal complaint letter using Gemini
    based on the citizen's raw input.
    """
    prompt = f"""Draft a formal, professional civic complaint letter based on the following details:

Complaint Type: {complaint_type}
Location: {location}
Citizen's Description: {description}

The letter should:
- Be addressed to "The Concerned Authority"
- Have a clear subject line
- Politely but firmly describe the issue
- Reference the location clearly
- Request prompt action/resolution with a reasonable timeline
- End with a professional closing (no need for a real name/signature, use "A Concerned Citizen")

Keep it under 250 words. Output only the letter text, no additional commentary.
"""
    system_instruction = "You are an assistant that drafts professional civic complaint letters for Indian citizens."
    return generate_text(prompt, system_instruction=system_instruction, temperature=0.6)


def translate_text(text, target_language="hi"):
    """Translate text using Gemini. target_language: 'hi' or 'en'."""
    target = "Hindi (Devanagari script)" if target_language == "hi" else "English"
    prompt = f"Translate the following text to {target}. Only output the translated text, nothing else:\n\n{text}"
    return generate_text(prompt, temperature=0.3)
