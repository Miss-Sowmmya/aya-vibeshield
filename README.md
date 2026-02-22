Aya VibeShield

AI Transaction Co-Pilot for proactive wallet risk intelligence.

Aya VibeShield is a fintech security prototype that analyzes blockchain transactions before execution and provides real-time risk insights using heuristic AI logic. The system is designed as a pre-transaction intelligence layer for multi-chain wallet ecosystems.



Overview

Aya VibeShield helps users evaluate the safety of a transaction before sending funds. It combines a clean fintech interface with an explainable risk engine and a visual trust graph.

The project demonstrates how AI can act as a transaction co-pilot to improve user safety in Web3 environments.



Key Features

AI-based transaction risk scoring

Beginner and Expert explanation modes

Interactive trust graph visualization

Live threat intelligence side panel

Dark-gold premium fintech UI

Responsive three-column layout

Lightweight heuristic backend



Tech Stack

Python 3.11

Streamlit

NetworkX

PyVis

HTML/CSS (custom fintech theme)



Project Structure
.
├── app.py
├── requirements.txt
├── .replit
├── replit.nix
└── README.md
Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/aya-vibeshield.git
cd aya-vibeshield



Install dependencies:

pip install -r requirements.txt
Run Locally
streamlit run app.py

The app will be available at:

http://localhost:8501
How It Works

User enters wallet address and transaction amount

Heuristic engine evaluates risk signals

Risk score (0–100) is generated

AI explanation is shown based on user mode

Trust graph visualizes transaction flow

Live intel panels simulate monitoring environment

Risk Engine Logic

The current prototype uses heuristic signals:

transaction size

wallet format pattern

address length anomaly

These signals are combined into a bounded risk score.

Note: This is a simulation prototype and not financial advice.

Deployment

The app is configured for deployment using Streamlit.

Replit deployment command:

streamlit run app.py --server.port 3000 --server.address 0.0.0.0
Future Improvements

Real blockchain data integration

Smart contract risk scanning

Wallet reputation scoring

Multi-chain support expansion

Real-time gas anomaly detection

ML-based risk model

AI Assistance (Prompt Context)

The following high-level AI assistance was used during development:

UI refinement prompts for fintech dark-gold theme

Streamlit layout optimization guidance

PyVis graph stabilization tuning

Three-column responsive layout design

Side intelligence panel concept generation

Risk explanation wording refinement

All final code was reviewed and manually integrated.

Author

Sowmmya G
IT Student | Fintech & AI Enthusiast

License

This project is for educational and hackathon demonstration purposes.
