# onboarding-gen

CLI tool that generates complete client onboarding documents using Claude AI. Give it a company name and product type — it produces a professional, ready-to-customize markdown package.

## What it does

Takes a company name and product description, then generates:
- **Welcome email** with personalized placeholders
- **Setup checklist** with step-by-step activation guide
- **Quick-start guide** highlighting core features
- **FAQ section** (8-10 questions covering billing, security, troubleshooting)
- **Escalation path** with SLA response times
- **30-60-90 day milestones** for customer success tracking

## Install

```bash
cd onboarding-gen
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

```bash
# Basic usage
python main.py "Monday.com" "project management SaaS"

# Enterprise tone, save to specific directory
python main.py "Wiz" "cloud security platform" --tone enterprise --output ./docs

# Casual tone, no terminal preview
python main.py "Lemonade" "insurance tech" --tone casual --no-preview
```

## Example Output

The tool generates a markdown file like `monday-com-onboarding.md` and renders a rich preview in terminal:

```
┌─── Onboarding Doc Generator ───┐
│ Company:  Monday.com           │
│ Product:  project management   │
│ Tone:     professional         │
└────────────────────────────────┘

⠋ Generating onboarding document with Claude...

✓ Saved to: monday-com-onboarding.md

┌─── Monday.com — Client Onboarding ────────────┐
│                                                │
│  # Welcome to Monday.com!                      │
│                                                │
│  Dear {CLIENT_NAME},                           │
│  ...                                           │
└────────────────────────────────────────────────┘
```

## Tone Options

| Tone | Best for |
|------|----------|
| `professional` | B2B SaaS, enterprise clients |
| `casual` | Consumer products, startups |
| `enterprise` | Large accounts, formal requirements |

## Project Structure

```
onboarding-gen/
├── main.py           # CLI entry point and document generation
├── requirements.txt  # Python dependencies
└── README.md
```
