# ✈️ FlightOptimizer
### The Intelligent Flight Selection Engine

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Logic](https://img.shields.io/badge/Logic-Stochastic_Simulation-orange?style=for-the-badge)
![Algorithm](https://img.shields.io/badge/Algorithm-Weighted_Sum_Model-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Operational-green?style=for-the-badge)

**FlightOptimizer** is a stochastic simulation tool designed to solve the *Traveler's Dilemma*: **"Should I buy the cheap ticket now, or wait for a better one?"**

Unlike basic scripts that pick random numbers, this engine simulates a living market. It uses a **Weighted Decision Matrix** (or "Pain Score") to mathematically quantify the trade-off between saving money and suffering through inconveniences like 4 AM departures, 12-hour layovers, or budget airlines with no legroom.

---

## 📚 Table of Contents
1. [The Concept (For Kids)](#-the-concept-eli5-for-junior-explorers)
2. [The Science (For Nerds)](#-the-science-deep-dive-for-data-nerds)
3. [The "Random Walk" Explained](#-the-secret-sauce-random-walk-theory)
4. [How the Math Works](#-the-math-calculating-the-pain-score)
5. [Installation & Usage](#-installation--usage)
6. [Configuration](#-configuration-personalize-your-ai)

---

## 👶 The Concept (ELI5: For Junior Explorers)

Imagine you want to buy a new video game.

* **Store A** sells it for **$20**. But... the store is 10 miles away, it's raining, and the box is ripped.
* **Store B** sells it for **$25**. But... they deliver it to your house instantly and give you a free candy bar.

If you only look at the price, Store A wins. **But Store A is actually a bad deal because of the hassle.**

**This program is a robot brain that understands "Hassle."**
1.  It pretends to look at flight tickets for the next 30 days.
2.  It looks at the price, but also checks if the seats are comfy or if the plane leaves while you're sleeping.
3.  It gives every flight a **"Pain Score."**
4.  It picks the flight with the lowest pain, ensuring you get the best deal for your wallet *and* your happiness.

---

## 🤓 The Science (Deep Dive: For Data Nerds)

For the engineers, economists, and data scientists, `FlightOptimizer` is a simulation of **Utility Theory** and **Market Dynamics**.

### Key Features:
* **Yield Management Simulation:** The script simulates the "booking curve." Flights departing in 0-3 days see an exponential price hike (Last Minute Panic).
* **Weekly Seasonality:** Implements demand curves where Friday/Sunday (leisure/return travel) command a premium, while Tuesday/Wednesday (low business travel) offer dips.
* **Market Segmentation:** Probabilistically generates "LuxAir" (Premium/High Cost) vs. "CheapJet" (Budget/Low Cost) options to test value perception.

---

## 📈 The Secret Sauce: Random Walk Theory

This is the most critical part of the simulation.

**The Problem with Most Code:**
Beginner programmers usually generate data using `random.randint(100, 1000)`. This creates "White Noise."
* *Day 1: $200*
* *Day 2: $900*
* *Day 3: $150*
* *Reality:* Markets don't crash and rally 500% in 24 hours.

**The Solution: The Random Walk (Brownian Motion):**
This project uses a stochastic process where the price of *tomorrow* is a function of the price of *today* plus volatility (drift).

```python
# Pseudo-code of the logic used
market_price_tomorrow = market_price_today + random_volatility

### Visualizing the Difference

**❌ Standard Randomness (Chaos)**

```text
$1000 |       *
 $800 | *
 $600 |             *
 $400 |
 $200 |    * *
      -----------------
       M  T  W  T  F
```

*(This is unrealistic. Prices represent static noise.)*

**✅ Random Walk (Evolution)**

```text
$1000 |
 $800 |    * *
 $600 | * * *
 $400 |
 $200 |
      -----------------
       M  T  W  T  F
```

*(This is realistic. The price "drifts" or "walks" up and down naturally based on market trends.)*

-----

## 🧮 The Math: Calculating the "Pain Score"

The script selects the winner by minimizing the **Total Pain Score**. We use a **Weighted Sum Model**.

The formula used in the code is:

$$Score = P_{ticket} + (T_{wait} \times C_{patience}) + P_{inconvenience} - V_{comfort}$$

### The Variables:

1.  **$P_{ticket}$ (Base Price):** The actual cash value of the ticket.
2.  **$T_{wait} \times C_{patience}$ (Time Value):**
      * We assign a cost to waiting. If a flight is $10 cheaper but requires waiting 25 days, is it worth it?
      * The `DAILY_PATIENCE_COST` variable defines this threshold.
3.  **$P_{inconvenience}$ (Penalties):**
      * **Layovers:** We add a virtual cost (e.g., +$60) to indirect flights.
      * **Bad Timing:** We add a virtual cost (e.g., +$40) to flights leaving at 5 AM.
4.  **$V_{comfort}$ (Bonuses):**
      * **Premium Airline:** We subtract value (e.g., -$50) from the score if the airline offers luxury, effectively justifying a higher ticket price.

-----

## 🚀 Installation & Usage

### Prerequisites

  * Python 3.6 or higher.
  * No external libraries required (uses standard `random` and `statistics`).

### Quick Start

1.  **Download** the script as `flight_sim.py`.
2.  **Run** the simulation:
    ```bash
    python flight_sim.py
    ```

### Sample Output

When you run the script, you will see a generated table and a final recommendation:

```text
DAY  | DOW  | AIRLINE   | PRICE   | SCORE  | NOTES
--------------------------------------------------------------------------------
0    | Wed  | CheapJet  | $1250   | 1220   | ❌ Last Minute Panic
1    | Thu  | LuxAir    | $1300   | 1250   | ❌ Last Minute Panic
...
12   | Mon  | LuxAir    | $580    | 590    | 💎 Luxury Value
13   | Tue  | CheapJet  | $560    | 640    | 
...
--------------------------------------------------------------------------------
🤖 RECOMMENDATION: Day 12 (Mon) on LuxAir
   • Price: $580
   • Details: 14:00, Direct
   • Insight: It's a Premium airline, so the higher price is worth it!
```

-----

## ⚙️ Configuration: Personalize Your AI

You can tweak the "Human Preferences" section at the top of the script to change how the AI makes decisions.

| Constant | Default | Description |
| :--- | :--- | :--- |
| `VALUE_OF_DIRECT_FLIGHT` | **60** | The dollar amount you'd pay to avoid a layover. Increase this if you hate changing planes. |
| `VALUE_OF_GOOD_TIME` | **40** | The dollar amount you'd pay to avoid waking up early. |
| `VALUE_OF_PREMIUM_AIRLINE` | **50** | How much is "Luxury" worth to you? (Legroom, free bags, etc). |
| `DAILY_PATIENCE_COST` | **5** | How much is one day of waiting worth? If set high, the AI will prefer flights sooner rather than later. |

-----

## 📜 License

This project is open-source. Feel free to fork it, modify the "Pain Score" weights to match your own travel preferences, or expand the Random Walk algorithm to include seasonality\!
