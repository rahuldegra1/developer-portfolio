# 🐍 Python Foundations

My programming work while pursuing an Online BCA at Manipal University Jaipur, built alongside a self-directed 3-year roadmap toward becoming an AI/ML engineer. Started August 2026.

This repository documents my progression from basic terminal scripts to object-oriented programming, local data science pipelines, classical machine learning models, local LLM/image inference engines, and live cloud-deployed web applications.

**Tech Stack:** Python 3, Flask, SQLite, Pandas, Scikit-Learn, Matplotlib, REST APIs (`requests`), Local Inference (`llama.cpp` / GGUF / Ollama), HTML/CSS, Git, Render (Cloud Hosting).

---

## 🤖 Local AI & Machine Learning Systems

### 1. Local AI Decision Router & Code Engine (`LLM/`)
* **What it does:** A lightweight local inference server built with PyTorch and FastAPI running on a local RTX 5050. It routes developer tasks and code refactoring workflows through quantized `Qwen2.5-Coder-3B-Instruct` (GGUF Q4_K_M) using dedicated API endpoints (`/v1/choice`, `/v1/generate_code`) with an expanded 16k context window.
* **Why I built it:** To master local GPU resource allocation, ChatML token structures, and local model quantization without relying on cloud APIs. Downsized from 7B to an optimized 3B Coder model to maximize inference speed and VRAM overhead for multi-stage retrieval workflows.
* **What I'd do differently:** Implement token streaming via Server-Sent Events (SSE) and hook into a local vector store for codebase-wide RAG retrieval.

### 2. Local Image Generation Pipeline
* **What it does:** An isolated, local diffusion pipeline running Fooocus and SDXL Lightning checkpoints on the RTX 5050 to generate high-resolution $1024 \times 1024$ image assets in 4–8 sampling steps.
* **Why I built it:** To benchmark local latent diffusion performance and explore offline multimodal generation workflows alongside the core text LLM server.

### 3. California Housing Price Predictor (Year 1 Capstone)
* **What it explored:** An earlier course project covered housing-price regression, geographic visualization, feature analysis, and Mean Squared Error. Its source script and dataset are not included in the current repository.
* **Why I built it:** To graduate from basic binary classification to continuous regression, satisfying my Year 1 Capstone requirement by handling advanced feature correlation and descriptive statistics.
* **What I'd do differently:** Swap the Linear Regression model for an ensemble Random Forest Regressor to capture non-linear geographical interactions.

---

## 🌐 Live Cloud Applications
*These full-stack web applications were built using Flask, styled with HTML/CSS, backed by SQLite databases, and deployed live to the public internet via Render.*

### 1. Financial Expense Tracker ([Live Demo](https://financial-expense-tracker-55kv.onrender.com))
* **What it does:** A production-ready financial dashboard that captures user expenses via HTML forms, permanently stores them in a cloud SQLite database, and dynamically calculates totals using Pandas (`df['amount'].sum()`).
* **Why I built it:** To synthesize database architecture (with automatic `init_db()` table generation), backend computation, and automated cloud deployment via GitHub CI/CD into a cohesive product.
* **What I'd do differently:** Group expenses by category (`.groupby()`) and render visual breakdowns directly on the frontend.

### 2. Global Weather App ([Live Demo](https://global-weather-app-uv6x.onrender.com))
* **What it does:** A cloud-deployed web app chaining two Open-Meteo REST APIs. It intercepts city searches, queries a Geocoding API to resolve coordinates, routes those into a Forecast API, and renders live temperatures on a dark-mode frontend.
* **Why I built it:** To transition from local datasets to external third-party API integration with dynamic query handling and URL injection. Initial testing monitored Tokyo conditions ahead of my first step to Japan.
* **What I'd do differently:** Add a 5-day forecast carousel below the live reading.

### 3. Client Data Dashboard
* **What it does:** A web application running on Flask connected to a local SQLite database (`client_data.db`) executing full CRUD operations with dynamic HTML table rendering.
* **Why I built it:** To learn dynamic URL parameter routing (`@app.route`) and HTTP request parsing (`POST`).
* **What I'd do differently:** Implement session-based authentication to guard administrative mutations.

---

## 🖥️ Core Python Projects (Terminal & CLI)

<details>
<summary><strong>Object-Oriented Programming (OOP) & Architecture</strong></summary>

* **Capstone Notes App Backend (`models.py`):** Structured domain entities with strict instance encapsulation, alternative constructors (`@classmethod`) for JSON payload ingestion, and `@staticmethod` utility validation.
* **Bank Account Simulation:** An `Account` class modeling balance state, transaction ledgers, and overdraft protection, extended by a `SavingAccount` subclass via inheritance.
* **To-Do List Manager:** CLI application utilizing stateful classes to manage nested item states and status toggles.
</details>

<details>
<summary><strong>Applied Mathematics & Probability</strong></summary>

* **Monty Hall Simulation:** Programmatic verification of conditional probability, proving statistical advantage across thousands of simulated runs.
* **Periodic Table Data Parser:** Parses structured `.csv` scientific data into dictionary lookups for fast retrieval.
</details>

<details>
<summary><strong>APIs & External Data</strong></summary>

* **User Lookup Tool:** Dynamically fetches and parses live JSON data from external REST endpoints using `requests`.
* **Dynamic Quiz App:** Ingests external question banks via `csv.DictReader` to manage game-state logic in the terminal.
* **Contact Book:** Flat-file serialization project persisting structured dictionary records to local storage.
</details>

---

## 🧩 Data Structures & Algorithms (LeetCode)

| # | Problem | Pattern / Approach | Complexity |
|---|---------|-------------------|------------|
| 001 | Two Sum | Hash Map (Single Pass) | $O(n)$ Time, $O(n)$ Space |
| 003 | Longest Substring Without Repeating Characters | Dynamic Sliding Window + Hash Set | $O(n)$ Time, $O(k)$ Space |
| 009 | Palindrome Number | Modulo / Floor Division (No string conversion) | $O(\log n)$ Time, $O(1)$ Space |
| 011 | Container With Most Water | Two Pointers (Greedy Inward) | $O(n)$ Time, $O(1)$ Space |
| 014 | Longest Common Prefix | Horizontal Scanning / String Slicing | $O(S)$ Time, $O(1)$ Space |
| 015 | 3Sum | Sorting + Two Pointers (Deduplicated) | $O(n^2)$ Time, $O(1)$ Space |
| 020 | Valid Parentheses | Stack (LIFO) + Matching Hash Map | $O(n)$ Time, $O(n)$ Space |
| 039 | Combination Sum | Backtracking DFS with Element Reuse | $O(2^t)$ Time |
| 046 | Permutations | Backtracking DFS (Path Permutations) | $O(n \cdot n!)$ Time |
| 078 | Subsets | Backtracking DFS (Include / Exclude Decision Tree) | $O(n \cdot 2^n)$ Time |
| 079 | Word Search | Backtracking DFS on 2D Matrix (In-place Visited Marker) | $O(m \cdot n \cdot 4^L)$ Time |
| 121 | Best Time to Buy and Sell Stock | Sliding Window (Two Pointers / Running Minimum) | $O(n)$ Time, $O(1)$ Space |
| 125 | Valid Palindrome | Two Pointers (Inward Convergence) | $O(n)$ Time, $O(1)$ Space |
| 131 | Palindrome Partitioning | Backtracking DFS + Substring Palindrome Check | $O(2^n \cdot n)$ Time |
| 150 | Evaluate Reverse Polish Notation | Stack Evaluation (Operand Push, Operator Pop) | $O(n)$ Time, $O(n)$ Space |
| 155 | Min Stack | Auxiliary Min-Stack Tracking Running Minimum | $O(1)$ Operations, $O(n)$ Space |
| 167 | Two Sum II (Sorted Array) | Two Pointers (Opposite Ends) | $O(n)$ Time, $O(1)$ Space |
| 206 | Reverse Linked List | Iterative 3-Pointer Reversal (`prev`, `curr`, `next`) | $O(n)$ Time, $O(1)$ Space |
| 217 | Contains Duplicate | Hash Set (Early Exit) | $O(n)$ Time, $O(n)$ Space |
| 226 | Invert Binary Tree | Recursive Depth-First Search (Node Swap) | $O(n)$ Time, $O(h)$ Space |
| 242 | Valid Anagram | Frequency Counter Hash Map | $O(n)$ Time, $O(1)$ Space |
| 347 | Top K Frequent Elements | Hash Map Frequency + Bucket Sort / Min-Heap | $O(n)$ Time, $O(n)$ Space |
| 509 | Fibonacci Number | Iterative DP / Base-Case Recursion | $O(n)$ Time, $O(1)$ Space |
| 704 | Binary Search | $O(\log n)$ Midpoint Elimination | $O(\log n)$ Time, $O(1)$ Space |
| 933 | Number of Recent Calls | Sliding Queue (FIFO via `collections.deque`) | $O(1)$ Amortized Time |

*Note: All implementations are logged in the repository alongside complexity analyses and pattern reflections.*

---

## 🧠 Core Skills Demonstrated

* **Local Machine Learning & LLM Systems:** Quantized GGUF inference serving, prompt formatting, local GPU hardware management (RTX 5050), and diffusion setup.
* **Data Science & ML:** Scikit-Learn regression pipelines, MSE metric validation, exploratory data analysis with Pandas, and data visualization via Matplotlib.
* **Full-Stack Backend Development:** Flask application architecture, RESTful routing, request payload parsing, and templating.
* **Database Design:** Schema initialization, transactional consistency, relational table modeling, and raw SQL CRUD execution.
* **Algorithmic Problem Solving:** Linear data structures (Stacks, Queues, Linked Lists), Trees, Two-Pointer technique, Sliding Window, and Backtracking DFS recursion.

---

## 🔜 Coming Next
* **Capstone Notes App Full-Stack Release:** Completing authentication, relational foreign key mappings, and integrating local Qwen 3B API routes for automated note summarization.
* **Advanced Algorithmic Patterns:** Monotonic stacks (`Daily Temperatures`), tree traversals, and dynamic programming.
* **Database Scaling:** Migrating from SQLite to PostgreSQL with connection pooling and schema migrations.
