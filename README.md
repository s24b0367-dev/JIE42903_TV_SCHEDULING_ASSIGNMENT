# JIE42903 TV Scheduling – Genetic Algorithm

## Run on a MacBook Air

1. Unzip the project and open **Terminal** (Applications → Utilities → Terminal).
2. Navigate into the extracted folder using `cd` (you can type `cd ` and drag the folder into Terminal).
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

4. Open the local address shown in Terminal, normally http://localhost:8501.
5. Adjust parameters and click **Run all three trials**.
6. To stop the server, press Ctrl+C in Terminal.

## Dataset modifications

The file `ratings_changes.csv` documents all six modifications to the original ratings. These are *illustrative assumptions*, not empirically verified audience changes. The original CSV is preserved separately.

## Algorithm and limitations

- Each chromosome contains **18 program names**, one per hour from 06:00 through 23:00, and repeats are permitted. The original tutorial instead starts from 10-program permutations, so this is an explicit design change to fill all 18 slots.
- Fitness = sum of ratings for the selected program at each corresponding time slot. Higher is better.
- Initial population is randomized, tournament selection chooses parents, one-point crossover recombines schedules, mutation replaces one randomly chosen program, and elitism preserves the best candidates.
- Mutation probability applies **once per child** (not once per gene), matching the tutorial's general approach.
- Trials use a common random seed, population size, and generation count. To make statistical claims, repeat across several seeds and report mean and standard deviation.
- The assignment contradicts itself about mutation: default 0.2 versus allowed range 0.01–0.05. The app uses 0.02 and the specified range pending lecturer clarification.
- The reported fitness is a total predicted audience rating, **not** a runtime measurement or a proof of global optimality.

## Deployment

Create a GitHub repository, upload `app.py`, `ga.py`, `requirements.txt`, `program_ratings_modified.csv`, and optionally the README and changes log. In Streamlit Community Cloud, select the repository, branch and `app.py` as the entry point. Copy the deployed app URL into the report appendix. Do not claim the app is deployed until you have tested its live URL.

## Suggested report structure

1. Introduction and objective
2. Dataset and documented changes (`ratings_changes.csv`)
3. GA methodology (chromosome, fitness, selection, crossover, mutation, elitism)
4. Streamlit interface (screenshots and controls)
5. Three trials (settings, full schedule tables, fitness results)
6. Discussion (differences, convergence, trade-offs, limitations)
7. Conclusion
8. Appendix (GitHub repository and deployed Streamlit links)
