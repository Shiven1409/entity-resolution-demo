
import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

st.set_page_config(
    page_title="Entity Resolution Control Tower",
    page_icon="🧭",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: #f6f2e8;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.app-shell {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 28px;
}

.side-panel {
    background: #fffefa;
    border: 1px solid #e6e0cf;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 28px rgba(40, 30, 10, 0.06);
}

.logo-row {
    display: flex;
    gap: 14px;
    align-items: center;
    margin-bottom: 24px;
}

.logo {
    background: #006b2e;
    color: #f8e96c;
    width: 58px;
    height: 58px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
}

.panel-title {
    font-weight: 800;
    font-size: 22px;
    margin-bottom: 2px;
}

.panel-subtitle {
    color: #3c4c3d;
    font-size: 16px;
}

.api-item {
    border: 1px solid #e7dfc9;
    border-radius: 14px;
    padding: 13px 15px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    background: #fbf8ee;
    font-size: 16px;
}

.api-name {
    font-weight: 700;
}

.api-meta {
    color: #39453a;
}

.highlight-box {
    margin-top: 18px;
    border: 8px solid #daf5dc;
    background: #f5fff8;
    border-radius: 22px;
    padding: 22px 18px;
    display: flex;
    gap: 14px;
    font-weight: 800;
    color: #006b2e;
}

.hero {
    background: #fffefa;
    border: 1px solid #e6e0cf;
    border-radius: 26px;
    padding: 22px 26px;
    box-shadow: 0 12px 28px rgba(40, 30, 10, 0.07);
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 34px;
    margin: 0;
}

.hero p {
    margin-top: 8px;
    font-size: 17px;
    color: #3e4a3f;
}

.card {
    background: #fffefa;
    border: 1px solid #e6e0cf;
    border-radius: 26px;
    padding: 22px 26px;
    box-shadow: 0 12px 28px rgba(40, 30, 10, 0.07);
    margin-bottom: 24px;
}

.card-header {
    display: grid;
    grid-template-columns: 80px 1fr 220px;
    align-items: start;
    gap: 10px;
}

.badge {
    background: #efecd9;
    border-radius: 10px;
    padding: 6px 10px;
    width: fit-content;
    font-size: 14px;
    color: #2d321f;
    font-weight: 700;
}

.entity-name {
    font-size: 23px;
    font-weight: 800;
    color: #041a1b;
}

.entity-subtitle {
    font-size: 16px;
    color: #3d4532;
}

.conf-label {
    font-size: 14px;
    letter-spacing: 3px;
    text-align: right;
    color: #102b28;
    font-weight: 600;
}

.bar-bg {
    height: 12px;
    background: #e7e8ce;
    border-radius: 20px;
    margin-top: 10px;
    overflow: hidden;
}

.bar-fill {
    height: 12px;
    background: #00a91c;
    border-radius: 20px;
}

.conf-score {
    text-align: right;
    color: #00751c;
    font-weight: 700;
    margin-top: 4px;
}

.evidence-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(145px, 1fr));
    gap: 12px;
    margin-top: 28px;
}

.evidence-box {
    border: 1px solid #b7e9bf;
    background: #f6fff8;
    border-radius: 13px;
    padding: 13px 15px;
    min-height: 68px;
}

.evidence-label {
    color: #06342d;
    font-size: 14px;
    letter-spacing: 1.5px;
    font-weight: 700;
}

.evidence-value {
    margin-top: 6px;
    color: #00651f;
    font-family: monospace;
    font-size: 15px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.reason {
    margin-top: 16px;
    font-weight: 800;
    color: #006b2e;
    font-size: 16px;
}

.reject {
    color: #9b1c1c;
}

.warn {
    color: #996b00;
}

.tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 22px;
}

.metric {
    background: #fffefa;
    border: 1px solid #e6e0cf;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 8px 18px rgba(40, 30, 10, 0.05);
}

.metric-number {
    font-size: 28px;
    font-weight: 800;
}

.metric-label {
    color: #445042;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


def similarity(a, b):
    return round(SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio(), 2)


examples = [
    {
        "id": "H-1042",
        "title": "Café Björn",
        "subtitle": "Weak match candidate",
        "confidence_before": 62,
        "confidence_after": 95,
        "decision": "Strengthened",
        "evidence": {
            "LEGAL NAME": "BJØRN CAFÉ ApS",
            "CVR": "41 20 98 87",
            "NACE": "56.10 Restaurants",
            "ADDRESS": "Gothersgade 22, Copenhagen",
        },
        "reason": "Strengthened, confidence raised from 62% to 95%",
        "source": "CVR Open Data + Google Places",
        "status": "AUTO APPROVE"
    },
    {
        "id": "M-7841",
        "title": "Vinter & Co Catering",
        "subtitle": "Weak match candidate",
        "confidence_before": 48,
        "confidence_after": 90,
        "decision": "Strengthened",
        "evidence": {
            "LEGAL NAME": "Vinter & Co Catering ApS",
            "CVR": "39 00 21 41",
            "NACE": "56.21 Event catering",
            "ADDRESS": "Kongensgade 8, Odense",
        },
        "reason": "Strengthened, confidence raised from 48% to 90%",
        "source": "CVR Open Data + krak.dk",
        "status": "AUTO APPROVE"
    },
    {
        "id": "H-1203",
        "title": "Bageriet på Hjørnet",
        "subtitle": "Weak match candidate",
        "confidence_before": 71,
        "confidence_after": 93,
        "decision": "Strengthened",
        "evidence": {
            "LEGAL NAME": "Bageriet på Hjørnet ApS",
            "PLACES ID": "ChIJ-OdenseBaker...",
            "HOURS": "Mon–Sat · 06:00–16:00",
            "ADDRESS": "Vestergade 44, Odense",
        },
        "reason": "Strengthened, confidence raised from 71% to 93%",
        "source": "Google Places",
        "status": "AUTO APPROVE"
    },
    {
        "id": "SE-2209",
        "title": "Restaurang ÄNG",
        "subtitle": "Client example: similar domain but different entity",
        "confidence_before": 82,
        "confidence_after": 18,
        "decision": "Rejected",
        "evidence": {
            "HL WEBSITE": "restaurangang.se",
            "CM WEBSITE": "restauranga.se",
            "HL ADDRESS": "Ästad 10, Tvååker",
            "CM ADDRESS": "Bränsle Gård, Åkersberga",
        },
        "reason": "Rejected, similar domain strings but different addresses and restaurant concepts",
        "source": "Website verification + Places",
        "status": "REJECT"
    },
    {
        "id": "DK-1038",
        "title": "Café N",
        "subtitle": "Perfect fuzzy name but weak external proof",
        "confidence_before": 100,
        "confidence_after": 42,
        "decision": "Downgraded",
        "evidence": {
            "HL WEBSITE": "cafe-n.dk",
            "CM DOMAIN": "hotmail.com",
            "NAME MATCH": "Café N ≈ Cafen",
            "RISK": "Generic email domain",
        },
        "reason": "Downgraded, generic email domain gives no firmographic proof",
        "source": "Domain quality rules",
        "status": "HUMAN REVIEW"
    },
]


def render_card(item):
    status_class = "reject" if item["status"] == "REJECT" else "warn" if item["status"] == "HUMAN REVIEW" else ""
    bar = item["confidence_after"]
    evidence_html = ""
    for label, value in item["evidence"].items():
        evidence_html += f"""
        <div class="evidence-box">
            <div class="evidence-label">{label}</div>
            <div class="evidence-value">{value}</div>
        </div>
        """

    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="badge">{item["id"]}</div>
            <div>
                <div class="entity-name">{item["title"]}</div>
                <div class="entity-subtitle">{item["subtitle"]}</div>
            </div>
            <div>
                <div class="conf-label">CONFIDENCE</div>
                <div class="bar-bg"><div class="bar-fill" style="width:{bar}%"></div></div>
                <div class="conf-score">{bar}%</div>
            </div>
        </div>
        <div class="evidence-grid">
            {evidence_html}
        </div>
        <div class="reason {status_class}">✣ {item["reason"]}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="app-shell">', unsafe_allow_html=True)

left, right = st.columns([0.31, 0.69], gap="large")

with left:
    st.markdown("""
    <div class="side-panel">
        <div class="logo-row">
            <div class="logo">🧭</div>
            <div>
                <div class="panel-title">External APIs</div>
                <div class="panel-subtitle">Firmographic & place data</div>
            </div>
        </div>

        <div class="api-item"><span class="api-name">CVR Open Data</span><span class="api-meta">DK · authoritative</span></div>
        <div class="api-item"><span class="api-name">krak.dk</span><span class="api-meta">B2B directory</span></div>
        <div class="api-item"><span class="api-name">Google Places</span><span class="api-meta">geo · hours</span></div>
        <div class="api-item"><span class="api-name">Dun & Bradstreet</span><span class="api-meta">firmographic</span></div>
        <div class="api-item"><span class="api-name">Web crawler</span><span class="api-meta">website proof</span></div>

        <div class="highlight-box">
            <div>⌁</div>
            <div>Streaming enrichments → weak matches → explainable decisions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("### Controls")
    market = st.selectbox("Market", ["All", "DK", "SE", "NO", "DE"])
    decision = st.selectbox("Decision", ["All", "AUTO APPROVE", "HUMAN REVIEW", "REJECT"])
    min_conf = st.slider("Minimum confidence", 0, 100, 0)

with right:
    st.markdown("""
    <div class="hero">
        <h1>Entity Resolution Control Tower</h1>
        <p>Databricks App demo for Huntlist ↔ Contact Master matching with external enrichment, proof, and explainable confidence.</p>
    </div>
    """, unsafe_allow_html=True)

    filtered = [
        x for x in examples
        if (decision == "All" or x["status"] == decision)
        and x["confidence_after"] >= min_conf
    ]

    approved = sum(1 for x in examples if x["status"] == "AUTO APPROVE")
    review = sum(1 for x in examples if x["status"] == "HUMAN REVIEW")
    rejected = sum(1 for x in examples if x["status"] == "REJECT")
    avg_conf = int(sum(x["confidence_after"] for x in examples) / len(examples))

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric"><div class="metric-number">{len(examples)}</div><div class="metric-label">Candidates evaluated</div></div>
        <div class="metric"><div class="metric-number">{approved}</div><div class="metric-label">Auto-approved</div></div>
        <div class="metric"><div class="metric-number">{review}</div><div class="metric-label">Human review</div></div>
        <div class="metric"><div class="metric-number">{avg_conf}%</div><div class="metric-label">Avg final confidence</div></div>
    </div>
    """, unsafe_allow_html=True)

    for item in filtered:
        render_card(item)

    st.write("### Match audit table")
    audit_df = pd.DataFrame([
        {
            "CandidateId": x["id"],
            "Entity": x["title"],
            "Before": x["confidence_before"],
            "After": x["confidence_after"],
            "Decision": x["status"],
            "Primary proof": x["source"],
            "Reason": x["reason"],
        }
        for x in examples
    ])
    st.dataframe(audit_df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)
