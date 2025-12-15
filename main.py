"""
Divisibility Sequence Tester

Tests whether a second-order linear recurrence with given parameters
yields a divisibility sequence.

Recurrence: x_n = P * x_{n-1} - Q * x_{n-2}
Initial conditions: x_0, x_1
"""

import math
from typing import Tuple, List, Optional


def generate_sequence(P: int, Q: int, x0: int, x1: int, n: int) -> List[int]:
    """Generate the first n+1 terms of the sequence (indices 0 through n)."""
    if n < 0:
        return []
    if n == 0:
        return [x0]

    seq = [x0, x1]
    for i in range(2, n + 1):
        seq.append(P * seq[i-1] - Q * seq[i-2])
    return seq


def check_divisibility(seq: List[int], verbose: bool = False) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """
    Check if the sequence satisfies the divisibility property:
    m | n implies seq[m] | seq[n] for all m, n in range.

    Returns:
        (is_divisibility_sequence, first_counterexample or None)
    """
    n = len(seq) - 1

    for m in range(1, n + 1):
        if seq[m] == 0:
            continue  # 0 divides everything, skip

        for k in range(2, n // m + 1):
            idx = m * k
            if idx > n:
                break

            if seq[idx] % seq[m] != 0:
                if verbose:
                    print(f"FAIL: {m} | {idx}, but x_{m} = {seq[m]} does not divide x_{idx} = {seq[idx]}")
                return False, (m, idx)

    return True, None


def check_strong_divisibility(seq: List[int], verbose: bool = False) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """
    Check if the sequence satisfies the strong divisibility property:
    gcd(seq[m], seq[n]) = seq[gcd(m, n)] for all m, n in range.

    Returns:
        (is_strong_divisibility_sequence, first_counterexample or None)
    """
    n = len(seq) - 1

    for m in range(1, n + 1):
        for k in range(m + 1, n + 1):
            g = math.gcd(m, k)
            gcd_terms = math.gcd(seq[m], seq[k])

            if gcd_terms != abs(seq[g]):
                if verbose:
                    print(f"FAIL: gcd(x_{m}, x_{k}) = gcd({seq[m]}, {seq[k]}) = {gcd_terms}")
                    print(f"      but x_gcd({m},{k}) = x_{g} = {seq[g]}")
                return False, (m, k)

    return True, None


def analyze_sequence(P: int, Q: int, x0: int, x1: int, max_n: int = 20,
                     verbose: bool = True, show_terms: bool = True):
    """
    Analyze a sequence for divisibility properties.

    Parameters:
        P, Q: Recurrence parameters (x_n = P*x_{n-1} - Q*x_{n-2})
        x0, x1: Initial conditions
        max_n: Number of terms to generate and test
        verbose: Print detailed failure information
        show_terms: Print individual sequence terms
    """
    print("=" * 60)
    print(f"Sequence Analysis")
    print("=" * 60)
    print(f"Recurrence: x_n = {P} * x_{{n-1}} - ({Q}) * x_{{n-2}}")
    print(f"Initial conditions: x_0 = {x0}, x_1 = {x1}")
    print(f"Characteristic polynomial: x² - {P}x + {Q} = 0")

    discriminant = P * P - 4 * Q
    print(f"Discriminant Δ = {discriminant}")
    print()

    # Generate sequence
    seq = generate_sequence(P, Q, x0, x1, max_n)

    if show_terms:
        print(f"First {max_n + 1} terms:")
        for i, val in enumerate(seq):
            print(f"  x_{i} = {val}")
        print()

    # Check divisibility
    is_div, counterex = check_divisibility(seq, verbose=verbose)
    if is_div:
        print(f"✓ DIVISIBILITY PROPERTY: Satisfied (up to n = {max_n})")
    else:
        m, n = counterex
        print(f"✗ DIVISIBILITY PROPERTY: FAILED")
        print(f"  Counterexample: {m} | {n}, but x_{m} = {seq[m]} ∤ x_{n} = {seq[n]}")
    print()

    # Check strong divisibility
    is_strong, counterex = check_strong_divisibility(seq, verbose=verbose)
    if is_strong:
        print(f"✓ STRONG DIVISIBILITY: Satisfied (up to n = {max_n})")
    else:
        m, n = counterex
        g = math.gcd(m, n)
        print(f"✗ STRONG DIVISIBILITY: FAILED")
        print(f"  Counterexample: gcd(x_{m}, x_{n}) = {math.gcd(seq[m], seq[n])} ≠ x_{g} = {seq[g]}")
    print()

    return seq, is_div, is_strong


def scan_all(P_range: Tuple[int, int], Q_range: Tuple[int, int],
             x0_range: Tuple[int, int], x1_range: Tuple[int, int],
             max_n: int = 20) -> List[dict]:
    """
    Scan all combinations of P, Q, x0, x1 in given ranges and test for divisibility.

    Parameters:
        P_range: (min_P, max_P) inclusive
        Q_range: (min_Q, max_Q) inclusive
        x0_range: (min_x0, max_x0) inclusive
        x1_range: (min_x1, max_x1) inclusive
        max_n: Number of terms to generate and test

    Returns:
        List of results for sequences that ARE divisibility sequences
    """
    results = []
    divisibility_sequences = []
    strong_divisibility_sequences = []

    P_count = P_range[1] - P_range[0] + 1
    Q_count = Q_range[1] - Q_range[0] + 1
    x0_count = x0_range[1] - x0_range[0] + 1
    x1_count = x1_range[1] - x1_range[0] + 1
    total = P_count * Q_count * x0_count * x1_count
    checked = 0

    print("=" * 60)
    print("Full Parameter Scan")
    print("=" * 60)
    print(f"P range: [{P_range[0]}, {P_range[1]}]")
    print(f"Q range: [{Q_range[0]}, {Q_range[1]}]")
    print(f"x_0 range: [{x0_range[0]}, {x0_range[1]}]")
    print(f"x_1 range: [{x1_range[0]}, {x1_range[1]}]")
    print(f"Testing up to n = {max_n}")
    print(f"Total combinations: {total}")
    print()

    for P in range(P_range[0], P_range[1] + 1):
        for Q in range(Q_range[0], Q_range[1] + 1):
            # Skip degenerate case
            if Q == 0:
                checked += x0_count * x1_count
                continue

            discriminant = P * P - 4 * Q

            for x0 in range(x0_range[0], x0_range[1] + 1):
                for x1 in range(x1_range[0], x1_range[1] + 1):
                    checked += 1

                    # Skip trivial case
                    if x0 == 0 and x1 == 0:
                        continue

                    seq = generate_sequence(P, Q, x0, x1, max_n)

                    # Check if sequence becomes trivial
                    if all(s == 0 for s in seq[1:]):
                        continue

                    is_div, _ = check_divisibility(seq, verbose=False)
                    is_strong, _ = check_strong_divisibility(seq, verbose=False)

                    result = {
                        'P': P,
                        'Q': Q,
                        'x0': x0,
                        'x1': x1,
                        'discriminant': discriminant,
                        'is_divisibility': is_div,
                        'is_strong_divisibility': is_strong,
                        'first_terms': seq[:6]
                    }
                    results.append(result)

                    if is_div:
                        divisibility_sequences.append(result)
                    if is_strong:
                        strong_divisibility_sequences.append(result)

    # Print summary
    print(f"Checked {checked} combinations\n")

    print("-" * 60)
    print(f"DIVISIBILITY SEQUENCES FOUND: {len(divisibility_sequences)}")
    print("-" * 60)
    if divisibility_sequences:
        for r in divisibility_sequences:
            strong_marker = " [STRONG]" if r['is_strong_divisibility'] else ""
            print(f"  P={r['P']:3}, Q={r['Q']:3}, x_0={r['x0']:3}, x_1={r['x1']:3}, Δ={r['discriminant']:4}{strong_marker}")
            print(f"    First terms: {r['first_terms']}")
    else:
        print("  None found.")
    print()

    print("-" * 60)
    print(f"STRONG DIVISIBILITY SEQUENCES: {len(strong_divisibility_sequences)}")
    print("-" * 60)
    if strong_divisibility_sequences:
        for r in strong_divisibility_sequences:
            print(f"  P={r['P']:3}, Q={r['Q']:3}, x_0={r['x0']:3}, x_1={r['x1']:3}, Δ={r['discriminant']:4}")
    else:
        print("  None found.")
    print()

    # Analyze patterns
    if divisibility_sequences:
        print("-" * 60)
        print("PATTERN ANALYSIS")
        print("-" * 60)

        # Check if x0=0 is required
        x0_zero_count = sum(1 for r in divisibility_sequences if r['x0'] == 0)
        x0_nonzero_count = len(divisibility_sequences) - x0_zero_count
        print(f"  With x_0 = 0: {x0_zero_count}")
        print(f"  With x_0 ≠ 0: {x0_nonzero_count}")

        if x0_nonzero_count > 0:
            print("\n  Non-zero x_0 cases:")
            for r in divisibility_sequences:
                if r['x0'] != 0:
                    print(f"    P={r['P']}, Q={r['Q']}, x_0={r['x0']}, x_1={r['x1']}")
        print()

    return results


def scan_initial_conditions(P: int, Q: int, x0_range: Tuple[int, int],
                            x1_range: Tuple[int, int], max_n: int = 20) -> List[dict]:
    """
    Scan all initial condition combinations in given ranges and test for divisibility.

    Parameters:
        P, Q: Fixed recurrence parameters
        x0_range: (min_x0, max_x0) inclusive
        x1_range: (min_x1, max_x1) inclusive
        max_n: Number of terms to generate and test

    Returns:
        List of results for sequences that ARE divisibility sequences
    """
    results = []
    divisibility_sequences = []
    strong_divisibility_sequences = []

    total = (x0_range[1] - x0_range[0] + 1) * (x1_range[1] - x1_range[0] + 1)
    checked = 0

    print("=" * 60)
    print("Initial Conditions Scan")
    print("=" * 60)
    print(f"Recurrence: x_n = {P} * x_{{n-1}} - ({Q}) * x_{{n-2}}")
    discriminant = P * P - 4 * Q
    print(f"Discriminant Δ = {discriminant}")
    print(f"x_0 range: [{x0_range[0]}, {x0_range[1]}]")
    print(f"x_1 range: [{x1_range[0]}, {x1_range[1]}]")
    print(f"Testing up to n = {max_n}")
    print(f"Total combinations: {total}")
    print()

    for x0 in range(x0_range[0], x0_range[1] + 1):
        for x1 in range(x1_range[0], x1_range[1] + 1):
            checked += 1

            # Skip trivial case
            if x0 == 0 and x1 == 0:
                continue

            seq = generate_sequence(P, Q, x0, x1, max_n)

            # Check if sequence becomes trivial (all zeros after start)
            if all(s == 0 for s in seq[1:]):
                continue

            is_div, _ = check_divisibility(seq, verbose=False)
            is_strong, _ = check_strong_divisibility(seq, verbose=False)

            result = {
                'x0': x0,
                'x1': x1,
                'is_divisibility': is_div,
                'is_strong_divisibility': is_strong,
                'first_terms': seq[:8]
            }
            results.append(result)

            if is_div:
                divisibility_sequences.append(result)
            if is_strong:
                strong_divisibility_sequences.append(result)

    # Print summary
    print(f"Checked {checked} combinations\n")

    print("-" * 60)
    print(f"DIVISIBILITY SEQUENCES FOUND: {len(divisibility_sequences)}")
    print("-" * 60)
    if divisibility_sequences:
        for r in divisibility_sequences:
            strong_marker = " [STRONG]" if r['is_strong_divisibility'] else ""
            print(f"  x_0={r['x0']:3}, x_1={r['x1']:3}{strong_marker}")
            print(f"    First terms: {r['first_terms']}")
    else:
        print("  None found.")
    print()

    print("-" * 60)
    print(f"STRONG DIVISIBILITY SEQUENCES: {len(strong_divisibility_sequences)}")
    print("-" * 60)
    if strong_divisibility_sequences:
        for r in strong_divisibility_sequences:
            print(f"  x_0={r['x0']:3}, x_1={r['x1']:3}")
    else:
        print("  None found.")
    print()

    return results


def scan_parameters(P_range: Tuple[int, int], Q_range: Tuple[int, int],
                    x0: int, x1: int, max_n: int = 20) -> List[dict]:
    """
    Scan all P,Q combinations in given ranges and test for divisibility.

    Parameters:
        P_range: (min_P, max_P) inclusive
        Q_range: (min_Q, max_Q) inclusive
        x0, x1: Initial conditions to test
        max_n: Number of terms to generate and test

    Returns:
        List of results for sequences that ARE divisibility sequences
    """
    results = []
    divisibility_sequences = []
    strong_divisibility_sequences = []

    total = (P_range[1] - P_range[0] + 1) * (Q_range[1] - Q_range[0] + 1)
    checked = 0

    print("=" * 60)
    print("Parameter Scan")
    print("=" * 60)
    print(f"P range: [{P_range[0]}, {P_range[1]}]")
    print(f"Q range: [{Q_range[0]}, {Q_range[1]}]")
    print(f"Initial conditions: x_0 = {x0}, x_1 = {x1}")
    print(f"Testing up to n = {max_n}")
    print(f"Total combinations: {total}")
    print()

    for P in range(P_range[0], P_range[1] + 1):
        for Q in range(Q_range[0], Q_range[1] + 1):
            checked += 1

            # Skip degenerate cases
            if Q == 0:
                continue

            seq = generate_sequence(P, Q, x0, x1, max_n)

            # Check if sequence becomes trivial (all zeros)
            if all(s == 0 for s in seq[1:]):
                continue

            is_div, _ = check_divisibility(seq, verbose=False)
            is_strong, _ = check_strong_divisibility(seq, verbose=False)

            discriminant = P * P - 4 * Q

            result = {
                'P': P,
                'Q': Q,
                'discriminant': discriminant,
                'is_divisibility': is_div,
                'is_strong_divisibility': is_strong,
                'first_terms': seq[:8]
            }
            results.append(result)

            if is_div:
                divisibility_sequences.append(result)
            if is_strong:
                strong_divisibility_sequences.append(result)

    # Print summary
    print(f"Checked {checked} combinations\n")

    print("-" * 60)
    print(f"DIVISIBILITY SEQUENCES FOUND: {len(divisibility_sequences)}")
    print("-" * 60)
    if divisibility_sequences:
        for r in divisibility_sequences:
            strong_marker = " [STRONG]" if r['is_strong_divisibility'] else ""
            print(f"  P={r['P']:3}, Q={r['Q']:3}, Δ={r['discriminant']:4}{strong_marker}")
            print(f"    First terms: {r['first_terms']}")
    else:
        print("  None found.")
    print()

    print("-" * 60)
    print(f"STRONG DIVISIBILITY SEQUENCES: {len(strong_divisibility_sequences)}")
    print("-" * 60)
    if strong_divisibility_sequences:
        for r in strong_divisibility_sequences:
            print(f"  P={r['P']:3}, Q={r['Q']:3}, Δ={r['discriminant']:4}")
    else:
        print("  None found.")
    print()

    return results


def main():
    print("\n" + "=" * 60)
    print("DIVISIBILITY SEQUENCE TESTER")
    print("=" * 60)
    print("\nRecurrence form: x_n = P * x_{n-1} - Q * x_{n-2}")
    print("(For Fibonacci-type recurrence x_n = x_{n-1} + x_{n-2}, use P=1, Q=-1)")
    print()

    print("Modes:")
    print("  1) Single test")
    print("  2) Scan P,Q range (fixed initial conditions)")
    print("  3) Scan initial conditions range (fixed P,Q)")
    print("  4) Scan all (P, Q, x_0, x_1 ranges)")
    mode = input("Select mode [default 1]: ").strip()

    if mode == '2':
        # Scan P,Q mode
        try:
            print("\nEnter P range:")
            P_min = int(input("  P min: "))
            P_max = int(input("  P max: "))
            print("Enter Q range:")
            Q_min = int(input("  Q min: "))
            Q_max = int(input("  Q max: "))
            x0 = int(input("Enter x_0: "))
            x1 = int(input("Enter x_1: "))
            max_n = int(input("Enter max index to test (default 20): ") or "20")
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_parameters((P_min, P_max), (Q_min, Q_max), x0, x1, max_n)

    elif mode == '3':
        # Scan initial conditions mode
        try:
            P = int(input("Enter P: "))
            Q = int(input("Enter Q: "))
            print("\nEnter x_0 range:")
            x0_min = int(input("  x_0 min: "))
            x0_max = int(input("  x_0 max: "))
            print("Enter x_1 range:")
            x1_min = int(input("  x_1 min: "))
            x1_max = int(input("  x_1 max: "))
            max_n = int(input("Enter max index to test (default 20): ") or "20")
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_initial_conditions(P, Q, (x0_min, x0_max), (x1_min, x1_max), max_n)

    elif mode == '4':
        # Scan all mode
        try:
            print("\nEnter P range:")
            P_min = int(input("  P min: "))
            P_max = int(input("  P max: "))
            print("Enter Q range:")
            Q_min = int(input("  Q min: "))
            Q_max = int(input("  Q max: "))
            print("Enter x_0 range:")
            x0_min = int(input("  x_0 min: "))
            x0_max = int(input("  x_0 max: "))
            print("Enter x_1 range:")
            x1_min = int(input("  x_1 min: "))
            x1_max = int(input("  x_1 max: "))
            max_n = int(input("Enter max index to test (default 20): ") or "20")
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_all((P_min, P_max), (Q_min, Q_max), (x0_min, x0_max), (x1_min, x1_max), max_n)

    else:
        # Single test mode
        try:
            P = int(input("Enter P: "))
            Q = int(input("Enter Q: "))
            x0 = int(input("Enter x_0: "))
            x1 = int(input("Enter x_1: "))
            max_n = int(input("Enter max index to test (default 20): ") or "20")
            show = input("Show individual terms? (y/n, default y): ").strip().lower()
            show_terms = show != 'n'
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        analyze_sequence(P, Q, x0, x1, max_n, show_terms=show_terms)


if __name__ == "__main__":
    main()