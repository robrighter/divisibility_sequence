"""
Divisibility Sequence Tester

Tests whether a second-order linear recurrence with given parameters
yields a divisibility sequence.

Recurrence: x_n = P * x_{n-1} - Q * x_{n-2}
Initial conditions: x_0, x_1
"""

import math
import sys
from datetime import datetime
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


def print_progress_bar(current: int, total: int, width: int = 40):
    """Print a progress bar to the console."""
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percent = progress * 100
    sys.stdout.write(f"\r  Progress: |{bar}| {percent:5.1f}% ({current}/{total})")
    sys.stdout.flush()


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


def write_results_to_file(filename: str, scan_type: str, params: dict,
                          divisibility_sequences: List[dict],
                          strong_divisibility_sequences: List[dict],
                          total_checked: int):
    """Write scan results to a file."""
    with open(filename, 'w') as f:
        # Header
        f.write("=" * 70 + "\n")
        f.write(f"DIVISIBILITY SEQUENCE SCAN RESULTS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        # Scan parameters
        f.write("SCAN PARAMETERS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Scan type: {scan_type}\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")
        f.write(f"Total combinations checked: {total_checked}\n")
        f.write("\n")

        # Divisibility sequences
        f.write("=" * 70 + "\n")
        f.write(f"DIVISIBILITY SEQUENCES FOUND: {len(divisibility_sequences)}\n")
        f.write("=" * 70 + "\n\n")

        if divisibility_sequences:
            for r in divisibility_sequences:
                strong_marker = " [STRONG]" if r.get('is_strong_divisibility', False) else ""
                if 'P' in r and 'x0' in r:
                    f.write(f"P={r['P']:3}, Q={r['Q']:3}, x_0={r['x0']:3}, x_1={r['x1']:3}, Δ={r['discriminant']:4}{strong_marker}\n")
                elif 'P' in r:
                    f.write(f"P={r['P']:3}, Q={r['Q']:3}, Δ={r['discriminant']:4}{strong_marker}\n")
                else:
                    f.write(f"x_0={r['x0']:3}, x_1={r['x1']:3}{strong_marker}\n")
                f.write(f"  First terms: {r['first_terms']}\n\n")
        else:
            f.write("None found.\n\n")

        # Strong divisibility sequences
        f.write("=" * 70 + "\n")
        f.write(f"STRONG DIVISIBILITY SEQUENCES: {len(strong_divisibility_sequences)}\n")
        f.write("=" * 70 + "\n\n")

        if strong_divisibility_sequences:
            for r in strong_divisibility_sequences:
                if 'P' in r and 'x0' in r:
                    f.write(f"P={r['P']:3}, Q={r['Q']:3}, x_0={r['x0']:3}, x_1={r['x1']:3}, Δ={r['discriminant']:4}\n")
                elif 'P' in r:
                    f.write(f"P={r['P']:3}, Q={r['Q']:3}, Δ={r['discriminant']:4}\n")
                else:
                    f.write(f"x_0={r['x0']:3}, x_1={r['x1']:3}\n")
        else:
            f.write("None found.\n")

        # Pattern analysis for scans with x0
        if divisibility_sequences and 'x0' in divisibility_sequences[0]:
            f.write("\n")
            f.write("=" * 70 + "\n")
            f.write("PATTERN ANALYSIS\n")
            f.write("=" * 70 + "\n\n")

            x0_zero_count = sum(1 for r in divisibility_sequences if r['x0'] == 0)
            x0_nonzero_count = len(divisibility_sequences) - x0_zero_count
            f.write(f"With x_0 = 0: {x0_zero_count}\n")
            f.write(f"With x_0 ≠ 0: {x0_nonzero_count}\n\n")

            if x0_nonzero_count > 0:
                f.write("Non-zero x_0 cases:\n")
                for r in divisibility_sequences:
                    if r['x0'] != 0:
                        if 'P' in r:
                            f.write(f"  P={r['P']}, Q={r['Q']}, x_0={r['x0']}, x_1={r['x1']}\n")
                        else:
                            f.write(f"  x_0={r['x0']}, x_1={r['x1']}\n")

        # Summary at bottom
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total combinations checked: {total_checked}\n")
        f.write(f"Divisibility sequences found: {len(divisibility_sequences)}\n")
        f.write(f"Strong divisibility sequences found: {len(strong_divisibility_sequences)}\n")
        if divisibility_sequences and 'x0' in divisibility_sequences[0]:
            x0_zero_count = sum(1 for r in divisibility_sequences if r['x0'] == 0)
            f.write(f"Divisibility sequences with x_0 = 0: {x0_zero_count}\n")
            f.write(f"Divisibility sequences with x_0 ≠ 0: {len(divisibility_sequences) - x0_zero_count}\n")


def print_summary(divisibility_sequences: List[dict], strong_divisibility_sequences: List[dict],
                  total_checked: int, filename: str):
    """Print summary to console."""
    print("\n")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total combinations checked: {total_checked}")
    print(f"Divisibility sequences found: {len(divisibility_sequences)}")
    print(f"Strong divisibility sequences found: {len(strong_divisibility_sequences)}")

    if divisibility_sequences and 'x0' in divisibility_sequences[0]:
        x0_zero_count = sum(1 for r in divisibility_sequences if r['x0'] == 0)
        x0_nonzero_count = len(divisibility_sequences) - x0_zero_count
        print(f"Divisibility sequences with x_0 = 0: {x0_zero_count}")
        print(f"Divisibility sequences with x_0 ≠ 0: {x0_nonzero_count}")

    print(f"\nResults written to: {filename}")
    print()


def scan_all(P_range: Tuple[int, int], Q_range: Tuple[int, int],
             x0_range: Tuple[int, int], x1_range: Tuple[int, int],
             max_n: int = 20, output_file: str = None) -> List[dict]:
    """
    Scan all combinations of P, Q, x0, x1 in given ranges and test for divisibility.
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
                print_progress_bar(checked, total)
                continue

            discriminant = P * P - 4 * Q

            for x0 in range(x0_range[0], x0_range[1] + 1):
                for x1 in range(x1_range[0], x1_range[1] + 1):
                    checked += 1

                    if checked % 100 == 0 or checked == total:
                        print_progress_bar(checked, total)

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

    print_progress_bar(total, total)
    print("\n")

    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"scan_all_{timestamp}.txt"

    # Write results to file
    params = {
        'P range': f"[{P_range[0]}, {P_range[1]}]",
        'Q range': f"[{Q_range[0]}, {Q_range[1]}]",
        'x_0 range': f"[{x0_range[0]}, {x0_range[1]}]",
        'x_1 range': f"[{x1_range[0]}, {x1_range[1]}]",
        'max_n': max_n
    }
    write_results_to_file(output_file, "Full Parameter Scan", params,
                          divisibility_sequences, strong_divisibility_sequences, checked)

    # Print summary to console
    print_summary(divisibility_sequences, strong_divisibility_sequences, checked, output_file)

    return results


def scan_initial_conditions(P: int, Q: int, x0_range: Tuple[int, int],
                            x1_range: Tuple[int, int], max_n: int = 20,
                            output_file: str = None) -> List[dict]:
    """
    Scan all initial condition combinations in given ranges and test for divisibility.
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

            if checked % 50 == 0 or checked == total:
                print_progress_bar(checked, total)

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

    print_progress_bar(total, total)
    print("\n")

    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"scan_initial_conditions_{timestamp}.txt"

    # Write results to file
    params = {
        'P': P,
        'Q': Q,
        'Discriminant Δ': discriminant,
        'x_0 range': f"[{x0_range[0]}, {x0_range[1]}]",
        'x_1 range': f"[{x1_range[0]}, {x1_range[1]}]",
        'max_n': max_n
    }
    write_results_to_file(output_file, "Initial Conditions Scan", params,
                          divisibility_sequences, strong_divisibility_sequences, checked)

    # Print summary to console
    print_summary(divisibility_sequences, strong_divisibility_sequences, checked, output_file)

    return results


def scan_parameters(P_range: Tuple[int, int], Q_range: Tuple[int, int],
                    x0: int, x1: int, max_n: int = 20,
                    output_file: str = None) -> List[dict]:
    """
    Scan all P,Q combinations in given ranges and test for divisibility.
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

            if checked % 20 == 0 or checked == total:
                print_progress_bar(checked, total)

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

    print_progress_bar(total, total)
    print("\n")

    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"scan_parameters_{timestamp}.txt"

    # Write results to file
    params = {
        'P range': f"[{P_range[0]}, {P_range[1]}]",
        'Q range': f"[{Q_range[0]}, {Q_range[1]}]",
        'x_0': x0,
        'x_1': x1,
        'max_n': max_n
    }
    write_results_to_file(output_file, "Parameter Scan (P, Q)", params,
                          divisibility_sequences, strong_divisibility_sequences, checked)

    # Print summary to console
    print_summary(divisibility_sequences, strong_divisibility_sequences, checked, output_file)

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
            output_file = input("Output filename (default: auto-generated): ").strip() or None
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_parameters((P_min, P_max), (Q_min, Q_max), x0, x1, max_n, output_file)

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
            output_file = input("Output filename (default: auto-generated): ").strip() or None
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_initial_conditions(P, Q, (x0_min, x0_max), (x1_min, x1_max), max_n, output_file)

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
            output_file = input("Output filename (default: auto-generated): ").strip() or None
        except ValueError:
            print("Invalid input. Please enter integers.")
            return

        print()
        scan_all((P_min, P_max), (Q_min, Q_max), (x0_min, x0_max), (x1_min, x1_max), max_n, output_file)

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