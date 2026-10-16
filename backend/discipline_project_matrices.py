"""
SkillBridge AI - Additional 10-Project Production Matrices.
Provides 10 comprehensive, industry-grade project blueprints (2 Beginner, 4 Intermediate, 4 Advanced)
for the remaining 6 core engineering disciplines:
  1. Data Engineering & Lakehouses (data_engineering)
  2. Machine Learning & MLOps (ml_engineering)
  3. Mobile Application Engineering (mobile_dev)
  4. Embedded Systems & Firmware (embedded_systems)
  5. Blockchain & Web3 Protocols (blockchain_web3)
  6. Fullstack General Engineering (fullstack_general)
"""

from typing import Dict, List, Any

ADDITIONAL_PROJECT_MATRICES: Dict[str, List[Dict[str, Any]]] = {
    # -------------------------------------------------------------------------
    # 1. Data Engineering & Lakehouses (10 Projects)
    # -------------------------------------------------------------------------
    "data_engineering": [
        # Beginner 1
        {
            "id": "de-beg-01",
            "title": "Automated Batch ETL Ingestion Pipeline with PySpark, Delta Lake & Parquet",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "Apache Spark", "SQL", "Docker", "Linux"],
            "non_tech_competencies": ["Data Modeling", "Schema Validation", "ETL Best Practices", "Git Hygiene"],
            "executive_summary": "Raw data ingestion without schema enforcement produces downstream analytics failures. This batch ETL pipeline ingests multi-source CSV/JSON feeds, enforces ACID transactions with Delta Lake, and outputs optimized partitioned Parquet tables.",
            "architecture_summary": "PySpark batch processing pipeline reading raw staged files, applying typed schema validations, and persisting partitioned tables to a local Delta Lake storage directory.",
            "key_features": [
                "Typed schema enforcement rejecting malformed records to a dead-letter quarantine table",
                "Automated data partition pruning by ingestion date and region for high query performance",
                "ACID transactional writes with Delta Lake time-travel and rollback capabilities",
                "Automated pytest test suite verifying transformation logic on synthetic sample datasets"
            ],
            "roadmap": [
                "Milestone 1: PySpark session setup and raw data ingestion schema contracts",
                "Milestone 2: Data cleaning, null handling, and type-casting transformation functions",
                "Milestone 3: Delta Lake table persistence with date-based column partitioning",
                "Milestone 4: Data validation assertions with Great Expectations and pytest fixtures"
            ],
            "industry_rubric": "Evaluates understanding of distributed data partitions, avoiding Cartesian joins, data type safety, and clean pipeline modularity."
        },
        # Beginner 2
        {
            "id": "de-beg-02",
            "title": "Relational Change Data Capture (CDC) Pipeline with Debezium & PostgreSQL",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["SQL", "PostgreSQL", "Docker", "Python", "Git"],
            "non_tech_competencies": ["CDC Architecture", "Write-Ahead Logging", "Data Synchronization"],
            "executive_summary": "Batch database dumps overload production systems and introduce hours of data lag. This service streams row-level changes from PostgreSQL write-ahead logs (WAL) in real-time to maintain low-latency analytics replicas.",
            "architecture_summary": "Change Data Capture pipeline reading PostgreSQL logical replication slots via Debezium and streaming INSERT/UPDATE/DELETE events into an audit store.",
            "key_features": [
                "PostgreSQL logical decoding configuration capturing full before/after row states",
                "Automated schema change tracking handling table alter events without downtime",
                "Idempotent event consumer recording audit trails with monotonic sequence numbers",
                "Containerized local Docker Compose harness running Postgres, Kafka, and consumer service"
            ],
            "roadmap": [
                "Milestone 1: PostgreSQL WAL replication slot and test table setup",
                "Milestone 2: Debezium connector configuration and event capture",
                "Milestone 3: Python consumer applying change deltas to an audit warehouse",
                "Milestone 4: Verification tests verifying zero dropped updates under burst write traffic"
            ],
            "industry_rubric": "Evaluates understanding of database replication internals, WAL mechanics, at-least-once delivery handling, and containerized integration testing."
        },
        # Intermediate 1
        {
            "id": "de-int-01",
            "title": "Real-Time Event Stream Ingestion Engine with Apache Kafka & ClickHouse",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "Apache Kafka", "SQL", "Docker", "PostgreSQL"],
            "non_tech_competencies": ["Stream Processing", "Columnar Database Design", "Backpressure Handling"],
            "executive_summary": "High-velocity telemetry and clickstream feeds require sub-second ingestion into analytical data stores. This service processes continuous Kafka event streams and batches them into ClickHouse columnar storage for real-time aggregation.",
            "architecture_summary": "Distributed event consumer using Python Kafka client, async micro-batching, and vectorized inserts into ClickHouse MergeTree tables.",
            "key_features": [
                "Dynamic micro-batching buffer maximizing ClickHouse write throughput (100k events/sec)",
                "Dead-letter queue (DLQ) isolation for corrupted JSON payloads without halting stream consumption",
                "ClickHouse ReplacingMergeTree engine for deduplicating repeated event IDs",
                "Prometheus metrics exporting consumer lag, ingestion throughput, and batch commit latency"
            ],
            "roadmap": [
                "Milestone 1: Kafka multi-partition topic design and mock event generator",
                "Milestone 2: Asynchronous batching consumer with graceful shutdown handling",
                "Milestone 3: ClickHouse schema design with column compression and sorting keys",
                "Milestone 4: Chaos test validating consumer group recovery after simulated worker crash"
            ],
            "industry_rubric": "Evaluates understanding of stream offsets, consumer lag management, columnar storage tuning, and resilient error recovery."
        },
        # Intermediate 2
        {
            "id": "de-int-02",
            "title": "Modern Data Stack Analytics Pipeline with dbt Core, DuckDB & Dagster",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["dbt", "SQL", "Python", "Git", "Docker"],
            "non_tech_competencies": ["Data Lineage", "DAG Scheduling", "Data Quality Testing"],
            "executive_summary": "Spaghetti SQL scripts cause conflicting analytics metrics across business teams. This project implements a modular dbt transformation DAG with lineage tracking, automated schema testing, and Dagster orchestration.",
            "architecture_summary": "Multi-tier dbt project (Staging -> Intermediate -> Marts) executed against embedded DuckDB and orchestrated via Dagster software-defined assets.",
            "key_features": [
                "Kimball dimensional modeling with Star Schema Fact and Dimension tables",
                "Automated dbt generic and singular tests verifying unique keys, not-null, and referential integrity",
                "Incremental model strategies reducing warehouse compute costs by 80%",
                "Interactive documentation and interactive data lineage graph visualization"
            ],
            "roadmap": [
                "Milestone 1: Raw data staging models with standardized column renaming and casting",
                "Milestone 2: Intermediate dimensional models with business logic joins and deduplication",
                "Milestone 3: Fact table marts and aggregated reporting views with dbt tests",
                "Milestone 4: Dagster pipeline automation with asset-based scheduling and Slack alerts"
            ],
            "industry_rubric": "Evaluates clean SQL modeling practices, avoidance of circular dependencies, comprehensive test assertions, and clear documentation."
        },
        # Intermediate 3
        {
            "id": "de-int-03",
            "title": "High-Throughput Distributed Data Warehouse Loader for Snowflake with S3 Staging",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["SQL", "Python", "Snowflake", "AWS", "Docker"],
            "non_tech_competencies": ["Cloud Economics", "Data Staging Architecture", "Idempotent Loading"],
            "executive_summary": "Ad-hoc database loading wastes expensive warehouse compute credits and creates lock contention. This engine stages compressed parquet files to Amazon S3 and executes bulk COPY INTO commands with transactional guarantees.",
            "architecture_summary": "Automated warehouse loading service leveraging S3 external stages, Snowpipe notifications, and idempotent COPY queries with error tracking.",
            "key_features": [
                "Gzip-compressed Parquet chunking optimized for Snowflake file size guidelines (100MB-250MB)",
                "Idempotent load verification checking load history tables to prevent duplicate records",
                "Automated warehouse suspend/resume management minimizing idle cloud compute costs",
                "Validation mode verification checking data syntax before executing live warehouse mutations"
            ],
            "roadmap": [
                "Milestone 1: Cloud storage staging pipeline and IAM policy least-privilege configuration",
                "Milestone 2: Snowflake external stage and target dimension/fact table DDL setup",
                "Milestone 3: Automated Python loading script executing COPY INTO with pattern matching",
                "Milestone 4: Load audit logging and automated validation error alert reporting"
            ],
            "industry_rubric": "Evaluates understanding of cloud data warehouse billing dynamics, external stage security, and bulk loading performance optimization."
        },
        # Intermediate 4
        {
            "id": "de-int-04",
            "title": "Automated Data Quality & Schema Drift Sentinel with Great Expectations & Slack Alerts",
            "difficulty": "Intermediate",
            "hours": 22,
            "primary_skills": ["Python", "SQL", "PostgreSQL", "Docker", "Git"],
            "non_tech_competencies": ["Data Observability", "Incident Management", "SLA Monitoring"],
            "executive_summary": "Silent schema alterations and unexpected null spikes pollute executive dashboards before engineers notice. This sentinel monitors database tables, evaluates statistical profiling suites, and dispatches webhook alerts upon breach.",
            "architecture_summary": "Scheduled data observability daemon executing Great Expectations validation suites against PostgreSQL and publishing Slack incident webhooks.",
            "key_features": [
                "Automated schema drift detection flagging unexpected new columns, altered types, or dropped fields",
                "Statistical distribution assertions checking row count velocity, null fractions, and outlier bounds",
                "HTML data documentation report generation with clear visual pass/fail indicators",
                "Webhook incident dispatcher with severity rating (CRITICAL for schema breakage, WARN for drift)"
            ],
            "roadmap": [
                "Milestone 1: Data profiling suite setup and expectation suite authoring",
                "Milestone 2: Automated validation runner querying production replica tables",
                "Milestone 3: Rich HTML audit report compilation and S3 artifact publishing",
                "Milestone 4: Slack webhook integration with action buttons to acknowledge data incidents"
            ],
            "industry_rubric": "Evaluates understanding of data reliability engineering (DRE), proactive quality gates, and actionable alerting without alert fatigue."
        },
        # Advanced 1
        {
            "id": "de-adv-01",
            "title": "Apache Iceberg Lakehouse Engine with Trino Distributed SQL Query Optimization",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "Apache Spark", "SQL", "Docker", "AWS"],
            "non_tech_competencies": ["Open Table Formats", "Lakehouse Architecture", "Query Optimization"],
            "executive_summary": "Proprietary data warehouse lock-in incurs massive licensing costs. This lakehouse project implements an open Apache Iceberg table format with Trino distributed SQL query engine, hidden partitioning, and table maintenance.",
            "architecture_summary": "Lakehouse storage architecture utilizing Apache Iceberg metadata layers, Parquet data files on object storage, and Trino distributed query execution.",
            "key_features": [
                "Hidden partitioning and partition evolution without rewriting historical table data",
                "Iceberg metadata compaction and snapshot expiration job preventing small-file degradation",
                "Row-level mutations (ACID Merge / Upsert) using copy-on-write and merge-on-read strategies",
                "Trino distributed SQL query benchmarking comparing execution plans against traditional Hive tables"
            ],
            "roadmap": [
                "Milestone 1: Iceberg catalog (REST/Nessie) and local MinIO S3 object storage setup",
                "Milestone 2: PySpark Iceberg table creation with partition transform specifications",
                "Milestone 3: Trino distributed query engine integration and EXPLAIN ANALYZE tuning",
                "Milestone 4: Automated maintenance maintenance script executing expire_snapshots and rewrite_data_files"
            ],
            "industry_rubric": "Evaluates deep mastery of modern lakehouse storage formats, metadata manifests, distributed execution plans, and file compaction tradeoffs."
        },
        # Advanced 2
        {
            "id": "de-adv-02",
            "title": "Fault-Tolerant Real-Time Stream Enrichment Engine with Apache Flink & Redis",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Python", "Apache Kafka", "Redis", "Docker", "Linux"],
            "non_tech_competencies": ["Exactly-Once Semantics", "Stateful Stream Processing", "Event-Time Watermarks"],
            "executive_summary": "Fraud detection and real-time bidding require joining streaming transactions with fast user metadata under sub-50ms latencies. This stateful streaming engine uses Apache Flink with RocksDB state backend and exactly-once processing guarantees.",
            "architecture_summary": "Real-time stateful stream processing pipeline reading Kafka transaction streams, enriching with Redis caching, and emitting enriched analytics events.",
            "key_features": [
                "Event-time processing with bounded out-of-orderness watermarks handling late arriving events",
                "Keyed state management with asynchronous checkpointing to cloud storage",
                "Async I/O enrichment against Redis preventing stream worker thread blocking",
                "Two-phase commit sink guaranteeing exactly-once semantics end-to-end"
            ],
            "roadmap": [
                "Milestone 1: Flink cluster environment setup with Kafka source and sink connectors",
                "Milestone 2: Watermark strategy and tumbling window aggregation implementation",
                "Milestone 3: Async I/O Redis enrichment operator with circuit-breaker fallback",
                "Milestone 4: Chaos testing verifying checkpoint recovery after hard worker termination"
            ],
            "industry_rubric": "Evaluates understanding of stream processing theory (event-time vs processing-time, watermarks, chandy-lamport checkpointing), and high-throughput tuning."
        },
        # Advanced 3
        {
            "id": "de-adv-03",
            "title": "Multi-Tenant Data Mesh Access Governance & Column-Level Anonymization Gateway",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["SQL", "PostgreSQL", "Python", "Docker", "Git"],
            "non_tech_competencies": ["Data Governance & Mesh", "GDPR / DPDP Compliance", "Zero-Trust Data Access"],
            "executive_summary": "Centralized data teams become bottlenecks while exposing sensitive PII to broad analytical queries. This project constructs a federated Data Mesh access gateway enforcing column-level dynamic data masking and tenant isolation.",
            "architecture_summary": "Proxy access layer intercepting analytical SQL queries, verifying tenant RBAC tokens, and applying dynamic column-level cryptographic hashing on PII fields.",
            "key_features": [
                "Dynamic SQL AST parsing (via sqlglot) intercepting queries to inject tenant WHERE filters",
                "Cryptographic HMAC anonymization of sensitive columns (email, phone, SSN) preserving join capability",
                "Granular role-based view synthesis based on requester department and data clearance level",
                "Comprehensive audit log recording every column access timestamp for GDPR compliance"
            ],
            "roadmap": [
                "Milestone 1: Multi-tenant schema design with data classification tags (PII, Financial, Public)",
                "Milestone 2: SQL query parser intercepting queries and rewriting AST with security predicates",
                "Milestone 3: Dynamic masking functions returning pseudonymized values to unauthorized roles",
                "Milestone 4: Compliance penetration test verifying zero PII leakage under adversarial SQL queries"
            ],
            "industry_rubric": "Evaluates understanding of modern data governance, SQL AST manipulation, legal compliance (GDPR/DPDP), and zero-trust data architecture."
        },
        # Advanced 4
        {
            "id": "de-adv-04",
            "title": "Petabyte-Scale Cross-Region Data Lake Migration & Integrity Verification Framework",
            "difficulty": "Advanced",
            "hours": 40,
            "primary_skills": ["Python", "Apache Spark", "AWS", "SQL", "Docker"],
            "non_tech_competencies": ["Disaster Recovery", "Data Migration Strategy", "Cryptographic Checksums"],
            "executive_summary": "Migrating mission-critical data lakes across cloud regions or providers without downtime requires parallel batch transfers, delta catch-ups, and byte-level checksum verification.",
            "architecture_summary": "Distributed migration orchestrator coordinating parallel multipart object copy, change delta replay, and automated Merkle tree integrity verification.",
            "key_features": [
                "Multipart parallel transfer engine with automatic exponential backoff retry and rate limiting",
                "Cutover synchronization window minimizing downtime to under 5 minutes",
                "Distributed checksum verification comparing MD5 and row count hashes between source and target",
                "Automated rollback runbook with immediate cutback DNS redirection"
            ],
            "roadmap": [
                "Milestone 1: Source and target cloud storage inventory scanning and transfer sizing model",
                "Milestone 2: Parallel batch copy orchestrator with progress tracking and bandwidth throttling",
                "Milestone 3: Incremental change sync capturing writes that occurred during batch copy",
                "Milestone 4: Distributed row-by-row hash verification suite validating 100% data fidelity"
            ],
            "industry_rubric": "Evaluates enterprise migration planning, risk mitigation, data integrity math (checksums, Merkle trees), and zero-downtime cutover strategy."
        }
    ],

    # -------------------------------------------------------------------------
    # 2. Machine Learning & MLOps (10 Projects)
    # -------------------------------------------------------------------------
    "ml_engineering": [
        # Beginner 1
        {
            "id": "ml-beg-01",
            "title": "End-to-End Supervised Learning Pipeline with Scikit-learn, MLflow & FastAPI",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "Scikit-learn", "Pandas", "FastAPI", "pytest"],
            "non_tech_competencies": ["ML Experimentation", "Feature Engineering", "Model Evaluation"],
            "executive_summary": "Jupyter notebooks cannot serve live business traffic. This project converts an exploratory churn prediction notebook into a clean, reproducible production training and inference microservice with MLflow experiment tracking.",
            "architecture_summary": "Modular ML repository separating data preprocessing, model training, MLflow parameter logging, and FastAPI REST prediction endpoints.",
            "key_features": [
                "Scikit-learn ColumnTransformer pipeline for automated imputation, scaling, and one-hot encoding",
                "MLflow tracking logging hyperparameters, ROC-AUC curves, and serialized model artifacts",
                "FastAPI REST endpoint accepting candidate JSON payloads and returning prediction probabilities",
                "Automated unit test suite asserting prediction latency < 20ms and deterministic output"
            ],
            "roadmap": [
                "Milestone 1: Exploratory data analysis, baseline model training, and metric selection",
                "Milestone 2: Production preprocessing pipeline and MLflow experiment logging",
                "Milestone 3: FastAPI inference endpoint with strict Pydantic v2 input schemas",
                "Milestone 4: Test harness verifying boundary condition handling (nulls, unknown categories)"
            ],
            "industry_rubric": "Evaluates avoidance of data leakage between train/test splits, clean separation of training from serving, and robust input validation."
        },
        # Beginner 2
        {
            "id": "ml-beg-02",
            "title": "Automated Feature Preprocessing & Model Evaluation Suite with NumPy & Pandas",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "NumPy", "Pandas", "Scikit-learn", "Git"],
            "non_tech_competencies": ["Feature Engineering", "Statistical Metrics", "Code Hygiene"],
            "executive_summary": "Unchecked feature transformations lead to catastrophic production bias and silent accuracy drops. This library provides reusable, vectorized feature engineering transformers with automated statistical drift validation.",
            "architecture_summary": "Vectorized feature preprocessing library utilizing NumPy and Pandas with automated test fixtures asserting statistical invariants.",
            "key_features": [
                "Vectorized outlier capping (Winsorization) and target encoding with smoothing priors",
                "Automated cross-validation matrix computing Precision, Recall, F1, and PR-AUC scores",
                "Confusion matrix and calibration curve exporter for model error analysis",
                "Comprehensive pytest test suite asserting zero NaN values and shape consistency"
            ],
            "roadmap": [
                "Milestone 1: Vectorized custom transformer classes adhering to Scikit-learn API",
                "Milestone 2: K-Fold cross-validation harness with stratification for imbalanced data",
                "Milestone 3: Model diagnostic visualization generator (ROC, PR curves, calibration plots)",
                "Milestone 4: Unit test suite asserting numerical stability on edge case distributions"
            ],
            "industry_rubric": "Evaluates mathematical correctness, vectorized operations without inefficient Python loops, and prevention of target leakage."
        },
        # Intermediate 1
        {
            "id": "ml-int-01",
            "title": "Production PyTorch Deep Learning Classifier with ONNX Runtime & Docker",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "PyTorch", "Docker", "FastAPI", "pytest"],
            "non_tech_competencies": ["Model Optimization", "Deep Learning Lifecycle", "Inference Latency"],
            "executive_summary": "Raw PyTorch models in production consume excessive memory and suffer from high CPU latency. This project trains a neural network classifier, exports it to optimized ONNX format, and serves it with 4x lower latency.",
            "architecture_summary": "PyTorch training module exporting weights to ONNX format, served inside a lightweight Docker container utilizing ONNX Runtime CPU execution.",
            "key_features": [
                "Custom PyTorch neural network architecture with Dropout and Batch Normalization",
                "Automated ONNX graph export with static shape verification and numerical parity tests",
                "ONNX Runtime inference server yielding sub-10ms P99 latency on standard CPU instances",
                "Containerized Docker packaging minimizing image footprint to under 350MB"
            ],
            "roadmap": [
                "Milestone 1: PyTorch model architecture definition and training loop with learning rate scheduling",
                "Milestone 2: Model evaluation, early stopping checkpointing, and ONNX graph serialization",
                "Milestone 3: High-performance ONNX Runtime inference service in FastAPI",
                "Milestone 4: Latency benchmarking suite comparing native PyTorch vs ONNX execution"
            ],
            "industry_rubric": "Evaluates understanding of neural network training dynamics, graph optimization, inference engine selection, and container footprint reduction."
        },
        # Intermediate 2
        {
            "id": "ml-int-02",
            "title": "Real-Time Low-Latency Feature Store with Feast & Redis for Online Inference",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "Redis", "PostgreSQL", "Docker", "FastAPI"],
            "non_tech_competencies": ["Feature Store Architecture", "Point-in-Time Correctness", "Online/Offline Drift"],
            "executive_summary": "Training models on batch data while serving predictions on real-time features causes training-serving skew. This feature store maintains offline historical features in PostgreSQL and synchronizes online features to Redis.",
            "architecture_summary": "Feast feature store setup synchronizing batch features from PostgreSQL into Redis for sub-5ms low-latency feature vector retrieval.",
            "key_features": [
                "Point-in-time correct historical feature retrieval preventing future data leakage in training sets",
                "Ultra-fast online feature vector lookups via Redis pipelining (< 4ms P99)",
                "Automated feature synchronization job transferring batch aggregates to online storage",
                "Feature validation checks ensuring online features conform to declared schema types"
            ],
            "roadmap": [
                "Milestone 1: Offline PostgreSQL feature entity definition and batch aggregation queries",
                "Milestone 2: Feast feature store definition and Redis online store connector setup",
                "Milestone 3: Materialization pipeline syncing latest entity features to Redis",
                "Milestone 4: Real-time inference integration test asserting sub-5ms feature enrichment"
            ],
            "industry_rubric": "Evaluates understanding of training-serving skew, point-in-time correctness, feature store ergonomics, and low-latency caching."
        },
        # Intermediate 3
        {
            "id": "ml-int-03",
            "title": "Distributed Training Cluster with PyTorch DDP & Ray Train on Multi-GPU",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["Python", "PyTorch", "Docker", "Linux", "CUDA"],
            "non_tech_competencies": ["Distributed Systems", "GPU Memory Management", "Cluster Scheduling"],
            "executive_summary": "Training large modern deep learning models on a single GPU takes weeks. This project implements PyTorch DistributedDataParallel (DDP) orchestrated via Ray Train to scale model training linearly across worker nodes.",
            "architecture_summary": "Distributed training harness using PyTorch DDP and Ray Train coordinating gradient synchronization across multi-worker processes.",
            "key_features": [
                "All-Reduce gradient synchronization minimizing inter-worker communication overhead",
                "Distributed data sampling ensuring non-overlapping batch distribution across ranks",
                "Mixed-precision training (FP16 / BF16) cutting GPU memory consumption in half",
                "Automated checkpoint synchronization saving best model weights to persistent cloud storage"
            ],
            "roadmap": [
                "Milestone 1: Multi-process PyTorch DDP initialization and rank assignment logic",
                "Milestone 2: Distributed DataLoader configuration with DistributedSampler",
                "Milestone 3: Automatic Mixed Precision (torch.cuda.amp) integration and loss scaling",
                "Milestone 4: Ray Train cluster runner evaluating scaling efficiency across 2 to 4 workers"
            ],
            "industry_rubric": "Evaluates understanding of distributed training mechanics (Ring-AllReduce, rank, world size), GPU memory bandwidth, and gradient synchronization."
        },
        # Intermediate 4
        {
            "id": "ml-int-04",
            "title": "High-Throughput Model Serving Engine with Triton Inference Server & Dynamic Batching",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "Docker", "Linux", "FastAPI", "pytest"],
            "non_tech_competencies": ["Inference Serving", "Dynamic Batching", "Concurrency & SLA"],
            "executive_summary": "Serving deep learning models sequentially wastes massive compute hardware. This service configures NVIDIA Triton Inference Server with dynamic request batching to process 10x more queries per second within latency budgets.",
            "architecture_summary": "Microservice gateway querying NVIDIA Triton Inference Server via gRPC with dynamic batching queues and model version routing.",
            "key_features": [
                "Dynamic batching aggregation combining asynchronous client requests within 5ms windows",
                "Concurrent model execution instances maximizing GPU/CPU core utilization",
                "Dual backend support running ONNX and TensorRT model instances concurrently",
                "Health and readiness probes integrated into Kubernetes rolling deployment manifest"
            ],
            "roadmap": [
                "Milestone 1: Triton model repository configuration (config.pbtxt) with dynamic batching parameters",
                "Milestone 2: High-speed Python gRPC client communicating with Triton inference ports",
                "Milestone 3: Load generation benchmark measuring throughput vs latency tradeoffs",
                "Milestone 4: Prometheus metrics dashboard tracking request queue latency and batch size distributions"
            ],
            "industry_rubric": "Evaluates understanding of inference server architectures, gRPC vs REST latency, dynamic batching windows, and SLA enforcement."
        },
        # Advanced 1
        {
            "id": "ml-adv-01",
            "title": "Enterprise MLOps Automated Retraining & Data Drift Detection Pipeline with Evidently AI",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "PostgreSQL", "Docker", "FastAPI", "pytest"],
            "non_tech_competencies": ["Continuous Delivery for ML", "Data Drift Detection", "Automated Rollback"],
            "executive_summary": "Production machine learning models degrade over time as customer behavior changes (concept drift). This enterprise MLOps platform monitors prediction distributions, detects drift with statistical tests, and triggers automated retraining.",
            "architecture_summary": "Continuous ML feedback loop collecting live inference logs, running Kolmogorov-Smirnov drift tests via Evidently AI, and triggering automated pipeline execution.",
            "key_features": [
                "Statistical drift detection (Wasserstein Distance, KS-Test) comparing inference logs to training baseline",
                "Automated retraining trigger dispatched when target feature drift exceeds critical threshold",
                "Champion-Challenger shadow evaluation validating that the newly trained model beats the current production model",
                "Canary deployment orchestrator routing 5% of live traffic to challenger before full cutover"
            ],
            "roadmap": [
                "Milestone 1: Inference telemetry logger recording inputs, outputs, and confidence scores",
                "Milestone 2: Automated statistical drift detection engine generating HTML diagnostic reports",
                "Milestone 3: Champion vs Challenger evaluation harness scoring models on recent ground-truth data",
                "Milestone 4: Automated canary release state machine with automated rollback on accuracy regression"
            ],
            "industry_rubric": "Evaluates understanding of production ML decay, statistical distribution testing, zero-downtime model cutover, and automated rollback triggers."
        },
        # Advanced 2
        {
            "id": "ml-adv-02",
            "title": "Low-Latency Recommendation Engine with Two-Tower Neural Embeddings & Milvus",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Python", "PyTorch", "Redis", "Docker", "SQL"],
            "non_tech_competencies": ["Vector Search Architecture", "Two-Tower Recommenders", "Sub-15ms Latency"],
            "executive_summary": "Personalized content and e-commerce platforms must rank millions of items for millions of users in real time. This engine implements a Two-Tower (User Tower + Item Tower) neural embedding architecture with ANN vector indexing.",
            "architecture_summary": "Two-Tower neural recommendation model exporting user and item embeddings into Milvus vector database with Redis candidate caching.",
            "key_features": [
                "Dual deep learning encoders mapping user history and item attributes into shared 128-dim latent space",
                "Approximate Nearest Neighbor (ANN) HNSW indexing in Milvus returning top-100 candidates in < 8ms",
                "Contextual re-ranking layer adjusting final rankings based on real-time availability and diversity",
                "Offline evaluation pipeline calculating NDCG@10, Mean Reciprocal Rank (MRR), and Hit Rate"
            ],
            "roadmap": [
                "Milestone 1: Two-Tower model architecture definition and negative sampling training strategy",
                "Milestone 2: Milvus vector collection setup and item embedding batch ingestion",
                "Milestone 3: Real-time query endpoint encoding user context and executing vector ANN retrieval",
                "Milestone 4: Evaluation test suite verifying sub-15ms latency and high NDCG@10 scores"
            ],
            "industry_rubric": "Evaluates deep mastery of modern retrieval-ranking pipelines, embedding spaces, negative sampling strategies, and scalable vector indexing."
        },
        # Advanced 3
        {
            "id": "ml-adv-03",
            "title": "Model Quantization, Pruning & TensorRT Optimization Suite with Latency Benchmarking",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["Python", "PyTorch", "Docker", "Linux", "CUDA"],
            "non_tech_competencies": ["Edge & Mobile AI", "Precision Quantization", "Hardware Acceleration"],
            "executive_summary": "Deploying 32-bit floating point models to edge devices or cost-sensitive cloud servers is unsustainable. This suite implements Post-Training Quantization (INT8), unstructured weight pruning, and TensorRT engine compilation.",
            "architecture_summary": "Model compression framework analyzing neural network layer sensitivity, applying calibration INT8 quantization, and validating accuracy retention.",
            "key_features": [
                "Post-Training Quantization (PTQ) converting FP32 weights to INT8 with calibration datasets",
                "Unstructured weight magnitude pruning removing 40% of zero-weight parameters",
                "TensorRT engine compilation fusing Conv-BatchNorm-ReLU layers for hardware acceleration",
                "Automated benchmark dashboard comparing model file size, VRAM footprint, throughput, and accuracy"
            ],
            "roadmap": [
                "Milestone 1: Baseline model profiling measuring layer-by-layer compute bottlenecks",
                "Milestone 2: INT8 quantization calibration and accuracy retention validation (assert < 1% drop)",
                "Milestone 3: TensorRT engine compilation and inference harness implementation",
                "Milestone 4: Comprehensive benchmark report comparing FP32 vs INT8 speedup metrics"
            ],
            "industry_rubric": "Evaluates understanding of numerical precision, quantization calibration algorithms (entropy vs min-max), layer fusion, and hardware architecture."
        },
        # Advanced 4
        {
            "id": "ml-adv-04",
            "title": "Fault-Tolerant Distributed Training Checkpoint & Spot Instance Recovery Orchestrator",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "PyTorch", "Docker", "AWS", "Linux"],
            "non_tech_competencies": ["Cloud FinOps", "Fault-Tolerant Orchestration", "Disaster Recovery"],
            "executive_summary": "Cloud GPU spot instances are 70% cheaper than on-demand instances but can be terminated with only 2 minutes notice. This orchestrator handles spot termination signals, flushes atomic checkpoints, and automatically resumes training.",
            "architecture_summary": "Resilient training supervisor intercepting AWS Spot Termination Notices via metadata endpoints, persisting state to S3, and respawning training workers.",
            "key_features": [
                "Asynchronous cloud storage checkpointing minimizing training epoch pause overhead",
                "AWS EC2 spot termination notice daemon catching 2-minute pre-termination warnings",
                "Atomic state restoration reconstructing optimizer momentum, learning rate schedule, and RNG seeds",
                "Automated cost savings calculation proving 65%+ reduction in training cloud expenditure"
            ],
            "roadmap": [
                "Milestone 1: Atomic checkpointing protocol saving model, optimizer, scheduler, and rank states",
                "Milestone 2: Spot termination watcher daemon querying instance metadata endpoints",
                "Milestone 3: Automated worker respawn logic downloading latest verified checkpoint from S3",
                "Milestone 4: Simulated spot interruption test verifying seamless training continuity"
            ],
            "industry_rubric": "Evaluates understanding of cloud spot economics, distributed state serialization, Linux system signal handling, and zero-data-loss recovery."
        }
    ],

    # -------------------------------------------------------------------------
    # 3. Mobile Application Engineering (10 Projects)
    # -------------------------------------------------------------------------
    "mobile_dev": [
        # Beginner 1
        {
            "id": "mob-beg-01",
            "title": "Offline-First Task & Habit Tracker with SQLite / Room & Jetpack Compose",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Kotlin", "SQLite", "Git", "Linux"],
            "non_tech_competencies": ["Mobile UI/UX", "Offline Persistence", "Declarative UI Patterns"],
            "executive_summary": "Mobile users expect instant responsiveness even in airplane mode or subways without internet. This Android app implements an offline-first architecture with Jetpack Compose declarative UI, Room SQLite database, and Kotlin Coroutines.",
            "architecture_summary": "Android Clean Architecture utilizing MVVM pattern, Room persistence, Flow reactive streams, and Jetpack Compose UI.",
            "key_features": [
                "Declarative UI components with Material 3 theming and dark mode support",
                "Local SQLite persistence using Android Room with indexed foreign key relationships",
                "Kotlin StateFlow reactive UI updates ensuring zero UI thread blocking",
                "Automated Android unit and integration tests with mock database DAOs"
            ],
            "roadmap": [
                "Milestone 1: Jetpack Compose screen scaffolding and navigation graph setup",
                "Milestone 2: Room SQLite database schema, DAOs, and repository layer implementation",
                "Milestone 3: ViewModel state management and reactive StateFlow data binding",
                "Milestone 4: Automated unit tests asserting offline CRUD operations and state integrity"
            ],
            "industry_rubric": "Evaluates clean MVVM separation, avoidance of main thread database operations, proper use of Kotlin Coroutines/Flows, and Material Design guidelines."
        },
        # Beginner 2
        {
            "id": "mob-beg-02",
            "title": "Cross-Platform REST Client with React Native, TypeScript & Redux Toolkit",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["TypeScript", "React", "JavaScript", "Git"],
            "non_tech_competencies": ["Cross-Platform Architecture", "State Management", "API Error Handling"],
            "executive_summary": "Startups need to ship iOS and Android apps simultaneously from a single codebase. This React Native project demonstrates type-safe REST API integration, client-side caching, and responsive cross-platform styling.",
            "architecture_summary": "React Native application with TypeScript strict typing, Redux Toolkit query (RTK Query) caching, and native responsive layouts.",
            "key_features": [
                "Strict TypeScript interfaces modeling all API payloads, responses, and navigation params",
                "RTK Query automated caching, background polling, and optimistic UI updates",
                "Platform-specific UI adjustments using Platform.select for iOS and Android ergonomics",
                "Graceful network error states with pull-to-refresh and offline warning banners"
            ],
            "roadmap": [
                "Milestone 1: React Native project initialization with TypeScript and React Navigation",
                "Milestone 2: Redux Toolkit store and RTK Query API endpoints configuration",
                "Milestone 3: Responsive card list, detail view, and search filter screen implementation",
                "Milestone 4: Jest unit tests and component snapshot tests verifying UI state rendering"
            ],
            "industry_rubric": "Evaluates TypeScript type safety, efficient re-render prevention (React.memo), clean state management, and native mobile UX paradigms."
        },
        # Intermediate 1
        {
            "id": "mob-int-01",
            "title": "Native iOS Financial Portfolio App with SwiftUI, Combine & CoreData Encrypted Storage",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Swift", "iOS", "Git", "SQLite"],
            "non_tech_competencies": ["Native iOS Design", "Data Protection & Keychain", "Reactive Programming"],
            "executive_summary": "Financial and wealth management apps handle sensitive asset balances that must be encrypted at rest and update live with market fluctuations. This native iOS app uses SwiftUI, Combine publishers, and Apple Keychain encryption.",
            "architecture_summary": "Native iOS application following MVVM architecture, Combine reactive pipelines, CoreData encrypted storage, and Apple Keychain security.",
            "key_features": [
                "Interactive financial charts with smooth animations using Swift Charts",
                "Biometric authentication (FaceID / TouchID) protecting sensitive transaction views",
                "Apple Keychain integration storing API credentials and sensitive user tokens",
                "Combine reactive streams merging WebSocket price tickers with local portfolio balances"
            ],
            "roadmap": [
                "Milestone 1: SwiftUI UI hierarchy and Swift Charts portfolio dashboard design",
                "Milestone 2: CoreData schema with SQLCipher / file-level encryption and repository protocols",
                "Milestone 3: LocalAuthentication framework integration for FaceID biometric gate",
                "Milestone 4: XCTest unit and UI test suite verifying financial balance calculations"
            ],
            "industry_rubric": "Evaluates adherence to Apple Human Interface Guidelines (HIG), proper memory management (ARC / weak self), Keychain usage, and Combine streams."
        },
        # Intermediate 2
        {
            "id": "mob-int-02",
            "title": "Native Android Audio Streaming Service with Kotlin Coroutines & ExoPlayer Background Service",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Kotlin", "Android", "Git", "Linux"],
            "non_tech_competencies": ["Background Processing", "Audio Focus & MediaSession", "Battery Optimization"],
            "executive_summary": "Mobile operating systems aggressively kill background processes to save battery. This Android service implements a foreground media playback architecture using Media3 ExoPlayer that survives app backgrounding and system sleep.",
            "architecture_summary": "Android Media3 ExoPlayer foreground service architecture with MediaSession notification controls and Kotlin Coroutines.",
            "key_features": [
                "MediaSession foreground service displaying interactive lockscreen and notification playback controls",
                "Audio focus management gracefully pausing playback during incoming phone calls or notifications",
                "Local cache-ahead buffer pre-fetching audio segments to prevent buffering stutter on weak cellular connections",
                "Deep battery profiling proving zero CPU wakelock leaks when playback is paused"
            ],
            "roadmap": [
                "Milestone 1: Android Media3 ExoPlayer setup and streaming audio URL playback handler",
                "Milestone 2: Foreground service lifecycle management with custom NotificationCompat builder",
                "Milestone 3: Audio focus listener and Bluetooth headphone disconnect handler",
                "Milestone 4: Automated Robolectric tests verifying playback state transitions"
            ],
            "industry_rubric": "Evaluates understanding of Android lifecycle management, foreground services, battery drain prevention, and MediaSession compliance."
        },
        # Intermediate 3
        {
            "id": "mob-int-03",
            "title": "Offline-First Synchronized Notes App with WatermelonDB & WebSocket Conflict Resolution",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["TypeScript", "React", "SQLite", "JavaScript", "Docker"],
            "non_tech_competencies": ["Distributed Data Sync", "CRDT & Conflict Resolution", "Offline UX"],
            "executive_summary": "When users edit documents on mobile while offline, merging changes later often overwrites server edits. This cross-platform app uses WatermelonDB SQLite indexing and Last-Write-Wins / Operational Transformation conflict resolution.",
            "architecture_summary": "React Native application powered by WatermelonDB SQLite engine, background sync worker, and WebSocket bi-directional synchronization.",
            "key_features": [
                "Lazy-loaded SQLite database handling 50,000+ local documents with sub-16ms UI render times",
                "Automated background sync worker batching local change sets into compact JSON payloads",
                "Deterministic conflict resolution handling concurrent edits across mobile and web clients",
                "Visual sync status indicator (Synced, Syncing, Offline Changes Pending)"
            ],
            "roadmap": [
                "Milestone 1: WatermelonDB local schema and observable query models",
                "Milestone 2: Local change tracking (created, updated, deleted timestamps)",
                "Milestone 3: Synchronization protocol endpoint resolving concurrent update conflicts",
                "Milestone 4: Network interruption test suite asserting zero data loss across offline sessions"
            ],
            "industry_rubric": "Evaluates understanding of mobile local database indexing, data synchronization patterns, conflict resolution heuristics, and smooth 60fps UI."
        },
        # Intermediate 4
        {
            "id": "mob-int-04",
            "title": "Mobile App Performance & Battery Profiling Suite with Memory Leak Canary",
            "difficulty": "Intermediate",
            "hours": 22,
            "primary_skills": ["Kotlin", "Android", "Python", "Git"],
            "non_tech_competencies": ["Performance Engineering", "Memory Leak Prevention", "Profiler Automation"],
            "executive_summary": "Hidden memory leaks and unoptimized UI redraws cause app crashes, poor app store ratings, and user uninstalls. This automated diagnostic suite integrates LeakCanary and frame rate monitors to detect performance regressions in CI.",
            "architecture_summary": "Diagnostic monitoring framework integrated into Android runtime tracking heap allocations, memory leaks, and dropped frame jank.",
            "key_features": [
                "Automated heap dump analysis via LeakCanary detecting retained Activity and Fragment references",
                "FrameMetrics listener logging 16ms frame deadline drops (jank) during intensive list scrolling",
                "Automated network payload profiler tracking cellular data consumption per API endpoint",
                "CI performance test runner failing pull requests if memory footprint increases by > 15%"
            ],
            "roadmap": [
                "Milestone 1: LeakCanary configuration and intentional leak test cases for baseline verification",
                "Milestone 2: JankStats and FrameMetrics implementation tracking rendering performance",
                "Milestone 3: Memory footprint logger exporting heap metrics to diagnostic JSON files",
                "Milestone 4: Automated benchmark suite running Espresso UI automated scroll tests"
            ],
            "industry_rubric": "Evaluates understanding of the JVM/Android garbage collector, reference lifecycles (WeakReference vs StrongReference), and rendering pipelines."
        },
        # Advanced 1
        {
            "id": "mob-adv-01",
            "title": "Real-Time Geospatial Driver & Rider Tracking App with Mapbox, WebSockets & Background Location",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Kotlin", "Swift", "TypeScript", "Redis", "Docker"],
            "non_tech_competencies": ["Geospatial Tracking", "Battery-Aware Location", "Real-Time Systems"],
            "executive_summary": "Ride-hailing and delivery apps require continuous location updates from drivers without draining phone batteries within 2 hours. This app implements an adaptive GPS polling engine with Kalman filtering and live WebSocket dispatch.",
            "architecture_summary": "Mobile client with native background location service, Kalman GPS noise filtering, and WebSocket stream transmitting coordinates to Redis GEO.",
            "key_features": [
                "Adaptive GPS polling throttled by accelerometer movement (high frequency when moving, sleep when stationary)",
                "Kalman filter algorithm smoothing erratic GPS noise and snapping coordinates to road networks",
                "Background location permission handling adhering to strict Android 14 and iOS 17 privacy mandates",
                "Interactive vector map displaying smooth driver vehicle rotation and route polyline updates"
            ],
            "roadmap": [
                "Milestone 1: FusedLocationProvider background service with foreground notification",
                "Milestone 2: Mathematical Kalman filter implementation in Kotlin/Swift for coordinate smoothing",
                "Milestone 3: WebSocket client transmitting compressed coordinate deltas to backend",
                "Milestone 4: Battery drain benchmark proving > 8 hours continuous tracking on standard battery"
            ],
            "industry_rubric": "Evaluates deep mastery of mobile operating system location permissions, sensor fusion, battery power budgeting, and real-time map rendering."
        },
        # Advanced 2
        {
            "id": "mob-adv-02",
            "title": "End-to-End Encrypted Mobile Messaging Client with Signal Protocol & Push Notifications",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Swift", "Kotlin", "TypeScript", "Cryptography", "Git"],
            "non_tech_competencies": ["Cryptographic Protocols", "Privacy Engineering", "Secure Push Notifications"],
            "executive_summary": "Centralized chat apps leak metadata and message content to compromised servers. This mobile client implements the Signal Double Ratchet protocol, providing forward secrecy and post-compromise security on mobile devices.",
            "architecture_summary": "Secure messaging application implementing Signal Protocol (X3DH + Double Ratchet), encrypted local SQLite storage, and silent push notification wakeup.",
            "key_features": [
                "Extended Triple Diffie-Hellman (X3DH) key agreement and Double Ratchet message encryption",
                "Forward secrecy and break-in recovery ensuring past messages cannot be decrypted if keys are compromised",
                "SQLCipher database encryption with cryptographic key derived via PBKDF2 from user passcode",
                "Silent APNs / FCM push notification wakeup decrypting messages on device before notification display"
            ],
            "roadmap": [
                "Milestone 1: Cryptographic key pair generation and public pre-key bundle publishing",
                "Milestone 2: Double Ratchet state machine implementation for message encryption/decryption",
                "Milestone 3: SQLCipher local database setup storing encrypted message history and contact keys",
                "Milestone 4: Security penetration test asserting zero plaintext message leakage in RAM or disk"
            ],
            "industry_rubric": "Evaluates understanding of modern mobile cryptography, key lifecycle management, zero-knowledge architectures, and secure notification handling."
        },
        # Advanced 3
        {
            "id": "mob-adv-03",
            "title": "Cross-Platform React Native Design System & Micro-Frontend Module Architecture",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["TypeScript", "React", "JavaScript", "Git", "Docker"],
            "non_tech_competencies": ["Design Systems", "Monorepo Architecture", "Enterprise Scaling"],
            "executive_summary": "Enterprise mobile apps built by 20+ feature teams turn into unmaintainable monoliths. This project architects a modular micro-frontend mobile architecture with isolated feature modules, shared design tokens, and CI packaging.",
            "architecture_summary": "Lerna / Turborepo monorepo structuring shared core UI libraries, isolated feature modules, and independent test harness applications.",
            "key_features": [
                "Unified design system with strict TypeScript tokens for typography, spacing, and color palettes",
                "Decoupled feature modules communicating strictly via type-safe event buses and deep linking",
                "Storybook for React Native cataloging all components with interactive props documentation",
                "Automated bundle size analyzer alerting when new dependencies bloat the JavaScript bundle"
            ],
            "roadmap": [
                "Milestone 1: Monorepo workspace configuration with shared TypeScript and ESLint configurations",
                "Milestone 2: Core design token engine and accessible primitive component library",
                "Milestone 3: Feature module encapsulation with decoupled routing and dependency injection",
                "Milestone 4: Storybook interactive documentation and automated visual regression test suite"
            ],
            "industry_rubric": "Evaluates modular software engineering, clean interface boundaries, monorepo dependency management, and design system governance."
        },
        # Advanced 4
        {
            "id": "mob-adv-04",
            "title": "Native Mobile CI/CD Automation Matrix with Fastlane, GitHub Actions & TestFlight / Play Store",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Git", "Docker", "Linux", "Bash", "Python"],
            "non_tech_competencies": ["Release Engineering", "Code Signing & Secrets", "CI/CD Pipeline Design"],
            "executive_summary": "Manual mobile builds and code signing certificates cause release delays and broken production deployments. This project automates the entire mobile release pipeline using Fastlane, GitHub Actions, and Match code signing.",
            "architecture_summary": "Automated mobile continuous delivery pipeline handling automated versioning, code signing with Apple Match, unit testing, and store distribution.",
            "key_features": [
                "Fastlane Match integration managing iOS provisioning profiles and distribution certificates via Git",
                "Automated Android Keystore signing and AAB (Android App Bundle) optimization in CI",
                "GitHub Actions matrix running parallel unit tests, linting, and build validation across OS runners",
                "Automated deployment to Apple TestFlight internal testing and Google Play Internal Track"
            ],
            "roadmap": [
                "Milestone 1: Fastlane configuration files (Fastfile, Appfile, Matchfile) for iOS and Android",
                "Milestone 2: Secure secret management in GitHub Actions for certificates and keystores",
                "Milestone 3: Automated version bump and changelog generation from conventional git commits",
                "Milestone 4: End-to-end dry-run build pipeline successfully uploading build artifacts to beta tracks"
            ],
            "industry_rubric": "Evaluates mobile code signing expertise, secret rotation security, pipeline speed optimization, and zero-touch store distribution."
        }
    ],

    # -------------------------------------------------------------------------
    # 4. Embedded Systems & Firmware (10 Projects)
    # -------------------------------------------------------------------------
    "embedded_systems": [
        # Beginner 1
        {
            "id": "emb-beg-01",
            "title": "Bare-Metal ARM Cortex-M GPIO & Timer Interrupt Driver in Embedded C",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["C", "Linux", "CMake", "Git"],
            "non_tech_competencies": ["Hardware Register Mapping", "Interrupt Service Routines", "Low-Level Debugging"],
            "executive_summary": "Using heavy high-level libraries on resource-constrained microcontrollers wastes RAM and introduces unpredictable latency. This bare-metal driver directly configures memory-mapped hardware registers and hardware timer interrupts in C.",
            "architecture_summary": "Bare-metal embedded C firmware without operating system overhead, targeting ARM Cortex-M microcontrollers with direct register pointers.",
            "key_features": [
                "Direct memory-mapped I/O register manipulation using volatile pointers and bitwise masks",
                "Hardware timer interrupt (SysTick / TIM2) driving a deterministic 1kHz system heartbeat",
                "GPIO interrupt handling with hardware debouncing logic for external button inputs",
                "Linker script and startup assembly file configuring the interrupt vector table and stack pointer"
            ],
            "roadmap": [
                "Milestone 1: Microcontroller memory map review and register header file authoring",
                "Milestone 2: Clock tree initialization (RCC) configuring system core clock frequency",
                "Milestone 3: GPIO configuration and Timer Interrupt Service Routine (ISR) implementation",
                "Milestone 4: QEMU ARM emulator automated unit testing verifying deterministic interrupt timing"
            ],
            "industry_rubric": "Evaluates correct use of volatile keywords, bitwise masking, avoiding non-reentrant calls inside ISRs, and understanding hardware memory maps."
        },
        # Beginner 2
        {
            "id": "emb-beg-02",
            "title": "High-Reliability Circular Buffer UART Serial Communication Protocol in C",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["C", "Linux", "CMake", "Git"],
            "non_tech_competencies": ["Serial Protocols", "Thread-Safe Ring Buffers", "Packet Framing"],
            "executive_summary": "Embedded microcontrollers frequently drop serial telemetry packets during high-load processing spikes. This driver implements an interrupt-driven lockless circular FIFO buffer with framing and CRC16 error detection.",
            "architecture_summary": "UART serial communication driver featuring lockless single-producer single-consumer circular buffer and packet framing parser in C.",
            "key_features": [
                "Lockless circular ring buffer safe for single-producer (UART ISR) single-consumer (Main loop)",
                "Packet framing protocol with Start-of-Frame (SOF), length, payload, and CRC-16 validation",
                "Buffer overrun and frame error detection with automated error statistics counters",
                "C unit test suite running under GCC host compilation verifying zero data loss under burst writes"
            ],
            "roadmap": [
                "Milestone 1: Circular buffer data structure with power-of-two capacity and bitmask wrapping",
                "Milestone 2: UART interrupt transmitter/receiver handler feeding the ring buffer",
                "Milestone 3: Packet parser state machine extracting verified payloads from raw byte streams",
                "Milestone 4: Host-compiled unit test suite with mock hardware registers asserting CRC validation"
            ],
            "industry_rubric": "Evaluates memory bounds checking, prevention of race conditions without heavy mutexes, defensive CRC validation, and clean C code style."
        },
        # Intermediate 1
        {
            "id": "emb-int-01",
            "title": "Multi-Tasking Sensor Node with FreeRTOS, Queues & Semaphores on ESP32 / STM32",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["C", "C++", "Linux", "CMake", "Git"],
            "non_tech_competencies": ["Real-Time Operating Systems", "Task Synchronization", "Deadlock Prevention"],
            "executive_summary": "Complex embedded devices executing multiple sensor readings, networking, and motor control cannot rely on naive while(1) loops. This project implements a real-time multi-tasking architecture using FreeRTOS tasks and queues.",
            "architecture_summary": "FreeRTOS embedded architecture separating high-priority sensor sampling, data processing, and telemetry dispatch across prioritized RTOS tasks.",
            "key_features": [
                "Preemptive priority-based task scheduling guaranteeing strict execution deadlines for sensor reads",
                "Inter-task communication via FreeRTOS Queues preventing shared memory race conditions",
                "Binary and counting semaphores protecting shared hardware peripherals (I2C/SPI bus)",
                "Stack watermark monitoring detecting stack overflow before system memory corruption"
            ],
            "roadmap": [
                "Milestone 1: FreeRTOS kernel configuration and tick rate setup on microcontroller hardware",
                "Milestone 2: Sensor acquisition task and telemetry logging task creation with priority assignment",
                "Milestone 3: Mutex and queue integration for thread-safe access to shared I2C bus",
                "Milestone 4: FreeRTOS runtime stats profiler monitoring CPU percentage per task"
            ],
            "industry_rubric": "Evaluates RTOS task design, avoiding priority inversion (priority inheritance mutexes), proper stack allocation, and real-time deadline meeting."
        },
        # Intermediate 2
        {
            "id": "emb-int-02",
            "title": "Non-Volatile Flash Memory Wear-Leveling File System Driver in Modern C++",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["C++", "C", "CMake", "Linux", "Git"],
            "non_tech_competencies": ["Flash Memory Physics", "Wear Leveling Algorithms", "Power-Fail Safety"],
            "executive_summary": "Raw NOR/NAND flash memory cells degrade after 100,000 write cycles. Writing repeatedly to the same address permanently destroys embedded hardware. This driver implements block wear-leveling and atomic power-fail safe writes in modern C++.",
            "architecture_summary": "Embedded flash storage engine implementing log-structured block allocation, dynamic wear-leveling, and power-cut recovery.",
            "key_features": [
                "Log-structured append-only storage distributing writes evenly across all physical flash sectors",
                "Atomic transaction journal guaranteeing zero metadata corruption if power is pulled mid-write",
                "Garbage collection mechanism reclaiming deleted sectors without stalling real-time operations",
                "Modern C++17 implementation using RAII, strict type safety, and zero dynamic heap allocation"
            ],
            "roadmap": [
                "Milestone 1: Flash block/sector memory abstraction layer and mock flash hardware simulator",
                "Milestone 2: Log-structured block allocation and erase-count tracking table",
                "Milestone 3: Power-failure simulation test harness asserting file system consistency",
                "Milestone 4: Benchmark suite measuring wear distribution uniformity across 1,000,000 simulated writes"
            ],
            "industry_rubric": "Evaluates understanding of flash physical characteristics (erase before write, sector wear), zero-heap embedded C++, and power-loss resiliency."
        },
        # Intermediate 3
        {
            "id": "emb-int-03",
            "title": "Automotive CAN Bus Telemetry Logger & Packet Sniffer with Python Analysis Suite",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["C", "Python", "Linux", "CMake", "Docker"],
            "non_tech_competencies": ["Automotive Protocols", "CAN Bus Architecture", "DBC File Parsing"],
            "executive_summary": "Modern vehicles communicate across high-speed Controller Area Network (CAN) buses. This embedded tool monitors CAN traffic, filters messages by arbitration ID, logs frames to an SD card, and streams decoded telemetry to a host dashboard.",
            "architecture_summary": "Dual-component system: Embedded C microcontroller CAN transceiver listener and Python host decoding service using SocketCAN.",
            "key_features": [
                "Hardware acceptance mask filtering dropping irrelevant CAN IDs at the silicon silicon controller level",
                "Ring-buffered SD card binary logging supporting continuous 1 Mbps CAN bus saturation",
                "Python DBC parser decoding raw CAN payloads into real physical values (RPM, Speed, Temperature)",
                "SocketCAN virtual CAN bus (vcan0) test harness simulating automotive ECU traffic"
            ],
            "roadmap": [
                "Milestone 1: CAN controller initialization (baud rate, timing segments, filter masks) in C",
                "Milestone 2: Interrupt-driven CAN frame reception and SD card FAT32 binary writer",
                "Milestone 3: Python SocketCAN ingestion script reading frames and parsing DBC signal definitions",
                "Milestone 4: End-to-end evaluation verifying zero dropped frames at 10,000 messages/sec"
            ],
            "industry_rubric": "Evaluates knowledge of automotive communication standards (CAN 2.0B / CAN FD), bit timing calculations, DBC signal decoding, and bus load management."
        },
        # Intermediate 4
        {
            "id": "emb-int-04",
            "title": "Secure Bootloader with Hardware Cryptographic Verification & Over-The-Air (OTA) Updates",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["C", "Cryptography", "Python", "CMake", "Linux"],
            "non_tech_competencies": ["Secure Boot Architecture", "Public Key Verification", "Fail-Safe Rollback"],
            "executive_summary": "Malicious firmware flashes or botched remote updates turn expensive IoT devices into permanently bricked hardware. This secure bootloader verifies RSA/ECDSA digital signatures on firmware binaries before booting and supports dual-bank A/B rollback.",
            "architecture_summary": "Secondary stage bootloader verifying firmware image headers and cryptographic signatures in internal flash before jumping to the application reset handler.",
            "key_features": [
                "Dual-bank A/B memory partitioning allowing live background OTA flashing to inactive bank",
                "ECDSA (secp256r1) digital signature verification validating firmware authenticity before boot",
                "Automatic watchdog rollback booting back to Bank A if new Bank B firmware fails to confirm health",
                "Python firmware packaging tool appending version headers, CRC32, and cryptographic signature"
            ],
            "roadmap": [
                "Milestone 1: Memory flash map partitioning (Bootloader, Bank A, Bank B, NVRAM configuration)",
                "Milestone 2: Microcontroller jump-to-application vector table relocation routine in C",
                "Milestone 3: TinyCrypt / mbedTLS integration validating public key ECDSA signature over firmware binary",
                "Milestone 4: Simulated corrupted firmware flash asserting 100% reliable rollback to golden image"
            ],
            "industry_rubric": "Evaluates understanding of hardware trust chains, vector table relocation (SCB->VTOR), public key verification, and brick-proof failover design."
        },
        # Advanced 1
        {
            "id": "emb-adv-01",
            "title": "Embedded Linux Kernel Device Driver for Custom I2C / SPI Sensor with sysfs Interface",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["C", "Linux", "CMake", "Git"],
            "non_tech_competencies": ["Linux Kernel Architecture", "Device Tree Compilation", "Kernel-User Space Boundary"],
            "executive_summary": "Industrial embedded Linux platforms (Raspberry Pi CM4, i.MX6/8) require kernel device drivers to interface hardware sensors with user applications. This project implements a full Linux character device driver with Device Tree bindings.",
            "architecture_summary": "Out-of-tree Linux kernel module (LKM) implementing I2C client driver, sysfs attributes, interrupt handling, and user-space character device nodes.",
            "key_features": [
                "Device Tree source (DTS) overlay binding hardware peripheral address, clock, and interrupt line",
                "Character device interface implementing open, read, write, and poll system calls",
                "sysfs attribute file interface enabling user-space configuration via standard echo/cat commands",
                "Thread-safe kernel synchronization using spinlocks and mutexes to protect device registers"
            ],
            "roadmap": [
                "Milestone 1: Device Tree overlay compilation and kernel cross-compilation toolchain setup",
                "Milestone 2: Kernel module scaffolding with module_init, module_exit, and I2C driver registration",
                "Milestone 3: Hardware register communication via i2c_smbus routines and interrupt bottom-half handler",
                "Milestone 4: User-space C client program interacting with driver via /dev/sensor character node"
            ],
            "industry_rubric": "Evaluates mastery of Linux kernel development, memory safety (copy_to_user / copy_from_user), kernel lock primitives, and Device Tree mechanics."
        },
        # Advanced 2
        {
            "id": "emb-adv-02",
            "title": "Hard Real-Time Motor Control & PID Loop Controller with Hardware Timers & DMA",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["C", "C++", "CMake", "Linux", "Git"],
            "non_tech_competencies": ["Control Systems Engineering", "Hard Real-Time Deadlines", "DMA Architecture"],
            "executive_summary": "Robotics and precision industrial machines require microsecond-accurate feedback loops. A jitter of 100 microseconds can cause motor oscillation or physical damage. This controller implements a 10kHz deterministic PID loop using ADC DMA and timer PWM.",
            "architecture_summary": "Hard real-time motor controller using Direct Memory Access (DMA) for zero-CPU ADC sampling and hardware timer center-aligned PWM generation.",
            "key_features": [
                "Zero-CPU ADC sampling utilizing circular DMA streaming directly into memory buffers",
                "10kHz deterministic Proportional-Integral-Derivative (PID) algorithm with anti-windup clamping",
                "Center-aligned Complementary PWM generation with configurable hardware dead-time insertion",
                "Hardware fault input (Break input) shutting down PWM outputs in < 50 nanoseconds upon overcurrent"
            ],
            "roadmap": [
                "Milestone 1: Timer PWM configuration with complementary channels and dead-time insertion",
                "Milestone 2: ADC multi-channel configuration triggered by Timer update events via DMA",
                "Milestone 3: Fixed-point / floating-point PID controller algorithm with derivative filter",
                "Milestone 4: Step response test suite verifying < 5% overshoot and sub-10ms settling time"
            ],
            "industry_rubric": "Evaluates control theory application (PID tuning, integral windup), DMA controller configuration, dead-time calculation to prevent MOSFET shoot-through, and zero-jitter timing."
        },
        # Advanced 3
        {
            "id": "emb-adv-03",
            "title": "Ultra-Low-Power Edge IoT Sensor with Sleep Modes, BLE Advertising & Power Profiling",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["C", "C++", "CMake", "Linux", "Git"],
            "non_tech_competencies": ["Low-Power Hardware Design", "Energy Harvesting Budgets", "BLE Protocols"],
            "executive_summary": "Battery-powered agricultural and environmental sensors must operate for 5+ years on a single coin-cell battery. This firmware optimizes CPU power domains, deep-sleep modes, and Bluetooth Low Energy (BLE) beaconing to achieve sub-15 microamp average current.",
            "architecture_summary": "Ultra-low-power firmware utilizing Nordic nRF52 / ESP32 deep-sleep modes, RTC wake-up timers, and optimized BLE advertising payloads.",
            "key_features": [
                "Aggressive power domain shutdown turning off RAM banks, flash clocks, and internal oscillators during sleep",
                "RTC external wake-up interrupt waking the CPU only once every 60 seconds for 12 milliseconds",
                "Compact Non-Connectable BLE Manufacturer Data beacon transmitting sensor telemetry without connection handshake",
                "Power consumption profile proving 12.4 uA average sleep current and 5-year coin-cell lifetime"
            ],
            "roadmap": [
                "Milestone 1: Microcontroller power mode configuration (Active, Sleep, Deep Sleep, System OFF)",
                "Milestone 2: Peripheral power gating isolating sensor power lines via P-channel MOSFET switches",
                "Milestone 3: BLE advertising stack broadcasting packed sensor telemetry in single packet bursts",
                "Milestone 4: Power profiling analysis validating mathematical battery life expectancy calculations"
            ],
            "industry_rubric": "Evaluates deep hardware energy budgeting, microamp measurement techniques, BLE advertising protocol efficiency, and peripheral leakage current mitigation."
        },
        # Advanced 4
        {
            "id": "emb-adv-04",
            "title": "Fault-Tolerant Embedded Flight Computer State Machine with Watchdog & Dual-Bank Fallback",
            "difficulty": "Advanced",
            "hours": 40,
            "primary_skills": ["C", "C++", "CMake", "Linux", "Git"],
            "non_tech_competencies": ["Mission-Critical Safety", "Hierarchical State Machines", "Fault Detection"],
            "executive_summary": "Aerospace, medical, and mission-critical embedded systems cannot be rebooted by a human when an exception occurs. This project implements a DO-178C inspired hierarchical state machine with hardware independent watchdogs and non-volatile black box flight recorder.",
            "architecture_summary": "Deterministic hierarchical state machine (HSM) in ANSI C with independent window watchdog supervision and crash dump logging.",
            "key_features": [
                "Strict hierarchical state machine (IDLE -> ARMED -> BOOST -> DESCENT -> LANDED) with transition guards",
                "Independent window watchdog timer (WWDG) resetting system if loop runs too fast or too slow",
                "Non-volatile black box crash logging writing CPU registers, stack pointers, and assert errors to FRAM",
                "Automated fault injection test suite verifying safe parachute deployment despite simulated sensor failures"
            ],
            "roadmap": [
                "Milestone 1: State machine architecture definition with state transition tables and event queues",
                "Milestone 2: Hardware window watchdog integration requiring precise tick-time refresh signals",
                "Milestone 3: Non-volatile black box fault recording handler intercepting HardFault exceptions",
                "Milestone 4: Hardware-in-the-loop (HIL) fault injection asserting zero unrecoverable state freezes"
            ],
            "industry_rubric": "Evaluates safety-critical embedded engineering, defensive programming (MISRA C guidelines), window watchdog mechanics, and deterministic fault containment."
        }
    ],

    # -------------------------------------------------------------------------
    # 5. Blockchain & Web3 Protocols (10 Projects)
    # -------------------------------------------------------------------------
    "blockchain_web3": [
        # Beginner 1
        {
            "id": "bc-beg-01",
            "title": "ERC-20 Token & Staking Smart Contract with OpenZeppelin & Foundry",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Solidity", "Git", "Docker", "Linux"],
            "non_tech_competencies": ["Smart Contract Standards", "Tokenomics", "Gas Optimization"],
            "executive_summary": "Flawed token smart contracts have led to billions of dollars in lost funds. This project implements a secure, gas-optimized ERC-20 token with time-locked staking rewards using OpenZeppelin standards and Foundry testing.",
            "architecture_summary": "Solidity smart contract suite utilizing Foundry for blazing-fast fuzz testing, gas profiling, and contract verification.",
            "key_features": [
                "ERC-20 implementation with strict OpenZeppelin SafeERC20 transfer guards",
                "Time-locked staking pool calculating linear reward distribution per block",
                "Emergency pause mechanism (Pausable) allowing owner to freeze transfers during security incidents",
                "100% test coverage using Foundry Forge with automated property-based fuzz tests"
            ],
            "roadmap": [
                "Milestone 1: Foundry development environment setup and ERC-20 token contract implementation",
                "Milestone 2: Staking rewards math calculation using reward-per-token-stored accumulator pattern",
                "Milestone 3: Automated Forge fuzz tests asserting invariants (total staked == sum of balances)",
                "Milestone 4: Gas optimization audit optimizing storage slot packing and calldata variables"
            ],
            "industry_rubric": "Evaluates adherence to established token standards, overflow protection, reentrancy defense, and thorough Foundry unit/fuzz testing."
        },
        # Beginner 2
        {
            "id": "bc-beg-02",
            "title": "Decentralized Escrow Smart Contract with Multi-Signature Verification & Slither",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Solidity", "Python", "Git", "Docker"],
            "non_tech_competencies": ["Escrow State Machines", "Security Static Analysis", "Smart Contract Auditing"],
            "executive_summary": "Freelance commerce and peer-to-peer trades require impartial funds escrow without trusting centralized platforms. This contract holds buyer ether in escrow and releases funds upon cryptographic multi-signature approval.",
            "architecture_summary": "Solidity escrow state machine contract with ECDSA signature verification and Slither static analysis security pipeline.",
            "key_features": [
                "Strict state machine (AWAITING_PAYMENT -> AWAITING_DELIVERY -> COMPLETE -> REFUNDED)",
                "2-of-3 Multi-Signature authorization (Buyer, Seller, Arbiter) resolving transaction disputes",
                "ReentrancyGuard on all state-changing external withdrawal calls",
                "Automated CI security pipeline executing Slither static analyzer to flag vulnerability patterns"
            ],
            "roadmap": [
                "Milestone 1: Escrow state machine contracts and custom error definitions (saving gas over require strings)",
                "Milestone 2: EIP-712 typed structured data signature verification for off-chain release approvals",
                "Milestone 3: Slither static analysis integration resolving all high and medium security warnings",
                "Milestone 4: Foundry test suite simulating dispute escalation and arbiter fee distribution"
            ],
            "industry_rubric": "Evaluates defensive smart contract architecture, checks-effects-interactions pattern, custom error usage, and static analysis tooling."
        },
        # Intermediate 1
        {
            "id": "bc-int-01",
            "title": "Automated Market Maker (AMM) Liquidity Pool with Constant Product Formula (x*y=k)",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Solidity", "TypeScript", "Docker", "Git"],
            "non_tech_competencies": ["DeFi Math & Mechanics", "Slippage & Price Impact", "Liquidity Economics"],
            "executive_summary": "Decentralized exchanges like Uniswap replace centralized order books with algorithmic liquidity pools. This project implements a Constant Product Automated Market Maker (AMM) supporting token swaps, LP shares, and flash swaps.",
            "architecture_summary": "DeFi smart contract architecture inspired by Uniswap v2, implementing ERC-20 liquidity pool pairing and constant-product invariant math.",
            "key_features": [
                "Constant product formula (x * y = k) pricing calculation with 0.3% liquidity provider fee deduction",
                "LP token minting and burning proportional to deposited liquidity share",
                "Slippage tolerance protection reverting transactions if output falls below minimum requested tokens",
                "TWAP (Time-Weighted Average Price) oracle accumulator providing manipulation-resistant price feeds"
            ],
            "roadmap": [
                "Milestone 1: Core Pair contract implementing mint, burn, and swap mechanics",
                "Milestone 2: Router contract managing multi-hop token swaps and deadline validations",
                "Milestone 3: Time-Weighted Average Price (TWAP) oracle accumulator implementation",
                "Milestone 4: Foundry invariant testing asserting k value never decreases after any swap"
            ],
            "industry_rubric": "Evaluates understanding of DeFi mathematical invariants, precision loss mitigation in Solidity integer math, and resistance to sandwich/frontrunning attacks."
        },
        # Intermediate 2
        {
            "id": "bc-int-02",
            "title": "NFT Dynamic Metadata & Royalty Engine with IPFS Storage & Merkle Tree Whitelisting",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Solidity", "TypeScript", "JavaScript", "Docker"],
            "non_tech_competencies": ["ERC-721 Standards", "Cryptographic Whitelisting", "EIP-2981 Royalties"],
            "executive_summary": "Storing NFT image assets and large whitelist arrays directly on Ethereum costs thousands of dollars in gas. This project uses Merkle Tree cryptographic proofs for zero-cost whitelisting and decentralized IPFS content storage.",
            "architecture_summary": "ERC-721A batch-optimized NFT smart contract with Merkle tree proof verification and EIP-2981 on-chain royalty enforcement.",
            "key_features": [
                "Merkle root verification allowing 100,000+ whitelist addresses with only a single 32-byte storage slot",
                "ERC-721A sequential batch minting cutting gas costs by 70% compared to standard ERC-721",
                "EIP-2981 standardized on-chain royalty specifications directing marketplace creator fees",
                "Automated IPFS pinning integration publishing decentralized metadata and verifiable image hashes"
            ],
            "roadmap": [
                "Milestone 1: Merkle tree generator in TypeScript creating cryptographic proofs from address lists",
                "Milestone 2: ERC-721A smart contract implementation with Merkle proof verification",
                "Milestone 3: EIP-2981 royalty interface integration with configurable royalty fee basis points",
                "Milestone 4: Foundry test suite validating proof verification and gas consumption benchmarks"
            ],
            "industry_rubric": "Evaluates understanding of Merkle proof verification, gas-efficient storage optimization, metadata standards, and decentralized IPFS storage."
        },
        # Intermediate 3
        {
            "id": "bc-int-03",
            "title": "DeFi Lending Vault & Collateralized Debt Position (CDP) Engine in Solidity",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["Solidity", "TypeScript", "Docker", "Git"],
            "non_tech_competencies": ["Lending Protocols", "Collateralization Ratios", "Liquidation Mechanics"],
            "executive_summary": "Decentralized lending protocols (like Aave or Compound) enable trustless borrowing against deposited crypto collateral. This project implements an over-collateralized lending pool with dynamic interest rates and automated liquidation triggers.",
            "architecture_summary": "Collateralized lending architecture managing collateral deposits, stablecoin borrowing, utilization-based interest rates, and liquidations.",
            "key_features": [
                "Over-collateralization ratio enforcement (150% LTV threshold) preventing under-collateralized bad debt",
                "Utilization-rate dynamic interest rate curve increasing borrow APR during high pool utilization",
                "Automated liquidation mechanism awarding liquidator bonuses for repaying under-collateralized loans",
                "Chainlink decentralized price oracle integration with heartbeat and staleness checks"
            ],
            "roadmap": [
                "Milestone 1: Collateral deposit and debt accounting ledger contracts",
                "Milestone 2: Chainlink price feed oracle consumer with circuit breakers for stale prices",
                "Milestone 3: Liquidation function executing collateral auction with liquidator discount",
                "Milestone 4: Foundry stress test simulating sudden price crashes and verifying pool solvency"
            ],
            "industry_rubric": "Evaluates understanding of systemic DeFi financial risk, oracle manipulation defense, precision math, and liquidation mechanics."
        },
        # Intermediate 4
        {
            "id": "bc-int-04",
            "title": "Web3 Event Indexer & GraphQL Subgraph with Rust, PostgreSQL & Docker",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Rust", "SQL", "PostgreSQL", "Docker", "Git"],
            "non_tech_competencies": ["Blockchain Indexing", "Event Decoding", "High-Speed RPC Ingestion"],
            "executive_summary": "Directly querying Ethereum nodes for historical smart contract activity is prohibitively slow. This high-speed indexer streams blockchain logs via JSON-RPC, decodes ABI event signatures, and indexes relational data for fast GraphQL queries.",
            "architecture_summary": "High-performance Rust indexing service listening to Ethereum WebSocket logs, decoding events via alloy/ethers-rs, and persisting to PostgreSQL.",
            "key_features": [
                "WebSocket block header and event listener handling chain reorganizations (reorgs) up to 7 blocks",
                "High-speed ABI event log decoding converting raw 32-byte topics into typed database rows",
                "PostgreSQL relational schema with B-Tree indexes on transaction hashes, addresses, and block timestamps",
                "GraphQL query interface allowing frontend clients to query entity activity in < 15ms"
            ],
            "roadmap": [
                "Milestone 1: Rust RPC client connection to local Anvil / Hardhat testnet node",
                "Milestone 2: Event signature hashing (keccak256) and binary ABI decoding pipeline",
                "Milestone 3: PostgreSQL persistence layer with block height checkpointing and reorg rollback logic",
                "Milestone 4: Automated benchmark asserting ingestion speed > 1,000 blocks/sec during sync"
            ],
            "industry_rubric": "Evaluates understanding of EVM log topics and data structures, blockchain reorg handling, RPC rate limiting, and database indexing."
        },
        # Advanced 1
        {
            "id": "bc-adv-01",
            "title": "Cross-Chain Token Bridge with Cryptographic Relayer & Reentrancy Lock",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Solidity", "Rust", "TypeScript", "Docker", "Git"],
            "non_tech_competencies": ["Cross-Chain Architecture", "Cryptographic Relayers", "Reentrancy Protection"],
            "executive_summary": "Bridges between blockchains are the single most targeted component in Web3 exploits. This project builds a lock-and-mint cross-chain bridge with cryptographic validator multi-signatures, replay attack protection, and timelocked withdrawals.",
            "architecture_summary": "Two-chain bridge architecture with Lock contract on Source Chain, Mint contract on Target Chain, and off-chain Rust relayer network.",
            "key_features": [
                "Lock-and-mint token mechanism burning or locking tokens on source before minting wrapped equivalents",
                "Threshold signature verification requiring M-of-N validator signatures before releasing bridge assets",
                "Replay protection incorporating unique nonce, chain ID (EIP-155), and transaction hash",
                "Emergency 24-hour time-lock for large transfers above threshold values to mitigate zero-day exploits"
            ],
            "roadmap": [
                "Milestone 1: Source and destination smart contracts with custom lock/mint events",
                "Milestone 2: Off-chain Rust relayer listening to events and aggregating validator ECDSA signatures",
                "Milestone 3: On-chain signature recovery and non-reentrant release logic",
                "Milestone 4: Comprehensive hack simulation suite testing reentrancy, signature replay, and cross-chain frontrunning"
            ],
            "industry_rubric": "Evaluates cross-chain security models, signature replay prevention, defensive time-locks, and deep familiarity with historical bridge hacks."
        },
        # Advanced 2
        {
            "id": "bc-adv-02",
            "title": "ERC-4337 Account Abstraction Smart Contract Wallet with Bundler & Paymaster",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Solidity", "TypeScript", "Docker", "Git"],
            "non_tech_competencies": ["Account Abstraction", "User Operation Lifecycle", "Gasless Transactions"],
            "executive_summary": "Seed phrases and gas token requirements are the biggest barrier to Web3 mass adoption. This project implements ERC-4337 Account Abstraction, enabling smart contract wallets with social recovery, session keys, and gasless sponsored transactions.",
            "architecture_summary": "ERC-4337 compliant smart wallet implementing IAccount, verified against EntryPoint contract, with Paymaster gas sponsorship.",
            "key_features": [
                "Smart contract wallet validation function validating UserOperation signatures and paymaster rules",
                "Paymaster contract sponsoring transaction gas fees for eligible users or accepting payment in ERC-20 tokens",
                "Session keys granting temporary, scoped spending permissions to third-party dApps without master key exposure",
                "Social recovery mechanism allowing a set of trusted guardians to recover wallet access if master key is lost"
            ],
            "roadmap": [
                "Milestone 1: Smart contract wallet implementing validateUserOp and execution routing",
                "Milestone 2: Paymaster contract validating token balances and pre-funding EntryPoint gas deposits",
                "Milestone 3: TypeScript bundler client constructing, signing, and transmitting UserOperations",
                "Milestone 4: Foundry test suite validating successful gasless token transfers and session key limits"
            ],
            "industry_rubric": "Evaluates mastery of ERC-4337 architecture, EntryPoint mechanics, UserOperation validation gas constraints, and smart wallet UX patterns."
        },
        # Advanced 3
        {
            "id": "bc-adv-03",
            "title": "Zero-Knowledge Proof (zk-SNARK) Identity Verification Circuit with Circom & SnarkJS",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Solidity", "TypeScript", "JavaScript", "Docker"],
            "non_tech_competencies": ["Zero-Knowledge Proofs", "Arithmetic Circuits", "Privacy Engineering"],
            "executive_summary": "Proving identity or age compliance on a public blockchain without revealing personal identity or date of birth requires Zero-Knowledge proofs. This project authors a Circom arithmetic circuit and deploys a Groth16 on-chain verifier.",
            "architecture_summary": "Privacy-preserving identity system featuring Circom R1CS circuit, SnarkJS proof generator, and Solidity Groth16 verifier contract.",
            "key_features": [
                "Circom arithmetic circuit proving age > 21 without revealing actual birthdate or name",
                "Groth16 trusted setup and zero-knowledge proof generation taking < 1 second in browser",
                "On-chain Solidity verifier smart contract accepting 256-bit proof points (A, B, C) and public inputs",
                "Replay protection using nullifiers preventing the same proof from being submitted multiple times"
            ],
            "roadmap": [
                "Milestone 1: Circom identity circuit authoring with Poseidon hashing and comparison constraints",
                "Milestone 2: SnarkJS Powers of Tau ceremony and Groth16 zkey generation",
                "Milestone 3: Solidity verifier contract export and on-chain verification test",
                "Milestone 4: End-to-end integration test proving valid compliance while concealing all private witness data"
            ],
            "industry_rubric": "Evaluates understanding of ZK mathematics (R1CS, QAP, Groth16), constraint count optimization, nullifier mechanics, and on-chain verification costs."
        },
        # Advanced 4
        {
            "id": "bc-adv-04",
            "title": "High-Throughput EVM MEV Arbitrage Bot with Flashbots RPC & Private Mempool",
            "difficulty": "Advanced",
            "hours": 40,
            "primary_skills": ["Rust", "Solidity", "Docker", "Linux"],
            "non_tech_competencies": ["Maximal Extractable Value (MEV)", "Latency Optimization", "Private Transactions"],
            "executive_summary": "Arbitrage opportunities between decentralized exchanges are closed in milliseconds. Broadcasting transactions to public mempools gets them frontrun. This high-speed bot monitors pending transactions and submits Flashbots bundles directly to block builders.",
            "architecture_summary": "Low-latency Rust arbitrage bot monitoring mempool events, calculating cyclic arbitrage loops, and bundling transactions via Flashbots private RPC.",
            "key_features": [
                "Sub-millisecond cyclic arbitrage cycle detector evaluating exchange price discrepancies across Uniswap and Sushiswap",
                "Atomic smart contract executor completing borrow-swap-swap-repay cycles in a single atomic transaction",
                "Flashbots bundle submission sending bids directly to block builders with zero risk of failed gas payment",
                "Simulation engine verifying transaction profitability against local fork before dispatching real bundles"
            ],
            "roadmap": [
                "Milestone 1: Atomic arbitrage smart contract executing multi-hop swaps and reverting if profit <= 0",
                "Milestone 2: Low-latency Rust mempool watcher calculating optimal input amounts using Bellman-Ford / convex optimization",
                "Milestone 3: Flashbots bundle builder and cryptographic signer sending private RPC payloads",
                "Milestone 4: Mainnet fork test suite simulating 10 real historical arbitrage opportunities with positive net profit"
            ],
            "industry_rubric": "Evaluates low-latency systems programming, EVM state simulation, mathematical arbitrage optimization, and Flashbots private transaction dynamics."
        }
    ],

    # -------------------------------------------------------------------------
    # 6. Fullstack General Engineering (10 Projects)
    # -------------------------------------------------------------------------
    "fullstack_general": [
        # Beginner 1
        {
            "id": "fs-beg-01",
            "title": "Full-Stack Task & Workspace Manager with Next.js 14, SQLite & Tailwind CSS",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["TypeScript", "Next.js", "React", "SQLite", "Tailwind CSS"],
            "non_tech_competencies": ["Fullstack Architecture", "Server Actions", "Responsive UI"],
            "executive_summary": "Modern web development requires seamless coordination between client interfaces and server persistence. This fullstack project demonstrates Server Components, Server Actions, SQLite persistence, and accessible Tailwind CSS styling.",
            "architecture_summary": "Next.js 14 App Router fullstack application utilizing Server Components, typed Server Actions, SQLite database, and responsive Tailwind UI.",
            "key_features": [
                "Next.js 14 App Router architecture leveraging React Server Components for fast initial page load",
                "Type-safe Server Actions handling CRUD mutations without manual REST boilerplate",
                "Optimistic UI updates providing instant drag-and-drop feedback during task reordering",
                "Accessible keyboard navigation adhering to WCAG 2.1 AA contrast and focus standards"
            ],
            "roadmap": [
                "Milestone 1: Next.js 14 App Router project setup with Tailwind CSS design tokens",
                "Milestone 2: SQLite database schema and typed database access repository",
                "Milestone 3: Server Actions implementation with Zod schema validation",
                "Milestone 4: End-to-end Playwright tests verifying task creation, editing, and deletion"
            ],
            "industry_rubric": "Evaluates clean fullstack separation of concerns, proper use of React Server Components vs Client Components, and type safety across client-server boundaries."
        },
        # Beginner 2
        {
            "id": "fs-beg-02",
            "title": "Markdown Technical Documentation Platform with Full-Text Search & SSR",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["TypeScript", "Next.js", "React", "Tailwind CSS", "Git"],
            "non_tech_competencies": ["Content Architecture", "Search Indexing", "SEO Optimization"],
            "executive_summary": "Software engineering teams need fast, easily navigable technical documentation. This project builds a static and server-rendered markdown documentation engine with client-side full-text search and syntax highlighting.",
            "architecture_summary": "Server-rendered documentation system parsing MDX files with frontmatter, generating table-of-contents, and indexing content with FlexSearch.",
            "key_features": [
                "MDX parsing pipeline with custom React components, syntax highlighting, and code copy buttons",
                "In-memory full-text search index (FlexSearch) returning highlighted search results in < 10ms",
                "Dynamic nested sidebar navigation generated automatically from folder directory hierarchy",
                "Automated SEO meta tags, OpenGraph previews, and canonical URL generation"
            ],
            "roadmap": [
                "Milestone 1: File system MDX loader and frontmatter schema validation with Zod",
                "Milestone 2: Markdown rendering components with Prism/Shiki code syntax highlighting",
                "Milestone 3: Client-side search modal with keyboard navigation (Cmd+K / Ctrl+K shortcut)",
                "Milestone 4: Lighthouse performance audit achieving 95+ scores across Performance, Accessibility, and SEO"
            ],
            "industry_rubric": "Evaluates semantic HTML structure, keyboard accessibility, bundle size optimization, and clean markdown AST processing."
        },
        # Intermediate 1
        {
            "id": "fs-int-01",
            "title": "Real-Time Collaborative Whiteboard with Next.js, WebSockets & Redis Pub/Sub",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["TypeScript", "React", "Next.js", "Redis", "Docker"],
            "non_tech_competencies": ["Real-Time Collaboration", "WebSocket Architecture", "Conflict-Free Sync"],
            "executive_summary": "Remote design and engineering teams require shared digital spaces where multiple users can draw, write, and ideate simultaneously. This project implements a real-time collaborative canvas with WebSocket synchronization and Redis Pub/Sub.",
            "architecture_summary": "Fullstack collaborative canvas utilizing HTML5 Canvas, WebSocket bi-directional transport, and Redis Pub/Sub for horizontal scaling across nodes.",
            "key_features": [
                "HTML5 Canvas rendering engine supporting freehand drawing, shapes, and text with 60fps responsiveness",
                "Multiplayer live cursor tracking broadcasting pointer coordinates with smooth interpolation",
                "WebSocket server utilizing Redis Pub/Sub broadcasting canvas delta events across multiple server replicas",
                "Undo/redo history stack supporting local and remote action reconciliation"
            ],
            "roadmap": [
                "Milestone 1: HTML5 Canvas drawing engine with vector element serialization",
                "Milestone 2: WebSocket server implementation handling user connection rooms and heartbeat pings",
                "Milestone 3: Redis Pub/Sub integration broadcasting drawing events across distributed server instances",
                "Milestone 4: Multi-client latency stress test proving sub-30ms canvas synchronization across 10 concurrent peers"
            ],
            "industry_rubric": "Evaluates real-time event throttling (debouncing / requestAnimationFrame), WebSocket reconnection resilience, and horizontal server scalability."
        },
        # Intermediate 2
        {
            "id": "fs-int-02",
            "title": "Multi-Tenant SaaS Workspace with Role-Based Access Control, FastAPI & PostgreSQL",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "PostgreSQL", "FastAPI", "React", "Docker"],
            "non_tech_competencies": ["Multi-Tenancy", "RBAC & Authorization", "Data Isolation"],
            "executive_summary": "B2B SaaS companies must isolate corporate tenant data while providing flexible team permissions. This application implements row-level tenant isolation, hierarchical roles (Owner, Admin, Member, Viewer), and invite workflows.",
            "architecture_summary": "Multi-tenant architecture with FastAPI backend, PostgreSQL row-level security (RLS), JWT tenant claims, and Next.js frontend management console.",
            "key_features": [
                "PostgreSQL Row-Level Security (RLS) policies guaranteeing tenant data isolation at the database level",
                "Granular Role-Based Access Control (RBAC) permission checking middleware protecting sensitive API routes",
                "Team member invitation system with cryptographic email invite tokens and automatic role assignment",
                "Audit log recording all critical tenant mutations with actor ID, timestamp, and IP address"
            ],
            "roadmap": [
                "Milestone 1: Multi-tenant relational schema design with tenant_id foreign keys and RLS policies",
                "Milestone 2: FastAPI auth middleware verifying JWT claims and injecting active tenant context",
                "Milestone 3: Next.js team management console with member table and permission toggles",
                "Milestone 4: Security test asserting zero cross-tenant data leakage under forced ID parameter tampering"
            ],
            "industry_rubric": "Evaluates understanding of B2B multi-tenancy models (shared schema vs isolated schema), robust RBAC enforcement, and data privacy safeguards."
        },
        # Intermediate 3
        {
            "id": "fs-int-03",
            "title": "High-Performance Media Asset Management System with Presigned S3 Uploads & Sharp",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["TypeScript", "Next.js", "Node.js", "AWS", "Docker"],
            "non_tech_competencies": ["Direct-to-Cloud Uploads", "Media Processing", "CDN Caching"],
            "executive_summary": "Uploading large images and video files directly to web application servers exhausts server memory and ties up worker threads. This service implements direct-to-S3 presigned uploads with background thumbnail optimization via Sharp.",
            "architecture_summary": "Media pipeline generating S3 presigned PUT URLs, receiving S3 upload webhooks, and generating multi-resolution WebP variants via Sharp.",
            "key_features": [
                "Direct browser-to-S3 upload using cryptographically signed presigned URLs with size and MIME type restrictions",
                "Asynchronous background image processing generating WebP and AVIF responsive thumbnail variants",
                "CloudFront CDN caching distribution with cache invalidation triggers on asset updates",
                "Media gallery UI with lazy loading, blurred placeholders, and infinite scroll pagination"
            ],
            "roadmap": [
                "Milestone 1: AWS S3 bucket configuration with strict CORS rules and IAM least-privilege credentials",
                "Milestone 2: API route generating presigned upload URLs with client-side direct upload progress bars",
                "Milestone 3: Image resizing worker utilizing Sharp to generate optimized responsive variants",
                "Milestone 4: End-to-end test validating upload of 25MB RAW image and instant WebP thumbnail generation"
            ],
            "industry_rubric": "Evaluates architectural understanding of direct-to-cloud uploads, asynchronous media optimization, CDN edge caching, and mobile-friendly responsive images."
        },
        # Intermediate 4
        {
            "id": "fs-int-04",
            "title": "Asynchronous Job Processing Dashboard with Celery, Redis & SSE Live Streaming",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "FastAPI", "Redis", "React", "Docker"],
            "non_tech_competencies": ["Asynchronous Workflows", "Server-Sent Events", "Background Workers"],
            "executive_summary": "Long-running computational tasks (PDF report generation, bulk email dispatch, CSV exports) time out standard HTTP requests. This system dispatches jobs to background Celery workers and streams real-time progress to clients via SSE.",
            "architecture_summary": "Decoupled architecture: FastAPI API producer, Redis message broker, Celery worker pool, and Server-Sent Events (SSE) streaming progress to a React UI.",
            "key_features": [
                "Asynchronous task queue with Celery and Redis supporting job cancellation, priority queues, and retries",
                "Server-Sent Events (SSE) streaming live 0-100% progress updates without heavy polling overhead",
                "Dead-letter retry strategy with exponential backoff for network-dependent background tasks",
                "Real-time administrative job monitor dashboard displaying active, completed, and failed worker jobs"
            ],
            "roadmap": [
                "Milestone 1: Celery worker configuration with Redis broker and result backend",
                "Milestone 2: Background task definitions (CSV report aggregation) with progress event hooks",
                "Milestone 3: FastAPI SSE endpoint streaming progress updates to frontend event listeners",
                "Milestone 4: Chaos test simulating worker crash and asserting automatic task retry recovery"
            ],
            "industry_rubric": "Evaluates asynchronous distributed task patterns, avoiding client HTTP timeouts, efficient SSE vs polling tradeoffs, and worker resilience."
        },
        # Advanced 1
        {
            "id": "fs-adv-01",
            "title": "Production E-Commerce Platform with Stripe Checkout, Webhook Idempotency & Algolia Search",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["TypeScript", "Next.js", "PostgreSQL", "Docker", "Tailwind CSS"],
            "non_tech_competencies": ["Payment Security & Compliance", "Webhook Idempotency", "Search UX"],
            "executive_summary": "E-commerce stores must handle inventory race conditions, payment fraud, and sudden traffic surges without losing customer orders. This platform integrates Stripe Checkout, transactional inventory decrements, and instant typo-tolerant search.",
            "architecture_summary": "Fullstack Next.js 14 e-commerce application with PostgreSQL transactional consistency, Stripe webhook handlers, and Algolia search indexing.",
            "key_features": [
                "Stripe Checkout session orchestration with webhook idempotency handling preventing double-fulfillment",
                "PostgreSQL transactional inventory reservations with row locks (SELECT FOR UPDATE) preventing overselling",
                "Typo-tolerant product catalog search and multi-facet filtering powered by Algolia",
                "Customer order dashboard with order history, PDF invoice downloading, and tracking status"
            ],
            "roadmap": [
                "Milestone 1: Relational catalog and order schema with foreign key constraints and transactional locks",
                "Milestone 2: Stripe payment intent integration and secure webhook verification endpoint",
                "Milestone 3: Real-time Algolia product indexing synchronization on inventory updates",
                "Milestone 4: Concurrent purchase load test simulating 50 customers attempting to buy the last 5 inventory units"
            ],
            "industry_rubric": "Evaluates financial transaction safety, prevention of inventory overselling race conditions, webhook idempotency keys, and PCI compliance adherence."
        },
        # Advanced 2
        {
            "id": "fs-adv-02",
            "title": "Enterprise Event-Driven Notification Engine with Kafka, Push Notifications & Email Failover",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "FastAPI", "Apache Kafka", "Redis", "Docker"],
            "non_tech_competencies": ["Event-Driven Architecture", "Multi-Channel Notification", "Rate Limiting"],
            "executive_summary": "Enterprise platforms must send millions of notifications across mobile push, SMS, and email while respecting user preferences, rate limits, and provider outages. This engine orchestrates multi-channel notifications with automatic fallback.",
            "architecture_summary": "Event-driven notification service reading Kafka event topics, checking user preference matrices in Redis, and dispatching multi-channel messages with failover.",
            "key_features": [
                "Multi-channel routing matrix (In-App -> Push -> Email -> SMS) cascading upon delivery failure",
                "Redis sliding window rate limiters preventing notification fatigue (max 3 notifications/hour per user)",
                "User notification preference engine supporting granular channel opt-outs and quiet hours",
                "Delivery receipt webhook tracking recording open rates, click-through rates, and bounce rates"
            ],
            "roadmap": [
                "Milestone 1: Kafka notification event topic definition and consumer group setup",
                "Milestone 2: Multi-provider abstraction layer (Firebase FCM for push, SendGrid for email, Twilio for SMS)",
                "Milestone 3: Redis user preference evaluation and rate limiting middleware",
                "Milestone 4: Provider outage simulation test verifying automatic fallback from push to email"
            ],
            "industry_rubric": "Evaluates event-driven decoupling, third-party provider failover architecture, rate limiting design, and notification delivery guarantees."
        },
        # Advanced 3
        {
            "id": "fs-adv-03",
            "title": "Full-Stack Observability & Error Tracking Platform with OpenTelemetry & TimescaleDB",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["TypeScript", "Next.js", "PostgreSQL", "Docker", "Linux"],
            "non_tech_competencies": ["Observability & APM", "Distributed Tracing", "Time-Series Aggregation"],
            "executive_summary": "Modern distributed applications fail in subtle, multi-service ways. This project builds an end-to-end observability and error reporting platform capturing frontend JavaScript exceptions, backend distributed traces, and server metrics.",
            "architecture_summary": "Fullstack telemetry platform receiving OpenTelemetry trace spans and client exception payloads, persisting into TimescaleDB time-series hypertable.",
            "key_features": [
                "Frontend error interception SDK capturing unhandled rejections, stack traces, and user breadcrumbs",
                "OpenTelemetry trace collector correlating frontend clicks with backend API spans and SQL query timings",
                "TimescaleDB time-series storage with automated continuous aggregates for P50, P95, and P99 latency charts",
                "Alerting engine dispatching alerts when error rate spikes exceed standard statistical deviation thresholds"
            ],
            "roadmap": [
                "Milestone 1: Ingestion API accepting OpenTelemetry spans and client error reports",
                "Milestone 2: TimescaleDB hypertable schema design with data retention and compression policies",
                "Milestone 3: Next.js analytical dashboard displaying trace waterfall timelines and error flamegraphs",
                "Milestone 4: End-to-end integration test tracing a user click through Next.js, API, and database"
            ],
            "industry_rubric": "Evaluates deep mastery of observability principles (Logs, Metrics, Traces), OpenTelemetry standards, time-series database indexing, and trace waterfall visualization."
        },
        # Advanced 4
        {
            "id": "fs-adv-04",
            "title": "Scalable Modular CMS & Micro-Frontend Architecture with Edge Middleware & SSR Caching",
            "difficulty": "Advanced",
            "hours": 40,
            "primary_skills": ["TypeScript", "Next.js", "React", "PostgreSQL", "Docker"],
            "non_tech_competencies": ["Edge Computing", "Micro-Frontend Composition", "Cache Invalidation"],
            "executive_summary": "Global digital publications demand instant page loads from edge nodes while allowing editors to publish breaking updates without manual cache clearing. This project implements an Edge-rendered CMS with stale-while-revalidate caching and micro-frontends.",
            "architecture_summary": "Edge-first Next.js architecture with Vercel/Cloudflare Edge Middleware, on-demand ISR (Incremental Static Regeneration), and headless CMS data layer.",
            "key_features": [
                "Edge Middleware routing evaluating user geolocation, A/B testing variants, and auth cookies in < 5ms",
                "On-Demand Incremental Static Regeneration (ISR) revalidating specific article pages via webhooks in < 300ms",
                "Modular micro-frontend architecture allowing independent teams to deploy header, catalog, and checkout modules",
                "Comprehensive caching strategy combining Edge Cache-Control, stale-while-revalidate, and surrogate keys"
            ],
            "roadmap": [
                "Milestone 1: Headless CMS schema and PostgreSQL relational content storage layer",
                "Milestone 2: Next.js Edge Middleware implementing custom request routing and A/B variant assignment",
                "Milestone 3: On-demand cache invalidation webhook handler purging stale static pages",
                "Milestone 4: Global performance benchmark verifying sub-100ms TTFB across worldwide synthetic testing nodes"
            ],
            "industry_rubric": "Evaluates edge computing paradigms, cache invalidation strategies (surrogate keys, ISR), micro-frontend composition, and global CDN delivery."
        }
    ]
}
