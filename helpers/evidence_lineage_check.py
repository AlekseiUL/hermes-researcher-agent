#!/usr/bin/env python3
"""Validate a public-safe research run, source lineages, and counterexample evidence."""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlparse

SCHEMA_VERSION = "research-run/v1"
MODES = {
    "quick_fact",
    "deep_research",
    "repo_tool",
    "community_pain",
    "live_visual",
    "monitoring_design",
}
SOURCE_CLASSES = {"primary", "structured_data", "independent", "community", "discovery"}
CAPTURE_METHODS = {"web", "browser", "api", "rss", "json", "document", "dom", "vision"}
ACCESS_STATES = {"public", "degraded", "blocked", "login_required", "paid_private"}
CLASSIFICATIONS = {"fact", "claim", "weak_signal", "hypothesis", "interpretation"}
COUNTEREXAMPLE_STATES = {"found", "none_found", "not_applicable"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
USABLE_ACCESS = {"public", "degraded"}
SENSITIVE_QUERY_KEYS = {
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "key",
    "password",
    "secret",
    "signature",
    "token",
}
_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}\Z")


class ValidationError(ValueError):
    """A stable, user-readable validation error."""


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def _exact_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(value))
    unknown = sorted(set(value) - fields)
    if missing:
        raise ValidationError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise ValidationError(f"{label} unknown fields: {', '.join(unknown)}")


def _text(value: Any, label: str, *, limit: int = 4096) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    text = value.strip()
    if len(text) > limit:
        raise ValidationError(f"{label} exceeds {limit} characters")
    return text


def _identifier(value: Any, label: str) -> str:
    text = _text(value, label, limit=128)
    if _ID.fullmatch(text) is None:
        raise ValidationError(f"{label} has an invalid identifier")
    return text


def _timestamp(value: Any, label: str) -> str:
    text = _text(value, label, limit=64)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValidationError(f"{label} must be ISO-8601") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidationError(f"{label} must include a timezone")
    return text


def _enum(value: Any, allowed: set[str], label: str) -> str:
    text = _text(value, label, limit=64)
    if text not in allowed:
        raise ValidationError(f"{label} is not supported: {text}")
    return text


def _string_list(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a non-empty list" if not allow_empty else "a list"
        raise ValidationError(f"{label} must be {qualifier}")
    result = [_identifier(item, f"{label} item") for item in value]
    if len(result) != len(set(result)):
        raise ValidationError(f"{label} contains duplicates")
    return result


def _url(value: Any, label: str) -> str:
    text = _text(value, label, limit=2048)
    try:
        parsed = urlparse(text)
        hostname = parsed.hostname
        parsed.port  # Validate port syntax.
    except ValueError as error:
        raise ValidationError(f"{label} must be a valid public HTTP(S) URL") from error
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValidationError(f"{label} must be a public HTTP(S) URL without credentials")
    normalized_host = hostname.rstrip(".").lower()
    if normalized_host == "localhost" or normalized_host.endswith(".localhost"):
        raise ValidationError(f"{label} must not expose a local host")
    if normalized_host.endswith(".local") or normalized_host.endswith(".internal"):
        raise ValidationError(f"{label} must not expose an internal host")
    try:
        address = ipaddress.ip_address(normalized_host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValidationError(f"{label} must not expose a non-public IP address")
    sensitive_keys = sorted(
        key
        for key, _ in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() in SENSITIVE_QUERY_KEYS
    )
    if sensitive_keys:
        raise ValidationError(
            f"{label} contains sensitive query fields: {', '.join(sensitive_keys)}"
        )
    return text


def validate_run(data: Any) -> dict[str, Any]:
    run = _object(data, "run")
    _exact_fields(
        run,
        {
            "schema_version",
            "research_id",
            "mode",
            "question",
            "decision",
            "collected_at",
            "sources",
            "claims",
            "coverage_gaps",
            "next_move",
        },
        "run",
    )
    if run["schema_version"] != SCHEMA_VERSION:
        raise ValidationError(f"schema_version must be {SCHEMA_VERSION}")
    _identifier(run["research_id"], "research_id")
    _enum(run["mode"], MODES, "mode")
    _text(run["question"], "question")
    _text(run["decision"], "decision")
    _timestamp(run["collected_at"], "collected_at")
    _text(run["next_move"], "next_move")
    if not isinstance(run["coverage_gaps"], list):
        raise ValidationError("coverage_gaps must be a list")
    for index, gap in enumerate(run["coverage_gaps"]):
        _text(gap, f"coverage_gaps[{index}]", limit=1024)

    raw_sources = run["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValidationError("sources must be a non-empty list")
    sources: dict[str, dict[str, str]] = {}
    for index, raw in enumerate(raw_sources):
        source = _object(raw, f"sources[{index}]")
        _exact_fields(
            source,
            {
                "id",
                "title",
                "url",
                "source_class",
                "capture_method",
                "lineage_id",
                "access_state",
                "checked_at",
            },
            f"sources[{index}]",
        )
        source_id = _identifier(source["id"], f"sources[{index}].id")
        if source_id in sources:
            raise ValidationError(f"duplicate source id: {source_id}")
        sources[source_id] = {
            "title": _text(source["title"], f"sources[{index}].title", limit=512),
            "url": _url(source["url"], f"sources[{index}].url"),
            "source_class": _enum(
                source["source_class"], SOURCE_CLASSES, f"sources[{index}].source_class"
            ),
            "capture_method": _enum(
                source["capture_method"], CAPTURE_METHODS, f"sources[{index}].capture_method"
            ),
            "lineage_id": _identifier(source["lineage_id"], f"sources[{index}].lineage_id"),
            "access_state": _enum(
                source["access_state"], ACCESS_STATES, f"sources[{index}].access_state"
            ),
            "checked_at": _timestamp(source["checked_at"], f"sources[{index}].checked_at"),
        }

    raw_claims = run["claims"]
    if not isinstance(raw_claims, list) or not raw_claims:
        raise ValidationError("claims must be a non-empty list")
    claim_ids: set[str] = set()
    relevant_claims = 0
    for index, raw in enumerate(raw_claims):
        claim = _object(raw, f"claims[{index}]")
        _exact_fields(
            claim,
            {
                "id",
                "statement",
                "classification",
                "decision_relevant",
                "evidence_source_ids",
                "counterexample_source_ids",
                "counterexample_status",
                "counterexample_note",
                "confidence",
            },
            f"claims[{index}]",
        )
        claim_id = _identifier(claim["id"], f"claims[{index}].id")
        if claim_id in claim_ids:
            raise ValidationError(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        _text(claim["statement"], f"claims[{index}].statement")
        _enum(claim["classification"], CLASSIFICATIONS, f"claims[{index}].classification")
        if type(claim["decision_relevant"]) is not bool:
            raise ValidationError(f"claims[{index}].decision_relevant must be a boolean")
        evidence_ids = _string_list(
            claim["evidence_source_ids"],
            f"claims[{index}].evidence_source_ids",
            allow_empty=not claim["decision_relevant"],
        )
        counterexample_ids = _string_list(
            claim["counterexample_source_ids"], f"claims[{index}].counterexample_source_ids"
        )
        counterexample_status = _enum(
            claim["counterexample_status"],
            COUNTEREXAMPLE_STATES,
            f"claims[{index}].counterexample_status",
        )
        counterexample_note = _text(
            claim["counterexample_note"], f"claims[{index}].counterexample_note", limit=1024
        )
        _enum(claim["confidence"], CONFIDENCE_LEVELS, f"claims[{index}].confidence")

        referenced = evidence_ids + counterexample_ids
        unknown = sorted(set(referenced) - set(sources))
        if unknown:
            raise ValidationError(f"claim {claim_id} references unknown sources: {', '.join(unknown)}")
        if counterexample_status == "found" and not counterexample_ids:
            raise ValidationError(f"claim {claim_id} says counterexample found but cites none")
        if counterexample_status != "found" and counterexample_ids:
            raise ValidationError(
                f"claim {claim_id} cites counterexamples but status is {counterexample_status}"
            )
        overlap = sorted(set(evidence_ids) & set(counterexample_ids))
        if overlap:
            raise ValidationError(
                f"claim {claim_id} uses the same sources as evidence and counterexamples: "
                + ", ".join(overlap)
            )

        if claim["decision_relevant"]:
            relevant_claims += 1
            usable = [sources[source_id] for source_id in evidence_ids]
            unusable_ids = [
                source_id
                for source_id in evidence_ids
                if sources[source_id]["access_state"] not in USABLE_ACCESS
            ]
            if unusable_ids:
                raise ValidationError(
                    f"claim {claim_id} uses inaccessible evidence: {', '.join(unusable_ids)}"
                )
            if any(source["source_class"] == "discovery" for source in usable):
                raise ValidationError(f"claim {claim_id} uses discovery-only material as evidence")
            lineages = {source["lineage_id"] for source in usable}
            if len(lineages) < 2:
                raise ValidationError(
                    f"claim {claim_id} needs at least two independent source lineages"
                )
            if not any(
                source["source_class"] in {"primary", "structured_data"} for source in usable
            ):
                raise ValidationError(
                    f"claim {claim_id} needs primary or structured-data evidence"
                )
            if counterexample_status == "found":
                inaccessible_counterexamples = [
                    source_id
                    for source_id in counterexample_ids
                    if sources[source_id]["access_state"] not in USABLE_ACCESS
                ]
                if inaccessible_counterexamples:
                    raise ValidationError(
                        f"claim {claim_id} uses inaccessible counterexamples: "
                        + ", ".join(inaccessible_counterexamples)
                    )

    if not relevant_claims:
        raise ValidationError("at least one claim must be decision_relevant")

    lineage_counts: dict[str, int] = {}
    for source in sources.values():
        lineage_counts[source["lineage_id"]] = lineage_counts.get(source["lineage_id"], 0) + 1
    duplicate_copies = sum(count - 1 for count in lineage_counts.values() if count > 1)
    return {
        "ok": True,
        "schema_version": SCHEMA_VERSION,
        "mode": run["mode"],
        "source_count": len(sources),
        "lineage_count": len(lineage_counts),
        "duplicate_copies_collapsed": duplicate_copies,
        "claim_count": len(raw_claims),
        "decision_relevant_claim_count": relevant_claims,
    }


def load_json(path: Path) -> Any:
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValidationError("research run exceeds 2 MiB")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"could not read strict JSON: {error}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate source independence and counterexample handling in a research run."
    )
    parser.add_argument("run", type=Path, help="path to a research-run/v1 JSON file")
    parser.add_argument("--json", action="store_true", help="print a JSON result")
    args = parser.parse_args(argv)
    try:
        result = validate_run(load_json(args.run))
    except (OSError, ValidationError) as error:
        payload = {"ok": False, "error": str(error)}
        print(json.dumps(payload, ensure_ascii=False) if args.json else f"FAIL: {error}")
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else "PASS: research run is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
