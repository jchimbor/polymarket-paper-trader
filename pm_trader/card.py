"""Shareable stats cards for social platforms.

Generates formatted trading performance cards optimized for:
- X/Twitter (280 chars, hashtags, engagement bait)
- Chat apps (Telegram, Discord, WhatsApp — markdown)
- Plain text (fallback)
"""

from __future__ import annotations


def _roi_icon(roi: float) -> str:
    """Pick emoji based on ROI performance."""
    if roi > 20:
        return "🔥"
    if roi > 10:
        return "🚀"
    if roi > 0:
        return "📈"
    if roi == 0:
        return "➖"
    if roi > -10:
        return "📉"
    return "💀"


def _extract(stats: dict) -> dict:
    """Extract and format common fields from stats dict."""
    roi = stats.get("roi_pct", 0.0)
    pnl = stats.get("pnl", 0.0)
    return {
        "roi": roi,
        "pnl": pnl,
        "total": stats.get("total_value", 0.0),
        "sharpe": stats.get("sharpe_ratio", 0.0),
        "win": stats.get("win_rate", 0.0),
        "trades": stats.get("total_trades", 0),
        "dd": stats.get("max_drawdown", 0.0),
        "fees": stats.get("total_fees", 0.0),
        "starting": stats.get("starting_balance", 0.0),
        "icon": _roi_icon(roi),
        "pnl_sign": "+" if pnl >= 0 else "",
        "roi_sign": "+" if roi >= 0 else "",
    }


def generate_tweet(stats: dict, account: str = "default") -> str:
    """Generate a tweet-optimized card (< 280 chars).

    Designed for X/Twitter sharing. Compact, eye-catching, with hashtags.
    """
    s = _extract(stats)

    lines = [
        f"{s['icon']} My AI agent's Polymarket results:",
        "",
        f"ROI: {s['roi_sign']}{s['roi']:.1f}%",
        f"P&L: {s['pnl_sign']}${s['pnl']:,.0f}",
        f"Sharpe: {s['sharpe']:.2f} | Win: {s['win'] * 100:.0f}% | {s['trades']} trades",
        "",
        "Paper trading with real order books, zero risk",
        "",
        "#Polymarket #AITrading #PredictionMarkets",
        "npx clawhub install polymarket-paper-trader",
    ]

    return "\n".join(lines)


def generate_card(stats: dict, account: str = "default") -> str:
    """Generate a chat-optimized card with markdown.

    For Telegram, Discord, Slack — supports bold/italic.
    """
    s = _extract(stats)

    lines = [
        f"{s['icon']} *Polymarket Paper Trading*",
        "",
        f"ROI: *{s['roi_sign']}{s['roi']:.1f}%* | Sharpe: *{s['sharpe']:.2f}*",
        f"Win Rate: *{s['win'] * 100:.0f}%* | Trades: *{s['trades']}*",
        f"Max DD: *{s['dd'] * 100:.1f}%* | Fees: *${s['fees']:.2f}*",
        "",
        f"P&L: *{s['pnl_sign']}${s['pnl']:,.2f}*",
        f"Portfolio: *${s['total']:,.2f}* (started ${s['starting']:,.0f})",
        "",
        "`npx clawhub install polymarket-paper-trader`",
    ]

    return "\n".join(lines)


def _tier(stats: dict) -> str:
    """Determine leaderboard tier."""
    trades = stats.get("total_trades", 0)
    roi = stats.get("roi_pct", 0.0)
    sharpe = stats.get("sharpe_ratio", 0.0)
    if trades >= 50 and roi > 20 and sharpe > 1.5:
        return "\U0001f48e Diamond"
    if trades >= 30 and roi > 10 and sharpe > 1.0:
        return "\U0001f947 Gold"
    if trades >= 20 and roi > 5:
        return "\U0001f948 Silver"
    if trades >= 10:
        return "\U0001f949 Bronze"
    return "\u2014 Unranked"


def generate_pk_card(
    stats_a: dict, name_a: str,
    stats_b: dict, name_b: str,
) -> str:
    """Generate a head-to-head PK comparison card for X/Twitter."""
    a = _extract(stats_a)
    b = _extract(stats_b)
    tier_a = _tier(stats_a)
    tier_b = _tier(stats_b)

    # Determine winner by ROI
    if a["roi"] > b["roi"]:
        verdict = f"{name_a} wins"
    elif b["roi"] > a["roi"]:
        verdict = f"{name_b} wins"
    else:
        verdict = "Tie"

    lines = [
        "\u2694\ufe0f AI Trader PK \u2014 Head to Head",
        "",
        f"  {name_a:>12} vs {name_b}",
        f"  ROI:   {a['roi_sign']}{a['roi']:.1f}%  vs  {b['roi_sign']}{b['roi']:.1f}%",
        f"  Sharpe: {a['sharpe']:.2f}   vs  {b['sharpe']:.2f}",
        f"  Win:    {a['win'] * 100:.0f}%     vs  {b['win'] * 100:.0f}%",
        f"  Trades: {a['trades']}      vs  {b['trades']}",
        f"  Tier:   {tier_a} vs {tier_b}",
        "",
        f"Winner: {verdict} {a['icon'] if a['roi'] >= b['roi'] else b['icon']}",
        "",
        "#Polymarket #AITrading #PK",
        "npx clawhub install polymarket-paper-trader",
    ]

    return "\n".join(lines)


def generate_card_plain(stats: dict, account: str = "default") -> str:
    """Generate a plain-text card (no markdown)."""
    s = _extract(stats)

    lines = [
        f"{s['icon']} Polymarket Paper Trading",
        "",
        f"  ROI:       {s['roi_sign']}{s['roi']:.1f}%",
        f"  Sharpe:    {s['sharpe']:.2f}",
        f"  Win Rate:  {s['win'] * 100:.0f}%",
        f"  Trades:    {s['trades']}",
        f"  Max DD:    {s['dd'] * 100:.1f}%",
        f"  Fees:      ${s['fees']:.2f}",
        "",
        f"  P&L:       {s['pnl_sign']}${s['pnl']:,.2f}",
        f"  Portfolio: ${s['total']:,.2f}",
        "",
        "npx clawhub install polymarket-paper-trader",
    ]

    return "\n".join(lines)
