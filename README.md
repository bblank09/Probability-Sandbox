# Probability Sandbox

> A Python simulation environment for exploring core probability theorems through empirical experimentation — run thousands of trials, observe convergence in real time, and verify theoretical predictions with a single command.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Motivation and Background](#2-motivation-and-background)
3. [Theoretical Foundations](#3-theoretical-foundations)
   - 3.1 [Law of Large Numbers (LLN)](#31-law-of-large-numbers-lln)
   - 3.2 [Central Limit Theorem (CLT)](#32-central-limit-theorem-clt)
   - 3.3 [Monte Carlo Method](#33-monte-carlo-method)
   - 3.4 [Confidence Intervals](#34-confidence-intervals)
4. [System Architecture](#4-system-architecture)
5. [Function Reference](#5-function-reference)
   - 5.1 [Simulation Layer](#51-simulation-layer)
   - 5.2 [Statistics Layer](#52-statistics-layer)
   - 5.3 [Visualization Layer](#53-visualization-layer)
   - 5.4 [CLI Layer](#54-cli-layer)
6. [File Structure](#6-file-structure)
7. [Dependencies](#7-dependencies)
8. [Installation](#8-installation)
9. [Usage](#9-usage)
10. [Sample Output](#10-sample-output)
11. [Dashboard Panels — Detailed Explanation](#11-dashboard-panels--detailed-explanation)
12. [Testing](#12-testing)
13. [Known Limitations and Caveats](#13-known-limitations-and-caveats)
14. [Roadmap](#14-roadmap)
15. [References](#15-references)

---

## 1. Project Overview

**Probability Sandbox** is a self-contained Python program that simulates five foundational probability experiments:

| Experiment | What is simulated | Theoretical concept verified |
|------------|-------------------|------------------------------|
| Coin flip | Bernoulli trials (p = 0.5) | Law of Large Numbers |
| Dice roll | Discrete uniform distribution | LLN + frequency distribution |
| Card draw | Sampling with replacement from a 52-card deck | Uniform categorical sampling |
| Monte Carlo π | Geometric probability via random point sampling | Monte Carlo integration |
| CLT demonstration | Repeated sampling from a discrete uniform population | Central Limit Theorem |

All results are printed as statistical summaries (mean, standard deviation, 95% confidence interval) and rendered as a **six-panel matplotlib dashboard** saved to a PNG file.

The program is fully configurable through a command-line interface and reproducible via a fixed random seed.

---

## 2. Motivation and Background

Probability theory forms the mathematical backbone of statistics, machine learning, data science, and countless fields of applied science. Concepts such as the Law of Large Numbers and the Central Limit Theorem are introduced in nearly every introductory course — yet they are commonly taught through static formulas and pre-drawn diagrams, which makes it difficult to develop genuine intuition for *why* they hold.

This project addresses that gap by making the experiments **interactive and empirical**. Instead of reading that "the sample mean converges to the population mean as n → ∞", a user can observe this convergence unfold across 10,000 live trials in a single chart.

The specific motivations behind each experiment are:

- **Coin flip / Dice roll** — The simplest random processes, ideal for demonstrating LLN convergence starting from high variance and settling toward the true mean.
- **Card draw** — Introduces categorical (non-numeric) sampling and suit/rank frequency analysis.
- **Monte Carlo π** — Demonstrates that randomness can be harnessed to estimate deterministic mathematical constants, a technique used in physics simulations, financial risk modeling, and numerical integration.
- **CLT demonstration** — Shows that even a flat, non-normal distribution (discrete uniform) produces normally distributed sample means — the result that justifies the use of z-tests and t-tests across virtually all of applied statistics.

---

## 3. Theoretical Foundations

### 3.1 Law of Large Numbers (LLN)

**Origin:** First formulated by Jacob Bernoulli in *Ars Conjectandi* (1713). The strong form was proven by Émile Borel (1909) and Andrei Kolmogorov.

**Statement:** Let $X_1, X_2, \ldots, X_n$ be independent, identically distributed random variables with finite expected value $\mu = \mathbb{E}[X]$. Then the sample mean $\bar{X}_n$ converges to $\mu$ as $n \to \infty$:

$$\bar{X}_n = \frac{1}{n} \sum_{i=1}^{n} X_i \xrightarrow{P} \mu \quad \text{as } n \to \infty$$

**Why it matters:** LLN is the formal justification for using sample averages to estimate population parameters. Without it, there would be no statistical guarantee that collecting more data brings us closer to the truth. It underpins polling, clinical trials, A/B testing, and virtually all empirical science.

**How this project demonstrates it:**

The `running_mean()` function computes the cumulative average after each new observation. Plotting this sequence against the theoretical mean (a horizontal dashed line) produces a convergence chart — the running average begins erratically and steadily stabilizes toward the true value as $n$ grows. This is done for both coin flips (true mean = 0.5) and dice rolls (true mean = (sides + 1) / 2).

---

### 3.2 Central Limit Theorem (CLT)

**Origin:** First informally stated by Abraham de Moivre (1733) for the binomial case. Pierre-Simon Laplace generalized it (1812). The modern proof was given by Aleksandr Lyapunov (1901).

**Statement:** Let $X_1, X_2, \ldots, X_n$ be i.i.d. random variables with mean $\mu$ and finite variance $\sigma^2$. Then the standardized sample mean converges in distribution to the standard normal:

$$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1) \quad \text{as } n \to \infty$$

Equivalently, $\bar{X}_n \sim \mathcal{N}\!\left(\mu,\ \dfrac{\sigma^2}{n}\right)$ approximately, for sufficiently large $n$.

**Why it matters:** The CLT is arguably the most important theorem in all of statistics. It explains why the normal distribution appears so frequently in practice, and it provides the theoretical foundation for:
- Z-tests and t-tests
- Confidence intervals
- Regression analysis
- Virtually all parametric statistical inference

**How this project demonstrates it:**

The `sample_means()` function repeatedly draws samples of size $n$ from a discrete uniform population (dice rolls), computes each sample's mean, and collects all means into a list. The `build_dashboard()` function plots these means as a histogram. Regardless of the flat shape of the original distribution, the resulting histogram converges to a bell curve — visually confirming the CLT.

The default parameters (2,000 samples of size 30) are chosen deliberately: sample size 30 is the conventional minimum for the CLT approximation to hold well for non-normal populations.

---

### 3.3 Monte Carlo Method

**Origin:** Developed by Stanislaw Ulam and John von Neumann at Los Alamos National Laboratory during the Manhattan Project (1940s). Named by Nicholas Metropolis after the Monte Carlo Casino in Monaco.

**Core idea:** Use random sampling to estimate quantities that are difficult or impossible to compute analytically. The accuracy of the estimate improves as the number of samples increases, typically scaling as $O(1/\sqrt{n})$.

**Application — Estimating π:**

A unit circle (radius = 1) inscribed in a square of side 2 has:

$$\frac{\text{Area of circle}}{\text{Area of square}} = \frac{\pi r^2}{(2r)^2} = \frac{\pi}{4}$$

Therefore, if we sample random points $(x, y)$ uniformly in $[-1, 1] \times [-1, 1]$, the fraction that satisfies $x^2 + y^2 \leq 1$ estimates $\pi / 4$:

$$\hat{\pi} = 4 \times \frac{\text{points inside the unit circle}}{\text{total points sampled}}$$

**Convergence rate:** The standard error of the Monte Carlo estimator is $O(1/\sqrt{n})$. This means:
- Doubling accuracy requires 4× more samples
- Increasing trials from 10,000 to 1,000,000 reduces error by ~10×

**Why it matters:** Monte Carlo methods are essential in:
- Numerical integration in high-dimensional spaces (where grid methods fail)
- Financial risk modeling (option pricing via stochastic simulation)
- Physics simulations (particle transport, thermodynamics)
- Bayesian posterior sampling (MCMC)

---

### 3.4 Confidence Intervals

**Origin:** Introduced by Jerzy Neyman (1937) as a frequentist alternative to Bayesian credible intervals.

**Definition:** A 95% confidence interval for the population mean $\mu$ is constructed as:

$$\bar{X} \pm z_{0.025} \cdot \frac{\sigma}{\sqrt{n}} = \bar{X} \pm 1.96 \cdot \frac{\sigma}{\sqrt{n}}$$

where $z_{0.025} = 1.96$ is the 97.5th percentile of the standard normal distribution.

**Correct interpretation:** If we were to repeat the experiment many times and construct a confidence interval each time, approximately 95% of those intervals would contain the true parameter $\mu$. A single interval either contains $\mu$ or it does not — it is the procedure, not the interval, that has the 95% coverage probability.

**Why this project includes it:** Every simulation outputs a 95% CI. This allows the user to verify that the true theoretical mean (0.5 for a fair coin, 3.5 for a 6-sided die) falls within the interval — providing a quantitative check on the simulation's correctness.

---

## 4. System Architecture

The program is organized into four cleanly separated layers, each with a single responsibility:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Layer (parse_args, main)             │
│   Parses user arguments, seeds the RNG, orchestrates all steps  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Simulation Layer                              │
│   simulate_coin_flips  simulate_dice_rolls  simulate_card_draws │
│   monte_carlo_pi                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Statistics Layer                              │
│   running_mean  sample_means  statistical_summary  print_summary│
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   Visualization Layer                            │
│   build_dashboard  (6-panel matplotlib figure)                  │
└─────────────────────────────────────────────────────────────────┘
```

Data flows strictly downward: simulation functions produce raw lists of outcomes, statistics functions transform those lists into summaries and running sequences, and the visualization layer renders everything into a single figure. No layer calls upward.

---

## 5. Function Reference

### 5.1 Simulation Layer

---

#### `simulate_coin_flips(n: int) → list[int]`

**Origin:** Models a Bernoulli trial with $p = 0.5$ — the simplest non-trivial random experiment, analyzed formally since the 17th century.

**Purpose:** Generate a sequence of $n$ fair coin flips as a binary list (0 = tails, 1 = heads).

**Importance:** Coin flips serve as the canonical example of the LLN. Because the true mean is exactly 0.5 by symmetry, any deviation in the running mean is immediately visible as drift from the center line on the convergence chart.

**How it works:**

```python
def simulate_coin_flips(n: int) -> list:
    return [random.randint(0, 1) for _ in range(n)]
```

`random.randint(0, 1)` draws from $\{0, 1\}$ with equal probability $\frac{1}{2}$ each, simulating a fair coin. The result is a Python list of integers suitable for further statistical processing.

**Expected behavior:**
- Single flip: result is 0 or 1 with ~50% probability each
- Running mean at n=100: typically 0.40–0.60
- Running mean at n=10,000: typically 0.495–0.505
- Running mean at n=100,000: typically 0.499–0.501

---

#### `simulate_dice_rolls(n: int, sides: int = 6) → list[int]`

**Origin:** Models a discrete uniform distribution $U\{1, k\}$ over $k$ faces. Dice have been used as probability models since antiquity; their formal analysis began with Cardano's *Liber de Ludo Aleae* (c. 1560).

**Purpose:** Generate $n$ independent rolls of a fair $k$-sided die.

**Importance:** The discrete uniform distribution has an analytically exact mean $\mu = (k+1)/2$ and variance $\sigma^2 = (k^2-1)/12$, making it ideal for verifying both LLN convergence and CLT behavior. It is also non-normal, which makes the CLT demonstration more striking — the original distribution is flat, yet sample means form a bell curve.

**How it works:**

```python
def simulate_dice_rolls(n: int, sides: int = 6) -> list:
    if sides < 1:
        raise ValueError("sides must be >= 1")
    return [random.randint(1, sides) for _ in range(n)]
```

`random.randint(1, sides)` draws uniformly from $\{1, 2, \ldots, k\}$. The guard clause rejects physically meaningless dice (0 or negative faces) by raising a `ValueError`, which is also tested in the unit test suite.

**Expected behavior (6-sided die):**
- True mean: $\mu = 3.5$
- True std: $\sigma = \sqrt{35/12} \approx 1.708$
- Each face appears with relative frequency $\approx 1/6 \approx 0.1\overline{6}$

---

#### `simulate_card_draws(n: int) → list[tuple[str, str]]`

**Origin:** Playing card probability problems appear in the earliest probability texts, including Cardano and Pascal. A standard 52-card deck is a classical example of a finite sample space.

**Purpose:** Draw $n$ cards **with replacement** from a standard 52-card deck, returning each card as a `(rank, suit)` tuple.

**Importance:** This function extends simulation beyond numeric outcomes to categorical data, introducing the analysis of frequency distributions over non-numeric events. It demonstrates that each suit should appear with probability $\frac{1}{4}$ and each rank with probability $\frac{1}{13}$.

**How it works:**

```python
def simulate_card_draws(n: int) -> list:
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", ..., "K"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return [random.choice(deck) for _ in range(n)]
```

The full 52-card deck is constructed as a list of `(rank, suit)` pairs. `random.choice(deck)` selects uniformly at random **with replacement**, meaning each draw is independent and the deck never depletes. This models scenarios like shuffling between draws.

**Note:** With-replacement sampling is intentional — it keeps each draw independent and identically distributed, satisfying the i.i.d. assumption required by LLN and CLT. Without-replacement sampling would produce a hypergeometric distribution and is reserved for a future version.

---

#### `monte_carlo_pi(n: int) → tuple[float, list[float]]`

**Origin:** The geometric approach to estimating π via random sampling was described by Georges-Louis Leclerc, Comte de Buffon in his *Needle Problem* (1777). The computational Monte Carlo method as used here was formalized at Los Alamos in the 1940s.

**Purpose:** Estimate the value of π by sampling random points in the unit square and counting how many fall inside the unit circle. Returns both the final estimate and the full history of running estimates.

**Importance:** This function demonstrates the most celebrated application of Monte Carlo integration. It shows that:
1. Randomness can be used to solve deterministic mathematical problems
2. The estimate converges at rate $O(1/\sqrt{n})$ — much slower than deterministic numerical methods, but dimension-independent
3. Visual confirmation (the scatter plot) makes the geometric intuition immediately clear

**How it works:**

```python
def monte_carlo_pi(n: int) -> tuple:
    inside = 0
    estimates = []
    for i in range(1, n + 1):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        if x * x + y * y <= 1.0:
            inside += 1
        estimates.append(4.0 * inside / i)
    return (estimates[-1] if estimates else 0.0), estimates
```

At each iteration, a point $(x, y)$ is sampled uniformly in $[-1,1]^2$. The condition $x^2 + y^2 \leq 1$ tests membership in the inscribed unit circle. The ratio of inside points to total points estimates $\pi/4$; multiplying by 4 gives the π estimate. The running estimate list enables the convergence plot in Panel 3 of the dashboard.

**Mathematical basis:**

$$P\!\left(x^2 + y^2 \leq 1\right) = \frac{\pi r^2}{(2r)^2} = \frac{\pi}{4} \implies \hat{\pi} = 4 \cdot \frac{\text{inside}}{n}$$

---

### 5.2 Statistics Layer

---

#### `running_mean(values: list) → list[float]`

**Origin:** The cumulative (running) average is a classical online statistic, computed incrementally without storing all past values — a technique used since the earliest numerical methods.

**Purpose:** Compute the cumulative mean at each position in a sequence, producing a list of the same length showing how the average evolves over time.

**Importance:** This is the primary tool for visualizing LLN convergence. By plotting the running mean against trial number, the user can directly observe the sample mean "settling down" as more data arrives. The running mean is also used in streaming data pipelines where computing the global mean repeatedly would be inefficient.

**How it works:**

```python
def running_mean(values: list) -> list:
    means = []
    total = 0.0
    for i, v in enumerate(values, 1):
        total += v
        means.append(total / i)
    return means
```

The function maintains a running total and divides by the current count at each step. This is the numerically stable incremental form — it avoids recomputing the sum from scratch at each step and handles empty lists gracefully by returning an empty list.

---

#### `sample_means(population_fn, sample_size: int, num_samples: int) → list[float]`

**Origin:** Repeated sampling from a population to study the distribution of sample statistics is the core operation of sampling theory, formalized by Ronald A. Fisher in the 1920s.

**Purpose:** Generate `num_samples` independent sample means, where each mean is computed from `sample_size` observations drawn by `population_fn`. This produces the empirical sampling distribution of $\bar{X}$.

**Importance:** This function is the engine of the CLT demonstration. By calling it with a discrete uniform population function (dice rolls) and plotting the results, the user observes a normal distribution emerge from a non-normal source — the defining characteristic of the CLT.

**How it works:**

```python
def sample_means(population_fn, sample_size: int, num_samples: int) -> list:
    return [
        sum(population_fn(sample_size)) / sample_size
        for _ in range(num_samples)
    ]
```

`population_fn` is passed as a callable (a lambda in `main()`), keeping this function general — it works for any population, not just dice. This follows the **strategy pattern**: the sampling mechanism is injected, not hardcoded.

**Effect of parameters:**
- Larger `sample_size` → narrower bell curve (smaller standard error $\sigma/\sqrt{n}$)
- Larger `num_samples` → smoother histogram (more data points to fill bins)

---

#### `statistical_summary(values: list, label: str = "") → dict`

**Origin:** Descriptive statistics (mean, variance, confidence intervals) were systematized by Karl Pearson and Ronald Fisher in the early 20th century. The 95% CI formula using $z = 1.96$ follows directly from the normal distribution's quantile function.

**Purpose:** Compute and return a dictionary of descriptive statistics for any numeric list: count, mean, population standard deviation, and 95% confidence interval.

**Importance:** Every simulation in this project outputs a statistical summary, making it possible to:
1. Verify that simulated means are close to theoretical values
2. Quantify uncertainty around the estimate
3. Check that true theoretical values fall within the confidence interval

**How it works:**

```python
def statistical_summary(values: list, label: str = "") -> dict:
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
```

The function computes the **population** standard deviation (divides by $n$, not $n-1$) because we are describing the observed sample, not estimating a population parameter. The confidence interval uses $z = 1.96$ from the standard normal, justified by the CLT — valid for large $n$ (which all default settings exceed).

The empty-list guard prevents `ZeroDivisionError` and returns `None` values, which the test suite explicitly verifies.

---

#### `print_summary(summary: dict) → None`

**Purpose:** Format and print a statistical summary dictionary to stdout with aligned columns and separator lines.

**How it works:** Reads the dict produced by `statistical_summary()` and prints each field with consistent formatting. Handles the `n=0` edge case by printing "(no data)". Used after every simulation step in `main()` to give the user immediate feedback before the chart is generated.

---

### 5.3 Visualization Layer

---

#### `build_dashboard(coin_flips, dice_rolls, dice_sides, pi_estimates, clt_means, save_path) → None`

**Origin:** Multi-panel statistical dashboards became standard in data science with the rise of matplotlib (2003) and seaborn. The specific combination of convergence charts, frequency distributions, and scatter plots follows the tradition of exploratory data analysis (EDA) visualization.

**Purpose:** Render all simulation results as a single 2×3 grid of subplots and save to a PNG file. Optionally display an interactive window.

**Importance:** The dashboard is the main deliverable of the project. It allows the user to see all five experiments simultaneously, making it easy to compare convergence rates and connect visual patterns to the underlying theory.

**How it works:**

A `GridSpec(2, 3)` layout is created inside a single `Figure`. Each subplot (`ax`) is populated independently:

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│ Panel 1              │ Panel 2              │ Panel 3              │
│ LLN: Coin Flip       │ LLN: Dice            │ Monte Carlo π        │
│ running_mean(coins)  │ running_mean(dice)   │ pi_estimates list    │
│ vs 0.5 (dashed red)  │ vs (k+1)/2           │ vs math.pi           │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Panel 4              │ Panel 5              │ Panel 6              │
│ Dice Frequency       │ CLT: Sample Means    │ Monte Carlo Scatter  │
│ Bar chart of         │ Histogram of         │ 3,000 random points  │
│ relative frequencies │ clt_means (density)  │ colored by in/out    │
└──────────────────────┴──────────────────────┴──────────────────────┘
```

The scatter plot in Panel 6 samples a fresh set of 3,000 points for visual clarity (independent of the `--trials` argument), ensuring the visualization remains readable at any trial count.

`plt.savefig()` is called before `plt.show()` to guarantee the file is written even if the display window is closed immediately.

---

### 5.4 CLI Layer

---

#### `parse_args() → argparse.Namespace`

**Purpose:** Define and parse all command-line arguments using Python's standard `argparse` module. Returns a `Namespace` object that `main()` reads to configure every simulation parameter.

**All arguments:**

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--trials` | int | 10,000 | Trials for coin/dice/Monte Carlo |
| `--sides` | int | 6 | Faces on the die |
| `--card-draws` | int | 100 | Card draws to simulate |
| `--clt-samples` | int | 2,000 | Number of CLT sample means |
| `--clt-size` | int | 30 | Sample size per CLT iteration |
| `--output` | str | `convergence_chart.png` | Output filename |
| `--seed` | int | 42 | Random seed |
| `--no-plot` | flag | False | Suppress display window |

---

#### `main() → None`

**Purpose:** Entry point. Seeds the RNG, runs all five simulations in order, prints summaries, and calls `build_dashboard()`. All logic is driven by `parse_args()` output — no hardcoded values.

**Execution order:**

```
1. parse_args()             → configuration
2. random.seed(seed)        → reproducibility
3. simulate_coin_flips()    → coins
4. statistical_summary()    → print coin stats
5. simulate_dice_rolls()    → dice
6. statistical_summary()    → print dice stats
7. simulate_card_draws()    → cards, print suit/rank counts
8. monte_carlo_pi()         → pi_est, pi_history, print error
9. sample_means()           → clt_means
10. statistical_summary()   → print CLT stats
11. build_dashboard()       → save + show chart
```

---

## 6. File Structure

```
Probability Sandbox/
├── probability_sandbox.py    ← Main program (all layers in one file)
├── tests/
│   ├── __init__.py           ← Makes tests/ a Python package
│   └── test_probability.py   ← 32 pytest unit tests
├── implementation_plan.md    ← Architecture and development plan
├── README.md                 ← This document
├── requirements.txt          ← pip dependencies
└── .gitignore                ← Excludes cache, venv, and chart PNGs
```

---

## 7. Dependencies

| Package | Minimum version | Role |
|---------|----------------|------|
| `matplotlib` | 3.7 | All charting and dashboard rendering |
| `pytest` | 7.0 | Unit test runner |

The core simulation and statistics logic uses **only Python standard library** modules:

| Module | Usage |
|--------|-------|
| `random` | All random number generation (`randint`, `choice`, `uniform`) |
| `math` | `math.sqrt()`, `math.pi`, `math.cos()` for scatter circle |
| `collections.Counter` | Suit/rank and dice face frequency counting |
| `argparse` | CLI argument parsing |

> `numpy` is intentionally excluded to keep the dependency footprint minimal and to demonstrate that the underlying statistics can be implemented from first principles.

---

## 8. Installation

### Requirements

- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/bblank09/Probability-Sandbox.git
cd Probability-Sandbox

# 2. (Recommended) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python3 probability_sandbox.py --help
```

### Verify tests pass

```bash
pytest tests/ -v
# Expected: 32 passed
```

---

## 9. Usage

### Quickstart (default parameters)

```bash
python3 probability_sandbox.py
```

Runs 10,000 trials with a 6-sided die, seeds RNG at 42, and saves `convergence_chart.png`.

---

### Full CLI Reference

```
usage: probability_sandbox [--trials N] [--sides K] [--card-draws N]
                           [--clt-samples N] [--clt-size N]
                           [--output FILE] [--seed N] [--no-plot]

optional arguments:
  --trials N        Number of trials for coin, dice, Monte Carlo (default: 10000)
  --sides K         Number of faces on the die (default: 6)
  --card-draws N    Number of card draws to simulate (default: 100)
  --clt-samples N   Number of repeated samples for CLT histogram (default: 2000)
  --clt-size N      Sample size for each CLT iteration (default: 30)
  --output FILE     Output chart filename — must end in .png (default: convergence_chart.png)
  --seed N          Random seed for full reproducibility (default: 42)
  --no-plot         Write the chart file without opening a display window
```

---

### Example Commands

```bash
# High-precision run: 100,000 trials
python3 probability_sandbox.py --trials 100000

# 20-sided die with output saved as my_result.png
python3 probability_sandbox.py --sides 20 --output my_result.png

# Headless mode (no pop-up window) — suitable for servers or CI
python3 probability_sandbox.py --no-plot

# CLT with larger samples for a sharper bell curve
python3 probability_sandbox.py --clt-samples 5000 --clt-size 50

# Explore a different random seed
python3 probability_sandbox.py --seed 7

# Full custom run
python3 probability_sandbox.py \
  --trials 50000 \
  --sides 12 \
  --card-draws 500 \
  --clt-samples 3000 \
  --clt-size 40 \
  --output custom_run.png \
  --seed 99 \
  --no-plot
```

---

## 10. Sample Output

### Terminal

```
==================================================
   Probability Sandbox  v1.0
==================================================
  seed    : 42
  trials  : 10,000
  sides   : 6

[1/5] Coin Flip Simulation  (n=10,000)

──────────────────────────────────────────────────
  Coin Flip  (1=Heads, 0=Tails)
  ──────────────────────────────────────────────
  n       :       10,000
  mean    :       0.501300
  std     :       0.500001
  95% CI  : (0.491517,  0.511083)
──────────────────────────────────────────────────

[2/5] Dice Roll Simulation  (n=10,000, sides=6)

──────────────────────────────────────────────────
  6-Sided Dice
  ──────────────────────────────────────────────
  n       :       10,000
  mean    :       3.497200
  std     :       1.707565
  95% CI  : (3.463739,  3.530661)
──────────────────────────────────────────────────

[3/5] Card Draw Simulation  (n=100)

  Suit distribution : {'♣': 24, '♦': 26, '♥': 26, '♠': 24}
  Top-3 ranks drawn : [('7', 14), ('K', 12), ('A', 10)]

[4/5] Monte Carlo  π  Estimation  (n=10,000)

  Estimated π = 3.141200
  True      π = 3.141593
  Error       = 0.000393  (0.0125%)

[5/5] Central Limit Theorem  (2,000 samples, size=30)

──────────────────────────────────────────────────
  CLT Sample Means  (dice, sample_size=30)
  ──────────────────────────────────────────────
  n       :        2,000
  mean    :       3.499867
  std     :       0.312018
  95% CI  : (3.486183,  3.513550)
──────────────────────────────────────────────────

Building 6-panel dashboard  →  convergence_chart.png

  [Chart saved → convergence_chart.png]

Done.
```

---

## 11. Dashboard Panels — Detailed Explanation

### Panel 1 — LLN: Coin Flip Convergence

**What is shown:** The running mean of coin flip outcomes (0 or 1) plotted against the number of trials. A horizontal dashed red line marks the true mean = 0.5.

**What to observe:** At low trial counts (left side of the chart), the running mean is unstable — a short streak of heads or tails causes large swings. As $n$ increases, the blue line narrows toward the red dashed line and stays close to it. This is the Law of Large Numbers in action.

**True mean:** $\mu = 0.5$ (by symmetry of a fair coin)

---

### Panel 2 — LLN: Dice Roll Convergence

**What is shown:** The running mean of dice roll outcomes plotted against the number of rolls. The dashed red line marks the true mean = $\frac{k+1}{2}$, where $k$ is the number of sides.

**What to observe:** Identical convergence behavior to Panel 1, but for a discrete uniform distribution. For a standard 6-sided die, the line converges toward 3.5. For a 20-sided die (`--sides 20`), it converges toward 10.5.

**True mean (6-sided):** $\mu = \frac{6+1}{2} = 3.5$

---

### Panel 3 — Monte Carlo π Convergence

**What is shown:** The running estimate of π after each new random point, plotted against the total number of points sampled. The dashed red line marks the true value $\pi \approx 3.14159$.

**What to observe:** The estimate starts highly variable (the first point produces either 0 or 4) and gradually narrows toward π. Unlike the LLN charts, the convergence here is slower (proportional to $1/\sqrt{n}$) — the estimate is still noticeably noisy at $n = 10,000$ compared to the coin and dice means.

---

### Panel 4 — Dice Frequency Distribution

**What is shown:** A bar chart of the relative frequency of each face value across all dice rolls. The dashed red line marks the expected relative frequency = $\frac{1}{k}$.

**What to observe:** For a fair die, all bars should be approximately equal, clustering around the red line. Small deviations from $\frac{1}{6}$ are expected due to randomness and decrease as `--trials` increases. This panel visually tests the uniformity hypothesis for the simulated die.

---

### Panel 5 — CLT: Distribution of Sample Means

**What is shown:** A normalized histogram (probability density) of the sample means generated by `sample_means()`. The dashed red line marks the grand mean of all sample means.

**What to observe:** Despite the dice rolls having a flat (discrete uniform) distribution, the sample means form a bell-shaped (normal) distribution. This is the Central Limit Theorem made visible. The bell becomes narrower as `--clt-size` increases (smaller standard error $\sigma/\sqrt{n}$) and smoother as `--clt-samples` increases.

**Theoretical prediction:**
- Center of the bell: $\mu = 3.5$ (for 6-sided die)
- Width (std of the bell): $\sigma/\sqrt{n} = 1.708/\sqrt{30} \approx 0.312$

---

### Panel 6 — Monte Carlo π Scatter Plot

**What is shown:** 3,000 randomly sampled points in $[-1,1]^2$. Points inside the unit circle ($x^2 + y^2 \leq 1$) are plotted in blue; points outside are in red. The unit circle boundary is drawn as a black line.

**What to observe:** The ratio of blue points to total points estimates $\pi/4$. The scatter plot provides geometric intuition for why the method works — the circle occupies exactly $\pi/4 \approx 78.5\%$ of the square's area.

---

## 12. Testing

### Running the Tests

```bash
# Run all 32 tests with verbose output
pytest tests/ -v

# Run a specific test class
pytest tests/ -v -k "TestMonteCarloPi"

# Run with coverage report (requires pytest-cov)
pip install pytest-cov
pytest tests/ --cov=probability_sandbox --cov-report=term-missing
```

### Test Suite Overview

| Test Class | Cases | What is verified |
|-----------|-------|-----------------|
| `TestSimulateCoinFlips` | 4 | Correct length, binary values only, empty input, LLN convergence at n=100,000 |
| `TestSimulateDiceRolls` | 7 | Correct length, all values in `[1, sides]`, `sides=1` always returns 1, empty input, LLN convergence, 20-sided die range, `sides=0` raises `ValueError` |
| `TestSimulateCardDraws` | 4 | Correct length, empty input, all `(rank, suit)` pairs are valid, all 4 suits appear in a large sample |
| `TestRunningMean` | 4 | Empty list → empty list, single value, known arithmetic check at 3 positions, convergence toward 0.5 |
| `TestMonteCarloPi` | 5 | `|estimate - π| < 0.05` at n=100,000, running list length equals n, n=1 returns 0.0 or 4.0, n=0 edge case, all estimates are non-negative |
| `TestStatisticalSummary` | 6 | Correct mean, std=0 for constant list, CI lower < CI upper, empty list returns `None` fields, label stored correctly, `n` matches input length |
| `TestSampleMeans` | 2 | Output list length equals `num_samples`, grand mean converges to population mean |
| **Total** | **32** | All pass in < 1 second |

### Design Principles

- **Statistical validation** tests use `random.seed()` to ensure deterministic results while still testing convergence behavior at realistic trial counts.
- **Edge case tests** cover empty inputs, minimum values (`sides=1`, `n=1`, `n=0`), and invalid inputs to ensure the code fails cleanly rather than silently.
- **No mocking** — all tests call the real functions with real random numbers (seeded), verifying both the implementation and the underlying probability.

---

## 13. Known Limitations and Caveats

### Performance

- `--trials` above 500,000 will noticeably increase runtime and memory usage. At n=1,000,000, expect approximately 10–30 seconds depending on hardware.
- The CLT step calls `simulate_dice_rolls()` `num_samples × sample_size` times total. At default settings this is 2,000 × 30 = 60,000 additional calls, which is fast, but scales with `--clt-samples` and `--clt-size`.
- Use `--no-plot` in headless or CI environments to skip the display window.

### Randomness and Reproducibility

- Default seed is 42. Using `--seed 42` will always produce identical output. Changing the seed changes all results.
- Monte Carlo π converges at rate $O(1/\sqrt{n})$, not $O(1/n)$. Doubling accuracy requires 4× more points. At n=10,000, expect errors around 0.01–0.05.
- The 95% CI assumes the CLT holds (large n). For very small trial counts, the CI may not be reliable.

### Card Draw Behavior

- Card draws use **with-replacement** sampling. This means drawing more than 52 cards is valid and each draw is independent. It does **not** model a real game scenario where drawn cards are removed from the deck.
- The simulation tracks suits and ranks but does not compute hand probabilities (flush, straight, etc.) — this is reserved for a future version.

### Output Files

- Chart files (`.png`) are excluded from git by `.gitignore`. To commit a chart, rename it to `sample_chart.png` (which is explicitly allowed) or edit `.gitignore`.
- The chart is always saved before being displayed — closing the window does not prevent the file from being written.

### Python Version

- Requires Python 3.8 or higher.
- Tested on Python 3.14.2 (macOS Sequoia). Expected to work on Python 3.8–3.14.
- Type hints use the basic `list` and `tuple` forms (no `list[int]` subscript syntax) for 3.8 compatibility.

---

## 14. Roadmap

### v1.0 — Current Release

- [x] Coin flip simulation with LLN convergence chart
- [x] Dice roll simulation with LLN convergence chart and frequency distribution
- [x] Card draw simulation with suit and rank frequency analysis
- [x] Monte Carlo π estimation with convergence chart and scatter plot
- [x] Central Limit Theorem visualization via sample means histogram
- [x] Statistical summary: mean, standard deviation, 95% confidence interval
- [x] Six-panel matplotlib dashboard saved as PNG
- [x] Full CLI interface via argparse
- [x] 32-case pytest unit test suite

### v1.1 — Planned

- [ ] **Birthday Paradox simulation** — estimate the probability that at least 2 people in a group of $n$ share a birthday; compare empirical vs. analytical result
- [ ] **Bayes' Theorem calculator** — interactive prior/likelihood/posterior demonstration with visual update
- [ ] **Binomial / Poisson / Geometric distributions** — parameterized simulation and PMF comparison
- [ ] **CSV export** — write per-trial data and summary statistics to structured CSV files
- [ ] **Streamlit web UI** — browser-based interactive version with sliders for all parameters

---

## 15. References

1. Bernoulli, J. (1713). *Ars Conjectandi*. Basel.
2. Laplace, P.-S. (1812). *Théorie analytique des probabilités*. Paris.
3. Neyman, J. (1937). Outline of a theory of statistical estimation based on the classical theory of probability. *Philosophical Transactions of the Royal Society A*, 236, 333–380.
4. Metropolis, N., & Ulam, S. (1949). The Monte Carlo Method. *Journal of the American Statistical Association*, 44(247), 335–341.
5. Fisher, R.A. (1925). *Statistical Methods for Research Workers*. Oliver and Boyd.
6. Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95.
7. Python Software Foundation. *random — Generate pseudo-random numbers*. https://docs.python.org/3/library/random.html

---

*Built with Python 3 · matplotlib · pytest*  
*Repository: https://github.com/bblank09/Probability-Sandbox*
