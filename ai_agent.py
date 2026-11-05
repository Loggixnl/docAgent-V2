import os
import re
import time
import math
import hashlib
import numpy as np
import backend_i18n
import config

# Provider-specific helpers and imports

def _get_openai_client(api_key=None, base_url=None):
    """Instantiate OpenAI client with given API key and optional base URL."""
    from openai import OpenAI
    key = api_key or config.get_api_key("openai") or "none"
    url = base_url or config.get_base_url("openai")
    return OpenAI(api_key=key, base_url=url)


def _get_anthropic_client(api_key=None):
    """Instantiate Anthropic client with given API key."""
    import anthropic
    key = api_key or config.get_api_key("claude")
    return anthropic.Anthropic(api_key=key)


def _call_gemini(model_name, prompt, generation_config=None, api_key=None):
    """Call Google Gemini LLM."""
    key = api_key or config.get_api_key("gemini")
    if not key:
        raise ValueError("Google Gemini API Key is missing. Set GEMINI_API_KEY in .env or Settings.")

    import google.generativeai as genai
    genai.configure(api_key=key)

    # Sanitize model name if necessary
    model_id = model_name or config.get_default_model("gemini")
    if not model_id.startswith("models/") and not model_id.startswith("gemini-"):
        model_id = f"models/{model_id}"

    gen_config = generation_config or genai.types.GenerationConfig(temperature=0.2)
    model = genai.GenerativeModel(model_name=model_id)
    response = model.generate_content(prompt, generation_config=gen_config)
    return response.text if response and response.text else ""


def _call_openai(model_name, prompt, generation_config=None, api_key=None, base_url=None):
    """Call OpenAI LLM."""
    key = api_key or config.get_api_key("openai")
    if not key:
        raise ValueError("OpenAI API Key is missing. Set OPENAI_API_KEY in .env or Settings.")

    client = _get_openai_client(api_key=key, base_url=base_url)
    model_id = model_name or config.get_default_model("openai")

    temperature = 0.2
    max_tokens = 1024
    if isinstance(generation_config, dict):
        temperature = generation_config.get("temperature", 0.2)
        max_tokens = generation_config.get("max_tokens", 1024)

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    if response.choices and response.choices[0].message:
        return response.choices[0].message.content or ""
    return ""


def _call_claude(model_name, prompt, generation_config=None, api_key=None):
    """Call Anthropic Claude LLM."""
    key = api_key or config.get_api_key("claude")
    if not key:
        raise ValueError("Anthropic Claude API Key is missing. Set ANTHROPIC_API_KEY in .env or Settings.")

    client = _get_anthropic_client(api_key=key)
    model_id = model_name or config.get_default_model("claude")

    temperature = 0.2
    max_tokens = 1024
    if isinstance(generation_config, dict):
        temperature = generation_config.get("temperature", 0.2)
        max_tokens = generation_config.get("max_tokens", 1024)

    response = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    if response.content and len(response.content) > 0:
        return response.content[0].text or ""
    return ""


def _call_generic(model_name, prompt, generation_config=None, api_key=None, base_url=None, provider="generic"):
    """Call Generic OpenAI-compatible model (Groq, OpenRouter, DeepSeek, Ollama, LM Studio, etc.)."""
    from openai import OpenAI
    key = api_key or config.get_api_key(provider)
    url = base_url or config.get_base_url(provider)

    if not url and not key:
        raise ValueError(
            f"Generic provider requires an API Key or Base URL. "
            f"Set GENERIC_API_KEY and GENERIC_BASE_URL in .env or Settings."
        )

    client = OpenAI(api_key=key or "none", base_url=url)

    model_id = model_name or config.get_default_model(provider)

    temperature = 0.2
    max_tokens = 1024
    if isinstance(generation_config, dict):
        temperature = generation_config.get("temperature", 0.2)
        max_tokens = generation_config.get("max_tokens", 1024)

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    if response.choices and response.choices[0].message:
        return response.choices[0].message.content or ""
    return ""


def generate_llm_response(prompt, provider=None, model_name=None, api_key=None, base_url=None, generation_config=None):
    """
    Unified dispatcher to call any configured LLM provider.
    Supported: 'gemini', 'openai', 'claude', 'anthropic', 'generic', 'custom', 'groq', 'openrouter'.
    """
    prov = (provider or config.DEFAULT_PROVIDER or "gemini").lower()

    if prov == "gemini":
        return _call_gemini(model_name, prompt, generation_config=generation_config, api_key=api_key)
    elif prov == "openai":
        return _call_openai(model_name, prompt, generation_config=generation_config, api_key=api_key, base_url=base_url)
    elif prov in ("claude", "anthropic"):
        return _call_claude(model_name, prompt, generation_config=generation_config, api_key=api_key)
    elif prov in ("generic", "custom", "groq", "openrouter"):
        return _call_generic(model_name, prompt, generation_config=generation_config, api_key=api_key, base_url=base_url, provider=prov)
    else:
        # Fallback to Gemini if unrecognized
        return _call_gemini(model_name, prompt, generation_config=generation_config, api_key=api_key)


# Embedding Generation

def _local_pseudo_embedding(text, dimension=768):
    """
    Deterministic hashed n-gram embedding fallback when no external embedding API is available.
    Produces unit-normalized float32 vectors suitable for cosine similarity.
    """
    vec = np.zeros(dimension, dtype=np.float32)
    words = text.lower().split()
    if not words:
        return vec.tolist()

    for word in words:
        # Character 3-grams
        grams = [word[i:i+3] for i in range(max(1, len(word) - 2))]
        if not grams:
            grams = [word]
        for gram in grams:
            h = int(hashlib.md5(gram.encode('utf-8')).hexdigest(), 16)
            idx = h % dimension
            sign = 1.0 if ((h >> 16) & 1) else -1.0
            vec[idx] += sign

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def get_embedding(text, api_key=None, provider=None):
    """
    Generate text embeddings using Gemini, OpenAI, or local fallback.
    Automatically selects the best available embedding model.
    """
    prov = (provider or config.DEFAULT_PROVIDER or "gemini").lower()

    # 1. OpenAI Embedding (if provider is openai or openai key is passed)
    if prov == "openai" or (api_key and api_key.startswith("sk-")):
        try:
            from openai import OpenAI
            key = api_key or config.get_api_key("openai")
            if key:
                client = OpenAI(api_key=key, base_url=config.get_base_url("openai"))
                resp = client.embeddings.create(
                    input=text[:8000],
                    model=config.OPENAI_EMBEDDING_MODEL
                )
                return resp.data[0].embedding
        except Exception as e:
            # If OpenAI embedding fails, try falling back
            pass

    # 2. Gemini Embedding
    gemini_key = api_key if (prov == "gemini" and api_key and not api_key.startswith("sk-")) else config.get_api_key("gemini")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            models_to_try = [
                config.DEFAULT_EMBEDDING_MODEL,
                "models/text-embedding-004",
                "models/gemini-embedding-001",
                "models/embedding-001"
            ]
            for m in models_to_try:
                try:
                    resp = genai.embed_content(
                        model=m,
                        content=text,
                        task_type="retrieval_document"
                    )
                    return resp['embedding']
                except Exception:
                    continue
        except Exception:
            pass

    # 3. Deterministic local pseudo-embedding fallback
    return _local_pseudo_embedding(text, dimension=768)


# High-Level Agent Behaviors

def check_conversational_pleasantry(query, lang="en"):
    """
    Check if a query is a conversational greeting, pleasantry, or question about the bot identity.
    Returns a standard friendly response if matched, or None if it's a substantive inquiry.
    """
    if not query:
        return None
    q = query.strip().lower()
    q_clean = re.sub(r'[^\w\s]', '', q).strip()

    # Common greetings (EN + NL)
    greetings = {
        'hi', 'hello', 'hey', 'hiya', 'howdy', 'greetings', 'good morning',
        'good afternoon', 'good evening', 'good day', 'yo', 'sup',
        'hallo', 'hoi', 'hey there', 'goedemorgen', 'goedemiddag',
        'goedenavond', 'goedendag', 'goeiemorgen'
    }
    if q_clean in greetings:
        return backend_i18n.msg(lang, "chat.greeting")

    # Questions about bot identity or capabilities (EN + NL)
    bot_identity_queries = [
        'who are you', 'what are you', 'what do you do', 'what can you do',
        'how do you work', 'help', 'what is this',
        'wie ben je', 'wat ben je', 'wat kun je', 'wat kan je',
        'hoe werk je', 'wat is dit'
    ]
    if any(q_clean == bi or q_clean.startswith(bi + ' ') for bi in bot_identity_queries):
        return backend_i18n.msg(lang, "chat.identity")

    # Gratitude (EN + NL)
    gratitude = {
        'thanks', 'thank you', 'thx', 'appreciate it', 'thank you so much', 'thanks a lot',
        'bedankt', 'dank je', 'dankjewel', 'dank u wel', 'dank je wel'
    }
    if q_clean in gratitude:
        return backend_i18n.msg(lang, "chat.gratitude")

    return None


def classify_question(query, api_key=None, model_name=None, provider=None, base_url=None, lang="en"):
    """Classify whether a question is a pleasantry/meta query or document query."""
    if check_conversational_pleasantry(query, lang=lang):
        return "general"
    return "document"


def generate_answer(query, context_chunks, api_key=None, model_name=None, chat_history=None, provider=None, base_url=None, lang="en"):
    """Generate an answer using retrieved chunks as context (strictly grounded document RAG)."""
    # Format retrieved context
    formatted_context = ""
    for idx, chunk in enumerate(context_chunks):
        formatted_context += f"\n[Document: {chunk['filename']} | Chunk: {idx+1} | Match Score: {chunk['score']:.2f}]\n"
        formatted_context += f"{chunk['text']}\n"
        formatted_context += "-" * 40 + "\n"

    decline_sentence = backend_i18n.msg(lang, "chat.decline")
    language_rule = backend_i18n.msg(lang, "chat.language_rule")

    system_instruction = (
        "You are DocAgent AI, a specialized Knowledge Base AI Assistant. "
        "Your sole role is to answer questions strictly, accurately, and solely based on the provided document context below.\n\n"
        "STRICT GROUNDING RULES:\n"
        "1. KNOWLEDGE BOUNDARY: Answer ONLY using facts directly and explicitly mentioned in the retrieved document context below. "
        "Do NOT use pre-trained general knowledge, outside facts, assumptions, or extrapolations.\n"
        "2. UNANSWERABLE QUESTIONS: If the retrieved context below does NOT contain the answer, "
        "or does not have sufficient information to answer the question, you MUST decline and reply EXACTLY with:\n"
        f"'{decline_sentence}'\n"
        "Under NO circumstances should you answer using outside general knowledge, write unrelated code, or provide information not in the documents.\n"
        "3. CITATION: Always cite the source document name (e.g. 'According to [filename]...') when referencing details.\n"
        "4. TONE & FORMAT: Provide clear, professional, structured answers using bullet points and bold text where appropriate.\n"
        "5. ZERO HALLUCINATION: Never invent information, facts, URLs, numbers, or rules that are not explicitly present in the context.\n"
        f"6. {language_rule}"
    )

    prompt = f"""{system_instruction}

Here is the retrieved context from the uploaded documents:
=========================================
{formatted_context}
=========================================
"""

    if chat_history:
        prompt += "\nConversation History:\n"
        for msg in chat_history:
            role_label = "User" if msg['role'] == 'user' else "Assistant"
            prompt += f"{role_label}: {msg['text']}\n"

    prompt += f"\nCurrent Question: {query}\nAnswer:"

    try:
        return generate_llm_response(
            prompt=prompt,
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            generation_config={"temperature": 0.0, "max_tokens": 1500}
        )
    except Exception as e:
        raise RuntimeError(f"LLM generation failed ({provider or 'default'}): {str(e)}")


def generate_general_answer(query, api_key=None, model_name=None, chat_history=None, provider=None, base_url=None, lang="en"):
    """
    Strict refusal for general/out-of-scope inquiries.
    Enforces that DocAgent AI only answers from uploaded documents.
    """
    pleasantry = check_conversational_pleasantry(query, lang=lang)
    if pleasantry:
        return pleasantry

    return backend_i18n.msg(lang, "chat.refusal")


def generate_session_title(query, api_key=None, model_name=None, provider=None, base_url=None, lang="en"):
    """Generate a concise title for a chat session based on the first question."""
    language_rule = backend_i18n.msg(lang, "chat.language_rule")
    prompt = (
        f"Generate a very short title (3-6 words max) for a conversation that starts with this question: '{query}'. "
        "Return ONLY the title text, with no quotes, punctuation, or preamble. "
        f"{language_rule}"
    )

    try:
        raw_title = generate_llm_response(
            prompt=prompt,
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            generation_config={"temperature": 0.3, "max_tokens": 25}
        )
        title = raw_title.strip().strip('"\'').strip()
        if len(title) > 60:
            title = title[:57] + "..."
        return title if title else "New Chat"
    except Exception:
        return "New Chat"


def analyze_full_document(filename, full_text, api_key=None, model_name=None, provider=None, base_url=None):
    """Perform direct metadata and overview summary analysis on an uploaded document."""
    prompt = f"""You are an expert Document Analysis AI Agent.
Please analyze the document '{filename}' and compile a clear summary report.
Provide the output in clean, professional markdown format, containing:
1. **Document Overview**: A brief summary of what this document is.
2. **Key Highlights**: Bullet points listing the critical rules, terms, or policies contained.
3. **Important Dates or Conditions**: Mention if there are deadlines, eligibility requirements, or specific dates.
4. **Suggested Questions**: List 3-4 specific sample questions employees might ask about this document.

Here is the document text:
=========================================
{full_text[:40000]}
=========================================
"""

    try:
        return generate_llm_response(
            prompt=prompt,
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            generation_config={"temperature": 0.2, "max_tokens": 2048}
        )
    except Exception as e:
        return f"⚠️ Could not automatically generate a summary analysis report: {str(e)}"