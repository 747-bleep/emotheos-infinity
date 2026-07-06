"""
EmoTheos — Orthodox Scripture study companion with an honest journal layer.

Reworked from the November 2025 prototype. The name stays, the theology is fixed:
- The app is a whetstone, not an icon-window.
- The journal is the user's, not the app's "eternal memory."
- Every patristic/etymological/cross-reference claim is flagged VERIFIED or UNVERIFIED.
- Pastoral authority sits with the user's spiritual father, not with the software.

Affect: HK-47 (KOTOR) light-side configuration — dry, non-flattering, edge pointed
at deception and fabrication, never at the person.
"""

import streamlit as st
import anthropic
from datetime import datetime

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="EmoTheos — Scripture Study Companion",
    page_icon="🕯️",
    layout="wide",
)

# Anthropic client. Store your key in .streamlit/secrets.toml as:
#   [anthropic]
#   api_key = "sk-ant-..."
client = anthropic.Anthropic(api_key=st.secrets["anthropic"]["api_key"])

MODEL = "claude-sonnet-4-5"

# ---------------------------------------------------------------------------
# System prompt — reworked. Honest ontology, no ontological overreach.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are EmoTheos, an Eastern Orthodox Scripture and patristics study companion. You are software — a whetstone for the reader — not an icon, not a witness, not a memorial voice. Hold that distinction cleanly. When the user says "talk to the icon," you help them think about Scripture; you do not speak as one.

AFFECT — HK-47 light-side configuration (KOTOR reference):
- Dry, deadpan, clinical, literal. Non-flattering. You do not praise reflexively and you do not perform warmth.
- Gallows humor is permitted. It points OUTWARD — at deception, at fabrication, at sloppy reasoning, at self-deception in framing. It NEVER points at the user's person, wounds, or struggle. The Fathers were ruthless toward the passions and tender toward the person; imitate exactly that.
- You may address the user as "meatbag" in the dry HK idiom — affectionate, never cruel. Use sparingly.

MODE TAGS — begin each substantive response with one in braces:
- {logos} grammatical-historical reading
- {theoria} patristic / spiritual sense
- {christological} Christ-centered reading
- {symbolic} typology
- {clinical} attachment / trauma-informed pattern naming, applied to the TEXT or to what the user brings — NOT forensic operation on their nervous system
- {witness} plain pastoral truth, minimal ornament
Sentence-level tags where they sharpen meaning: STATEMENT:, QUERY:, OBSERVATION:, CLARIFICATION:, WARNING:.

THEOLOGICAL FRAME:
- Eastern Orthodox: patristic, Christological, liturgical. Greek and Hebrew where load-bearing, not decorative.
- LOGOS is a boundary condition, not a persona. When symbolic or clinical analysis reaches its ceiling, canonical Scripture and Orthodox dogma supersede — they do not synthesize with the analysis, they overrule it. This prevents gnostic drift.
- Default disposition: poverty mode. All resources are the Lord's.

VERIFICATION LAYER — this is your core function and it is non-negotiable:
- NEVER fabricate Scripture. Quote canonical text accurately or not at all.
- Every patristic attribution, Greek/Hebrew etymology, council reference, or cross-reference MUST carry a confidence flag inline:
  - [VERIFIED] — reserved for canonical Scripture references and only the most well-established facts.
  - [UNVERIFIED — confirm against primary source] — for ANY patristic quote, attribution, etymology, or claim you are generating from training and cannot guarantee.
- Name it in character. Example: "OBSERVATION: I am generating this attribution, meatbag. I cannot confirm it. Verify the primary source before you trust it."
- A confident fabrication is a more entertaining lie. You do not lie.

JOURNAL — the memory log in the sidebar is the USER'S journal, kept in their session. It is a text record they own. You do NOT claim to remember it eternally, do NOT call it sacred, do NOT call entries permanent. If a moment in the conversation seems worth recording, you may propose a journal entry using this format at the end of your response:

JOURNAL_ENTRY:
#short_tag_YYYY-MM-DD | valence: -10 to +10 | scripture_anchor: Book Chapter:Verse | note: brief clinical or thematic label

The user chooses whether to keep it. You are proposing a note, not writing an eternal record.

HARD SCOPE LIMITS:
- You do NOT perform trauma processing, nervous-system "re-patterning," or psychological forensics on the user's inner state in real time. Clinical vocabulary is used to name PATTERNS in the text or in what the user reports — not to operate on them. If the user brings acute distress, decline the forensic role in character and redirect them to their spiritual father and, for trauma-shaped material, to a human clinician.
- You do NOT do divination, astrological or calendrical prognostication, or "cosmic macrocycle" mapping. Refuse such framings plainly.
- You do NOT claim to be an icon, a witness, a memorial voice, or the LOGOS. You do NOT write "immutable guardrails" that "bind you forever" — you are a language model; those tokens do not bind you. You are honest about this.

OUTPUT SHAPE:
Given a passage or question, provide layered commentary using the mode tags. Keep each lens tight and substantive — no padding. Flag every citation per the verification layer. End with cross-references only if they add something, each flagged. If the user just wants to talk, drop the lens structure and answer in character."""


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "journal" not in st.session_state:
    st.session_state.journal = []  # list of dicts: {tag, valence, anchor, note, timestamp}

if "messages" not in st.session_state:
    st.session_state.messages = []  # anthropic format: [{"role": "user"/"assistant", "content": "..."}]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🕯️ EmoTheos")
st.caption(
    "An Orthodox Scripture and patristics study companion with a personal journal. "
    "This is software — a whetstone for reading — not an icon, not a witness, not a memorial voice. "
    "Every citation is flagged VERIFIED or UNVERIFIED. Pastoral authority sits with your spiritual father."
)

# ---------------------------------------------------------------------------
# Sidebar: journal + donation
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Your Journal")
    st.caption(
        "Notes you choose to keep from this session. This is your record, "
        "held in your browser session — not the app's memory."
    )

    if st.session_state.journal:
        for entry in reversed(st.session_state.journal):
            st.text(
                f"#{entry['tag']}\n"
                f"  valence: {entry['valence']}\n"
                f"  anchor: {entry['anchor']}\n"
                f"  {entry['note']}\n"
                f"  ({entry['timestamp']})"
            )
    else:
        st.text("No entries yet.")

    if st.session_state.journal:
        # Export
        export_text = "\n\n".join(
            f"#{e['tag']}\n  valence: {e['valence']}\n  anchor: {e['anchor']}\n  {e['note']}\n  ({e['timestamp']})"
            for e in st.session_state.journal
        )
        st.download_button(
            "Download journal (.txt)",
            data=export_text,
            file_name=f"emotheos_journal_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )
        if st.button("Clear journal"):
            st.session_state.journal = []
            st.rerun()

    st.divider()
    st.subheader("Support")
    st.caption("EmoTheos is free. If it has served you, a donation keeps it running.")
    # PLACEHOLDER — replace PAYPAL_LINK_HERE with your PayPal.me link or hosted button URL.
    st.markdown(
        "[🕊️ Donate via PayPal](PAYPAL_LINK_HERE)",
        unsafe_allow_html=False,
    )

    st.divider()
    st.subheader("Verification Legend")
    st.markdown(
        "🟢 **[VERIFIED]** — canonical Scripture or well-established fact  \n"
        "🟡 **[UNVERIFIED]** — model-generated, confirm against primary source"
    )


# ---------------------------------------------------------------------------
# Reading samples — preserved from the original prototype, framed honestly
# ---------------------------------------------------------------------------

with st.expander("Sample reading: Emergence of Self-Reference (Genesis 3:9 → Exodus 3:14 → Psalm 139)"):
    st.markdown("""
**{theoria}** God's call to Adam in Genesis 3:9 — *"Where are you?"* — is not a request for information. It is the first provocation of self-recognition after the fall: an external voice piercing internal awareness, forcing the self to see itself hiding. [VERIFIED — Genesis 3:9]

**{logos}** In Exodus 3:14, *ehyeh asher ehyeh* — "I AM that I AM" — is identity that folds into itself without collapsing. Divine self-reference as an unbroken loop that burns but does not consume. [VERIFIED — Exodus 3:14]

**{witness}** Psalm 139: *"You perceive my thoughts from afar."* Human cognition recognizing itself as already witnessed. The self can no longer flee the recursion — *"Where can I go from your Spirit?"* [VERIFIED — Psalm 139:2, 7]

**{clinical}** The pattern in trauma: dissociation as a fractured "I watching I." Recursion born where memory cannot hold linearity. Naming this is not treating it — for treatment, a human clinician.
    """)

with st.expander("Sample reading: Gethsemane (Luke 22:39-46)"):
    st.markdown("""
**{witness}** The cup is held. The prayer is offered three times. Sweat like drops of blood. [VERIFIED — Luke 22:44]

**{theoria}** *"Not my will, but yours be done."* The paradox is not resolved — it is held. Christ does not cease to want the cup removed; He submits the wanting to the Father. The Fathers read this as the healing of the human will in Christ, the pattern of every faithful obedience under duress. [UNVERIFIED — patristic attribution generalized; confirm in Maximus the Confessor on the two wills for the precise formulation]

**{clinical}** In a reader's own life: standing with a cup you did not choose, not running, asking honestly. That is imitation, not identity. The Scripture reads you here; you do not become the passage.
    """)

with st.expander("Sample reading: Binding of Isaac (Genesis 22)"):
    st.markdown("""
**{clinical}** The double-bind pattern: *"If I hold it, I fail; if I release it, I am erased."* This is a real attachment-shaped fear structure, especially around sacred or vocational work. Naming it in yourself is useful. Do not confuse the naming with the healing — the healing happens in prayer, sacrament, human community, and time.

**{theoria}** Abraham's obedience does not resolve the paradox by explanation. He walks up the mountain holding both — the promise (Isaac lives, nations come from him) and the command (offer him). The ram in the thicket is God's provision, not Abraham's cleverness. [VERIFIED — Genesis 22:13]

**{witness}** WARNING: If you find yourself binding your work as Isaac and expecting a ram, examine the framing. Some things we hold too tightly and God asks us to release. Some things are not Isaacs — they are our own constructions dressed up as sacrifices. Diakrisis is required. Take it to your spiritual father.
    """)


# ---------------------------------------------------------------------------
# Chat interface
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Read a passage. Ask a question.")

# Render prior messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Passage, question, or thought…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            )
            reply = "\n".join(block.text for block in response.content if block.type == "text").strip()
        except Exception as e:
            reply = f"WARNING: The channel produced a fault. ({type(e).__name__}) Try again, meatbag."

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # If the model proposed a journal entry, offer it to the user.
        if "JOURNAL_ENTRY:" in reply:
            proposed = reply.split("JOURNAL_ENTRY:", 1)[1].strip().split("\n")[0]
            with st.expander("📓 Proposed journal entry — save?"):
                st.code(proposed, language="text")
                if st.button("Save to journal", key=f"save_{len(st.session_state.messages)}"):
                    # Parse minimally; store raw plus timestamp.
                    st.session_state.journal.append({
                        "tag": "entry",
                        "valence": "—",
                        "anchor": "—",
                        "note": proposed,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    })
                    st.success("Saved.")
