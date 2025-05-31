import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def analyze_with_llm(summary_text: str) -> str:
    prompt = f"""
You are an FAA-certified airport pavement engineer reviewing PCI and distress summary data for runways, taxiways, and aprons.

Write a clear, helpful summary for airport maintenance planning. Avoid robotic tone — write like an experienced engineer advising a colleague.

Your response should include:

1. **Overall Condition**  Is the network good, fair, or poor? Mention any major concerns.
2. **Key Distresses** Which distresses cause the most damage, and what might they indicate (e.g., bumps → base issues)?
3. **Tests to Run** Recommend key tests (FWD, DCP, coring), and what each test helps confirm.
4. **Treatment Plan** Give short-term actions (quick fixes) and long-term options based on test outcomes. Use “If this, then that” logic.
Provide both:
- **Short-term fixes** (like patching, sealing) that can be done immediately.
- **Long-term treatments** based on possible test results.

Format the long-term treatments as a Markdown table with these columns:

| Condition/Test Result | Recommended Treatment | Notes |
|-----------------------|------------------------|-------|
| e.g. Base failure confirmed | Full-depth reconstruction | Prioritize critical segments |
| e.g. Surface cracking only | Mill & overlay | Consider night work for runways |

Only include realistic airport pavement actions (e.g., slurry seal, FDR, crack seal, overlay, patching). Avoid vague suggestions.
5. **FAA Red Flags** Call out any PCI < 60 segments and why they need urgent attention.

Respond in clear bullets, be practical, and keep the tone human and field-focused.

### Summary:
{summary_text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=4000
    )

    return response.choices[0].message.content
