# CDCL SAT Solver

This project is a custom implementation of a SAT (Satisfiability) solver based on the **Conflict-Driven Clause Learning (CDCL)** procedure, developed as part of the *Automated Reasoning* course in the Master's Degree in Artificial Intelligence at the University of Verona.

Author: **Tommaso Menti**  
Academic Year: **2023/2024**  
Professor: *Maria Paola Bonacina*

---

## 🧠 About the Project

This solver aims to determine whether a given Boolean formula in **CNF (Conjunctive Normal Form)** is satisfiable (SAT) or not (UNSAT). The CDCL procedure allows the solver to learn from conflicts during the search and to backjump intelligently, increasing efficiency.

The solver was built **from scratch in Python**, without using existing solvers or libraries, to deepen understanding of the CDCL algorithm and its heuristics.

---

## ⚙️ How It Works

1. **Input**: The program asks for the path to a `.cnf` file.
2. **Clause Matrix**: Each clause becomes a row in a matrix.
3. **Clause Simplification**: The `Subsume` function removes subsumed clauses.
4. **VSIDS Heuristic**: Initializes a scoring system for each literal to prioritize decisions.
5. **Main CDCL Loop**:
   - **Two-Watched Literals**: Used for unit propagation and conflict detection.
   - **Decision**: Chooses literals with the highest VSIDS score.
   - **Conflict Handling**: Increments scores of literals involved in conflicts.
   - **Explain + Learn (1UIP)**: Performs conflict analysis and learns a new clause.
   - **Backjumping**: Jumps to the appropriate decision level.
   - **Clause Forgetting**: Periodically deletes long learned clauses.
   - **Satisfiability Check**: If all clauses are satisfied, returns SAT; if a conflict is found at level 0, returns UNSAT.

---

## 🧪 Heuristics Implemented

- **VSIDS (Variable State Independent Decaying Sum)**  
  Prioritizes literals based on conflict involvement. Updated each cycle.

- **First UIP (Unique Implication Point)**  
  Used for efficient clause learning and backjumping after conflicts.

- **Clause Forgetting**  
  Deletes learned clauses that are 3x longer than the average clause length every 15 iterations.

---

## 🔍 Other Features

- **Two-Watched Literals Propagation**: Efficient unit propagation method.
- **Proof Generation (for UNSAT)**: Tracks clause derivations in a dictionary.
- **Output Files**: For each input, an output file is saved with the result and runtime.

---

## 📊 Performance

| File Name       | Result | Time (s)         |
|-----------------|--------|------------------|
| uf20-08.cnf     | SAT    | 0.00534          |
| uuf50-013.cnf   | UNSAT  | 0.74535          |
| uuf100-03.cnf   | UNSAT  | 164.39224        |
| uf125-05.cnf    | SAT    | 1084.30888       |
| uf100-02.cnf    | SAT    | 54.09852         |

> Output files are saved in the `output` folder as `{input_file}_output.txt`.

---

## 🧪 Experimental Notes

- Performance does **not scale linearly** with problem size.
- Solver performs well for small and mid-size instances.
- Execution time may grow **exponentially** for larger problems.
- In very large cases, execution had to be manually interrupted due to long runtimes.

---

## 💡 Reflections

This project was built entirely from scratch as a personal challenge. Early versions used simple heuristics based on literal frequency. As understanding of CDCL deepened, VSIDS and 1UIP heuristics were introduced, drastically improving performance and decision quality. While not the most optimized solver, it was a significant step forward in understanding automated reasoning, conflict analysis, and SAT solving.

---

## 📁 How to Use

1. Clone the repository
2. Run the main script:
   ```bash
   python cdcl_solver.py
