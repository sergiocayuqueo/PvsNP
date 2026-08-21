import random
import matplotlib.pyplot as plt
import numpy as np

class SAT3Solver:
    """A recursive DPLL-based solver to demonstrate the complexity of 3-SAT."""
    def __init__(self):
        self.steps = 0

    def solve(self, clauses, assignment):
        self.steps += 1
        if not clauses: return True
        if any(not c for c in clauses): return False
        
        # Heuristic: Choose the most frequent variable
        var = abs(clauses[0][0])
        
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clauses = self.reduce(clauses, var, val)
            if self.solve(new_clauses, new_assignment):
                return True
        return False

    def reduce(self, clauses, var, val):
        new_clauses = []
        for c in clauses:
            if (var in c and val) or (-var in c and not val):
                continue
            new_c = [l for l in c if l != var and l != -var]
            new_clauses.append(new_c)
        return new_clauses

def generate_3sat(n_vars, n_clauses):
    clauses = []
    for _ in range(n_clauses):
        c = random.sample(range(1, n_vars + 1), 3)
        clauses.append([l * random.choice([-1, 1]) for l in c])
    return clauses

# --- EXPERIMENT: THE PHASE TRANSITION ---
n_vars = 15
ratios = np.linspace(2, 6, 15)
avg_steps = []

print("Running Complexity Analysis...")
for r in ratios:
    n_clauses = int(r * n_vars)
    total_steps = 0
    for _ in range(10): # Average over 10 trials
        solver = SAT3Solver()
        clauses = generate_3sat(n_vars, n_clauses)
        solver.solve(clauses, {})
        total_steps += solver.steps
    avg_steps.append(total_steps / 10)
    print(f"Ratio {r:.2f} | Avg Steps: {total_steps/10}")

# Plotting the "Hardness" curve
plt.plot(ratios, avg_steps, marker='o', color='purple')
plt.axvline(x=4.26, color='red', linestyle='--', label='Critical Threshold (α ≈ 4.26)')
plt.title("The P vs NP Boundary: 3-SAT Complexity Peak")
plt.xlabel("Ratio (Clauses / Variables)")
plt.ylabel("Computational Steps (DPLL Backtracking)")
plt.legend()
plt.show()
