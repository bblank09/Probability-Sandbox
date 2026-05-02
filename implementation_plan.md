# Implementation Plan — Probability Sandbox

## Project Overview

Python simulation sandbox สำหรับ concept หลักของทฤษฎีความน่าจะเป็น  
ครอบคลุม coin flip, dice, card draw, LLN, CLT, Monte Carlo และ statistical summary  
output เป็น multi-panel dashboard chart พร้อม CLI ที่กำหนดค่าได้

---

## File Structure

```
Probability Sandbox/
├── probability_sandbox.py    # Main simulation + CLI entry point
├── tests/
│   └── test_probability.py   # Unit tests (pytest)
├── implementation_plan.md    # This file
├── README.md                 # Project doc พร้อม math อธิบาย
└── requirements.txt          # Dependencies
```

---

## Features ที่จะสร้าง (v1.0)

| # | Feature | รายละเอียด |
|---|---------|-----------|
| 1 | Coin Flip Simulation | simulate n ครั้ง, output 0/1 |
| 2 | Dice Roll Simulation | k-sided die, กำหนด sides ได้ผ่าน CLI |
| 3 | Card Draw Simulation | 52 ใบ, draw with replacement, นับ suit |
| 4 | LLN Convergence Chart | running mean เทียบกับ true mean |
| 5 | CLT Visualization | distribution ของ sample means |
| 6 | Monte Carlo π Estimation | random point ในวงกลม + scatter plot |
| 7 | Statistical Summary | mean, std, 95% confidence interval |
| 8 | Multi-panel Dashboard | 6 subplots ใน figure เดียว |
| 9 | Interactive CLI | argparse: --trials --sides --output ฯลฯ |
| 10 | Unit Tests | edge cases + statistical validation |

---

## Architecture — `probability_sandbox.py`

### Simulation Layer

```python
simulate_coin_flips(n)           → list[int]           # 0 or 1
simulate_dice_rolls(n, sides)    → list[int]           # 1..sides
simulate_card_draws(n)           → list[tuple[str,str]] # (rank, suit)
monte_carlo_pi(n)                → (float, list[float]) # estimate + history
```

### Statistics Layer

```python
running_mean(values)                    → list[float]
sample_means(fn, sample_size, n)        → list[float]   # สำหรับ CLT
statistical_summary(values, label)      → dict           # mean, std, CI
print_summary(summary)                  → None           # print to stdout
```

### Visualization Layer

```python
build_dashboard(coins, dice, sides, pi_estimates, clt_means, save_path)
```

**6 subplots layout (2×3):**

```
┌──────────────────┬──────────────────┬──────────────────┐
│ LLN: Coin Flip   │ LLN: Dice        │ Monte Carlo π    │
│ (running mean)   │ (running mean)   │ (convergence)    │
├──────────────────┼──────────────────┼──────────────────┤
│ Dice Frequency   │ CLT: Sample Mean │ Monte Carlo π    │
│ Distribution     │ Distribution     │ (scatter plot)   │
└──────────────────┴──────────────────┴──────────────────┘
```

### CLI Interface

```bash
python probability_sandbox.py \
  --trials     10000   # จำนวน trials หลัก
  --sides      6       # หน้าลูกเต๋า
  --card-draws 100     # จำนวนหยิบไพ่
  --clt-samples 2000   # จำนวน samples สำหรับ CLT
  --clt-size   30      # sample size แต่ละรอบ (CLT)
  --output     convergence_chart.png
  --no-plot            # save chart โดยไม่ pop-up window
```

---

## Testing Strategy — `tests/test_probability.py`

| Test Class | สิ่งที่ทดสอบ |
|-----------|------------|
| `TestCoinFlips` | length, ค่า binary, n=0, convergence ที่ n=100k |
| `TestDiceRolls` | length, range valid, sides=1, n=0, convergence |
| `TestCardDraws` | length, valid rank/suit, n=0 |
| `TestRunningMean` | single value, convergence, empty list |
| `TestMonteCarloPi` | \|est − π\| < 0.05, length, edge n=1 |
| `TestStatSummary` | mean correct, std=0 case, CI ordering |

---

## README Math Sections

README.md จะอธิบาย 3 ทฤษฎีด้วย LaTeX-style markdown:

**Law of Large Numbers:**
$$\bar{X}_n \xrightarrow{P} \mu \quad \text{as } n \to \infty$$

**Central Limit Theorem:**
$$\frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1)$$

**Monte Carlo π:**
$$\hat{\pi} = 4 \cdot \frac{\text{points inside circle}}{\text{total points}}$$

---

## Dependencies

```
matplotlib>=3.7
```

numpy ไม่จำเป็น — ใช้ `math` และ `random` จาก standard library

---

## Roadmap — v1.1 (Future)

- [ ] Bayes' Theorem simulator
- [ ] Birthday Paradox simulation  
- [ ] Binomial / Poisson / Geometric distributions
- [ ] Export stats to CSV
- [ ] Streamlit interactive web UI

---

## Build Order

1. `requirements.txt`
2. `probability_sandbox.py` — simulation + stats + CLI
3. `tests/test_probability.py` — unit tests
4. `README.md` — documentation + math
5. git init → push to GitHub
