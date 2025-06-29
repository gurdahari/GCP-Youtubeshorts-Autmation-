# openai_handler.py
import openai
import random
from config import OPENAI_API_KEY, SHOP_URL

openai.api_key = OPENAI_API_KEY

# A list of sample call‑to‑action phrases tailored for the ANIMAL niche.
CTAS = [
    "click to explore the shop",
]


def get_random_cta():
    """Returns a random call‑to‑action from the list."""
    return random.choice(CTAS)


def generate_metadata_for_short(file_name: str):
    """
    Uses GPT‑4‑turbo to generate metadata (title, description, tags)
    for a YouTube Short featuring an ANIMAL‑themed clip, based on the given file
    name.

    The prompt instructs GPT to write like a popular YouTuber with a natural,
    engaging, and authentic tone. The prompt asks for:
      1) A short, catchy title (no extra quotes).
      2) A friendly, authentic description (2‑4 lines max) that mentions the
         featured animal moment and includes a link to the Shopify store.
      3) A comma‑separated list of 5 relevant tags.

    The description ends with a brief call‑to‑action (CTA) and the hashtag
    "#Shorts".

    If GPT fails, a fallback set of metadata is returned.
    """
    prompt_text = (
        f"Imagine you are a popular YouTuber known for your energetic and authentic style. "
        f"You just recorded a 15‑second YouTube Short featuring an adorable animal moment called '{file_name}'. "
        "Please generate the following content in a natural and conversational tone:\n\n"
        "1. A short, catchy title that grabs attention (do not include any extra quotes).\n"
        "2. A friendly and authentic description (2‑4 lines maximum) that briefly describes the animal moment, "
        f"mentions why it's special, and includes a link to your Shopify store at {SHOP_URL}.\n"
        "3. A list of 5 relevant tags, separated by commas.\n\n"
        "At the end of the description, add a short call‑to‑action (CTA) and end with '#Shorts'."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt‑4.1",  # Use your chosen GPT model
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7,
            max_tokens=300,
        )
        gpt_output = response["choices"][0]["message"]["content"]
    except Exception:
        # Fallback if there's an error calling the API.
        gpt_output = (
            f"Title: {file_name}\n"
            f"Description: Enjoy this adorable animal moment! Find more cuteness at {SHOP_URL}\n"
            "Tags: animals, cute, pets, shorts, trending"
        )

    # Initialize output variables.
    title = ""
    description = ""
    tags = []

    # Process each line of the GPT output safely.
    for line in gpt_output.splitlines():
        l = line.strip()
        if l.lower().startswith("title:"):
            parts = l.split("title:", 1)
            if len(parts) > 1:
                title = parts[1].strip().strip('"')
        elif l.lower().startswith("description:"):
            parts = l.split("description:", 1)
            if len(parts) > 1:
                description = parts[1].strip().strip('"')
        elif l.lower().startswith("tags:"):
            parts = l.split("tags:", 1)
            if len(parts) > 1:
                t = parts[1]
                tags = [x.strip() for x in t.split(",") if x.strip()]

    # Use fallback values if any field is missing or empty.
    if not title:
        title = file_name
    if not description:
        description = f"Enjoy this produdct enviroment moment! Check it out: {SHOP_URL}"
    if not tags:
        tags = ["t shirt", "cute", "white", "funny", "shorts"]

    # Append a random call‑to‑action (CTA) and the "#Shorts" hashtag to the description.
    cta = get_random_cta()
    description += f"\n\n{cta}\n\n#Shorts"

    return title, description, tags
