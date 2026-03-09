#!/usr/bin/env python3
"""
onboarding-gen: Generates complete client onboarding documents using Claude AI.
Takes a company name + product type → outputs professional markdown.
"""

import os
import re
import click
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import box

console = Console()


def generate_onboarding_doc(company, product_type, tone="professional", api_key=None):
    """Call Claude to generate a full onboarding document."""
    client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    prompt = f"""Generate a complete client onboarding document for a new customer of {company},
which offers a {product_type} product/service.

Create a professional, ready-to-send onboarding package in markdown format with these sections:

## 1. Welcome Email
Write a warm, professional welcome email from the Customer Success team. Include:
- Personalized greeting (use {{{{CLIENT_NAME}}}} as placeholder)
- Brief value proposition reminder
- What to expect in the first 30 days
- Direct contact information

## 2. Setup Checklist
A step-by-step checklist (use markdown checkboxes) covering:
- Account activation steps
- Key integrations to configure
- Team member invitations
- Initial configuration items
- First milestone to achieve

## 3. Product Quick-Start Guide
- 3-5 core features to explore first
- Common workflows with brief descriptions
- Tips for getting value quickly

## 4. FAQ
Write 8-10 frequently asked questions with clear answers covering:
- Billing and plans
- Technical requirements
- Data security/privacy
- Common troubleshooting
- Feature requests process

## 5. Escalation Path
A clear escalation matrix:
- Level 1: Self-service resources (docs, knowledge base)
- Level 2: Email/chat support (include response time SLAs)
- Level 3: Dedicated account manager
- Level 4: Engineering escalation
Include expected response times for each level.

## 6. Key Milestones
A 30-60-90 day success plan with specific goals for each period.

Use a {tone} tone throughout. Make it specific to {company} and {product_type} —
don't be generic. Include realistic details that show domain knowledge.

Format everything in clean, well-structured markdown."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def save_document(content, company, output_dir="."):
    """Save the generated document as a markdown file."""
    # Sanitize company name for filename
    safe_name = re.sub(r'[^\w\s-]', '', company).strip().lower().replace(' ', '-')
    filename = f"{safe_name}-onboarding.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(content)

    return filepath


@click.command()
@click.argument("company")
@click.argument("product_type")
@click.option("--tone", "-t", default="professional",
              type=click.Choice(["professional", "casual", "enterprise"]),
              help="Document tone.")
@click.option("--output", "-o", default=".", help="Output directory.")
@click.option("--preview/--no-preview", default=True, help="Preview in terminal.")
def main(company, product_type, tone, output, preview):
    """Generate an onboarding document for COMPANY with PRODUCT_TYPE."""
    console.print(Panel(
        f"[bold]Company:[/bold]  {company}\n"
        f"[bold]Product:[/bold]  {product_type}\n"
        f"[bold]Tone:[/bold]     {tone}",
        title="[bold magenta]Onboarding Doc Generator[/bold magenta]",
        border_style="magenta",
    ))

    # Generate with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating onboarding document with Claude...", total=None)
        content = generate_onboarding_doc(company, product_type, tone)
        progress.update(task, description="Document generated!")

    # Save to file
    filepath = save_document(content, company, output)
    console.print(f"\n[green]Saved to:[/green] [bold]{filepath}[/bold]\n")

    # Preview in terminal
    if preview:
        console.print(Panel(
            Markdown(content),
            title=f"[bold]{company} — Client Onboarding[/bold]",
            border_style="magenta",
            padding=(1, 2),
        ))


if __name__ == "__main__":
    main()
