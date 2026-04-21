from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Mapping, Sequence


FAQ = "FAQ"
UX_GAP = "UX_GAP"
DEFECT = "DEFECT"

P1 = "P1"
P2 = "P2"

CUSTOMER_REPLY = "Customer Reply Draft"
UX_REVIEW = "UX Review"
HOTFIX_QUEUE = "Hotfix Queue"
SPRINT_BACKLOG = "Sprint Backlog"
BACKLOG = "Backlog"

DEFECT_KEYWORDS = (
    "error",
    "fails",
    "failed",
    "failure",
    "crash",
    "500",
    "blocked",
    "cannot",
    "can't",
    "never completes",
    "delayed",
    "lags",
    "late",
)

UX_GAP_KEYWORDS = (
    "confusing",
    "unclear",
    "label",
    "tooltip",
    "dashboard",
    "report",
    "reports",
    "filter",
    "navigation",
    "wording",
)

FAQ_KEYWORDS = (
    "how do i",
    "how can i",
    "where do i",
    "where is",
    "what is",
    "how to",
    "guide",
    "documented",
    "document",
)

P1_KEYWORDS = (
    "bid",
    "bidding",
    "integration",
    "sync",
    "checkout",
    "pay",
    "payment",
    "api",
    "webhook",
)

P2_KEYWORDS = (
    "insight",
    "insights",
    "report",
    "reports",
    "dashboard",
    "analytics",
    "filter",
    "export",
    "chart",
)


@dataclass(frozen=True)
class NormalizedTicket:
    ticket_id: str
    source: str
    received_at: str
    language: str
    customer: str
    title: str
    content: str
    attachments_summary: str
    ux_area: str
    prior_similar_ux_count: int
    search_text: str


@dataclass(frozen=True)
class TicketAnalysis:
    ticket_id: str
    source: str
    customer: str
    title: str
    category: str
    severity: str
    scope_label: str
    route: str
    rationale: str
    evidence: tuple[str, ...]
    received_at: str
    language: str
    attachments_summary: str
    codex_pr_candidate: bool


@dataclass(frozen=True)
class PipelineReport:
    source_path: str
    tickets: tuple[TicketAnalysis, ...]
    category_counts: dict[str, int]
    scope_counts: dict[str, int]
    route_counts: dict[str, int]


def load_seed_tickets(path: str | Path | Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(path, (str, Path)):
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        raw = path

    tickets = raw.get("tickets", []) if isinstance(raw, Mapping) else raw
    if not isinstance(tickets, list):
        raise TypeError("Seed data must contain a list of tickets")
    return [dict(item) for item in tickets]


def normalize_ticket(raw_ticket: Mapping[str, Any], position: int) -> NormalizedTicket:
    ticket_id = str(raw_ticket.get("id") or raw_ticket.get("ticket_id") or f"ticket-{position}")
    source = _clean_text(raw_ticket.get("source"), default="seed")
    received_at = _clean_text(raw_ticket.get("received_at"))
    language = _clean_text(raw_ticket.get("language"), default="en")
    customer = _clean_text(
        raw_ticket.get("customer_name")
        or raw_ticket.get("customer_org")
        or raw_ticket.get("customer")
        or "Unknown"
    )
    title = _clean_text(raw_ticket.get("title"))
    content = _clean_text(raw_ticket.get("raw_content") or raw_ticket.get("content") or "")
    attachments_summary = _clean_text(raw_ticket.get("attachments_summary") or "none")
    ux_area = _clean_text(raw_ticket.get("ux_area") or "general")
    prior_similar_ux_count = _coerce_int(raw_ticket.get("prior_similar_ux_count"), default=0)
    search_text = " ".join(part for part in (title, content, attachments_summary) if part).lower()

    return NormalizedTicket(
        ticket_id=ticket_id,
        source=source,
        received_at=received_at,
        language=language,
        customer=customer,
        title=title,
        content=content,
        attachments_summary=attachments_summary,
        ux_area=ux_area,
        prior_similar_ux_count=prior_similar_ux_count,
        search_text=search_text,
    )


def analyze_ticket(ticket: NormalizedTicket) -> TicketAnalysis:
    category, category_evidence, category_rationale = classify_category(ticket.search_text)
    severity = classify_severity(ticket.search_text) if category in {UX_GAP, DEFECT} else "-"
    scope_label, scope_evidence = classify_scope(ticket.search_text)
    route = derive_route(category, severity)
    codex_pr_candidate = category == UX_GAP and (ticket.prior_similar_ux_count + 1) >= 3
    evidence = tuple(dict.fromkeys(category_evidence + scope_evidence))
    rationale_parts = [category_rationale, _scope_rationale(scope_label, scope_evidence)]
    if codex_pr_candidate:
        rationale_parts.append(
            f"UX area '{ticket.ux_area}' already had {ticket.prior_similar_ux_count} similar cases, so this ticket crosses the Codex PR trigger threshold."
        )

    return TicketAnalysis(
        ticket_id=ticket.ticket_id,
        source=ticket.source,
        customer=ticket.customer,
        title=ticket.title,
        category=category,
        severity=severity,
        scope_label=scope_label,
        route=route,
        rationale=" ".join(part for part in rationale_parts if part),
        evidence=evidence,
        received_at=ticket.received_at,
        language=ticket.language,
        attachments_summary=ticket.attachments_summary,
        codex_pr_candidate=codex_pr_candidate,
    )


def classify_category(search_text: str) -> tuple[str, list[str], str]:
    defect_matches = _matched_keywords(search_text, DEFECT_KEYWORDS)
    if defect_matches:
        return DEFECT, defect_matches, f"Defect signals matched: {', '.join(defect_matches)}."

    ux_gap_matches = _matched_keywords(search_text, UX_GAP_KEYWORDS)
    if ux_gap_matches:
        return UX_GAP, ux_gap_matches, f"UX gap signals matched: {', '.join(ux_gap_matches)}."

    faq_matches = _matched_keywords(search_text, FAQ_KEYWORDS)
    if faq_matches:
        return FAQ, faq_matches, f"FAQ phrasing matched: {', '.join(faq_matches)}."

    return FAQ, [], "No defect or UX gap signals matched, so the ticket defaults to FAQ."


def classify_severity(search_text: str) -> str:
    high_markers = ("blocked", "cannot", "can't", "crash", "500", "payment", "checkout", "never completes")
    medium_markers = ("fails", "failed", "error", "lag", "delayed", "partial")
    if _contains_any(search_text, high_markers):
        return "HIGH"
    if _contains_any(search_text, medium_markers):
        return "MEDIUM"
    return "LOW"


def classify_scope(search_text: str) -> tuple[str, list[str]]:
    p1_matches = _matched_keywords(search_text, P1_KEYWORDS)
    if p1_matches:
        return P1, p1_matches
    p2_matches = _matched_keywords(search_text, P2_KEYWORDS)
    if p2_matches:
        return P2, p2_matches
    return P2, ["defaulted-to-p2"]


def derive_route(category: str, severity: str) -> str:
    if category == FAQ:
        return CUSTOMER_REPLY
    if category == UX_GAP:
        return UX_REVIEW
    if severity == "HIGH":
        return HOTFIX_QUEUE
    if severity == "MEDIUM":
        return SPRINT_BACKLOG
    return BACKLOG


def run_pipeline(seed_path: str | Path, output_path: str | Path | None = None) -> PipelineReport:
    raw_tickets = load_seed_tickets(seed_path)
    analyses = [analyze_ticket(normalize_ticket(ticket, index + 1)) for index, ticket in enumerate(raw_tickets)]
    report = PipelineReport(
        source_path=str(Path(seed_path)),
        tickets=tuple(analyses),
        category_counts=dict(Counter(item.category for item in analyses)),
        scope_counts=dict(Counter(item.scope_label for item in analyses)),
        route_counts=dict(Counter(item.route for item in analyses)),
    )
    if output_path is not None:
        write_markdown_report(report, output_path)
    return report


def write_markdown_report(report: PipelineReport, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown_report(report), encoding="utf-8")
    return output


def render_markdown_report(report: PipelineReport) -> str:
    lines = [
        "# CS triage demo report",
        "",
        f"Source seed: `{report.source_path}`",
        f"Tickets processed: {len(report.tickets)}",
        "",
        "## Tickets",
        "",
    ]
    for ticket in report.tickets:
        evidence = ", ".join(ticket.evidence) if ticket.evidence else "none"
        lines.extend(
            [
                f"### {ticket.ticket_id} - {ticket.title}",
                "",
                f"- Source: {ticket.source}",
                f"- Customer: {ticket.customer}",
                f"- Received: {ticket.received_at}",
                f"- Language: {ticket.language}",
                f"- Category: {ticket.category}",
                f"- Severity: {ticket.severity}",
                f"- Scope: {ticket.scope_label}",
                f"- Route: {ticket.route}",
                f"- Codex PR candidate: {'yes' if ticket.codex_pr_candidate else 'no'}",
                f"- Evidence: {evidence}",
                f"- Rationale: {ticket.rationale}",
                f"- Attachments: {ticket.attachments_summary}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _clean_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _matched_keywords(search_text: str, keywords: Sequence[str]) -> list[str]:
    return [keyword for keyword in keywords if keyword in search_text]


def _contains_any(search_text: str, keywords: Sequence[str]) -> bool:
    return any(keyword in search_text for keyword in keywords)


def _scope_rationale(scope_label: str, scope_evidence: Sequence[str]) -> str:
    if len(scope_evidence) == 1 and scope_evidence[0] == "defaulted-to-p2":
        return "No explicit bid/integration or reporting cues were found, so the ticket defaults to P2."
    if scope_label == P1:
        return f"P1 scope was selected because the ticket touches: {', '.join(scope_evidence)}."
    return f"P2 scope was selected because the ticket touches: {', '.join(scope_evidence)}."


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
