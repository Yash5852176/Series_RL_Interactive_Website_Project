# Series RL Circuit — Interactive Transient Lab

A shareable Streamlit website for a Semester III Physics assignment.

**Student:** Yash Montu Yadav  
**USN:** 25BSR00210  
**Date:** 23 October 2026

## Features
- Interactive voltage, resistance, target time constant, and duration controls
- Live RL transient-response graph
- Calculated inductance for selected time constant
- Fitted analysis of the transcribed lab measurements
- R² fit metric and data table
- CSV downloads for simulated and fitted data
- Theory, equations, and reproducibility notes

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish as a website
1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository, branch, and `app.py`.
4. Deploy and copy the public app URL.
5. Add that real URL to your PDF. Do not use a placeholder URL.

The site is an ideal-model simulation using transcribed observations. Verify the lab instrument units and actual component values before interpreting the fitted inductance physically.
