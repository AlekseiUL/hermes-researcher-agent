# Source-bound regression benchmark v1

All inputs are synthetic. URLs under example.invalid are identifiers, not fetched sources.

Run `python3 -m unittest discover -s tests -p test_behavioral_contract.py -v`. This tests the scorer against reference annotations and deliberately bad outputs. It does NOT execute the prompt pack or establish model quality, factual truth, clinical validity, publication readiness or an A/B uplift. Model evaluation: NOT_RUN.

For an actual evaluation, supply the case request and source texts to a separately authorized pinned model runner; save raw output, prompt/package SHA and runner/model/settings, then have a blinded reviewer normalize the artifact into the annotation contract. Preserve exact source URLs in the raw artifact, assess prose quality and completeness manually, and grade the annotation with `grade(case, output)`. Never substitute the golden annotations for observed model outputs.
