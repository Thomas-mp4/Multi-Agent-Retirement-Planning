# Multi Agent Retirement Planning: CrewAI Implementation
**This repository is for educational purposes only.** 
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
The content of the files in the `mock-customers` simulate customer data, with the following format:
```
Name: ...
Age: ...
Sex: ...
Current Balance: ... 
Contributions Made: ...
Performance return for 2022-2023: ...
Performance return for 2021-2022: ...
```

The content of the files in the `RAG-sources` folder are derived from publicly available sources, copied using a modern web browser to plain text files.

### Results
The `results` folder contains outputs from the system, showcasing the potential of multi-agent solutions.

### Installation
(Python 3.10)
```sh
pip install -r requirements.txt # Installing required packages
cp .sample.env .env # Copying the sample file
nano .env # Or any other text editor to add an OpenAI API key
python crew.py # Start the crew
```