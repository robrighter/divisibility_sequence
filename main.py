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
        seq.append(P * seq[i - 1] - Q * seq[i - 2])
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


def analyze_sequence(P: int, Q: int, x0: int, x1: int, max_n: int = 20, verbose: bool = True):
    """
    Analyze a sequence for divisibility properties.

    Parameters:
        P, Q: Recurrence parameters (x_n = P*x_{n-1} - Q*x_{n-2})
        x0, x1: Initial conditions
        max_n: Number of terms to generate and test
        verbose: Print detailed output
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


def main():
    print("\n" + "=" * 60)
    print("DIVISIBILITY SEQUENCE TESTER")
    print("=" * 60)
    print("\nRecurrence form: x_n = P * x_{n-1} - Q * x_{n-2}")
    print("(For Fibonacci-type recurrence x_n = x_{n-1} + x_{n-2}, use P=1, Q=-1)")
    print()

    # Get parameters from user
    try:
        P = int(input("Enter P: "))
        Q = int(input("Enter Q: "))
        x0 = int(input("Enter x_0: "))
        x1 = int(input("Enter x_1: "))
        max_n = int(input("Enter max index to test (default 20): ") or "20")
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    print()
    analyze_sequence(P, Q, x0, x1, max_n)

    # Compare with U-type sequence
    print("\n" + "-" * 60)
    print("COMPARISON: U-type sequence with same P, Q")
    print("-" * 60)
    analyze_sequence(P, Q, 0, 1, max_n, verbose=False)


if __name__ == "__main__":
    main()