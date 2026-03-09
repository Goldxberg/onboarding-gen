"""
onboarding-gen web app — generates client onboarding documents via Claude AI.
"""

import os
import anthropic
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def generate_onboarding_doc(company, product_type, tone="professional"):
    """Call Claude to generate a full onboarding document."""
    client = anthropic.Anthropic()

    prompt = f"""Generate a complete client onboarding document for a new customer of {company},
which offers a {product_type} product/service.

Create a professional, ready-to-send onboarding package in markdown format with these sections:

## 1. Welcome Email
Write a warm welcome email from the Customer Success team. Use {{{{CLIENT_NAME}}}} as placeholder.
Include value proposition reminder, what to expect in first 30 days, and contact info.

## 2. Setup Checklist
Step-by-step checklist (use markdown checkboxes) covering account activation,
key integrations, team invitations, initial configuration, and first milestone.

## 3. Product Quick-Start Guide
3-5 core features to explore first with common workflows and tips.

## 4. FAQ
8-10 frequently asked questions covering billing, technical requirements,
security, troubleshooting, and feature requests.

## 5. Escalation Path
Clear escalation matrix from self-service to engineering escalation with response time SLAs.

## 6. Key Milestones
A 30-60-90 day success plan with specific goals.

Use a {tone} tone. Be specific to {company} and {product_type}.
Format everything in clean, well-structured markdown."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    company = data.get("company", "").strip()
    product_type = data.get("product_type", "").strip()
    tone = data.get("tone", "professional")

    if not company or not product_type:
        return jsonify({"error": "Company and product type are required"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured on server"}), 500

    try:
        doc = generate_onboarding_doc(company, product_type, tone)
        return jsonify({"document": doc, "company": company})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
