"""
BASELINE bot (no AI): keyword router + template answer.
Keep this! It is your control experiment: later you prove the AI version beats it
on messy questions (typos, Nepali/English mixing, follow-ups, new procedures).
"""
import re
from typing import Dict, Optional, Tuple
from .schemas import Procedure, AskResponse


def _tokens(text: str):
    return set(re.findall(r"\w+", text.lower()))


def route(question: str, kb: Dict[str, Procedure]) -> Tuple[str, Optional[Procedure], float]:
    q = _tokens(question)
    best, best_score = None, 0.0
    for p in kb.values():
        words = set()
        for a in [p.title_en, p.title_ne or ""] + p.aliases:
            words |= _tokens(a)
        if not words:
            continue
        score = len(q & words) / len(words)
        if score > best_score:
            best, best_score = p, score
    if best is None or best_score == 0:
        return "defer_to_office", None, 0.0
    if best_score < 0.25:
        return "ask_clarifying", best, best_score
    return "answer_from_kb", best, best_score


def compose(p: Procedure) -> str:
    req = [d for d in p.documents if d.required]
    opt = [d for d in p.documents if not d.required]
    lines = [f"**{p.title_en}**", f"Office: {p.office} ({p.municipality})", f"Mode: {p.mode}"]
    if p.practical_tip:
        lines.append(f"Tip ({p.tip_source_type}): {p.practical_tip}")
    lines.append("\nSteps:")
    lines += [f"{s.order}. {s.action}" + (f" — {s.where}" if s.where else "") for s in p.steps]
    lines.append("\nRequired documents:")
    lines += [f"- {d.name}" for d in req]
    if opt:
        lines.append("\nOptional but useful:")
        lines += [f"- {d.name}" + (f" — {d.reason}" if d.reason else "") for d in opt]
    if p.fee:
        lines.append(f"\nFee: {p.fee}")
    if p.time_needed:
        lines.append(f"Time: {p.time_needed}")
    lines.append(f"\nLast verified: {max(s.last_verified for s in p.sources)}")
    return "\n".join(lines)


def answer(question: str, kb: Dict[str, Procedure]) -> AskResponse:
    r, p, conf = route(question, kb)
    if r == "answer_from_kb" and p:
        return AskResponse(route=r, answer=compose(p), procedure_id=p.id,
                           confidence=round(conf, 2), sources=p.sources)
    if r == "ask_clarifying":
        return AskResponse(route=r, procedure_id=p.id if p else None, confidence=round(conf, 2),
                           answer="I am not sure which procedure you mean. Can you say it differently?")
    return AskResponse(route=r, answer="I don't have verified information on this yet. "
                                       "Please confirm at the ward/municipal office.")
