# Divisibility Sequence Tester

A Python tool for investigating divisibility properties of second-order linear recurrence sequences, with a focus on Lucas sequences and the classification of initial conditions that yield divisibility sequences.

## Background

A **divisibility sequence** is a sequence of integers $(a_n)$ where $m \mid n$ implies $a_m \mid a_n$. The classical example is the Fibonacci sequence, which satisfies the stronger property:

$$\gcd(F_m, F_n) = F_{\gcd(m,n)}$$

This tool explores **Lucas sequences** $U_n(P, Q)$ and $V_n(P, Q)$, which arise from the recurrence:

$$x_n = P \cdot x_{n-1} - Q \cdot x_{n-2}$$

with different initial conditions:

| Type | $x_0$ | $x_1$ | Example |
|------|-------|-------|---------|
| U-type | 0 | 1 | Fibonacci numbers |
| V-type | 2 | $P$ | Lucas numbers |

It is known that U-type sequences are always strong divisibility sequences, while V-type sequences generally are not. This tool allows systematic investigation of which parameter combinations $(P, Q, x_0, x_1)$ yield divisibility sequences.

## Installation

No external dependencies required beyond Python 3.6+.

```bash
git clone <repository-url>
cd divisibility-sequences
```

## Usage

### Interactive Mode

```bash
python divisibility_tester.py
```

The program offers four modes:

1. **Single test** — Analyze one specific sequence
2. **Scan P,Q range** — Test multiple recurrence parameters with fixed initial conditions
3. **Scan initial conditions range** — Test multiple initial conditions with fixed $P$, $Q$
4. **Scan all** — Test all combinations of $P$, $Q$, $x_0$, $x_1$ in specified ranges

### Programmatic Usage

```python
from divisibility_tester import (
    analyze_sequence,
    scan_parameters,
    scan_initial_conditions,
    scan_all
)

# Analyze a single sequence (Fibonacci)
seq, is_div, is_strong = analyze_sequence(P=1, Q=-1, x0=0, x1=1, max_n=20)

# Scan P,Q combinations with U-type initial conditions
results = scan_parameters(P_range=(-5, 5), Q_range=(-5, 5), x0=0, x1=1, max_n=15)

# Scan initial conditions for Fibonacci recurrence
results = scan_initial_conditions(P=1, Q=-1, x0_range=(-10, 10), x1_range=(-10, 10), max_n=15)

# Full parameter scan
results = scan_all(
    P_range=(-3, 3), 
    Q_range=(-3, 3), 
    x0_range=(-5, 5), 
    x1_range=(-5, 5), 
    max_n=15
)
```

### Options

| Parameter | Description |
|-----------|-------------|
| `P`, `Q` | Recurrence parameters: $x_n = Px_{n-1} - Qx_{n-2}$ |
| `x0`, `x1` | Initial conditions $x_0$ and $x_1$ |
| `max_n` | Maximum index to test (default: 20) |
| `show_terms` | Display individual sequence terms (default: True) |
| `verbose` | Show detailed failure information (default: True) |

## Output

The tool tests two properties:

1. **Divisibility property**: $m \mid n \Rightarrow x_m \mid x_n$
2. **Strong divisibility property**: $\gcd(x_m, x_n) = x_{\gcd(m,n)}$

Example output:

```
============================================================
Sequence Analysis
============================================================
Recurrence: x_n = 1 * x_{n-1} - (-1) * x_{n-2}
Initial conditions: x_0 = 0, x_1 = 1
Characteristic polynomial: x² - 1x + -1 = 0
Discriminant Δ = 5

First 9 terms:
  x_0 = 0
  x_1 = 1
  x_2 = 1
  x_3 = 2
  x_4 = 3
  x_5 = 5
  x_6 = 8
  x_7 = 13
  x_8 = 21

✓ DIVISIBILITY PROPERTY: Satisfied (up to n = 8)

✓ STRONG DIVISIBILITY: Satisfied (up to n = 8)
```

## Key Findings

Empirical observations from systematic scans:

1. **U-type sequences** ($x_0 = 0$, $x_1 = k$) are divisibility sequences for all tested $P$, $Q$ values, confirming the theoretical result that scalar multiples of $U_n(P,Q)$ preserve divisibility.

2. **V-type sequences** ($x_0 = 2$, $x_1 = P$) fail the divisibility property for most non-degenerate cases.

3. **Non-zero $x_0$ divisibility sequences** exist but are typically:
   - Degenerate cases ($P = 0$, giving $x_n = -Qx_{n-2}$)
   - Constant sequences ($x_0 = x_1$ with specific $P$, $Q$)
   - Periodic sequences with special structure

4. The **discriminant** $\Delta = P^2 - 4Q$ appears to influence which additional initial conditions work, but $x_0 = 0$ remains the robust choice.

## Mathematical Background

### Characteristic Roots

The recurrence $x_n = Px_{n-1} - Qx_{n-2}$ has characteristic polynomial $t^2 - Pt + Q = 0$ with roots:

$$\alpha = \frac{P + \sqrt{\Delta}}{2}, \quad \beta = \frac{P - \sqrt{\Delta}}{2}$$

where $\Delta = P^2 - 4Q$ is the discriminant.

### Binet Formulas

The closed forms for Lucas sequences are:

$$U_n = \frac{\alpha^n - \beta^n}{\alpha - \beta}, \qquad V_n = \alpha^n + \beta^n$$

The algebraic structure of $U_n$ (difference of powers) naturally factors in ways that enforce divisibility, while $V_n$ (sum of powers) does not.

### Why U-type Works

The key identity is:

$$\alpha^{mk} - \beta^{mk} = (\alpha^m - \beta^m)(\alpha^{m(k-1)} + \alpha^{m(k-2)}\beta^m + \cdots + \beta^{m(k-1)})$$

This factorization directly implies $U_m \mid U_{mk}$, establishing the divisibility property.

## Research Applications

This tool supports investigation of:

- Classification of initial conditions yielding divisibility sequences
- Relationship between discriminant and divisibility properties
- Computational verification of theoretical results
- Discovery of non-obvious divisibility sequences

## References

- Ribenboim, P. — *The New Book of Prime Number Records*
- Williams, H.C. — *Édouard Lucas and Primality Testing*
- Ballot, C. — Papers on divisibility sequences and Lucas functions
- Ward, M. — "Memoir on Elliptic Divisibility Sequences"

## License

MIT License