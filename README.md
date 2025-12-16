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

All scan modes include:
- A **progress bar** showing scan completion
- **File output** containing the full list of found sequences
- **Console summary** with key statistics

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
results = scan_parameters(
    P_range=(-5, 5), 
    Q_range=(-5, 5), 
    x0=0, x1=1, 
    max_n=15,
    output_file="pq_scan_results.txt"
)

# Scan initial conditions for Fibonacci recurrence
results = scan_initial_conditions(
    P=1, Q=-1, 
    x0_range=(-10, 10), 
    x1_range=(-10, 10), 
    max_n=15,
    output_file="initial_conditions_scan.txt"
)

# Full parameter scan
results = scan_all(
    P_range=(-3, 3), 
    Q_range=(-3, 3), 
    x0_range=(-5, 5), 
    x1_range=(-5, 5), 
    max_n=15,
    output_file="full_scan_results.txt"
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
| `output_file` | Filename for scan results (default: auto-generated with timestamp) |

### Output Files

Scan operations generate output files containing:

1. **Header** — Timestamp and scan type
2. **Scan Parameters** — All input ranges and settings
3. **Divisibility Sequences** — Full list with parameters and first terms
4. **Strong Divisibility Sequences** — Subset satisfying the stronger gcd property
5. **Pattern Analysis** — Breakdown of $x_0 = 0$ vs $x_0 \neq 0$ cases
6. **Summary** — Total counts and statistics

Example output file structure:
```
======================================================================
DIVISIBILITY SEQUENCE SCAN RESULTS
Generated: 2025-12-16 00:46:07
======================================================================

SCAN PARAMETERS
----------------------------------------------------------------------
Scan type: Full Parameter Scan
P range: [-2, 2]
Q range: [-2, 2]
...

======================================================================
DIVISIBILITY SEQUENCES FOUND: 336
======================================================================

P= -2, Q= -2, x_0=  0, x_1= -3, Δ=  12
  First terms: [0, -3, 6, -18, 48, -132]
...

======================================================================
SUMMARY
======================================================================
Total combinations checked: 1225
Divisibility sequences found: 336
Strong divisibility sequences found: 152
```

If no filename is specified, files are auto-generated with timestamps (e.g., `scan_all_20251216_003703.txt`).

## Console Output

During scans, the console displays:

1. **Scan configuration** — Parameter ranges and total combinations
2. **Progress bar** — Visual progress indicator with percentage
3. **Summary** — Key statistics (no sequence listings)

```
============================================================
Full Parameter Scan
============================================================
P range: [-2, 2]
Q range: [-2, 2]
x_0 range: [-3, 3]
x_1 range: [-3, 3]
Testing up to n = 15
Total combinations: 1225

  Progress: |████████████████████████████████████████| 100.0% (1225/1225)

============================================================
SUMMARY
============================================================
Total combinations checked: 1225
Divisibility sequences found: 336
Strong divisibility sequences found: 152
Divisibility sequences with x_0 = 0: 120
Divisibility sequences with x_0 ≠ 0: 216

Results written to: scan_all_20251216_003703.txt
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