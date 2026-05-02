"""
Unit tests for probability_sandbox.py
Run with:  pytest tests/ -v
"""

import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from probability_sandbox import (
    simulate_coin_flips,
    simulate_dice_rolls,
    simulate_card_draws,
    running_mean,
    monte_carlo_pi,
    sample_means,
    statistical_summary,
)


# ─── Coin Flips ───────────────────────────────────────────────────────────────

class TestSimulateCoinFlips:
    def test_returns_correct_length(self):
        assert len(simulate_coin_flips(100)) == 100

    def test_values_are_binary(self):
        flips = simulate_coin_flips(1000)
        assert all(f in (0, 1) for f in flips)

    def test_zero_flips_returns_empty(self):
        assert simulate_coin_flips(0) == []

    def test_lln_convergence_to_half(self):
        random.seed(0)
        flips = simulate_coin_flips(100_000)
        mean = sum(flips) / len(flips)
        assert abs(mean - 0.5) < 0.01, f"Expected ~0.5 but got {mean}"


# ─── Dice Rolls ───────────────────────────────────────────────────────────────

class TestSimulateDiceRolls:
    def test_returns_correct_length(self):
        assert len(simulate_dice_rolls(50, 6)) == 50

    def test_values_within_valid_range(self):
        rolls = simulate_dice_rolls(5000, 6)
        assert all(1 <= r <= 6 for r in rolls)

    def test_single_sided_die_always_returns_one(self):
        rolls = simulate_dice_rolls(20, 1)
        assert all(r == 1 for r in rolls)

    def test_zero_rolls_returns_empty(self):
        assert simulate_dice_rolls(0, 6) == []

    def test_lln_convergence_to_expected_mean(self):
        random.seed(0)
        rolls = simulate_dice_rolls(100_000, 6)
        mean = sum(rolls) / len(rolls)
        assert abs(mean - 3.5) < 0.05, f"Expected ~3.5 but got {mean}"

    def test_twenty_sided_die_range(self):
        rolls = simulate_dice_rolls(2000, 20)
        assert all(1 <= r <= 20 for r in rolls)

    def test_invalid_sides_raises(self):
        try:
            simulate_dice_rolls(10, 0)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


# ─── Card Draws ───────────────────────────────────────────────────────────────

class TestSimulateCardDraws:
    SUITS = {"♠", "♥", "♦", "♣"}
    RANKS = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

    def test_returns_correct_length(self):
        assert len(simulate_card_draws(52)) == 52

    def test_zero_draws_returns_empty(self):
        assert simulate_card_draws(0) == []

    def test_all_cards_are_valid(self):
        cards = simulate_card_draws(500)
        for rank, suit in cards:
            assert suit in self.SUITS, f"Invalid suit: {suit}"
            assert rank in self.RANKS, f"Invalid rank: {rank}"

    def test_all_suits_appear_in_large_sample(self):
        random.seed(0)
        cards = simulate_card_draws(1000)
        suits_seen = {suit for _, suit in cards}
        assert suits_seen == self.SUITS


# ─── Running Mean ─────────────────────────────────────────────────────────────

class TestRunningMean:
    def test_empty_list_returns_empty(self):
        assert running_mean([]) == []

    def test_single_value(self):
        assert running_mean([7]) == [7.0]

    def test_known_values(self):
        result = running_mean([2, 4, 6])
        assert abs(result[0] - 2.0) < 1e-9
        assert abs(result[1] - 3.0) < 1e-9
        assert abs(result[2] - 4.0) < 1e-9

    def test_converges_toward_true_mean(self):
        random.seed(0)
        flips = simulate_coin_flips(10_000)
        means = running_mean(flips)
        assert abs(means[-1] - 0.5) < 0.02


# ─── Monte Carlo π ────────────────────────────────────────────────────────────

class TestMonteCarloPi:
    def test_estimate_close_to_pi(self):
        random.seed(42)
        est, _ = monte_carlo_pi(100_000)
        assert abs(est - math.pi) < 0.05, f"Expected ~π but got {est}"

    def test_running_estimates_length_matches_n(self):
        _, estimates = monte_carlo_pi(500)
        assert len(estimates) == 500

    def test_single_point_is_zero_or_four(self):
        _, estimates = monte_carlo_pi(1)
        assert estimates[0] in (0.0, 4.0)

    def test_zero_points_returns_zero_and_empty(self):
        est, estimates = monte_carlo_pi(0)
        assert est == 0.0
        assert estimates == []

    def test_all_estimates_are_positive(self):
        random.seed(1)
        _, estimates = monte_carlo_pi(1000)
        assert all(e >= 0 for e in estimates)


# ─── Statistical Summary ──────────────────────────────────────────────────────

class TestStatisticalSummary:
    def test_mean_is_correct(self):
        result = statistical_summary([1.0, 2.0, 3.0, 4.0, 5.0])
        assert abs(result["mean"] - 3.0) < 1e-9

    def test_std_is_zero_for_constant_list(self):
        result = statistical_summary([5.0, 5.0, 5.0, 5.0])
        assert result["std"] == 0.0

    def test_ci_lower_less_than_upper(self):
        random.seed(0)
        values = [random.random() for _ in range(1000)]
        result = statistical_summary(values)
        lo, hi = result["95%_CI"]
        assert lo < hi

    def test_empty_list_returns_none_values(self):
        result = statistical_summary([])
        assert result["n"] == 0
        assert result["mean"] is None
        assert result["std"] is None

    def test_label_stored_correctly(self):
        result = statistical_summary([1.0, 2.0], label="test label")
        assert result["label"] == "test label"

    def test_n_matches_input_length(self):
        data = [float(i) for i in range(50)]
        result = statistical_summary(data)
        assert result["n"] == 50


# ─── Sample Means (CLT) ───────────────────────────────────────────────────────

class TestSampleMeans:
    def test_returns_correct_number_of_samples(self):
        random.seed(0)
        means = sample_means(lambda n: simulate_coin_flips(n), 30, 200)
        assert len(means) == 200

    def test_sample_means_converge_to_population_mean(self):
        random.seed(0)
        means = sample_means(lambda n: simulate_dice_rolls(n, 6), 100, 500)
        grand_mean = sum(means) / len(means)
        assert abs(grand_mean - 3.5) < 0.1, f"Expected ~3.5 but got {grand_mean}"
