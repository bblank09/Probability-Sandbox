#!/usr/bin/env python3
"""
Probability Sandbox
===================
Simulate coin flips, dice rolls, card draws, Law of Large Numbers (LLN),
Central Limit Theorem (CLT), and Monte Carlo estimation of pi.

Usage:
    python probability_sandbox.py [--trials N] [--sides K] [--output FILE]
    python probability_sandbox.py --help
"""

import argparse
import math
import random
from collections import Counter

import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt


# ─── Simulation Layer ─────────────────────────────────────────────────────────

def simulate_coin_flips(n: int) -> list:
    """Simulate n coin flips. Returns list of 0 (tails) or 1 (heads)."""
    return [random.randint(0, 1) for _ in range(n)]


def simulate_dice_rolls(n: int, sides: int = 6) -> list:
    """Simulate n rolls of a k-sided die. Returns list of outcomes in [1, sides]."""
    if sides < 1:
        raise ValueError("sides must be >= 1")
    return [random.randint(1, sides) for _ in range(n)]


def simulate_card_draws(n: int) -> list:
    """Draw n cards with replacement from a standard 52-card deck."""
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return [random.choice(deck) for _ in range(n)]


def monte_carlo_pi(n: int) -> tuple:
    """
    Estimate pi by sampling random points in a unit square.
    Points inside the unit circle → inside / total × 4 ≈ pi.
    Returns (final_estimate, list_of_running_estimates).
    """
    inside = 0
    estimates = []
    for i in range(1, n + 1):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        if x * x + y * y <= 1.0:
            inside += 1
        estimates.append(4.0 * inside / i)
    return (estimates[-1] if estimates else 0.0), estimates


# ─── Statistics Layer ─────────────────────────────────────────────────────────

def running_mean(values: list) -> list:
    """Return cumulative running mean for each position in values."""
    means = []
    total = 0.0
    for i, v in enumerate(values, 1):
        total += v
        means.append(total / i)
    return means


def sample_means(population_fn, sample_size: int, num_samples: int) -> list:
    """
    Generate num_samples sample means, each computed from sample_size draws
    produced by population_fn(sample_size).  Used for CLT demonstration.
    """
    return [
        sum(population_fn(sample_size)) / sample_size
        for _ in range(num_samples)
    ]


def statistical_summary(values: list, label: str = "") -> dict:
    """Compute mean, population std, and 95% confidence interval."""
    n = len(values)
    if n == 0:
        return {"label": label, "n": 0, "mean": None, "std": None, "95%_CI": (None, None)}
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)
    se = std / math.sqrt(n) if n > 1 else 0.0
    return {
        "label": label,
        "n": n,
        "mean": mean,
        "std": std,
        "95%_CI": (mean - 1.96 * se, mean + 1.96 * se),
    }


def print_summary(summary: dict) -> None:
    """Pretty-print a statistical summary dict."""
    print(f"\n{'─' * 46}")
    if summary["label"]:
        print(f"  {summary['label']}")
        print(f"  {'─' * 42}")
    if summary["n"] == 0:
        print("  (no data)")
    else:
        ci_lo, ci_hi = summary["95%_CI"]
        print(f"  n       : {summary['n']:>12,}")
        print(f"  mean    : {summary['mean']:>14.6f}")
        print(f"  std     : {summary['std']:>14.6f}")
        print(f"  95% CI  : ({ci_lo:.6f},  {ci_hi:.6f})")
    print(f"{'─' * 46}")


# ─── Visualization Layer ──────────────────────────────────────────────────────

def build_dashboard(
    coin_flips: list,
    dice_rolls: list,
    dice_sides: int,
    pi_estimates: list,
    clt_means: list,
    save_path: str = "convergence_chart.png",
) -> None:
    """Render and save a 2×3 dashboard of probability simulation results."""

    fig = plt.figure(figsize=(18, 10))
    fig.suptitle(
        "Probability Sandbox — Simulation Dashboard",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.35)

    n_coins = len(coin_flips)
    n_dice = len(dice_rolls)
    coin_x = range(1, n_coins + 1)
    dice_x = range(1, n_dice + 1)

    # ── Panel 1: LLN Coin Flip ────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(coin_x, running_mean(coin_flips), color="#4C72B0", lw=1.0, alpha=0.9)
    ax1.axhline(0.5, color="#C44E52", lw=1.2, linestyle="--", label="True mean = 0.5")
    ax1.set_title("LLN: Coin Flip Convergence", fontsize=11, pad=6)
    ax1.set_xlabel("Number of Flips")
    ax1.set_ylabel("Running Mean P(Heads)")
    ax1.set_ylim(0.3, 0.7)
    ax1.legend(fontsize=8)

    # ── Panel 2: LLN Dice ─────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    true_dice_mean = (dice_sides + 1) / 2.0
    ax2.plot(dice_x, running_mean(dice_rolls), color="#55A868", lw=1.0, alpha=0.9)
    ax2.axhline(
        true_dice_mean,
        color="#C44E52",
        lw=1.2,
        linestyle="--",
        label=f"True mean = {true_dice_mean}",
    )
    ax2.set_title(f"LLN: {dice_sides}-Sided Dice Convergence", fontsize=11, pad=6)
    ax2.set_xlabel("Number of Rolls")
    ax2.set_ylabel("Running Mean")
    ax2.legend(fontsize=8)

    # ── Panel 3: Monte Carlo π convergence ───────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(
        range(1, len(pi_estimates) + 1),
        pi_estimates,
        color="#8172B2",
        lw=0.8,
        alpha=0.85,
    )
    ax3.axhline(
        math.pi,
        color="#C44E52",
        lw=1.2,
        linestyle="--",
        label=f"π = {math.pi:.5f}",
    )
    ax3.set_title("Monte Carlo: Estimating π", fontsize=11, pad=6)
    ax3.set_xlabel("Number of Points")
    ax3.set_ylabel("Estimate of π")
    ax3.legend(fontsize=8)

    # ── Panel 4: Dice frequency distribution ──────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 0])
    counts = Counter(dice_rolls)
    faces = sorted(counts)
    freqs = [counts[f] / n_dice for f in faces]
    expected = 1.0 / dice_sides
    ax4.bar(faces, freqs, color="#4C72B0", alpha=0.75, edgecolor="white", width=0.6)
    ax4.axhline(
        expected,
        color="#C44E52",
        lw=1.2,
        linestyle="--",
        label=f"Expected = {expected:.3f}",
    )
    ax4.set_title("Dice Frequency Distribution", fontsize=11, pad=6)
    ax4.set_xlabel("Face Value")
    ax4.set_ylabel("Relative Frequency")
    ax4.set_xticks(faces)
    ax4.legend(fontsize=8)

    # ── Panel 5: CLT sample mean distribution ────────────────────────────────
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.hist(
        clt_means,
        bins=40,
        color="#55A868",
        edgecolor="white",
        density=True,
        alpha=0.80,
    )
    clt_mean = sum(clt_means) / len(clt_means) if clt_means else 0
    ax5.axvline(
        clt_mean,
        color="#C44E52",
        lw=1.5,
        linestyle="--",
        label=f"Sample mean = {clt_mean:.2f}",
    )
    ax5.set_title("CLT: Distribution of Sample Means", fontsize=11, pad=6)
    ax5.set_xlabel("Sample Mean")
    ax5.set_ylabel("Density")
    ax5.legend(fontsize=8)

    # ── Panel 6: Monte Carlo π scatter ───────────────────────────────────────
    ax6 = fig.add_subplot(gs[1, 2])
    n_scatter = 3000
    xs = [random.uniform(-1.0, 1.0) for _ in range(n_scatter)]
    ys = [random.uniform(-1.0, 1.0) for _ in range(n_scatter)]
    inside_color = "#4C72B0"
    outside_color = "#C44E52"
    colors = [inside_color if x ** 2 + y ** 2 <= 1.0 else outside_color for x, y in zip(xs, ys)]
    ax6.scatter(xs, ys, c=colors, s=2, alpha=0.5)
    theta = [i * 2 * math.pi / 360 for i in range(361)]
    ax6.plot([math.cos(t) for t in theta], [math.sin(t) for t in theta], "k-", lw=1.0)
    ax6.set_aspect("equal")
    ax6.set_title("Monte Carlo: π Scatter (n=3,000)", fontsize=11, pad=6)
    ax6.set_xlabel("x")
    ax6.set_ylabel("y")

    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"\n  [Chart saved → {save_path}]")
    plt.show()


# ─── CLI ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog="probability_sandbox",
        description="Probability Sandbox — simulate core probability phenomena",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--trials", type=int, default=10_000,
        help="Number of trials for coin/dice/Monte Carlo (default: 10000)",
    )
    parser.add_argument(
        "--sides", type=int, default=6,
        help="Number of sides on the die (default: 6)",
    )
    parser.add_argument(
        "--card-draws", type=int, default=100,
        help="Number of card draws (default: 100)",
    )
    parser.add_argument(
        "--clt-samples", type=int, default=2000,
        help="Number of samples for CLT demonstration (default: 2000)",
    )
    parser.add_argument(
        "--clt-size", type=int, default=30,
        help="Sample size per CLT iteration (default: 30)",
    )
    parser.add_argument(
        "--output", type=str, default="convergence_chart.png",
        help="Filename for the output chart (default: convergence_chart.png)",
    )
    parser.add_argument(
        "--no-plot", action="store_true",
        help="Save chart without opening a display window",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    random.seed(args.seed)

    if args.no_plot:
        matplotlib.use("Agg")

    print("=" * 50)
    print("   Probability Sandbox  v1.0")
    print("=" * 50)
    print(f"  seed    : {args.seed}")
    print(f"  trials  : {args.trials:,}")
    print(f"  sides   : {args.sides}")

    # ── 1. Coin Flips ─────────────────────────────────────────────────────────
    print(f"\n[1/5] Coin Flip Simulation  (n={args.trials:,})")
    coins = simulate_coin_flips(args.trials)
    print_summary(statistical_summary([float(c) for c in coins], "Coin Flip  (1=Heads, 0=Tails)"))

    # ── 2. Dice Rolls ─────────────────────────────────────────────────────────
    print(f"\n[2/5] Dice Roll Simulation  (n={args.trials:,}, sides={args.sides})")
    dice = simulate_dice_rolls(args.trials, args.sides)
    print_summary(statistical_summary([float(d) for d in dice], f"{args.sides}-Sided Dice"))

    # ── 3. Card Draws ─────────────────────────────────────────────────────────
    print(f"\n[3/5] Card Draw Simulation  (n={args.card_draws})")
    cards = simulate_card_draws(args.card_draws)
    suit_counts = Counter(c[1] for c in cards)
    rank_counts = Counter(c[0] for c in cards)
    print(f"\n  Suit distribution : {dict(sorted(suit_counts.items()))}")
    print(f"  Top-3 ranks drawn : {rank_counts.most_common(3)}")

    # ── 4. Monte Carlo π ──────────────────────────────────────────────────────
    print(f"\n[4/5] Monte Carlo  π  Estimation  (n={args.trials:,})")
    pi_est, pi_history = monte_carlo_pi(args.trials)
    error = abs(pi_est - math.pi)
    print(f"\n  Estimated π = {pi_est:.6f}")
    print(f"  True      π = {math.pi:.6f}")
    print(f"  Error       = {error:.6f}  ({error / math.pi * 100:.4f}%)")

    # ── 5. CLT ────────────────────────────────────────────────────────────────
    print(
        f"\n[5/5] Central Limit Theorem  "
        f"({args.clt_samples:,} samples, size={args.clt_size})"
    )
    clt_means = sample_means(
        lambda n: simulate_dice_rolls(n, args.sides),
        args.clt_size,
        args.clt_samples,
    )
    print_summary(
        statistical_summary(
            clt_means,
            f"CLT Sample Means  (dice, sample_size={args.clt_size})",
        )
    )

    # ── Chart ─────────────────────────────────────────────────────────────────
    print(f"\nBuilding 6-panel dashboard  →  {args.output}")
    build_dashboard(
        coin_flips=coins,
        dice_rolls=dice,
        dice_sides=args.sides,
        pi_estimates=pi_history,
        clt_means=clt_means,
        save_path=args.output,
    )

    print("\nDone.\n")


if __name__ == "__main__":
    main()
