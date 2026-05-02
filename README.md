# Probability Sandbox

> ห้องทดลองจำลองทฤษฎีความน่าจะเป็นด้วย Python — เห็นตัวเลข เห็น chart เข้าใจจริง

---

## สารบัญ

1. [โปรเจกต์นี้คืออะไร](#โปรเจกต์นี้คืออะไร)
2. [ทำมาทำไม](#ทำมาทำไม)
3. [ทฤษฎีที่ใช้งาน](#ทฤษฎีที่ใช้งาน)
4. [ฟีเจอร์ทั้งหมด](#ฟีเจอร์ทั้งหมด)
5. [โครงสร้างไฟล์](#โครงสร้างไฟล์)
6. [การติดตั้ง](#การติดตั้ง)
7. [วิธีใช้งาน](#วิธีใช้งาน)
8. [ตัวอย่าง Output](#ตัวอย่าง-output)
9. [รายละเอียด Dashboard](#รายละเอียด-dashboard)
10. [การทดสอบ](#การทดสอบ)
11. [ข้อควรระวัง](#ข้อควรระวัง)
12. [Roadmap](#roadmap)

---

## โปรเจกต์นี้คืออะไร

**Probability Sandbox** คือโปรแกรม Python สำหรับจำลอง (simulate) ปรากฏการณ์ทางความน่าจะเป็น  
แทนที่จะท่องสูตรอย่างเดียว โปรแกรมนี้ให้คุณ **รันการทดลองจริง หลายหมื่นครั้ง** แล้วดูว่าผลลัพธ์  
เป็นไปตามทฤษฎีหรือไม่ พร้อม dashboard 6 panel ที่แสดงผลเป็น chart ทั้งหมด

**เหมาะสำหรับ**
- นักศึกษาที่เรียนวิชา Probability / Statistics
- ผู้ที่ต้องการเข้าใจ Law of Large Numbers และ Central Limit Theorem แบบ visual
- ใครก็ตามที่ต้องการดูว่าความสุ่มทำงานอย่างไร

---

## ทำมาทำไม

ทฤษฎีความน่าจะเป็นเป็นรากฐานของ Data Science, Machine Learning, และ Statistics  
แต่คนส่วนใหญ่เรียนผ่านสูตรและกราฟในหนังสือ ซึ่งยากที่จะ "รู้สึก" ได้จริงว่ามันทำงานอย่างไร

โปรเจกต์นี้สร้างขึ้นเพื่อตอบคำถามเหล่านี้ด้วยการ **ลงมือทดลองจริง**:

| คำถาม | การทดลองใน Sandbox |
|-------|-------------------|
| ทำไมโยนเหรียญหลายๆ ครั้งถึงได้หัวประมาณ 50%? | LLN coin flip convergence |
| ทำไม sample mean ถึงกระจายเป็น bell curve? | CLT dice demonstration |
| ประมาณค่า π ด้วยความสุ่มได้จริงไหม? | Monte Carlo simulation |
| ลูกเต๋ายุติธรรมหรือเปล่า? | Dice frequency distribution |

---

## ทฤษฎีที่ใช้งาน

### 1. Law of Large Numbers (LLN)

เมื่อจำนวนการทดลอง n เพิ่มขึ้น ค่าเฉลี่ยตัวอย่างจะเข้าหาค่าเฉลี่ยจริงของประชากร

$$\bar{X}_n \xrightarrow{P} \mu \quad \text{as } n \to \infty$$

**ตัวอย่าง:** โยนเหรียญ 10 ครั้ง อาจได้หัว 3/10 = 30%  
แต่โยน 100,000 ครั้ง จะได้หัว ≈ 50,000/100,000 = 50.000%

---

### 2. Central Limit Theorem (CLT)

ไม่ว่า distribution เดิมจะมีรูปร่างอย่างไร ถ้าสุ่ม sample ขนาด n ซ้ำหลายๆ รอบ  
การกระจายของ sample mean จะเข้าใกล้ Normal distribution เมื่อ n มากพอ

$$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

**ตัวอย่าง:** ลูกเต๋า 6 หน้า distribution เป็นแบบ uniform  
แต่ถ้าสุ่ม sample 30 ลูกและหาค่าเฉลี่ย ทำซ้ำ 2,000 รอบ → ได้ bell curve

---

### 3. Monte Carlo Estimation

ใช้ความสุ่มเพื่อประมาณค่าที่คำนวณยาก โดยอาศัยสัดส่วนทางเรขาคณิต

$$\hat{\pi} = 4 \times \frac{\text{จำนวนจุดที่อยู่ในวงกลม}}{\text{จำนวนจุดทั้งหมด}}$$

**วิธีการ:** สุ่มจุด (x, y) ในจตุรัส [-1, 1] × [-1, 1]  
ถ้า $x^2 + y^2 \leq 1$ → จุดอยู่ในวงกลม  
สัดส่วน × 4 ≈ π

---

## ฟีเจอร์ทั้งหมด

| # | ฟีเจอร์ | รายละเอียด |
|---|---------|-----------|
| 1 | Coin Flip Simulation | จำลอง n ครั้ง วิเคราะห์ mean, std, 95% CI |
| 2 | Dice Roll Simulation | ลูกเต๋า k หน้า กำหนดเองได้ผ่าน CLI |
| 3 | Card Draw Simulation | หยิบไพ่ 52 ใบ with replacement แสดง suit/rank distribution |
| 4 | LLN Convergence Chart | running mean แบบ real-time เทียบกับ true mean |
| 5 | CLT Visualization | histogram ของ sample means แสดง normal convergence |
| 6 | Monte Carlo π | ประมาณค่า π พร้อม convergence chart + scatter plot |
| 7 | Statistical Summary | mean, std deviation, 95% confidence interval |
| 8 | Multi-panel Dashboard | 6 subplots ใน figure เดียว บันทึกเป็น PNG |
| 9 | Interactive CLI | กำหนด trials, sides, output ฯลฯ ผ่าน argument |
| 10 | Unit Tests | 32 test cases ครอบคลุม edge cases และ statistical validation |

---

## โครงสร้างไฟล์

```
Probability Sandbox/
├── probability_sandbox.py    ← โปรแกรมหลัก (simulation + chart + CLI)
├── tests/
│   ├── __init__.py
│   └── test_probability.py   ← Unit tests (32 cases)
├── implementation_plan.md    ← แผนการพัฒนา
├── README.md                 ← ไฟล์นี้
├── requirements.txt          ← dependencies
└── .gitignore
```

---

## การติดตั้ง

### ความต้องการของระบบ

- Python 3.8 ขึ้นไป
- pip

### ขั้นตอน

```bash
# 1. Clone repository
git clone https://github.com/bblank09/Probability-Sandbox.git
cd Probability-Sandbox

# 2. (แนะนำ) สร้าง virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. ติดตั้ง dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | เวอร์ชันขั้นต่ำ | ใช้ทำอะไร |
|---------|--------------|---------|
| `matplotlib` | 3.7 | วาด chart และ dashboard |
| `pytest` | 7.0 | รัน unit tests |

> โปรแกรมใช้ `random` และ `math` จาก Python standard library เป็นหลัก ไม่ต้องติดตั้ง numpy

---

## วิธีใช้งาน

### รันด้วยค่า default (แนะนำสำหรับครั้งแรก)

```bash
python3 probability_sandbox.py
```

จะใช้ค่า: 10,000 trials, ลูกเต๋า 6 หน้า, บันทึก chart เป็น `convergence_chart.png`

---

### CLI Arguments ทั้งหมด

```bash
python3 probability_sandbox.py [OPTIONS]

Options:
  --trials N          จำนวน trials หลัก (coin, dice, Monte Carlo)
                      default: 10000

  --sides K           จำนวนหน้าลูกเต๋า
                      default: 6

  --card-draws N      จำนวนครั้งที่หยิบไพ่
                      default: 100

  --clt-samples N     จำนวน samples สำหรับ CLT
                      default: 2000

  --clt-size N        ขนาด sample แต่ละรอบ (CLT)
                      default: 30

  --output FILE       ชื่อไฟล์ output chart (.png)
                      default: convergence_chart.png

  --seed N            Random seed (สำหรับ reproducibility)
                      default: 42

  --no-plot           บันทึก chart โดยไม่เปิด window (เหมาะสำหรับ server)
```

---

### ตัวอย่างคำสั่ง

```bash
# ทดลองด้วย 50,000 trials และลูกเต๋า 20 หน้า
python3 probability_sandbox.py --trials 50000 --sides 20

# บันทึกผลเป็นไฟล์ชื่อ result.png โดยไม่เปิด window
python3 probability_sandbox.py --output result.png --no-plot

# CLT ขนาด sample ใหญ่ขึ้น เพื่อดู normal distribution ชัดขึ้น
python3 probability_sandbox.py --clt-samples 5000 --clt-size 50

# เปลี่ยน seed เพื่อดูผลลัพธ์ต่างกัน
python3 probability_sandbox.py --seed 123
```

---

## ตัวอย่าง Output

### Terminal Output

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
  ──────────────────────────────────────────
  n       :       10,000
  mean    :       0.501300
  std     :       0.500001
  95% CI  : (0.491500,  0.511100)
──────────────────────────────────────────────────

[4/5] Monte Carlo  π  Estimation  (n=10,000)

  Estimated π = 3.141200
  True      π = 3.141593
  Error       = 0.000393  (0.0125%)
```

### Dashboard Chart (6 Panels)

```
┌──────────────────┬──────────────────┬──────────────────┐
│ LLN: Coin Flip   │ LLN: Dice        │ Monte Carlo π    │
│ running mean     │ running mean     │ convergence line │
│ → 0.5            │ → 3.5            │ → π              │
├──────────────────┼──────────────────┼──────────────────┤
│ Dice Frequency   │ CLT: Sample Mean │ Monte Carlo π    │
│ Bar Chart        │ Histogram        │ Scatter Plot     │
│ (vs expected)    │ (bell curve)     │ (blue=in circle) │
└──────────────────┴──────────────────┴──────────────────┘
```

---

## รายละเอียด Dashboard

### Panel 1 — LLN: Coin Flip Convergence
แสดง running mean ของการโยนเหรียญสะสม เส้นสีแดงประคือ true mean = 0.5  
ยิ่ง n มาก เส้นสีน้ำเงินยิ่งวิ่งเข้าหาเส้นแดง

### Panel 2 — LLN: Dice Convergence
เหมือน Panel 1 แต่เป็นลูกเต๋า true mean = (sides + 1) / 2  
ลูกเต๋า 6 หน้า → true mean = 3.5

### Panel 3 — Monte Carlo π Convergence
แสดงค่าประมาณ π ที่เปลี่ยนไปตาม n  
เส้นกราฟสั่นในช่วงแรก และค่อยๆ นิ่งเข้าหา π = 3.14159...

### Panel 4 — Dice Frequency Distribution
bar chart แสดงความถี่สัมพัทธ์ของแต่ละหน้าลูกเต๋า  
เส้นแดงประคือความถี่ที่คาดหวัง = 1/sides  
ถ้าลูกเต๋ายุติธรรม ทุก bar ควรใกล้เส้นแดง

### Panel 5 — CLT: Distribution of Sample Means
histogram ของ sample means 2,000 ชุด แต่ละชุดขนาด 30  
แม้ distribution เดิม (ลูกเต๋า) จะเป็น uniform แต่ histogram นี้จะออกมาเป็น bell curve  
นี่คือ Central Limit Theorem ในทางปฏิบัติ

### Panel 6 — Monte Carlo π Scatter Plot
จุดสีน้ำเงิน = อยู่ในวงกลม (x² + y² ≤ 1)  
จุดสีแดง = อยู่นอกวงกลม  
สัดส่วนจุดน้ำเงิน × 4 ≈ π

---

## การทดสอบ

### รัน Unit Tests

```bash
# รัน test ทั้งหมด
pytest tests/ -v

# รัน test เฉพาะ class
pytest tests/ -v -k "TestMonteCarloPi"

# แสดง coverage (ถ้าติดตั้ง pytest-cov)
pytest tests/ --cov=probability_sandbox
```

### Test Coverage

| Test Class | จำนวน Cases | สิ่งที่ทดสอบ |
|-----------|------------|------------|
| `TestSimulateCoinFlips` | 4 | length, binary values, empty, LLN convergence |
| `TestSimulateDiceRolls` | 7 | length, range, sides=1, empty, LLN, 20-sided, invalid sides |
| `TestSimulateCardDraws` | 4 | length, empty, valid cards, all suits appear |
| `TestRunningMean` | 4 | empty, single value, known values, convergence |
| `TestMonteCarloPi` | 5 | accuracy, length, n=1 edge, n=0 edge, positive values |
| `TestStatisticalSummary` | 6 | mean, std=0, CI order, empty, label, n |
| `TestSampleMeans` | 2 | count, population mean convergence |
| **รวม** | **32** | |

---

## ข้อควรระวัง

### ด้านประสิทธิภาพ
- `--trials` สูงกว่า 500,000 จะใช้เวลาและ RAM มากขึ้น แนะนำไม่เกิน 100,000 สำหรับเครื่องทั่วไป
- Chart generation จะ pop-up window — ใช้ `--no-plot` ถ้ารันบน server หรือ CI

### ด้านความสุ่ม
- ใช้ `random.seed(42)` เป็น default เพื่อ reproducibility  
  เปลี่ยน seed ด้วย `--seed N` เพื่อดูผลที่แตกต่างกัน
- Monte Carlo π มีความแม่นยำสูงขึ้นตาม √n ไม่ใช่ n  
  เพิ่ม trials 100× จะได้ error ลดลงแค่ 10×

### ด้านผลลัพธ์
- `.png` chart จะถูก `.gitignore` (ยกเว้น `sample_chart.png`)  
  ถ้าต้องการ commit chart ให้ใช้ชื่อ `sample_chart.png` หรือแก้ `.gitignore`
- Card draws ใช้ **with replacement** (หยิบแล้วคืน) ดังนั้นหยิบได้เกิน 52 ใบ

### ด้าน Python version
- ต้องการ Python 3.8+ สำหรับ type hints และ f-strings รูปแบบที่ใช้
- ทดสอบบน Python 3.14 (macOS) และควรทำงานได้บน 3.8–3.14

---

## Roadmap

### v1.0 (ปัจจุบัน)
- [x] Coin flip simulation + LLN
- [x] Dice roll simulation + LLN
- [x] Card draw simulation
- [x] Monte Carlo π estimation
- [x] Central Limit Theorem visualization
- [x] Statistical summary (mean, std, CI)
- [x] 6-panel matplotlib dashboard
- [x] CLI interface (argparse)
- [x] 32 unit tests

### v1.1 (planned)
- [ ] Birthday Paradox simulation
- [ ] Bayes' Theorem calculator
- [ ] Binomial / Poisson / Geometric distributions
- [ ] Export statistics to CSV
- [ ] Streamlit interactive web UI

---

## License

MIT License — ใช้งาน ดัดแปลง แจกจ่ายได้อย่างอิสระ

---

*สร้างด้วย Python 3 · matplotlib · pytest*
