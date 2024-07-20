# Multi Agent Retirement Planning: CrewAI Implementation

## Guide
This implementation showcases the potential of multi-agent solutions in Fintech, specifically through the utilization of CrewAI, in the context of retirement planning.

### Assets
Important to note is that this system utilizes an assets folder to retrieve information. In order for this implementation to function, the following, or a similar structure if adjustments are made, is required:
```
.
└── assets/
    ├── mock-customers/
    │   └── John_Doe.txt
    └── RAG-sources/
        ├── concessional-contributions-cap.txt
        ├── industry-average-performance-return.txt
        ├── non-concessional-contributions.txt
        ├── restrictions-on-voluntary-contributions.txt
        ├── superannuation-account-balances.txt
        └── understanding-contributions.txt
```
### Installation
```sh
pip install -r requirements.txt # Installing required packages
cp .sample.env .env # Copying the sample file
nano .env # Or any other text editor to add an OpenAI API key
python crew.py # Start the crew
```
