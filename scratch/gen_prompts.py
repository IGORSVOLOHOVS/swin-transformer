import os

prompts = [
    (
        "01-requirements.md",
        "Requirement Extraction & ISO 25010 Profiling",
        "Analyze the user request and extract functional and non-functional requirements. Profile the software based on ISO 25010 Quality Characteristics (Performance, Reliability, Security, Maintainability).",
    ),
    (
        "02-adr.md",
        "Architectural Decision Record (ADR)",
        "Document a critical architectural decision using the MADR template. Explain the context, options considered, and the final justification based on quality attribute trade-offs.",
    ),
    (
        "03-c4-modeling.md",
        "C4 System Modeling",
        "Create Mermaid.js diagrams for C4 Level 1 (System Context), Level 2 (Container), and Level 3 (Component). Focus on boundaries and communication protocols.",
    ),
    (
        "04-skeleton.md",
        "Technical Skeleton & Config",
        "Generate the project structure and primary configuration files (CMakeLists.txt or pyproject.toml). Ensure strict linting and build standards are initialized.",
    ),
    (
        "05-ddd-modeling.md",
        "Domain-Driven Design Modeling",
        "Identify Value Objects, Entities, and Aggregates. Define the Ubiquitous Language and Bounded Contexts for the core domain.",
    ),
    (
        "06-api-contracts.md",
        "API & Contract Design",
        "Design the public interface/API. Focus on header-only definitions (C++) or abstract base classes (Python) to establish strict contracts before implementation.",
    ),
    (
        "07-docker-ci.md",
        "Docker & CI Pipeline",
        "Create a multi-stage Dockerfile and a GitHub Actions / GitLab CI pipeline. Focus on reproducible builds and automated quality gates.",
    ),
    (
        "08-testing-infra.md",
        "Testing Infrastructure Setup",
        "Configure the testing framework (doctest or pytest). Set up mock objects, test fixtures, and coverage measurement tools.",
    ),
    (
        "09-functional-core.md",
        "Atomic Functional Core",
        "Implement the core business logic as a set of pure, stateless functions. Avoid side effects and ensure maximum testability.",
    ),
    (
        "10-monadic-errors.md",
        "Monadic Error Flow",
        "Integrate `std::expected` (C++) or Result patterns (Python) into the logic. Ensure all error paths are handled explicitly without exceptions.",
    ),
    (
        "11-concurrency-state.md",
        "Concurrency & Message Passing",
        "Implement state management using the Actor Model or Message Passing. Avoid shared-state mutexes in favor of thread isolation.",
    ),
    (
        "12-imperative-shell.md",
        "Imperative Shell & Adapters",
        "Implement adapters for external systems (Database, Network, File System). Ensure isolation from the Functional Core.",
    ),
    (
        "13-observability.md",
        "Structured Logging & Telemetry",
        "Integrate structured logging and performance telemetry. Ensure every major event is traceable and measurable.",
    ),
    (
        "14-perf-baselines.md",
        "Performance Budgeting",
        "Establish performance budgets and baselines for critical paths using micro-benchmarking tools (nanobench or pytest-benchmark).",
    ),
    (
        "15-optimization.md",
        "High-Performance Honing",
        "Analyze and optimize critical paths for cache locality, SIMD utilization, or algorithmic complexity.",
    ),
    (
        "16-security-audit.md",
        "Comprehensive Security Audit",
        "Run static and dynamic security scans (Bandit, Sanitizers). Audit for common vulnerabilities (OWASP, Buffer Overflows, Python Injection).",
    ),
    (
        "17-lint-cleanup.md",
        "Technical Debt & Smells Audit",
        "Identify and resolve code smells, duplication, and technical debt. Ensure strict adherence to the project's Clean Code rules.",
    ),
    (
        "18-modernization.md",
        "Language Standard Upgrade",
        "Verify that the codebase fully utilizes the latest language features (C++23 Ranges/Concepts or Python 3.12+ type features).",
    ),
    (
        "19-docs-auto.md",
        "Automated API Documentation",
        "Generate professional API documentation (Doxygen or pdoc). Ensure all public interfaces are fully documented with examples.",
    ),
    (
        "20-readme-crafting.md",
        "User-Centric Documentation",
        "Write high-quality READMEs, Tutorials, and Installation guides. Focus on the user experience and clear onboarding.",
    ),
    (
        "21-validation.md",
        "Full Validation Sweep",
        "Run the complete verification suite (Format -> Lint -> Test -> Build). Ensure zero regressions before merging.",
    ),
    (
        "22-compliance.md",
        "Licensing & Standards Audit",
        "Audit for license compliance (OSS scanners) and adherence to industry standards (MISRA, PEP8, ISO).",
    ),
    (
        "23-packaging.md",
        "Distribution Artifact Generation",
        "Configure packaging (Conan, CPack, or Wheels). Build and verify final distributable artifacts.",
    ),
    (
        "24-release-prep.md",
        "Release & Changelog Automation",
        "Generate a detailed changelog and release notes. Automate version tagging and deployment notifications.",
    ),
    (
        "25-handoff.md",
        "Final Project Handoff",
        'Perform a deep "Brain Extraction" of the entire project status. Provide a comprehensive summary for the next maintenance session.',
    ),
]

output_dir = "workflow_prompts"
os.makedirs(output_dir, exist_ok=True)

for filename, title, content in prompts:
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Prompt: {title}\n{content}\n")
    print(f"Created {filepath}")

print("\nSummary Table:")
print("| Stage | File | Title |")
print("|-------|------|-------|")
for i, (filename, title, _) in enumerate(prompts, 1):
    print(f"| {i:02} | `{filename}` | {title} |")
