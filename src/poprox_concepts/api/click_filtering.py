from collections import defaultdict
from datetime import timedelta
from itertools import chain, zip_longest
from uuid import UUID

from poprox_concepts.domain import Click

INHUMAN_SPEED_MS = 250
CLICK_DEBOUNCE_MS = 10000


def filter_click_histories(click_histories: dict[UUID, list[Click]]) -> dict[UUID, list[Click]]:
    filtered_click_histories = {}
    for account_id, click_history in click_histories.items():
        clicks_by_newsletter = defaultdict(list)
        for click in click_history:
            clicks_by_newsletter[click.newsletter_id].append(click)

        for newsletter_id, newsletter_clicks in clicks_by_newsletter.items():
            clicks_by_newsletter[newsletter_id] = filter_newsletter_clicks(newsletter_clicks)

        filtered_click_histories[account_id] = sorted(
            chain.from_iterable(clicks_by_newsletter.values()), key=lambda c: c.timestamp
        )

    return filtered_click_histories


def filter_newsletter_clicks(clicks: list[Click]) -> list[Click]:
    if len(clicks) < 2:
        return clicks

    sorted_clicks = sorted(clicks, key=lambda c: c.timestamp)

    # Deduplicate successive double clicks on the same article
    deduped_clicks = []
    for click, next_click in zip_longest(sorted_clicks, sorted_clicks[1:]):
        if (
            next_click is None
            or click.article_id != next_click.article_id
            or next_click.timestamp - click.timestamp > timedelta(seconds=CLICK_DEBOUNCE_MS / 1000)
        ):
            deduped_clicks.append(click)

    # Remove runs of clicks on different articles in under a second
    organic_clicks = []
    prev_click = None
    for click, next_click in zip_longest(deduped_clicks, deduped_clicks[1:]):
        if (
            next_click is None or next_click.timestamp - click.timestamp > timedelta(seconds=INHUMAN_SPEED_MS / 1000)
        ) and (
            prev_click is None or click.timestamp - prev_click.timestamp > timedelta(seconds=INHUMAN_SPEED_MS / 1000)
        ):
            organic_clicks.append(click)
        prev_click = click

    return organic_clicks
