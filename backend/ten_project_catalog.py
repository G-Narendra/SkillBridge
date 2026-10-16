"""
SkillBridge AI - 10-Project Production Matrix Catalog.
Provides 10 comprehensive, industry-grade project blueprints (2 Beginner, 4 Intermediate, 4 Advanced)
for every primary technical discipline, with deep technical detail, architecture patterns,
milestone roadmaps, and automated starter code generation.
"""

from typing import Dict, List, Any, Optional

TEN_PROJECT_MATRICES: Dict[str, List[Dict[str, Any]]] = {
    # -------------------------------------------------------------------------
    # 1. Backend Systems & API Engineering (10 Projects)
    # -------------------------------------------------------------------------
    "backend_systems": [
        # Beginner 1
        {
            "id": "be-beg-01",
            "title": "Clean Architecture RESTful Inventory API with SQLite & Pytest",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "FastAPI", "SQLite", "pytest"],
            "non_tech_competencies": ["Clean Architecture", "Unit Testing", "API Documentation", "Git Hygiene"],
            "executive_summary": "Small to medium logistics operations require reliable item tracking without heavy database clusters. This service provides robust inventory tracking with validation, deterministic testing, and Swagger docs.",
            "architecture_summary": "Three-layer architecture (Controllers -> Services -> Repository) using FastAPI and SQLite with Pydantic v2 schemas and pytest test suite.",
            "key_features": [
                "Typed CRUD operations for stock items, SKUs, and categories",
                "Strict request/response validation with Pydantic v2",
                "Isolated SQLite database layer with transactional commits",
                "Comprehensive unit and integration test suite with > 85% coverage"
            ],
            "roadmap": [
                "Milestone 1: Domain models, Pydantic schemas, and in-memory repository",
                "Milestone 2: SQLite database connector, table migrations, and transactional CRUD",
                "Milestone 3: FastAPI REST route handlers, custom error handling, and Swagger docs",
                "Milestone 4: Automated pytest suite, test fixtures, and GitHub Actions CI workflow"
            ],
            "industry_rubric": "Evaluates clean code structure, separation of business logic from HTTP layer, meaningful assertions in tests, and absence of hardcoded values."
        },
        # Beginner 2
        {
            "id": "be-beg-02",
            "title": "JWT Authenticated User Session Service with Argon2 & PostgreSQL",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "PostgreSQL", "FastAPI", "SQLAlchemy"],
            "non_tech_competencies": ["Security Mindset", "Database Migrations", "API Design"],
            "executive_summary": "Modern web applications require stateless, cryptographically secure authentication. This microservice implements user registration, login, Argon2 password hashing, and signed JWT issuance.",
            "architecture_summary": "Service-oriented auth layer using FastAPI, SQLAlchemy 2.0 async sessions, PostgreSQL persistence, and Alembic migrations.",
            "key_features": [
                "User registration with unique email constraints and password complexity checks",
                "Argon2id password hashing to prevent brute-force and timing attacks",
                "Stateless JWT access and refresh token lifecycle management",
                "Alembic database migrations and automated PostgreSQL schema generation"
            ],
            "roadmap": [
                "Milestone 1: PostgreSQL schema design and Alembic migration setup",
                "Milestone 2: Cryptographic hashing service and JWT token encoder/decoder",
                "Milestone 3: Signup, login, and token refresh route endpoints with rate-limiting",
                "Milestone 4: Auth middleware testing with pytest, mocking database calls"
            ],
            "industry_rubric": "Evaluates secure token handling, avoidance of plain-text passwords, SQL injection protection via parameterized ORM, and error message security."
        },
        # Intermediate 1
        {
            "id": "be-int-01",
            "title": "High-Throughput E-Commerce Order Processing API with Redis Caching",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
            "non_tech_competencies": ["Cache-Aside Pattern", "Transaction Safety", "Docker Containerization"],
            "executive_summary": "High-traffic retail platforms experience read-heavy catalog queries and write-heavy order checkouts. This service implements a cache-aside architecture with Redis and transactional PostgreSQL checkouts.",
            "architecture_summary": "Layered FastAPI service with Redis cache-aside layer, PostgreSQL ACID transactions with row-level locking for inventory, and Docker Compose topology.",
            "key_features": [
                "Read-through / Cache-aside product catalog with Redis TTL invalidation",
                "ACID transaction order placement with row-level locks preventing double-spending",
                "Docker Compose environment orchestrating PostgreSQL, Redis, and FastAPI",
                "Prometheus metrics middleware tracking latency and cache hit/miss ratio"
            ],
            "roadmap": [
                "Milestone 1: Product and Order relational data models with index optimization",
                "Milestone 2: Redis caching client with automatic TTL expiration and cache-busting",
                "Milestone 3: Atomic checkout transaction service with inventory reservation",
                "Milestone 4: Dockerfile, docker-compose.yml, and Locust load testing suite"
            ],
            "industry_rubric": "Evaluates cache stampede prevention, correct rollback on partial failure, Docker multi-stage build efficiency, and p99 latency under concurrency."
        },
        # Intermediate 2
        {
            "id": "be-int-02",
            "title": "Asynchronous Background Task Queue & Email Dispatcher with Celery & RabbitMQ",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "Celery", "RabbitMQ", "Redis", "Docker"],
            "non_tech_competencies": ["Asynchronous Architecture", "Dead-Letter Queues", "System Observability"],
            "executive_summary": "Long-running operations (PDF generation, notifications, data export) must never block HTTP threads. This service offloads heavy workloads to asynchronous worker pools with automatic retries and dead-letter queues.",
            "architecture_summary": "Message-driven worker cluster using Celery, RabbitMQ broker, Redis result backend, and supervisor health monitoring.",
            "key_features": [
                "Decoupled asynchronous task dispatching with non-blocking HTTP acknowledgment",
                "Exponential backoff retry policy for transient third-party email failures",
                "Dead-letter exchange (DLX) routing unrecoverable tasks for human inspection",
                "Flower monitoring dashboard for real-time worker throughput telemetry"
            ],
            "roadmap": [
                "Milestone 1: Celery application configuration with RabbitMQ broker and Redis backend",
                "Milestone 2: Task definitions for batch notification and report generation",
                "Milestone 3: Retry decorators with jitter and dead-letter queue routing",
                "Milestone 4: Multi-container Docker Compose with worker autoscaling and Flower UI"
            ],
            "industry_rubric": "Evaluates task idempotency, prevention of message loss during worker crash, clean separation of producer/consumer, and graceful shutdown handling."
        },
        # Intermediate 3
        {
            "id": "be-int-03",
            "title": "Multi-Tenant SaaS Subscription & Billing API with Stripe Webhooks",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["Python", "FastAPI", "PostgreSQL", "Stripe API", "Docker"],
            "non_tech_competencies": ["Multi-Tenancy Isolation", "Webhook Idempotency", "PCI Compliance Awareness"],
            "executive_summary": "SaaS businesses require strict data isolation between corporate tenants and automated subscription lifecycle management through Stripe payment events.",
            "architecture_summary": "Shared database with tenant-discriminator column architecture, HMAC cryptographic webhook signature verification, and idempotency key handling.",
            "key_features": [
                "Tenant context middleware extracting tenant_id from JWT claims",
                "Stripe Webhook handler with cryptographic payload signature verification",
                "Idempotent event processing preventing duplicate credits or subscription renewals",
                "Customer portal integration and tiered subscription quota enforcement"
            ],
            "roadmap": [
                "Milestone 1: Multi-tenant database schemas with foreign key tenant scoping",
                "Milestone 2: Stripe checkout session generation and customer customer mapping",
                "Milestone 3: Webhook processing engine with signature verification and event logging",
                "Milestone 4: Tier-based quota middleware and end-to-end webhook replay tests"
            ],
            "industry_rubric": "Evaluates strict isolation preventing cross-tenant data leaks, rejection of unverified webhooks, and idempotent database mutations."
        },
        # Intermediate 4
        {
            "id": "be-int-04",
            "title": "Automated Database Migration & Query Optimization Suite with PostgreSQL EXPLAIN",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Python", "PostgreSQL", "SQL", "Alembic", "pytest"],
            "non_tech_competencies": ["Query Optimization", "Index Strategy", "Technical Documentation"],
            "executive_summary": "Unindexed queries and reckless schema migrations cause costly production downtime. This suite benchmarks SQL query plans, detects sequential scans, and runs safe backward-compatible Alembic migrations.",
            "architecture_summary": "Database benchmarking test harness utilizing PostgreSQL EXPLAIN ANALYZE, pg_stat_statements, and automated migration verification.",
            "key_features": [
                "Automated migration verification asserting backward compatibility on rollbacks",
                "CI query linter parsing EXPLAIN ANALYZE to detect full table scans on > 10K rows",
                "Composite B-tree and partial index optimization benchmarks",
                "Synthetic realistic data seeder populating 100,000 relational rows"
            ],
            "roadmap": [
                "Milestone 1: Large-scale relational schema with synthetic seeder script",
                "Milestone 2: Alembic up/down migration test harness verifying rollback safety",
                "Milestone 3: Query analyzer script parsing cost, execution time, and index usage",
                "Milestone 4: Performance comparison reports before and after indexing"
            ],
            "industry_rubric": "Evaluates deep SQL understanding (B-Tree vs Hash vs GIN), index write overhead awareness, and zero-downtime migration strategies (e.g. concurrent indexing)."
        },
        # Advanced 1
        {
            "id": "be-adv-01",
            "title": "Distributed Event-Driven Order Saga Orchestrator with Apache Kafka",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "Apache Kafka", "FastAPI", "PostgreSQL", "Docker"],
            "non_tech_competencies": ["Distributed Consensus", "Eventual Consistency", "Compensating Transactions"],
            "executive_summary": "In microservice architectures, distributed transactions across multiple services cannot rely on two-phase commit. This system implements an event-driven Saga pattern coordinating Payment, Inventory, and Shipping via Kafka.",
            "architecture_summary": "Choreographed Saga architecture using Apache Kafka event topics, transactional outbox pattern, and compensating transactions on failure.",
            "key_features": [
                "Transactional Outbox pattern ensuring atomic database update and message publishing",
                "Compensating transaction workflows rolling back inventory if payment fails",
                "Idempotent Kafka event consumers with consumer group partition rebalancing",
                "End-to-end distributed transaction tracing with Correlation ID propagation"
            ],
            "roadmap": [
                "Milestone 1: Kafka broker setup, topic schema contracts, and Avro/JSON serialization",
                "Milestone 2: Transactional Outbox publisher and polling relay service",
                "Milestone 3: Service consumers: OrderService, InventoryService, PaymentService",
                "Milestone 4: Chaos failure injection tests validating compensating rollbacks"
            ],
            "industry_rubric": "Evaluates mastery of distributed transactions, understanding of at-least-once delivery duplicates, and clean error recovery mechanisms."
        },
        # Advanced 2
        {
            "id": "be-adv-02",
            "title": "Zero-Downtime Microservice API Gateway with Rate-Limiting & Circuit Breakers",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Python", "FastAPI", "Redis", "Docker", "Prometheus"],
            "non_tech_competencies": ["System Resilience", "Fault Tolerance", "Traffic Management"],
            "executive_summary": "Downstream microservices can fail or get overloaded. This API Gateway acts as the frontline shield, implementing Token Bucket rate limiting, circuit breaker pattern, and reverse proxy routing.",
            "architecture_summary": "Reverse proxy gateway built on async HTTP client (httpx), Redis-backed distributed rate limiting, and Netflix Hystrix-style circuit breaker state machine.",
            "key_features": [
                "Sliding window and Token Bucket rate limiter per API key / IP address via Redis Lua scripts",
                "Circuit breaker state machine (Closed, Open, Half-Open) preventing cascading failures",
                "Dynamic reverse proxy request forwarding with header sanitization and CORS",
                "Real-time Prometheus metrics exporter for request volume, error rates, and latency"
            ],
            "roadmap": [
                "Milestone 1: Async reverse proxy core with URL path routing and header propagation",
                "Milestone 2: Distributed Redis Token Bucket rate limiting algorithm",
                "Milestone 3: Circuit breaker implementation with fallback mock responses",
                "Milestone 4: High-concurrency benchmark testing using k6 or Locust"
            ],
            "industry_rubric": "Evaluates understanding of cascading failure mitigation, non-blocking asynchronous I/O, Lua script atomicity in Redis, and clear fallback policies."
        },
        # Advanced 3
        {
            "id": "be-adv-03",
            "title": "Real-Time WebSocket Collaborative Canvas Service with Redis Pub/Sub",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["Python", "FastAPI", "WebSockets", "Redis", "Docker"],
            "non_tech_competencies": ["Real-Time Protocol Design", "State Synchronization", "Horizontal Scalability"],
            "executive_summary": "Multiplayer editing tools (like Figma or Google Docs) require sub-50ms synchronized state broadcast across clustered servers. This service coordinates real-time cursor tracking and canvas updates via WebSockets and Redis Pub/Sub.",
            "architecture_summary": "Clustered WebSocket servers synchronized across instances via Redis Pub/Sub channels, with conflict-free heartbeat detection and room isolation.",
            "key_features": [
                "Full-duplex WebSocket connection manager with ping/pong keep-alive frames",
                "Redis Pub/Sub broadcasting messages across multiple backend service instances",
                "Room-based presence tracking showing active connected collaborators",
                "Graceful disconnection handling with state persistence to PostgreSQL on session close"
            ],
            "roadmap": [
                "Milestone 1: WebSocket route handler with binary/JSON message protocol",
                "Milestone 2: Redis Pub/Sub integration for horizontal multi-server scaling",
                "Milestone 3: Room session manager and participant presence tracking",
                "Milestone 4: Multi-client automated simulation tests verifying message ordering"
            ],
            "industry_rubric": "Evaluates connection leak prevention, handling of dropped network connections, horizontal scalability without sticky sessions, and memory efficiency."
        },
        # Advanced 4
        {
            "id": "be-adv-04",
            "title": "Enterprise Cloud Audit & Compliance Engine with OpenTelemetry & Sentry",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Python", "OpenTelemetry", "PostgreSQL", "Docker", "Sentry"],
            "non_tech_competencies": ["Compliance & Governance", "Observability Engineering", "Root Cause Analysis"],
            "executive_summary": "Enterprise platforms must comply with SOC2, GDPR, and ISO standards by immutably auditing every state change and providing distributed tracing across microservices.",
            "architecture_summary": "Append-only cryptographic audit ledger with OpenTelemetry distributed trace spans, RFC 7807 problem details, and Sentry exception capture.",
            "key_features": [
                "Tamper-evident append-only audit trail with SHA-256 hash chaining",
                "OpenTelemetry instrumentation tracing request lifecycle across database and external APIs",
                "RFC 7807 Problem Details for standardized HTTP error reporting",
                "Automated compliance report export in JSON and CSV for security auditors"
            ],
            "roadmap": [
                "Milestone 1: Cryptographic hash-chained audit database table design",
                "Milestone 2: OpenTelemetry tracing SDK setup with Jaeger exporter",
                "Milestone 3: Audit middleware capturing user actions, IP address, and payload delta",
                "Milestone 4: Verification test asserting ledger integrity failure on manual row edit"
            ],
            "industry_rubric": "Evaluates understanding of audit immutability, zero-overhead tracing, clean RFC 7807 compliance, and production privacy (PII scrubbing)."
        }
    ],

    # -------------------------------------------------------------------------
    # 2. Data Analytics & Business Intelligence (10 Projects)
    # -------------------------------------------------------------------------
    "data_analytics": [
        # Beginner 1
        {
            "id": "da-beg-01",
            "title": "Exploratory Sales & Revenue Analytics Suite with Pandas & Matplotlib",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "Pandas", "Matplotlib", "SQL"],
            "non_tech_competencies": ["Data Storytelling", "Statistical Cleaning", "Metric Definition"],
            "executive_summary": "Business executives require fast, accurate analysis of retail sales to understand seasonal trends and product margin distributions. This project cleans raw transactional data and generates automated visual summaries.",
            "architecture_summary": "Modular Python data analysis package with pandas data pipeline, automated null/outlier handling, and visualization export.",
            "key_features": [
                "Automated ingestion and type casting of multi-year CSV sales transactions",
                "Statistical outlier detection using Interquartile Range (IQR) filtering",
                "Monthly revenue run-rate, gross margin, and top-selling product breakdowns",
                "Exportable publication-ready charts with clear executive annotations"
            ],
            "roadmap": [
                "Milestone 1: Dataset schema validation, handling missing records and duplicate orders",
                "Milestone 2: Descriptive statistics, revenue calculations, and product categorizations",
                "Milestone 3: Data visualizations (time-series revenue, category bar charts, scatter plots)",
                "Milestone 4: Automated markdown report generator synthesizing key business takeaways"
            ],
            "industry_rubric": "Evaluates data integrity hygiene (no silent dropna), accurate formula calculations, clean chart labeling (units, legends, titles), and business actionable insights."
        },
        # Beginner 2
        {
            "id": "da-beg-02",
            "title": "Interactive Operations & KPI Dashboard in Power BI with DAX Measures",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Power BI", "DAX", "SQL", "Excel"],
            "non_tech_competencies": ["Executive Dashboard Design", "DAX Formulation", "Stakeholder Communication"],
            "executive_summary": "Operations leaders need a centralized, interactive dashboard to monitor daily fulfillment rates, delivery bottlenecks, and customer satisfaction scores in real time.",
            "architecture_summary": "Star-schema dimensional model in Power BI with Fact and Dimension tables connected to SQL backend with calculated DAX business measures.",
            "key_features": [
                "Star schema modeling separating Fact_Orders from Dim_Customer, Dim_Date, Dim_Product",
                "Custom DAX calculations for Year-over-Year (YoY) Growth, MoM Variance, and Rolling Averages",
                "Interactive slicers, cross-filtering, and drill-through to individual transaction details",
                "Mobile and desktop optimized visual layouts with clear visual hierarchy"
            ],
            "roadmap": [
                "Milestone 1: Power Query ETL, data cleansing, and star schema relationship modeling",
                "Milestone 2: Authoring foundational and complex DAX measures (CALCULATE, SAMEPERIODLASTYEAR)",
                "Milestone 3: Designing UI/UX dashboard layout with KPI summary cards and trend visuals",
                "Milestone 4: User acceptance testing, row-level security (RLS) setup, and publishing guide"
            ],
            "industry_rubric": "Evaluates proper dimensional modeling (no bi-directional relationships on large tables), efficient DAX measures, clean dashboard layout (avoiding visual clutter), and high usability."
        },
        # Intermediate 1
        {
            "id": "da-int-01",
            "title": "Predictive Customer Churn & Cohort Retention Model with Pandas & Scikit-learn",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "Pandas", "Scikit-learn", "SQL", "Jupyter"],
            "non_tech_competencies": ["Cohort Analysis", "Feature Engineering", "Business Impact Translation"],
            "executive_summary": "Customer acquisition is 5x more expensive than customer retention. This project calculates customer cohort retention curves and builds a churn risk classification model to trigger proactive account outreach.",
            "architecture_summary": "End-to-end analytical modeling pipeline calculating monthly customer cohorts and training Logistic Regression / Random Forest classifiers to predict churn probability.",
            "key_features": [
                "Cohort analysis matrix tracking user retention percentages over 12 billing cycles",
                "Feature engineering from usage frequency, support ticket volume, and payment recency",
                "Supervised classification model with cross-validated ROC-AUC, Precision, and Recall",
                "Feature importance analysis quantifying the primary drivers of account churn"
            ],
            "roadmap": [
                "Milestone 1: Relational SQL extraction of user signup dates and recurring subscription logs",
                "Milestone 2: Triangular cohort heatmap visualization showing retention drop-offs",
                "Milestone 3: Data preprocessing (one-hot encoding, feature scaling) and model training",
                "Milestone 4: Customer risk tier segmentation and automated recommendation playbook"
            ],
            "industry_rubric": "Evaluates handling of class imbalance (SMOTE/class weights), feature leak avoidance (no future data in training set), and ability to explain model weights in plain business terms."
        },
        # Intermediate 2
        {
            "id": "da-int-02",
            "title": "Cloud Data Warehouse Dimensional Model & Transformation Pipeline with dbt & Snowflake",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Snowflake", "dbt", "SQL", "Git"],
            "non_tech_competencies": ["Kimball Dimensional Modeling", "Data Testing", "Version Controlled Analytics"],
            "executive_summary": "Modern analytics teams treat data models like software code. This project builds a production dbt project on Snowflake transforming raw transactional staging tables into clean dimensional marts.",
            "architecture_summary": "Three-layer dbt DAG (Staging -> Intermediate -> Marts) running on Snowflake with automated schema assertions and Jinja templating.",
            "key_features": [
                "Staging models standardizing column names, data types, and surrogate key generation",
                "Dimensional Kimball modeling with reusable Dim_Customers, Dim_Products, and Fact_Sales",
                "Automated dbt generic tests (unique, not_null, accepted_values, relationships)",
                "dbt documentation generation with lineage DAG visualization and column descriptions"
            ],
            "roadmap": [
                "Milestone 1: Snowflake database, warehouse, and role-based access configuration",
                "Milestone 2: dbt staging models with source freshness tests and schema.yml assertions",
                "Milestone 3: Intermediate aggregation tables and business logic transformations",
                "Milestone 4: Fact and Dimension mart models, dbt test suite, and lineage documentation"
            ],
            "industry_rubric": "Evaluates clean DAG structure (no cyclic dependencies), surrogate key hashing, idempotency of incremental models, and comprehensive dbt test coverage."
        },
        # Intermediate 3
        {
            "id": "da-int-03",
            "title": "Automated Data Quality & Anomaly Detection Engine with Great Expectations & SQL",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Python", "SQL", "PostgreSQL", "Great Expectations", "Git"],
            "non_tech_competencies": ["Data Governance", "SLA Monitoring", "Root Cause Analysis"],
            "executive_summary": "Bad data entering downstream dashboards erodes executive trust. This suite runs automated statistical checks and schema validation assertions on incoming production datasets before business consumption.",
            "architecture_summary": "Validation engine using Great Expectations and SQL query assertions with automated HTML validation report generation and Slack alert dispatching.",
            "key_features": [
                "Expectation suites validating column completeness, value ranges, and regex formats",
                "Statistical distribution checks detecting anomalous spikes in daily record volume",
                "Automated Data Docs HTML dashboard detailing historical data quality pass/fail rates",
                "CLI and CI integration failing pipelines when critical data quality rules break"
            ],
            "roadmap": [
                "Milestone 1: PostgreSQL test database populated with dirty and anomalous sample data",
                "Milestone 2: Great Expectations suite authoring for core business entity validation",
                "Milestone 3: Automated validation checkpoint runner generating Data Docs reports",
                "Milestone 4: Alerting webhook dispatching failure summaries with offending record details"
            ],
            "industry_rubric": "Evaluates preventative data engineering hygiene, clear expectation definitions, separation of warning vs critical assertions, and informative alert messaging."
        },
        # Intermediate 4
        {
            "id": "da-int-04",
            "title": "Financial Run-Rate & Operational Capacity Forecast Engine with Prophet & Python",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "Pandas", "Prophet", "SQL", "Streamlit"],
            "non_tech_competencies": ["Financial Modeling", "Scenario Planning", "Interactive UI"],
            "executive_summary": "Finance and operations teams need forward-looking forecasts to allocate capital and plan hiring. This engine uses Meta Prophet to project 12-month revenue with seasonal adjustments and what-if sliders.",
            "architecture_summary": "Time-series forecasting pipeline using Meta Prophet, historical SQL transaction data, and an interactive Streamlit simulation web app.",
            "key_features": [
                "Additive time-series decomposition into overall trend, weekly seasonality, and holiday effects",
                "Upper and lower 95% confidence intervals quantifying forecast uncertainty",
                "Interactive Streamlit web interface allowing executives to tweak growth rate assumptions",
                "Scenario simulation modeling optimistic, base-case, and conservative financial outcomes"
            ],
            "roadmap": [
                "Milestone 1: Time-series historical data ingestion, aggregation, and stationarity checks",
                "Milestone 2: Prophet model training, hyperparameter tuning, and cross-validation backtesting",
                "Milestone 3: What-if parameter engine modeling variable marketing spend and inflation",
                "Milestone 4: Interactive Streamlit application deployment with chart downloads"
            ],
            "industry_rubric": "Evaluates realistic confidence intervals, proper train/test backtesting evaluation (MAPE/RMSE), and clean interactive interface tailored for non-technical stakeholders."
        },
        # Advanced 1
        {
            "id": "da-adv-01",
            "title": "Enterprise Executive Tableau KPI Suite with BigQuery & Real-Time Sync",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Tableau", "BigQuery", "SQL", "Python"],
            "non_tech_competencies": ["Executive Presence", "Data Architecture", "Performance Tuning"],
            "executive_summary": "C-suite executives need real-time pulse of company performance across ARR, Net Burn, Customer CAC, and LTV. This project connects Tableau to Google BigQuery with partitioned query acceleration.",
            "architecture_summary": "Direct-query BigQuery BI layer connected to partitioned analytical views, with row-level security (RLS) and sub-second Tableau dashboard rendering.",
            "key_features": [
                "Partitioned and clustered BigQuery SQL views minimizing query bytes scanned and cost",
                "Executive KPI scorecard: Gross Margin, Net Retention Rate (NRR), CAC Payback Period",
                "Row-level security granting department heads access only to their specific cost centers",
                "Sub-second interactive rendering using Tableau extract and live query optimization"
            ],
            "roadmap": [
                "Milestone 1: BigQuery analytical views with date partitioning and clustering",
                "Milestone 2: Executive scorecard design with sparklines, bullet graphs, and KPI tiles",
                "Milestone 3: Row-level security user filtering and permissions matrix setup",
                "Milestone 4: Performance tuning and executive presentation rehearsal"
            ],
            "industry_rubric": "Evaluates query cost optimization (avoiding SELECT * on PB-scale tables), professional executive styling (Apple/Bloomberg standard), and robust security permissions."
        },
        # Advanced 2
        {
            "id": "da-adv-02",
            "title": "Automated Marketing Attribution & Multi-Touch Conversion Funnel Engine",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["SQL", "Python", "Pandas", "Snowflake", "dbt"],
            "non_tech_competencies": ["Attribution Modeling", "Unit Economics", "Marketing ROI"],
            "executive_summary": "Marketing budgets are wasted when companies rely on simplistic first-touch or last-touch attribution. This engine models multi-touch attribution (Linear, Time-Decay, Position-Based) across ad channels.",
            "architecture_summary": "Complex SQL and Python transformation engine mapping multi-channel customer touchpoints to ultimate deal conversion revenue in Snowflake.",
            "key_features": [
                "Session stitching algorithm resolving anonymous visitor cookies to identified user profiles",
                "Comparison models: First-Touch, Last-Touch, Linear, and 40-20-40 Position-Based attribution",
                "Channel ROI analysis calculating blended vs paid Customer Acquisition Cost (CAC)",
                "Automated weekly attribution reports advising CMO on ad budget reallocation"
            ],
            "roadmap": [
                "Milestone 1: Clickstream and conversion event schema normalization in Snowflake",
                "Milestone 2: User identity resolution and multi-touch journey windowing logic",
                "Milestone 3: Attribution model algorithms implemented in dbt SQL and verified with Python",
                "Milestone 4: Interactive visualization dashboard comparing channel values across models"
            ],
            "industry_rubric": "Evaluates window function mastery in SQL, deep comprehension of marketing metrics, and objective data-driven budget recommendations."
        },
        # Advanced 3
        {
            "id": "da-adv-03",
            "title": "Product Engagement & Feature Adoption Analytics Engine with Mixpanel / PostHog Schema",
            "difficulty": "Advanced",
            "hours": 30,
            "primary_skills": ["SQL", "Python", "PostgreSQL", "dbt", "Tableau"],
            "non_tech_competencies": ["Product Analytics", "Behavioral Segmentation", "Funnel Dropoff Analysis"],
            "executive_summary": "Product teams need to know which features drive user stickiness and where users drop off during onboarding. This project designs an event taxonomy, models funnel conversion steps, and calculates sticky ratios (DAU/MAU).",
            "architecture_summary": "Event-driven product analytics warehouse schema modeled after Mixpanel/PostHog, calculating funnel drop-offs, user session durations, and retention curves.",
            "key_features": [
                "Clean event taxonomy tracking user actions (pageview, feature_clicked, checkout_started)",
                "Multi-step conversion funnel analyzing exact drop-off percentages at each step",
                "Stickiness calculations measuring Daily Active Users / Monthly Active Users (DAU/MAU)",
                "Power User curve (L28 histogram) showing user frequency distribution over 28 days"
            ],
            "roadmap": [
                "Milestone 1: Event stream schema design and sample event generator script",
                "Milestone 2: Funnel calculation SQL queries with configurable conversion time windows",
                "Milestone 3: DAU/MAU stickiness metrics and cohort retention by signup feature",
                "Milestone 4: Product insight dashboard with actionable UI/UX friction point findings"
            ],
            "industry_rubric": "Evaluates understanding of product metrics (activation, engagement, retention), sophisticated window SQL queries, and actionable product recommendations."
        },
        # Advanced 4
        {
            "id": "da-adv-04",
            "title": "Real-Time Operational Anomaly & Fraud Detection Engine with SQL & Streamlit",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Python", "SQL", "PostgreSQL", "Pandas", "Streamlit"],
            "non_tech_competencies": ["Fraud Analysis", "Real-Time Telemetry", "Risk Mitigation"],
            "executive_summary": "Financial and e-commerce platforms suffer from fraudulent transactions and bot attacks. This engine evaluates transaction streams in real time using statistical z-scores and geographic velocity checks.",
            "architecture_summary": "Streaming analytical pipeline calculating rolling transaction volume, statistical outlier z-scores, and suspicious geographic leaps with live alert dashboard.",
            "key_features": [
                "Rolling statistical baseline calculating running mean and standard deviation per merchant",
                "Velocity checks flagging accounts making rapid consecutive transactions in different locations",
                "Configurable risk scoring matrix ranking transactions into Low, Medium, and Critical risk",
                "Live Streamlit investigator console allowing fraud analysts to review and freeze flagged transactions"
            ],
            "roadmap": [
                "Milestone 1: Transaction streaming schema and synthetic normal/fraud data generator",
                "Milestone 2: SQL window functions calculating rolling velocity and deviation scores",
                "Milestone 3: Real-time risk scoring engine assigning risk probability to new transactions",
                "Milestone 4: Analyst dashboard with transaction drill-down and one-click action triggers"
            ],
            "industry_rubric": "Evaluates false-positive rate minimization, latency of scoring pipeline, clear audit trail for compliance, and ergonomic investigator workflows."
        }
    ],

    # -------------------------------------------------------------------------
    # 3. Frontend & Web Engineering (10 Projects)
    # -------------------------------------------------------------------------
    "frontend_ui": [
        # Beginner 1
        {
            "id": "fe-beg-01",
            "title": "Accessible Component Design System & UI Library in React with Tailwind CSS",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["React", "TypeScript", "Tailwind CSS", "Storybook", "Jest"],
            "non_tech_competencies": ["Design System Alignment", "Accessibility (WCAG)", "Component Architecture"],
            "executive_summary": "Engineering teams need consistent, reusable UI building blocks that comply with accessibility standards. This library provides buttons, modals, dropdowns, and form inputs with dark/light mode and Storybook docs.",
            "architecture_summary": "Component-driven design system built with React, TypeScript, Tailwind CSS, Storybook documentation, and automated Jest/React Testing Library tests.",
            "key_features": [
                "WCAG 2.1 AA compliant components with keyboard navigation and ARIA attributes",
                "Comprehensive design tokens (colors, spacing, typography) with dark/light themes",
                "Interactive Storybook catalog documenting props, variants, and interactive states",
                "Unit tests verifying focus trapping, keyboard Enter/Esc triggers, and click handlers"
            ],
            "roadmap": [
                "Milestone 1: Design tokens, Tailwind CSS configuration, and TypeScript type contracts",
                "Milestone 2: Atomic components (Button, Input, Badge, Tooltip) with accessible states",
                "Milestone 3: Compound components (Modal, Dropdown, Accordion) with keyboard focus management",
                "Milestone 4: Storybook interactive documentation and automated Jest component test suite"
            ],
            "industry_rubric": "Evaluates strict adherence to WCAG accessibility guidelines, clean prop interfaces, zero CSS specificity wars, and 100% TypeScript coverage."
        },
        # Beginner 2
        {
            "id": "fe-beg-02",
            "title": "Responsive Product Catalog & Shopping Cart with React & LocalStorage",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["React", "TypeScript", "Tailwind CSS", "LocalStorage"],
            "non_tech_competencies": ["Client-Side State", "Responsive Design", "User Experience Empathy"],
            "executive_summary": "Online storefronts must load instantly, adapt gracefully to mobile devices, and persist customer shopping carts across browser tabs. This project implements an interactive catalog with cart management.",
            "architecture_summary": "Single Page Application using React, custom Context API hooks for state management, LocalStorage persistence, and responsive Tailwind CSS layout.",
            "key_features": [
                "Category filtering, price range sorting, and instant search query debouncing",
                "Interactive slide-over shopping cart with item quantity updates and subtotal calculation",
                "LocalStorage state persistence keeping cart items intact on browser reload",
                "Responsive mobile-first layout with smooth micro-interactions and transitions"
            ],
            "roadmap": [
                "Milestone 1: Product catalog mock data, grid card layouts, and responsive breakpoints",
                "Milestone 2: Custom useCart hook managing item additions, quantity updates, and removal",
                "Milestone 3: Slide-over cart drawer with animated transitions and total calculations",
                "Milestone 4: LocalStorage sync and automated component interaction unit tests"
            ],
            "industry_rubric": "Evaluates clean hook abstraction, performance of re-renders on cart update, smooth UX on mobile viewports, and clean responsive CSS."
        },
        # Intermediate 1
        {
            "id": "fe-int-01",
            "title": "Production Next.js 14 SaaS Dashboard & Web Application with Server Components & Auth",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Next.js", "TypeScript", "React", "Tailwind CSS", "NextAuth.js"],
            "non_tech_competencies": ["SSR Performance", "SEO Best Practices", "Auth State Governance"],
            "executive_summary": "Modern web platforms require fast Server-Side Rendering (SSR) for search engine indexing and responsive client interactivity. This project implements a Next.js 14 App Router application with authentication and dashboard analytics.",
            "architecture_summary": "Next.js 14 App Router architecture combining React Server Components (RSC) for data fetching and Client Components for interactivity, secured with NextAuth.",
            "key_features": [
                "React Server Components streaming data directly with suspense boundaries and loading skeletons",
                "NextAuth.js authentication supporting credentials and OAuth with session cookies",
                "Protected dashboard routes with middleware redirecting unauthenticated users",
                "SEO optimization with automated OpenGraph tags, sitemap.xml, and semantic metadata"
            ],
            "roadmap": [
                "Milestone 1: Next.js 14 App Router layout, font optimization, and Tailwind setup",
                "Milestone 2: Server-side data fetching with streaming Suspense fallbacks",
                "Milestone 3: NextAuth integration with protected middleware routes",
                "Milestone 4: Interactive client charts and Lighthouse performance audit reaching >= 95 score"
            ],
            "industry_rubric": "Evaluates proper separation of Server vs Client components, avoidance of waterfall fetching, Lighthouse performance metrics, and clean routing structure."
        },
        # Intermediate 2
        {
            "id": "fe-int-02",
            "title": "Enterprise Kanban Task Management Board with Redux Toolkit & Drag-and-Drop",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["React", "TypeScript", "Redux Toolkit", "Tailwind CSS"],
            "non_tech_competencies": ["Complex State Management", "Performance Optimization", "User Experience Empathy"],
            "executive_summary": "Productivity platforms require smooth, responsive drag-and-drop task boards with optimistic UI updates. This project builds a multi-column Kanban board with Redux Toolkit and persistence.",
            "architecture_summary": "Component hierarchy using React, Redux Toolkit normalized entity adapters, HTML5 Drag and Drop API, and optimistic UI mutations.",
            "key_features": [
                "Multi-column workflow board (Backlog, In Progress, Review, Done) with reordering",
                "Drag-and-drop card movement across columns with visual drop target indicators",
                "Normalized Redux state slice using createEntityAdapter for O(1) card lookups",
                "Optimistic UI updates reverting state cleanly if mock backend updates fail"
            ],
            "roadmap": [
                "Milestone 1: Normalized Redux state structure and action creators for board CRUD",
                "Milestone 2: Board UI layout, column containers, and task card components",
                "Milestone 3: Drag-and-drop event handlers managing dragStart, dragOver, and drop",
                "Milestone 4: Filter chips (priority, assignee, tags) and automated state unit tests"
            ],
            "industry_rubric": "Evaluates normalized state structure (no nested objects in Redux), smooth 60fps drag animations, and resilient optimistic update error handling."
        },
        # Intermediate 3
        {
            "id": "fe-int-03",
            "title": "Real-Time Financial Crypto Ticker & Interactive Chart with WebSockets & Canvas",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["React", "TypeScript", "WebSockets", "Chart.js", "Tailwind CSS"],
            "non_tech_competencies": ["Real-Time UI Performance", "Memory Management", "Data Throttling"],
            "executive_summary": "Financial traders need millisecond updates without browser freezing or memory leaks. This project streams real-time crypto price updates via WebSockets and renders smooth interactive candlestick charts.",
            "architecture_summary": "Real-time client streaming WebSocket messages through a throttling buffer to an interactive Canvas/Chart.js rendering surface.",
            "key_features": [
                "Full-duplex WebSocket client with automated reconnection and backoff on network loss",
                "Throttled render queue preventing browser frame drops during high-frequency price ticks",
                "Interactive candlestick and line charts with timeframe switching (1m, 5m, 1h, 1d)",
                "Visual price change flash animations (green for gain, red for loss) using CSS keyframes"
            ],
            "roadmap": [
                "Milestone 1: WebSocket connection manager with connection health indicator",
                "Milestone 2: Incoming message buffer and requestAnimationFrame render scheduling",
                "Milestone 3: Interactive candlestick chart integration with zoom and tooltip inspection",
                "Milestone 4: Memory leak profiling with Chrome DevTools asserting stable RAM usage over 1 hour"
            ],
            "industry_rubric": "Evaluates prevention of React re-render thrashing, cleanup of event listeners on unmount, and zero memory leaks under 100+ events/second."
        },
        # Intermediate 4
        {
            "id": "fe-int-04",
            "title": "Comprehensive End-to-End Test Automation Suite for Web Apps with Playwright",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["TypeScript", "Playwright", "React", "GitHub Actions"],
            "non_tech_competencies": ["Test Automation Strategy", "Quality Assurance", "CI/CD Integration"],
            "executive_summary": "Manual regression testing slows down releases and misses critical UI bugs. This project builds a production Playwright test harness testing critical user journeys (login, checkout, account settings).",
            "architecture_summary": "Page Object Model (POM) test architecture using Playwright, cross-browser test matrix (Chromium, Firefox, WebKit), and CI report publishing.",
            "key_features": [
                "Page Object Model (POM) separating UI selector locators from test assertion logic",
                "Complete user journey tests: User Signup -> Cart Add -> Checkout Flow",
                "Visual regression snapshot testing detecting unintended pixel and layout shifts",
                "Automated GitHub Actions CI workflow running tests headlessly on every pull request"
            ],
            "roadmap": [
                "Milestone 1: Playwright configuration, multi-browser runners, and base Page classes",
                "Milestone 2: Auth and Navigation Page Objects with resilient ARIA locators",
                "Milestone 3: E2E scenario test authoring with mock API intercepts and network mocking",
                "Milestone 4: CI pipeline integration uploading HTML trace reports and video artifacts on failure"
            ],
            "industry_rubric": "Evaluates reliance on accessible locators (getByRole, getByText) rather than brittle CSS/XPath selectors, zero flaky sleeps, and clean Page Object structure."
        },
        # Advanced 1
        {
            "id": "fe-adv-01",
            "title": "Micro-Frontend Modular Enterprise Portal with Module Federation & Webpack 5",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["React", "TypeScript", "Webpack 5", "Module Federation", "Tailwind CSS"],
            "non_tech_competencies": ["Architecture Decoupling", "Independent Team Deployment", "Contract Testing"],
            "executive_summary": "Large organizations cannot have 50 developers committing to a single monolithic frontend. This project architecturally decouples a portal into independent micro-apps (Header, Billing, Analytics) unified via Module Federation.",
            "architecture_summary": "Host shell container dynamically mounting remote micro-frontend applications at runtime via Webpack 5 Module Federation with shared dependencies.",
            "key_features": [
                "Host shell container dynamically loading remote bundles without page reload",
                "Shared singleton dependencies (React, ReactDOM, Tailwind) preventing duplicate bundle size",
                "Cross-micro-frontend event bus coordinating authentication state and route changes",
                "Resilient error boundary wrappers displaying graceful fallbacks if a remote app goes offline"
            ],
            "roadmap": [
                "Milestone 1: Host container and remote applications Webpack 5 federation configuration",
                "Milestone 2: Shared UI component package and dependency version alignment",
                "Milestone 3: Cross-app state communication via custom events and global store",
                "Milestone 4: Resilience testing simulating remote server outages with error boundaries"
            ],
            "industry_rubric": "Evaluates deep Webpack 5 knowledge, understanding of shared dependency version collision resolution, and isolated deployment capability."
        },
        # Advanced 2
        {
            "id": "fe-adv-02",
            "title": "High-Performance Data Grid with Virtualized Scrolling & Web Workers",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["React", "TypeScript", "Web Workers", "Tailwind CSS"],
            "non_tech_competencies": ["Extreme Client Optimization", "Multithreaded JavaScript", "Memory Profiling"],
            "executive_summary": "Rendering 100,000 table rows causes browser tabs to crash due to DOM node overload. This project builds a virtualized data table rendering only the visible viewport and offloading sorting/filtering to Web Workers.",
            "architecture_summary": "DOM virtualization engine calculating dynamic row offsets, paired with a dedicated Web Worker thread for heavy CPU sorting and filtering.",
            "key_features": [
                "Custom DOM virtualization rendering only ~30 visible DOM rows out of 100,000+",
                "Dedicated Web Worker thread performing multi-column sorting and fuzzy search without blocking UI",
                "Smooth 60 FPS scrolling with dynamic row height calculation and sticky header support",
                "Column reordering, resizing, and CSV export streaming"
            ],
            "roadmap": [
                "Milestone 1: Virtual scroll viewport calculation hook (scrollTop, clientHeight, rowHeight)",
                "Milestone 2: Web Worker setup for asynchronous array sorting and filtering",
                "Milestone 3: Table UI with sticky headers, column resize handles, and row selection",
                "Milestone 4: Performance benchmarking testing 200,000 rows with Chrome DevTools performance traces"
            ],
            "industry_rubric": "Evaluates absence of main-thread lag (zero jank), minimal memory footprint, and clean worker postMessage communication architecture."
        },
        # Advanced 3
        {
            "id": "fe-adv-03",
            "title": "Offline-First Progressive Web App (PWA) with Service Workers & Background Sync",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["React", "TypeScript", "Service Workers", "IndexedDB", "PWA"],
            "non_tech_competencies": ["Offline Resilience", "Data Conflict Resolution", "Mobile-First UX"],
            "executive_summary": "Mobile field workers frequently lose internet connectivity. This PWA caches assets for offline operation, stores edits in client IndexedDB, and automatically syncs changes to the server when connection returns.",
            "architecture_summary": "Progressive Web App using Service Worker cache strategies (Stale-While-Revalidate), IndexedDB outbox storage, and Background Sync API.",
            "key_features": [
                "Service Worker caching application shell and static assets for instant offline boot",
                "IndexedDB local persistence storing draft notes and task edits while offline",
                "Background Sync queue replaying pending mutations when navigator.onLine triggers",
                "PWA install banner and manifest.json supporting native app installation on mobile and desktop"
            ],
            "roadmap": [
                "Milestone 1: Web App Manifest, Service Worker lifecycle registration, and asset caching",
                "Milestone 2: IndexedDB wrapper managing local mutation outbox queue",
                "Milestone 3: Online/offline transition listener with automatic sync engine",
                "Milestone 4: Conflict resolution handling when server records changed during offline state"
            ],
            "industry_rubric": "Evaluates thorough offline testing (Network Throttling: Offline in DevTools), deterministic conflict resolution, and Service Worker cache eviction hygiene."
        },
        # Advanced 4
        {
            "id": "fe-adv-04",
            "title": "Interactive 3D Product Customizer & Spatial Showcase with Three.js & React Three Fiber",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["React", "TypeScript", "Three.js", "React Three Fiber", "WebGL"],
            "non_tech_competencies": ["3D Graphics Optimization", "Spatial UI/UX", "GPU Memory Management"],
            "executive_summary": "Luxury e-commerce and automotive sites use 3D configurators to boost sales conversions. This project renders interactive 3D GLTF models in browser with customizable materials, lighting, and orbit controls.",
            "architecture_summary": "Declarative 3D scene built with React Three Fiber, Drei helpers, WebGL shaders, and smooth camera transitions.",
            "key_features": [
                "GLTF/GLB model loading with Draco compression for fast network delivery",
                "Real-time material customization (colors, roughness, metallic sheen, textures)",
                "Dynamic lighting environment maps with realistic shadows and ambient occlusion",
                "Responsive camera transitions focusing on specific product component hot-spots"
            ],
            "roadmap": [
                "Milestone 1: R3F Canvas setup, orbit controls, and lighting environment",
                "Milestone 2: Optimized GLTF model loading with Suspense loading states",
                "Milestone 3: Material configuration state machine allowing live color/texture swapping",
                "Milestone 4: GPU performance profiling ensuring consistent 60 FPS on mobile devices"
            ],
            "industry_rubric": "Evaluates WebGL memory disposal on unmount (preventing GPU memory leaks), Draco geometry compression, and responsive touch controls on mobile."
        }
    ],

    # -------------------------------------------------------------------------
    # 4. DevOps, SRE & Cloud Platform (10 Projects)
    # -------------------------------------------------------------------------
    "devops_platform": [
        {
            "id": "do-beg-01",
            "title": "Docker Multi-Stage Containerization & Linting Pipeline with GitHub Actions",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Docker", "Linux", "GitHub Actions", "Bash"],
            "non_tech_competencies": ["Container Hygiene", "CI/CD Basics", "Least-Privilege Security"],
            "executive_summary": "Bloated Docker images waste bandwidth and introduce security vulnerabilities. This project builds optimized multi-stage Dockerfiles with non-root execution and automated GitHub Actions builds.",
            "architecture_summary": "Multi-stage Docker build pipeline separating build dependencies from minimal scratch/alpine runtime images, linted with Hadolint in CI.",
            "key_features": [
                "Multi-stage Docker build reducing production image size by > 70%",
                "Non-root system user configuration preventing privilege escalation attacks",
                "Automated Hadolint Dockerfile linting enforcing container best practices",
                "GitHub Actions workflow building, testing, and pushing images to GitHub Container Registry"
            ],
            "roadmap": [
                "Milestone 1: Base image selection, multi-stage layers, and dependency cache mounting",
                "Milestone 2: Security hardening with unprivileged appuser and minimal runtime packages",
                "Milestone 3: Healthcheck directives and lightweight entrypoint scripts",
                "Milestone 4: GitHub Actions matrix build and container vulnerability scan"
            ],
            "industry_rubric": "Evaluates image size reduction, absence of root execution, clean cache utilization, and passing vulnerability scans."
        },
        {
            "id": "do-beg-02",
            "title": "Automated Linux Server Baseline & Hardening Suite with Bash & Cron",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Linux", "Bash", "SSH", "UFW Firewall"],
            "non_tech_competencies": ["OS Hardening", "Automation Scripting", "System Administration"],
            "executive_summary": "Unconfigured cloud virtual machines are targeted by brute-force bots within minutes. This project scripts automated server provisioning, SSH key authentication, UFW firewall rules, and unattended security updates.",
            "architecture_summary": "Idempotent Bash provisioning scripts setting up CIS Level-1 security baselines, Fail2ban intrusion prevention, and logrotate daemon configs.",
            "key_features": [
                "Automated SSH hardening disabling password authentication and root login",
                "UFW firewall configuration restricting ingress ports to SSH, HTTP, and HTTPS",
                "Fail2ban intrusion prevention banning IPs with repeated SSH authentication failures",
                "Nightly cron automation executing unattended security updates and disk space checks"
            ],
            "roadmap": [
                "Milestone 1: Shell script scaffolding with strict error checking (set -euo pipefail)",
                "Milestone 2: User management, sudoer permissions, and SSH authorized_keys setup",
                "Milestone 3: UFW firewall and Fail2ban jail configurations",
                "Milestone 4: Automated verification tests asserting open ports and banned rogue IPs"
            ],
            "industry_rubric": "Evaluates script idempotency (safe to re-run multiple times), error trapping, and adherence to security baselines."
        },
        {
            "id": "do-int-01",
            "title": "Modular Cloud Infrastructure as Code with Terraform & AWS VPC",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Terraform", "AWS", "Linux", "Git"],
            "non_tech_competencies": ["Infrastructure as Code", "Network Topologies", "Cloud Cost Awareness"],
            "executive_summary": "Manual AWS console provisioning leads to configuration drift and security blindspots. This project authors reusable Terraform modules for a production-ready AWS VPC with public/private subnets and NAT gateways.",
            "architecture_summary": "Modular Terraform architecture utilizing remote S3 state storage, DynamoDB state locking, and multi-environment workspaces (dev, staging, prod).",
            "key_features": [
                "Reusable VPC module with multi-AZ public and private subnets and NAT Gateway routing",
                "Remote Terraform backend in AWS S3 with state encryption and DynamoDB locking",
                "Security Groups following least-privilege principle isolating backend DB from public internet",
                "tflint and checkov security policy scans integrated into pull request workflows"
            ],
            "roadmap": [
                "Milestone 1: Remote state S3 bucket and DynamoDB lock table provisioning",
                "Milestone 2: Modular VPC network design with CIDR calculations and routing tables",
                "Milestone 3: Security Groups and Bastion host EC2 instance configuration",
                "Milestone 4: Automated terraform plan/apply CI workflow and Checkov compliance check"
            ],
            "industry_rubric": "Evaluates clean module parameterization, avoidance of hardcoded region/CIDR strings, remote state locking, and secure IAM definitions."
        },
        {
            "id": "do-int-02",
            "title": "High-Availability Kubernetes Container Cluster with Ingress & Probes",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["Kubernetes", "Docker", "Helm", "Linux"],
            "non_tech_competencies": ["Container Orchestration", "Traffic Ingress", "Zero-Downtime Deployments"],
            "executive_summary": "Production microservices need automated self-healing, rolling updates without downtime, and ingress traffic routing. This project packages applications as Helm charts deployed to a Kubernetes cluster.",
            "architecture_summary": "Declarative Kubernetes cluster topology managed via Helm charts, with Nginx Ingress Controller, cert-manager TLS certificates, and Horizontal Pod Autoscalers.",
            "key_features": [
                "Deployments with rolling update strategies and readiness/liveness health probes",
                "ConfigMaps and Secrets separation managing environment variables securely",
                "Nginx Ingress Controller routing hostnames to specific internal ClusterIP services",
                "Horizontal Pod Autoscaler (HPA) dynamically scaling replicas based on CPU/Memory thresholds"
            ],
            "roadmap": [
                "Milestone 1: Kubernetes manifest scaffolding (Deployment, Service, Ingress, ConfigMap)",
                "Milestone 2: Packaging manifests into a configurable Helm chart with values.yaml",
                "Milestone 3: Ingress routing and TLS certificate provisioning via cert-manager",
                "Milestone 4: Zero-downtime rolling update load test using k6 simulating continuous traffic"
            ],
            "industry_rubric": "Evaluates accurate probe configuration (avoiding premature pod restart loops), resource requests/limits definitions, and zero dropped requests during rolling deploys."
        },
        {
            "id": "do-int-03",
            "title": "Declarative CI/CD Pipeline with Automated Security Scans (Trivy & Semgrep)",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["GitHub Actions", "Docker", "Linux", "Git"],
            "non_tech_competencies": ["DevSecOps Hygiene", "Build Optimization", "Pipeline Security"],
            "executive_summary": "Vulnerable dependencies and leaked API keys must be caught before code reaches production. This CI/CD pipeline implements a DevSecOps gate scanning source code (SAST), dependencies (SCA), and Docker images.",
            "architecture_summary": "Multi-stage GitHub Actions pipeline combining parallel linting, automated unit testing, Semgrep static analysis, and Trivy container vulnerability scanning.",
            "key_features": [
                "Parallel job execution matrix optimizing CI pipeline execution to under 3 minutes",
                "Semgrep static application security testing (SAST) blocking SQL injections and hardcoded secrets",
                "Trivy vulnerability scanner failing builds on CRITICAL or HIGH severity CVEs",
                "Automated artifact caching for pip/npm modules reducing pipeline runtime"
            ],
            "roadmap": [
                "Milestone 1: GitHub Actions workflow file design with branch protection rules",
                "Milestone 2: Test matrix runner with dependency caching and coverage threshold enforcement",
                "Milestone 3: Security scanner jobs: Secret scanning (Gitleaks) and image scanning (Trivy)",
                "Milestone 4: Automated PR status check reporter publishing security summary comments"
            ],
            "industry_rubric": "Evaluates pipeline speed, clear failure logs, prevention of secret exposure in logs, and deterministic pass/fail exit codes."
        },
        {
            "id": "do-int-04",
            "title": "Production SRE Observability Stack with Prometheus, Grafana & Sentry",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Prometheus", "Grafana", "Docker", "Linux", "Sentry"],
            "non_tech_competencies": ["SRE Observability", "Alert Threshold Design", "SLA/SLO Monitoring"],
            "executive_summary": "Engineers cannot fix what they cannot see. This observability stack collects system metrics, application request latencies, and exception traces, visualizing them on production Grafana dashboards with Slack alerts.",
            "architecture_summary": "Prometheus metric scraping engine paired with Grafana visualization, Node Exporter host telemetry, and Sentry application crash tracing.",
            "key_features": [
                "Prometheus scrape jobs collecting RED metrics (Rate, Errors, Duration) from services",
                "Node Exporter monitoring server host hardware metrics (CPU load, memory saturation, disk I/O)",
                "Grafana dashboard with p50, p95, and p99 latency heatmaps and error rate percentage panels",
                "Alertmanager rules triggering notifications when error budget burn rates spike"
            ],
            "roadmap": [
                "Milestone 1: Docker Compose deployment of Prometheus, Grafana, and Node Exporter",
                "Milestone 2: Instrumenting Python/Node backend service with Prometheus client metrics",
                "Milestone 3: Authoring Grafana dashboards visualizing golden signals of monitoring",
                "Milestone 4: Alertmanager webhook configuration testing high-load simulated alert triggers"
            ],
            "industry_rubric": "Evaluates golden signal instrumentation (Latency, Traffic, Errors, Saturation), clear alert routing without alert fatigue, and reproducible dashboard JSON exports."
        },
        {
            "id": "do-adv-01",
            "title": "GitOps Continuous Deployment Pipeline with ArgoCD & Kubernetes Helm",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Kubernetes", "Helm", "Git", "Linux"],
            "non_tech_competencies": ["GitOps Paradigm", "Configuration Drift Remediation", "Declarative Operations"],
            "executive_summary": "Direct kubectl edits in production cause dangerous configuration drift. This GitOps pipeline uses ArgoCD to treat Git as the single source of truth, continuously reconciling cluster state to git commits.",
            "architecture_summary": "GitOps controller architecture using ArgoCD deployed on Kubernetes, monitoring a dedicated infrastructure repository and executing automated drift reconciliation.",
            "key_features": [
                "ArgoCD declarative Application and App-of-Apps pattern managing multi-service deployments",
                "Automated sync policies with self-healing reverting unauthorized manual cluster mutations",
                "Canary deployment rollouts using Argo Rollouts with automated metric analysis rollback",
                "Fine-grained RBAC permissions mapping engineering roles to specific cluster namespaces"
            ],
            "roadmap": [
                "Milestone 1: ArgoCD installation and infrastructure git repository setup",
                "Milestone 2: Declarative Helm chart packaging and Application manifests",
                "Milestone 3: Automated drift reconciliation and self-healing verification tests",
                "Milestone 4: Argo Rollouts canary deployment with automated rollback on error spike"
            ],
            "industry_rubric": "Evaluates pure declarative state (no imperative scripts), proper secret management (e.g. SealedSecrets / ExternalSecrets), and automated rollback safety."
        },
        {
            "id": "do-adv-02",
            "title": "Multi-Region Active-Active Cloud Architecture with Terraform & Route53",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Terraform", "AWS", "Linux", "Docker"],
            "non_tech_competencies": ["Disaster Recovery Strategy", "High Availability", "Latency-Based Routing"],
            "executive_summary": "Cloud region outages (e.g. us-east-1) can take down global businesses. This project architectures an active-active deployment across two AWS regions (us-east-1 and eu-west-1) with Route53 latency routing.",
            "architecture_summary": "Multi-region Terraform deployment provisioning identical VPCs, ECS/EKS clusters, and DynamoDB Global Tables, connected via Route53 health checks.",
            "key_features": [
                "Terraform provider aliasing deploying identical infrastructure stacks across two regions",
                "AWS Route53 latency-based routing directing users to the closest healthy geographical region",
                "Automated DNS failover routing 100% of traffic to the backup region if health probes fail",
                "DynamoDB Global Tables with multi-region bidirectional replication"
            ],
            "roadmap": [
                "Milestone 1: Multi-region Terraform modular setup and provider configuration",
                "Milestone 2: Replicated compute cluster provisioning in primary and secondary regions",
                "Milestone 3: Route53 health check probes and latency DNS routing policy",
                "Milestone 4: Disaster recovery simulation: terminating primary cluster and asserting zero-downtime DNS failover"
            ],
            "industry_rubric": "Evaluates understanding of RTO (Recovery Time Objective) and RPO (Recovery Point Objective), cross-region data consistency, and DNS TTL propagation dynamics."
        },
        {
            "id": "do-adv-03",
            "title": "Chaos Engineering & Automated Self-Healing Mesh with Chaos Mesh & Kubernetes",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["Kubernetes", "Linux", "Docker", "Prometheus"],
            "non_tech_competencies": ["Chaos Engineering", "Resilience Verification", "Fault Injection"],
            "executive_summary": "Systems must be tested against unexpected hardware and network failures. This project introduces Chaos Mesh into a Kubernetes cluster to deliberately inject pod kills, network latency, and packet loss.",
            "architecture_summary": "Chaos injection framework running on Kubernetes with Prometheus telemetry verifying that circuit breakers and replica autoscalers maintain SLA targets.",
            "key_features": [
                "Chaos Mesh experiments: PodChaos (random container kills), NetworkChaos (100ms jitter, 10% packet drop)",
                "StressChaos testing CPU saturation to verify Kubernetes horizontal pod autoscaling",
                "SLO telemetry dashboard asserting availability remains > 99.9% during active chaos drills",
                "Automated chaos injection pipeline integrated into staging environment nightly tests"
            ],
            "roadmap": [
                "Milestone 1: Chaos Mesh operator installation and experiment CRD definition",
                "Milestone 2: Pod kill injection experiment verifying Kubernetes replica self-healing",
                "Milestone 3: Network partition experiment testing database reconnection retries",
                "Milestone 4: Post-chaos resilience scorecard evaluating system recovery time"
            ],
            "industry_rubric": "Evaluates scientific hypothesis methodology (Steady State -> Hypothesis -> Inject -> Verify), automated containment safety, and resilient system architecture."
        },
        {
            "id": "do-adv-04",
            "title": "Zero-Trust Cloud Security & IAM Governance Automation Engine",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Python", "Terraform", "AWS", "Docker"],
            "non_tech_competencies": ["Zero-Trust Architecture", "IAM Least-Privilege", "Compliance Governance"],
            "executive_summary": "Over-privileged cloud IAM roles are the #1 root cause of enterprise cloud security breaches. This engine analyzes AWS IAM permissions, detects wildcard * access, and automatically rewrites least-privilege policies.",
            "architecture_summary": "Automated security governance engine using AWS CloudTrail access logs, AWS IAM Access Analyzer, and Python policy reduction algorithms.",
            "key_features": [
                "Automated IAM scanner identifying unused credentials and dangerous AdministratorAccess roles",
                "CloudTrail log parser identifying exact API actions used over the last 90 days",
                "Automated policy generator rewriting broad policies into precise least-privilege JSON contracts",
                "Nightly compliance audit report detailing security posture improvements and risk scores"
            ],
            "roadmap": [
                "Milestone 1: IAM scanner client querying roles, policies, and last-accessed service data",
                "Milestone 2: Access log analyzer computing minimal required permission boundaries",
                "Milestone 3: Automated policy synthesizer generating compliant Terraform IAM blocks",
                "Milestone 4: Audit report generator with Slack notification on policy violations"
            ],
            "industry_rubric": "Evaluates deep understanding of AWS IAM evaluation logic (SCP -> Permission Boundary -> Identity Policy), least privilege enforcement, and automated compliance auditing."
        }
    ],

    # -------------------------------------------------------------------------
    # 5. AI Agents, LLMs & Cognitive Systems (10 Projects)
    # -------------------------------------------------------------------------
    "ai_agents": [
        {
            "id": "ai-beg-01",
            "title": "Function-Calling Tool-Use Agent with Python & OpenAI API",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "FastAPI", "OpenAI API", "pytest"],
            "non_tech_competencies": ["Prompt Engineering", "Structured Output Validation", "API Integration"],
            "executive_summary": "LLMs hallucinate when asked for factual data. This project builds a tool-using AI assistant that executes deterministic Python functions (weather lookup, database query, calculator) via OpenAI tool calling.",
            "architecture_summary": "FastAPI service orchestrating an iterative LLM tool-calling loop with JSON schema function contracts and Pydantic validation.",
            "key_features": [
                "Declared JSON Schema tool definitions for mathematical evaluation and data search",
                "Autonomous tool-calling loop parsing model tool_calls, executing functions, and returning answers",
                "Pydantic schema validation preventing malformed arguments from executing",
                "Automated mock unit tests verifying tool execution without incurring live LLM token costs"
            ],
            "roadmap": [
                "Milestone 1: Tool definitions and strict Pydantic argument models",
                "Milestone 2: Execution loop managing conversation history and function responses",
                "Milestone 3: FastAPI REST API exposing an interactive agent chat endpoint",
                "Milestone 4: Mocked unit test suite verifying tool invocation and error recovery"
            ],
            "industry_rubric": "Evaluates prevention of infinite tool loops, clean argument validation, proper token cost awareness, and high test coverage."
        },
        {
            "id": "ai-beg-02",
            "title": "Document Question-Answering Bot with PyPDF & ChromaDB Embeddings",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "ChromaDB", "FastAPI", "OpenAI API"],
            "non_tech_competencies": ["RAG Fundamentals", "Chunking Strategy", "Citation Traceability"],
            "executive_summary": "Enterprises struggle to find answers in 100-page policy manuals and technical specifications. This project parses PDFs, generates vector embeddings, and answers queries with exact page citations.",
            "architecture_summary": "Retrieval-Augmented Generation (RAG) pipeline parsing documents with PyPDF, storing vectors in ChromaDB, and synthesizing grounded answers via GPT-4.",
            "key_features": [
                "Document chunking engine splitting text with semantic sentence boundaries and overlaps",
                "Vector embedding storage and cosine similarity search using local ChromaDB",
                "Grounded prompt template enforcing 'answer strictly based on context or state I do not know'",
                "Source citation metadata returning document name, page number, and matched excerpt"
            ],
            "roadmap": [
                "Milestone 1: PDF ingestion and text extraction pipeline with page number tracking",
                "Milestone 2: Chunking strategy and embedding generation via OpenAI text-embedding-3-small",
                "Milestone 3: Similarity retrieval and grounded response synthesis prompt",
                "Milestone 4: Evaluation test checking hallucination suppression on unanswerable questions"
            ],
            "industry_rubric": "Evaluates hallucination suppression, clean chunking boundaries (avoiding cutting words in half), and clear source citation accuracy."
        },
        {
            "id": "ai-int-01",
            "title": "Production Hybrid RAG Search Engine with BM25, Pinecone & Reranking",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "Pinecone", "FastAPI", "Docker", "OpenAI API"],
            "non_tech_competencies": ["Hybrid Search Architecture", "Information Retrieval", "Re-Ranking Optimization"],
            "executive_summary": "Pure vector search fails on exact keyword searches (part numbers, acronyms, IDs). This production RAG engine fuses dense vector embeddings with sparse BM25 keyword search using Reciprocal Rank Fusion (RRF) and Cohere reranking.",
            "architecture_summary": "Two-stage retrieval pipeline: Stage 1 (Hybrid Pinecone Dense + BM25 Sparse retrieval fused via RRF k=60) -> Stage 2 (Cross-Encoder Re-Ranking).",
            "key_features": [
                "Dual retrieval engine querying Pinecone dense vector index and BM25 sparse keyword index",
                "Reciprocal Rank Fusion (RRF) combining keyword and semantic scores into unified ranks",
                "Cross-encoder re-ranking scoring top-20 retrieved candidates down to top-5 most relevant passages",
                "Lost-in-the-Middle context reordering placing highest-scoring passages at start and end of prompt"
            ],
            "roadmap": [
                "Milestone 1: Ingestion pipeline generating dense vector and sparse lexical representations",
                "Milestone 2: Hybrid search query execution and Reciprocal Rank Fusion implementation",
                "Milestone 3: Cross-encoder reranking integration and context reordering",
                "Milestone 4: Ground truth retrieval evaluation measuring Precision@5 and Recall@5"
            ],
            "industry_rubric": "Evaluates profound understanding of retrieval failure modes, mathematical RRF fusion implementation, and measurable retrieval precision."
        },
        {
            "id": "ai-int-02",
            "title": "Autonomous Multi-Tool Research Agent with LangChain & SerpAPI",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "LangChain", "FastAPI", "Docker"],
            "non_tech_competencies": ["Agentic Reasoning", "Task Decomposition", "Error Recovery"],
            "executive_summary": "Knowledge workers spend hours scouring the web and summarizing articles. This autonomous research agent takes a high-level research prompt, breaks it into search queries, scrapes articles, and writes comprehensive briefs.",
            "architecture_summary": "ReAct (Reason + Act) agent loop built with LangChain, integrated with SerpAPI web search, BeautifulSoup scraper, and Markdown synthesis.",
            "key_features": [
                "Plan-and-Execute agent architecture decomposing queries into sequential search tasks",
                "Web search tool fetching live Google results and scraping long-form article text",
                "Summarization map-reduce chain synthesizing findings into structured reports",
                "Execution safety timeout and token budget limiter preventing runaway API costs"
            ],
            "roadmap": [
                "Milestone 1: Web search and content scraper tool implementation with rate-limiting",
                "Milestone 2: LangChain ReAct agent configuration with scratchpad reasoning steps",
                "Milestone 3: Multi-document synthesis chain generating structured research briefings",
                "Milestone 4: FastAPI streaming endpoint delivering real-time agent thought logs to client"
            ],
            "industry_rubric": "Evaluates structured thought tracing, prevention of circular search loops, clean handling of blocked/empty websites, and synthesized report quality."
        },
        {
            "id": "ai-int-03",
            "title": "Semantic Cache & Rate-Limited Model Gateway with Redis & FastAPI",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Python", "Redis", "FastAPI", "Docker", "OpenAI API"],
            "non_tech_competencies": ["API Cost Optimization", "Semantic Similarity", "High-Throughput Gateway"],
            "executive_summary": "Users repeatedly ask similar questions, incurring massive LLM token bills and high latency. This gateway uses Redis vector similarity to return cached answers for semantically equivalent queries.",
            "architecture_summary": "Reverse proxy gateway calculating prompt embeddings, querying Redis Vector Search with a 0.96 cosine threshold, and falling back to OpenAI on cache misses.",
            "key_features": [
                "Semantic caching matching query variations ('How to reset password?' vs 'Password reset steps?')",
                "Redis vector indexing storing prompt embeddings and associated LLM responses with TTL",
                "Token-bucket rate limiting per tenant API key protecting upstream LLM accounts",
                "Cache analytics dashboard tracking cost savings and cache hit ratio percentage"
            ],
            "roadmap": [
                "Milestone 1: Redis Vector Search index configuration with cosine distance metric",
                "Milestone 2: Embedding computation and semantic cache lookup middleware",
                "Milestone 3: Cache storage logic with TTL and background cache eviction",
                "Milestone 4: Benchmark load test demonstrating 90% latency reduction on semantic cache hits"
            ],
            "industry_rubric": "Evaluates choice of cosine similarity threshold (preventing false-positive cache hits), cache invalidation strategy, and sub-15ms cache lookup speed."
        },
        {
            "id": "ai-int-04",
            "title": "LLM Guardrail & Prompt Injection Defense Firewall with LlamaGuard & Python",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "FastAPI", "Docker", "pytest"],
            "non_tech_competencies": ["AI Safety & Red-Teaming", "Security Guardrails", "Regex & ML Defenses"],
            "executive_summary": "Public AI applications face jailbreaks, prompt injections ('Ignore previous instructions'), and toxic output risks. This defense gateway inspects inputs and outputs, blocking malicious prompts before reaching models.",
            "architecture_summary": "Two-tier firewall: Tier 1 (Fast heuristic pattern matchers and token leak detectors) -> Tier 2 (ML classification guardrail using LlamaGuard / OpenAI Moderation).",
            "key_features": [
                "Input sanitization detecting prompt injection keywords, base64 obfuscation, and system prompt extractors",
                "PII redaction engine stripping emails, phone numbers, and SSNs before sending queries to LLM",
                "Output validator asserting that response does not leak confidential system prompt instructions",
                "Adversarial test suite simulating 50+ known jailbreak vectors (DAN, cipher prompts, roleplay exploits)"
            ],
            "roadmap": [
                "Milestone 1: Heuristic regex and entropy-based prompt injection detection rules",
                "Milestone 2: PII scrubbing engine using Microsoft Presidio or custom regex tokenizers",
                "Milestone 3: Integration with OpenAI Moderation API for hate/violence/toxicity checks",
                "Milestone 4: Adversarial red-teaming test harness validating > 95% injection block rate"
            ],
            "industry_rubric": "Evaluates low false-positive rate on legitimate complex queries, low latency overhead (< 30ms for heuristic filter), and thorough coverage of jailbreak attack types."
        },
        {
            "id": "ai-adv-01",
            "title": "Hierarchical Multi-Agent Supervisor Platform with CrewAI & Webhooks",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "CrewAI", "FastAPI", "Docker", "PostgreSQL"],
            "non_tech_competencies": ["Multi-Agent Architecture", "Task Orchestration", "Supervisory Governance"],
            "executive_summary": "Complex business operations require multiple specialized agents collaborating (e.g. CodeWriter, CodeReviewer, TestRunner). This platform coordinates hierarchical agent teams with a supervisor agent.",
            "architecture_summary": "Hierarchical multi-agent framework where a Supervisor Agent decomposes tasks, delegates sub-tasks to specialized worker agents, reviews outputs, and requests revisions.",
            "key_features": [
                "Role-based agent specialization with explicit goals, backstories, and tool boundaries",
                "Supervisor agent dynamically delegating and quality-checking worker deliverables",
                "Revision loop allowing supervisor to reject low-quality drafts and request improvements",
                "Execution history and agent conversation state persisted in PostgreSQL database"
            ],
            "roadmap": [
                "Milestone 1: CrewAI agent definitions: ProjectManager, SeniorEngineer, SecurityReviewer",
                "Milestone 2: Task dependency graph and sequential/hierarchical process configuration",
                "Milestone 3: FastAPI webhook integration notifying external systems upon task completion",
                "Milestone 4: Stress-testing agent team with ambiguous complex tasks and verifying output quality"
            ],
            "industry_rubric": "Evaluates clear role boundaries, prevention of circular debate between agents, deterministic stop conditions, and high-quality final deliverables."
        },
        {
            "id": "ai-adv-02",
            "title": "Self-Reflective Code Generation Agent with Docker Sandbox Execution",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Python", "Docker", "FastAPI", "Linux", "pytest"],
            "non_tech_competencies": ["Self-Healing Algorithms", "Sandbox Security", "Automated Testing"],
            "executive_summary": "LLMs often generate code with syntax errors or failing unit tests. This agent writes code, executes it inside an isolated, secure Docker container, inspects stderr and failing test traces, and self-corrects until tests pass.",
            "architecture_summary": "Reflective feedback loop: LLM writes code -> Executes inside disposable non-root Docker container -> Passes stderr stacktrace back to LLM -> LLM patches code.",
            "key_features": [
                "Disposable Docker container runtime executing untrusted code with zero network access and 5s timeout",
                "Automated test runner capturing exit codes, stdout, and failing assertion messages",
                "Self-correction loop iterating up to 3 times to fix syntax errors and failing unit tests",
                "Resource throttling (CPU/Memory limits) preventing fork bombs and memory leaks"
            ],
            "roadmap": [
                "Milestone 1: Secure Docker container runner using docker-py with CPU/memory limits and no network",
                "Milestone 2: Code generation prompt and output parser extracting runnable python scripts",
                "Milestone 3: Feedback reflection loop feeding test failure stacktraces back into the prompt",
                "Milestone 4: Evaluation benchmark testing 30 algorithmic coding challenges and logging success rates"
            ],
            "industry_rubric": "Evaluates strict sandbox containment (preventing host breakout), intelligent prompt reflection (not just retrying the same code), and high problem resolution rate."
        },
        {
            "id": "ai-adv-03",
            "title": "Enterprise Knowledge Graph RAG with Neo4j, LangChain & Vector Search",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "Neo4j", "LangChain", "Docker", "Cypher"],
            "non_tech_competencies": ["Graph Theory", "Knowledge Graph Modeling", "Relational Semantic Search"],
            "executive_summary": "Vector search cannot navigate multi-hop relationships (e.g. 'Which employees report to managers who own approved security patents?'). This GraphRAG system combines vector search with Neo4j knowledge graphs.",
            "architecture_summary": "GraphRAG hybrid architecture storing entities and relationships in Neo4j, enriched with vector embeddings for hybrid graph-traversal semantic retrieval.",
            "key_features": [
                "Automated entity and relationship extraction converting unstructured text into Neo4j graph nodes and edges",
                "Text-to-Cypher query generation translating natural language questions into Neo4j queries",
                "Multi-hop relationship traversal finding non-obvious connections across disconnected documents",
                "Hybrid search combining Cypher graph queries with vector similarity retrieval"
            ],
            "roadmap": [
                "Milestone 1: Neo4j database setup and graph schema design (Entities, Relationships, Attributes)",
                "Milestone 2: Entity extraction pipeline populating the graph from enterprise text documents",
                "Milestone 3: LangChain Cypher QA Chain integrating schema introspection and query validation",
                "Milestone 4: Comparative evaluation showing GraphRAG answering queries where vector search fails"
            ],
            "industry_rubric": "Evaluates clean Cypher query generation (preventing graph query timeouts), entity deduplication, and demonstration of multi-hop question answering."
        },
        {
            "id": "ai-adv-04",
            "title": "Automated Model Evaluation Harness with Ragas & TruLens in CI/CD",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Python", "Ragas", "GitHub Actions", "pytest", "Docker"],
            "non_tech_competencies": ["AI Quality Engineering", "CI/CD Gatekeeping", "Metric-Driven Evaluation"],
            "executive_summary": "Deploying RAG pipelines without automated evaluation leads to silent regressions in answer quality. This CI/CD test harness runs automated RAG evaluations asserting Context Precision >= 0.90 and Faithfulness >= 0.95.",
            "architecture_summary": "Automated testing pipeline running on GitHub Actions, evaluating RAG responses against a synthetic ground-truth testset using Ragas metrics.",
            "key_features": [
                "Automated testset generation synthesizing questions, contexts, and ground-truth answers",
                "Evaluation of core Ragas metrics: Faithfulness, Answer Relevance, Context Precision, and Context Recall",
                "CI/CD quality gate failing pull requests if accuracy metrics drop below agreed thresholds",
                "Visual HTML regression report tracking score trends across pull requests and model versions"
            ],
            "roadmap": [
                "Milestone 1: Golden dataset creation covering 50 representative enterprise customer queries",
                "Milestone 2: Ragas evaluation script computing Faithfulness and Context Precision scores",
                "Milestone 3: GitHub Actions workflow running evaluation and uploading artifacts",
                "Milestone 4: Threshold assertion logic failing CI build on regression detection"
            ],
            "industry_rubric": "Evaluates statistical validity of testset, avoidance of noisy LLM-as-a-judge scoring, and automated CI gate enforcement."
        }
    ],

    # -------------------------------------------------------------------------
    # 6. Technology Leadership, Architecture Strategy & Advisory (10 Projects)
    # -------------------------------------------------------------------------
    "tech_leadership_advisory": [
        {
            "id": "tl-beg-01",
            "title": "Architecture Decision Record (ADR) Governance Suite & RFC Workflow",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["System Architecture", "RFC Processes", "Git", "Markdown"],
            "non_tech_competencies": ["Architecture Governance", "Technical Writing", "Stakeholder Consensus"],
            "executive_summary": "Engineering teams suffer from tribal knowledge and repeated architecture mistakes when design choices are not documented. This project establishes an automated RFC/ADR governance framework.",
            "architecture_summary": "Version-controlled architectural decision registry using MADR (Markdown Architectural Decision Records), linter validation, and pull-request review templates.",
            "key_features": [
                "Standardized ADR templates capturing Context, Decision Drivers, Considered Options, and Consequences",
                "Automated linter asserting required sections (Status, Tradeoffs, Security Considerations)",
                "Living architecture documentation website generated automatically via MkDocs",
                "Team RFC review workflow template with explicit stakeholder sign-off stages"
            ],
            "roadmap": [
                "Milestone 1: ADR specification templates and decision driver rubric authoring",
                "Milestone 2: Authoring 3 foundational ADRs for a hypothetical scaling platform",
                "Milestone 3: Automated markdown linting and status badge validator script",
                "Milestone 4: MkDocs static documentation site generation and deployment workflow"
            ],
            "industry_rubric": "Evaluates balanced analysis of negative consequences/tradeoffs, clarity of context, and structured decision governance."
        },
        {
            "id": "tl-beg-02",
            "title": "Engineering Team Health & DORA Metrics Telemetry Dashboard",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "SQL", "GitHub Actions", "Docker"],
            "non_tech_competencies": ["Engineering Productivity", "DORA Metrics", "Continuous Improvement"],
            "executive_summary": "Engineering leaders must balance delivery speed with system stability. This project collects git and deployment metadata to calculate the 4 DORA metrics: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and MTTR.",
            "architecture_summary": "Analytics pipeline extracting GitHub commit/PR data and release events into PostgreSQL, visualizing DORA performance tiers (Low, Medium, High, Elite).",
            "key_features": [
                "Automated webhook ingestion capturing pull request merge and deployment release events",
                "Calculation engine computing the 4 core DORA metrics on rolling 30-day windows",
                "Identification of engineering delivery bottlenecks (PR review lag, long test runs)",
                "Executive dashboard classifying team performance against DORA state of devops benchmarks"
            ],
            "roadmap": [
                "Milestone 1: Webhook receiver service capturing GitHub pull request and workflow run events",
                "Milestone 2: SQL aggregation queries calculating Deployment Frequency and Change Failure Rate",
                "Milestone 3: Calculation of Lead Time for Changes (commit to production release)",
                "Milestone 4: Interactive dashboard visualizing team velocity and deployment stability"
            ],
            "industry_rubric": "Evaluates accurate metric definitions (preventing vanity metrics), actionable bottleneck diagnosis, and clean data modeling."
        },
        {
            "id": "tl-int-01",
            "title": "Enterprise Monolith-to-Microservices Decomposition & API Governance Blueprint",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["System Architecture", "Domain-Driven Design", "API Governance", "Microservices"],
            "non_tech_competencies": ["Strangler Fig Pattern", "Domain-Driven Design", "Risk Management"],
            "executive_summary": "Legacy monolithic codebases become unmaintainable as engineering headcounts grow. This project models the step-by-step architectural decomposition of an enterprise monolith using the Strangler Fig pattern.",
            "architecture_summary": "Domain-Driven Design (DDD) bounded context mapping, API Gateway routing, and asynchronous event integration ensuring zero downtime during migration.",
            "key_features": [
                "Domain-Driven Design (DDD) strategic mapping identifying Core, Supporting, and Generic subdomains",
                "Strangler Fig migration roadmap detailing phased proxy routing at API Gateway level",
                "Anti-Corruption Layer (ACL) specification preventing legacy models from polluting new services",
                "Data migration strategy moving from shared database to database-per-service with Dual-Writes"
            ],
            "roadmap": [
                "Milestone 1: As-is monolithic system audit and bounded context identification",
                "Milestone 2: Target microservices topology architecture diagram and interface specifications",
                "Milestone 3: Phased 4-stage Strangler Fig migration plan with rollback trigger points",
                "Milestone 4: Anti-Corruption Layer code prototype and data synchronization strategy"
            ],
            "industry_rubric": "Evaluates realistic risk assessment, avoidance of distributed monolith anti-patterns, and robust data consistency planning."
        },
        {
            "id": "tl-int-02",
            "title": "Cloud FinOps Unit Economics & Infrastructure Cost Governance Engine",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Cloud Strategy", "FinOps", "Python", "AWS", "SQL"],
            "non_tech_competencies": ["Cloud Financial Management", "Cost Allocation", "Executive Communication"],
            "executive_summary": "Unchecked cloud spending damages startup runways and corporate margins. This engine analyzes AWS billing data, maps costs to product features, and identifies idle/oversized infrastructure resources.",
            "architecture_summary": "FinOps data ingestion pipeline parsing AWS Cost & Usage Reports (CUR), allocating costs by tenant/team tags, and generating automated cost reduction recommendations.",
            "key_features": [
                "Cost allocation engine attributing cloud compute and storage costs to specific product features",
                "Detection algorithms identifying unattached EBS volumes, idle NAT gateways, and unindexed databases",
                "Reserved Instance (RI) and Savings Plan coverage modeling maximizing discounted commitments",
                "Automated anomaly alerts warning engineering managers when daily service spend jumps by > 20%"
            ],
            "roadmap": [
                "Milestone 1: Ingestion of AWS Cost and Usage Reports into analytical database",
                "Milestone 2: Unit economics calculation (Cost per Active User, Cost per API Request)",
                "Milestone 3: Wastage detection rules and automated rightsizing recommendations",
                "Milestone 4: Executive cost report outlining 30-day savings plan with expected ROI"
            ],
            "industry_rubric": "Evaluates focus on unit economics rather than raw cuts, accurate AWS pricing models, and pragmatic engineering tradeoffs."
        },
        {
            "id": "tl-int-03",
            "title": "SOC2 Type II Security Due-Diligence & Vulnerability Governance Suite",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Security Auditing", "Compliance", "Python", "Git"],
            "non_tech_competencies": ["SOC2 / ISO 27001", "Vendor Risk Assessment", "Security Due-Diligence"],
            "executive_summary": "Enterprise sales stall when companies cannot provide proof of SOC2 compliance. This suite automates evidence collection for Common Criteria controls (access reviews, encryption at rest, change management).",
            "architecture_summary": "Compliance automation framework polling cloud APIs, GitHub settings, and HR systems to verify security controls and compile continuous audit evidence.",
            "key_features": [
                "Automated check asserting all production S3 buckets and database volumes have KMS encryption enabled",
                "GitHub branch protection auditor ensuring pull requests require 2 approvals and passing CI before merge",
                "Quarterly user access review automation identifying inactive employee accounts across systems",
                "Automated SOC2 readiness scorecard generating downloadable compliance evidence binder"
            ],
            "roadmap": [
                "Milestone 1: Mapping SOC2 Trust Services Criteria (Security, Availability, Confidentiality) to technical checks",
                "Milestone 2: Automated cloud audit scripts querying AWS APIs for configuration compliance",
                "Milestone 3: Version control change management verification checking signed commits and reviews",
                "Milestone 4: Continuous audit report generator with gap remediation priority checklist"
            ],
            "industry_rubric": "Evaluates understanding of auditor expectations, automated evidence reproducibility, and practical remediation recommendations."
        },
        {
            "id": "tl-int-04",
            "title": "Disaster Recovery & Business Continuity Simulation Suite (RTO/RPO)",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Disaster Recovery", "Cloud Strategy", "Python", "AWS"],
            "non_tech_competencies": ["Disaster Recovery Planning", "Business Continuity", "Crisis Management"],
            "executive_summary": "Disaster recovery plans that are never tested fail during real emergencies. This project designs a comprehensive DR runbook and automated failover verification script asserting RTO < 30m and RPO < 5m.",
            "architecture_summary": "Disaster recovery testing framework orchestrating cross-region database snapshot replication, automated DNS cutover simulation, and data loss verification.",
            "key_features": [
                "Formal Disaster Recovery Plan defining RTO (Recovery Time Objective) and RPO (Recovery Point Objective)",
                "Automated backup verification restoring database snapshots into an isolated VPC and running integrity checks",
                "Emergency DNS failover runbook and scripted CLI cutover automation",
                "Post-disaster reconciliation script verifying zero transactional data loss"
            ],
            "roadmap": [
                "Milestone 1: Disaster recovery classification matrix (Pilot Light vs Warm Standby vs Multi-Site)",
                "Milestone 2: Backup automation and cross-region replication script implementation",
                "Milestone 3: Failover simulation testing database restoration and health check validation",
                "Milestone 4: Disaster recovery tabletop drill scenario runbook with executive communications"
            ],
            "industry_rubric": "Evaluates realistic RTO/RPO expectations, thorough backup validation (not just backup creation), and clear step-by-step incident runbooks."
        },
        {
            "id": "tl-adv-01",
            "title": "Multi-Year Enterprise Cloud Modernization & Tech Debt Governance Strategy",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["System Architecture", "Cloud Strategy", "Technical Leadership", "FinOps"],
            "non_tech_competencies": ["Tech Debt Valuation", "Multi-Year Roadmapping", "Executive Board Defense"],
            "executive_summary": "Legacy technology debt slows down feature delivery and increases attrition. This executive project formulates a 3-year modernization roadmap balancing technical debt refactoring with business product delivery.",
            "architecture_summary": "Comprehensive architectural blueprint detailing legacy system retirement, event-driven modernization, cloud-native adoption, and organizational Team Topologies alignment.",
            "key_features": [
                "Technical debt quantification framework measuring interest rate (developer friction hours) vs principal",
                "3-Year phased modernization roadmap with clear quarterly delivery milestones and budget forecasts",
                "Team Topologies organizational alignment mapping Stream-Aligned, Enabling, and Platform teams",
                "Executive board presentation slide deck defending the ROI of platform modernization"
            ],
            "roadmap": [
                "Milestone 1: Enterprise application inventory audit and technical debt scoring matrix",
                "Milestone 2: Target cloud-native architecture blueprint with decoupled microservice domains",
                "Milestone 3: Phased 36-month migration schedule with risk mitigation and cost projections",
                "Milestone 4: Executive business case presentation translating tech improvements to revenue retention"
            ],
            "industry_rubric": "Evaluates ability to communicate technical concepts to board members, realistic timeline estimations, and balance between business delivery and technical excellence."
        },
        {
            "id": "tl-adv-02",
            "title": "Zero-Trust Identity Federation & Enterprise RBAC Architecture Strategy",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["Security Auditing", "System Architecture", "Cloud Strategy", "OAuth2"],
            "non_tech_competencies": ["Zero-Trust Architecture", "Enterprise Security Governance", "Identity Federation"],
            "executive_summary": "Perimeter firewalls are obsolete; modern enterprises must verify every request explicitly. This architecture designs a Zero-Trust identity federation model supporting SSO, mTLS, and dynamic role-based access control.",
            "architecture_summary": "Zero-Trust architecture blueprint utilizing OpenID Connect (OIDC) identity federation, mutual TLS (mTLS) service-to-service authentication, and attribute-based access control (ABAC).",
            "key_features": [
                "Identity Provider (IdP) federation architecture integrating Okta/Azure AD with internal applications",
                "Mutual TLS (mTLS) specification for microservice communication with automated certificate rotation",
                "Role-Based and Attribute-Based Access Control (RBAC/ABAC) policy engine design",
                "Security incident response playbook for credential compromise and session revocation"
            ],
            "roadmap": [
                "Milestone 1: Identity architecture specification detailing OIDC flows and JWT claims",
                "Milestone 2: Service-to-service mTLS mesh architecture and certificate lifecycle design",
                "Milestone 3: RBAC/ABAC authorization policy contract and enforcement middleware design",
                "Milestone 4: Comprehensive threat model (STRIDE) analyzing identity spoofing and elevation risks"
            ],
            "industry_rubric": "Evaluates strict adherence to NIST Zero-Trust guidelines, avoidance of implicit trust networks, and clear security policy contracts."
        },
        {
            "id": "tl-adv-03",
            "title": "Global Distributed Systems Scalability & Data Residency Governance Blueprint",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["System Architecture", "Data Governance", "Cloud Strategy", "SQL"],
            "non_tech_competencies": ["Data Residency & GDPR", "Global Scale Architecture", "CAP Theorem Tradeoffs"],
            "executive_summary": "Global businesses must store customer data within specific legal borders (GDPR in Europe, DPDP in India, CCPA in USA) while providing low-latency access globally. This project designs a multi-region data residency architecture.",
            "architecture_summary": "Partitioned global distributed system architecture using localized data stores, geofenced Kafka clusters, and global read-only routing layers.",
            "key_features": [
                "Data residency partitioning framework routing customer writes strictly to compliant local jurisdictions",
                "Asynchronous cross-border anonymized aggregation pipeline for global analytics without GDPR violation",
                "CAP theorem trade-off analysis evaluating consistency vs availability across international WAN links",
                "Regulatory audit compliance documentation certifying complete tenant isolation by geography"
            ],
            "roadmap": [
                "Milestone 1: Regulatory legal requirement matrix (EU GDPR, India DPDP, USA CCPA)",
                "Milestone 2: Distributed database topology design with localized sharding keys",
                "Milestone 3: Global API routing layer directing traffic based on user legal jurisdiction",
                "Milestone 4: Data audit verification suite validating no PII leaves designated legal boundaries"
            ],
            "industry_rubric": "Evaluates legal and regulatory accuracy, deep distributed database mastery, and robust latency/consistency tradeoff analysis."
        },
        {
            "id": "tl-adv-04",
            "title": "Executive Board Technical Due-Diligence & M&A Technology Valuation Framework",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Technical Leadership", "System Architecture", "Security Auditing", "FinOps"],
            "non_tech_competencies": ["M&A Due Diligence", "Technology Valuation", "Executive Board Defense"],
            "executive_summary": "During mergers and acquisitions (M&A) or private equity buyouts, acquiring companies must audit target codebases, infrastructure costs, and technical risks. This project authors an enterprise M&A technical due diligence report.",
            "architecture_summary": "Auditing framework evaluating target company software architecture, intellectual property risks (GPL contamination), security vulnerabilities, infrastructure scalability, and team dependency.",
            "key_features": [
                "Comprehensive Due-Diligence checklist covering Architecture, Scalability, Security, IP, and Team",
                "Open Source Software (OSS) license compliance audit detecting copyleft (GPL) legal risks",
                "Infrastructure scalability audit calculating the cost to 10x current transaction volume",
                "Executive Red-Flag summary highlighting catastrophic technical deal-breakers for the Board of Directors"
            ],
            "roadmap": [
                "Milestone 1: Technical due-diligence audit rubric authoring across 5 core technical pillars",
                "Milestone 2: Conducting simulated technical audit of a candidate acquisition target company",
                "Milestone 3: IP risk and software licensing compliance analysis",
                "Milestone 4: Final Investment Committee due-diligence report with valuation adjustment recommendations"
            ],
            "industry_rubric": "Evaluates executive rigor, detection of non-obvious technical liabilities, objective valuation adjustments, and clear presentation to non-technical investors."
        }
    ],

    # -------------------------------------------------------------------------
    # 7. Marketplace Systems & Algorithmic Engineering (10 Projects)
    # -------------------------------------------------------------------------
    "marketplace_systems": [
        # Beginner 1
        {
            "id": "mp-beg-01",
            "title": "Two-Sided Service Marketplace Matching API with Redis Geospatial Indexing",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "FastAPI", "Redis", "PostgreSQL", "pytest"],
            "non_tech_competencies": ["Geospatial Indexing", "Supply-Demand Matching", "API Design"],
            "executive_summary": "On-demand local service marketplaces (like TaskRabbit or Thumbtack) require radius-based provider search and deterministic order assignment. This service indexes provider locations in Redis and matches service requests to the nearest qualified provider.",
            "architecture_summary": "FastAPI REST API with Redis GEOADD and GEOSEARCH geospatial indexing, PostgreSQL request records, and automated pytest fixtures.",
            "key_features": [
                "Radius-bounded geospatial query filtering nearby verified providers within N kilometers",
                "Deterministic assignment logic matching customer requests to highest-rated nearby providers",
                "Reservation state machine (REQUESTED -> MATCHED -> FULFILLED) with automatic timeout expiry",
                "Atomic Redis transactions preventing race conditions when two customers request the same provider"
            ],
            "roadmap": [
                "Milestone 1: Geospatial location schema & Redis GEO indexing setup",
                "Milestone 2: Service request submission and nearest-neighbor radius search",
                "Milestone 3: Atomic locking & reservation state machine transitions",
                "Milestone 4: Automated load tests asserting sub-15ms match latency under concurrent bookings"
            ],
            "industry_rubric": "Evaluates understanding of spatial queries, race conditions when two customers book the same provider simultaneously, and clean API design."
        },
        # Beginner 2
        {
            "id": "mp-beg-02",
            "title": "Marketplace Bayesian Rating & Review Normalization Service",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "SQL", "PostgreSQL", "FastAPI", "pytest"],
            "non_tech_competencies": ["Trust & Reputation Systems", "Statistical Normalization", "Cold-Start Economics"],
            "executive_summary": "A 5.0-star rating from 1 review should not outrank a 4.9-star rating from 2,000 reviews. This service implements Wilson score interval and empirical Bayes estimation to rank marketplace sellers fairly.",
            "architecture_summary": "Statistical ranking microservice computing Bayesian mean scores and Wilson score lower bounds on PostgreSQL review tables.",
            "key_features": [
                "Empirical Bayes prior calculation damping low-sample variance for new sellers",
                "Wilson score confidence intervals for thumbs up/down feedback",
                "Anti-shilling review velocity rate limiters preventing spam review bursts",
                "Deterministic sorting query optimization using functional indexes"
            ],
            "roadmap": [
                "Milestone 1: Relational review schema & mock distribution generator",
                "Milestone 2: Mathematical formula implementation for Bayesian mean & Wilson score",
                "Milestone 3: Fast ranking API endpoint with cached scores",
                "Milestone 4: Statistical validation tests asserting cold-start seller fairness"
            ],
            "industry_rubric": "Evaluates statistical rigor, avoidance of naive arithmetic averages, and efficient database query indexing."
        },
        # Intermediate 1
        {
            "id": "mp-int-01",
            "title": "Real-Time Supply-Demand Surge Pricing & Elasticity Engine",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "FastAPI", "Redis", "Pandas", "Docker"],
            "non_tech_competencies": ["Dynamic Pricing & Economics", "Elasticity Modeling", "Market Equilibrium"],
            "executive_summary": "When localized ride or delivery demand exceeds active driver supply, market failure occurs. This engine calculates real-time price multipliers using demand-supply elasticity curves to balance liquidity.",
            "architecture_summary": "Real-time pricing engine polling supply/demand counts from Redis sliding windows and recalculating surge multipliers per geographic zone.",
            "key_features": [
                "Dynamic multiplier calculation (1.0x to 3.5x) based on supply-to-demand ratio",
                "Price elasticity demand curve simulation damping demand spikes",
                "Regional geofence boundaries with smooth multiplier gradient transitions",
                "Audit log recording every surge quote with timestamp and market metrics"
            ],
            "roadmap": [
                "Milestone 1: Redis sliding window event tracker for search events & available units",
                "Milestone 2: Elasticity pricing algorithm and multiplier ceiling caps",
                "Milestone 3: Real-time quote generation API with cryptographic quote tokens",
                "Milestone 4: Simulated demand spike stress tests proving market equilibrium"
            ],
            "industry_rubric": "Evaluates understanding of market clearing price mechanisms, prevention of sudden price cliff edges between adjacent zones, and algorithmic stability."
        },
        # Intermediate 2
        {
            "id": "mp-int-02",
            "title": "Multi-Party Marketplace Escrow & Split Payouts with Stripe Connect",
            "difficulty": "Intermediate",
            "hours": 30,
            "primary_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "SQL"],
            "non_tech_competencies": ["Payment Escrow Architecture", "Double-Entry Accounting", "Regulatory Compliance"],
            "executive_summary": "Marketplaces cannot directly pocket transaction funds; they act as intermediaries holding buyer payments in escrow, deducting a platform take-rate, and releasing payouts upon verified delivery.",
            "architecture_summary": "Payment orchestration engine managing multi-party escrow states, Stripe Connect destination charges, and automated fee distribution.",
            "key_features": [
                "Two-phase payment intent with capture on fulfillment verification",
                "Configurable platform take-rate / commission calculation",
                "Automated seller transfer routing with reverse transfer on refund",
                "Webhook idempotency handling guaranteeing zero duplicate charges"
            ],
            "roadmap": [
                "Milestone 1: Multi-party transaction database schema (Orders, Escrows, Payouts)",
                "Milestone 2: Stripe Connect API client with idempotency-key headers",
                "Milestone 3: Webhook listener processing checkout.session.completed & delivery confirmations",
                "Milestone 4: Edge-case test harness simulating partial refunds and dispute chargebacks"
            ],
            "industry_rubric": "Evaluates idempotency handling, avoidance of floating-point money rounding errors (integer cents only), and resilient multi-party state transitions."
        },
        # Intermediate 3
        {
            "id": "mp-int-03",
            "title": "High-Throughput Batch Order Dispatcher with Bipartite Graph Matching",
            "difficulty": "Intermediate",
            "hours": 28,
            "primary_skills": ["Python", "Go", "Redis", "PostgreSQL", "pytest"],
            "non_tech_competencies": ["Combinatorial Optimization", "Batch Dispatching", "Queue Management"],
            "executive_summary": "Greedy first-come-first-served dispatching leads to suboptimal routes and long wait times. This dispatcher pools orders in 10-second batch windows and solves the assignment problem using bipartite graph matching (Hungarian algorithm).",
            "architecture_summary": "Background batch optimization worker consuming pending orders and available couriers, executing cost matrix minimization, and dispatching assignments atomically.",
            "key_features": [
                "Time-windowed batch accumulator collecting orders and candidate couriers",
                "Cost matrix generation factoring in distance, wait time, and courier ratings",
                "Kuhn-Munkres (Hungarian) matching maximizing global fulfillment efficiency",
                "Fallback to greedy assignment if batch worker latency exceeds 2 seconds"
            ],
            "roadmap": [
                "Milestone 1: Order queue and batch window scheduler",
                "Milestone 2: Cost matrix calculation engine with distance weighting",
                "Milestone 3: Bipartite matching solver with atomic Redis reservation",
                "Milestone 4: Comparative benchmark proving >= 22% reduction in total customer wait time vs greedy dispatch"
            ],
            "industry_rubric": "Evaluates algorithmic optimization skills, awareness of O(N^3) computational limits, and practical timeout fallbacks."
        },
        # Intermediate 4
        {
            "id": "mp-int-04",
            "title": "Marketplace Disintermediation & Fee-Evasion Detection Pipeline",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"],
            "non_tech_competencies": ["Platform Leakage & Fraud", "Content Moderation", "Heuristic Detection"],
            "executive_summary": "Platform disintermediation occurs when buyers and sellers connect on-platform but conduct payments off-platform (e.g. Venmo, WhatsApp, cash) to evade commission fees. This pipeline inspects message streams to detect and flag fee evasion.",
            "architecture_summary": "Message auditing pipeline scanning in-platform buyer-seller chat for phone numbers, email obfuscations, off-platform payment handles, and external links.",
            "key_features": [
                "Regex and phonetic pattern matching for obfuscated phone numbers",
                "Detection of payment keyword handles ('venmo', 'zelle', 'cashapp', 'paypal', 'wire')",
                "Risk scoring engine assigning disintermediation probability to buyer-seller pairs",
                "Automated warning prompts and seller shadowbanning workflows"
            ],
            "roadmap": [
                "Milestone 1: Chat message ingestion schema and message audit ledger",
                "Milestone 2: Obfuscated contact pattern extractor and phonetic normalizer",
                "Milestone 3: Real-time interceptor middleware evaluating message risk score",
                "Milestone 4: Adversarial test suite with 50+ adversarial evasion tricks"
            ],
            "industry_rubric": "Evaluates understanding of platform economics, regex precision/recall tradeoffs, and non-blocking asynchronous pipeline design."
        },
        # Advanced 1
        {
            "id": "mp-adv-01",
            "title": "Uber-Scale Geospatial Ride Dispatch & Dynamic Pricing System with H3 Grid & Kafka",
            "difficulty": "Advanced",
            "hours": 38,
            "primary_skills": ["Python", "Go", "Redis", "Apache Kafka", "Docker"],
            "non_tech_competencies": ["Large-Scale Distributed Systems", "Hexagonal Geospatial Indexing", "High-Throughput Streaming"],
            "executive_summary": "High-frequency ridehailing platforms process tens of thousands of GPS updates per second across hexagonal grid partitions. This system utilizes Uber H3 spatial indexes and Kafka event streams to coordinate distributed dispatching and localized surge pricing.",
            "architecture_summary": "Distributed event-driven architecture ingesting driver telemetry into Kafka, indexing locations into H3 resolution-8 hexagonal cells in Redis, and executing localized dispatching.",
            "key_features": [
                "Uber H3 spatial index mapping latitude/longitude coordinates to resolution-8 hexagonal cells",
                "Kafka topic partitioning by geospatial cell ID for linear horizontal scalability",
                "Sub-50ms supply/demand aggregations per hexagon",
                "Ring-k neighborhood expansion looking up drivers in adjacent hexes when immediate cell is depleted"
            ],
            "roadmap": [
                "Milestone 1: Kafka GPS telemetry ingestion pipeline with H3 spatial encoding",
                "Milestone 2: Redis in-memory hex registry with TTL expiration for inactive drivers",
                "Milestone 3: Multi-hex ring expansion dispatch algorithm",
                "Milestone 4: High-volume Locust load test simulating 5,000 active concurrent drivers and 500 requests/sec"
            ],
            "industry_rubric": "Evaluates distributed partition strategies, memory footprint optimization in Redis, and zero deadlocks during high-concurrency dispatch."
        },
        # Advanced 2
        {
            "id": "mp-adv-02",
            "title": "Double-Entry Multi-Party Accounting Ledger with ACID Transaction Guarantees",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "SQL", "PostgreSQL", "FastAPI", "Docker"],
            "non_tech_competencies": ["Financial Ledger Engineering", "ACID Transactions", "Idempotency & Auditability"],
            "executive_summary": "In a three-party marketplace (Buyer, Seller, Platform), every penny must balance. This system implements an immutable, double-entry financial ledger where every credit has an equal and opposite debit, backed by strict database constraints.",
            "architecture_summary": "Append-only relational accounting ledger built on PostgreSQL with strict foreign keys, check constraints preventing negative balance drifts, and serialized transactions.",
            "key_features": [
                "Immutable journal entry table with line items enforcing sum(Credits) - sum(Debits) = 0",
                "Optimistic concurrency control with account versioning",
                "Cryptographic SHA-256 hash chaining verifying ledger integrity",
                "Automated end-of-day balance reconciliation script asserting zero variance"
            ],
            "roadmap": [
                "Milestone 1: Double-entry ledger schema (Accounts, Journals, Postings) with check constraints",
                "Milestone 2: Atomic posting service supporting escrow holds, fee splits, and payouts",
                "Milestone 3: Concurrent transfer simulation with PostgreSQL SERIALIZABLE transaction isolation",
                "Milestone 4: Automated audit runner verifying cryptographic hash chain against tampering"
            ],
            "industry_rubric": "Evaluates financial engineering rigor, mastery of relational transaction isolation levels (SERIALIZABLE vs READ COMMITTED), and prevention of race condition overdrafts."
        },
        # Advanced 3
        {
            "id": "mp-adv-03",
            "title": "Generalized Second-Price (GSP) Sponsored Listing Auction Engine",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "FastAPI", "Redis", "PostgreSQL", "Docker"],
            "non_tech_competencies": ["Auction Theory & Mechanism Design", "Ad Monetization", "Latency Budgets"],
            "executive_summary": "E-commerce marketplaces monetize search rankings via sponsored listing auctions. This engine runs a real-time Generalized Second-Price (GSP) auction calculating winning ad placements and second-price cost-per-click (CPC) within a 20ms SLA.",
            "architecture_summary": "In-memory auction bidding engine ranking seller bids using Expected Cost Per Mille (eCPM = Bid * CTR) and calculating second-price billing amounts.",
            "key_features": [
                "Generalized Second-Price auction mechanism where winner pays the minimum bid necessary to retain rank",
                "Historical Click-Through Rate (CTR) quality score weighting bids to protect user experience",
                "Sub-20ms auction execution using Redis sorted sets and pre-computed quality scores",
                "Budget pacing algorithm distributing daily seller spend evenly across hours"
            ],
            "roadmap": [
                "Milestone 1: Advertiser campaign schema, bidding limits, and daily budget counters",
                "Milestone 2: In-memory GSP auction solver calculating winner rankings and second-price charges",
                "Milestone 3: Fast auction endpoint integrated into search query pipeline",
                "Milestone 4: Benchmark suite verifying sub-20ms P99 latency under 2,000 requests/sec"
            ],
            "industry_rubric": "Evaluates auction mechanism theory (truthful bidding incentives), real-time latency budget management, and algorithmic correctness."
        },
        # Advanced 4
        {
            "id": "mp-adv-04",
            "title": "Zero-Trust Marketplace Fraud & Sybil Attack Prevention Mesh",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["Python", "FastAPI", "Redis", "PostgreSQL", "Docker"],
            "non_tech_competencies": ["Trust & Safety Engineering", "Graph Anomaly Detection", "Sybil Resistance"],
            "executive_summary": "Fraudulent rings create fake buyer and seller accounts to execute wash trading, fake review farming, and stolen credit card cashouts. This security mesh builds a graph-based identity network detecting collusion and Sybil rings.",
            "architecture_summary": "Real-time fraud detection pipeline analyzing device fingerprints, IP subnets, payment method hashes, and interaction graphs.",
            "key_features": [
                "Graph network analysis identifying circular transaction loops between buyer and seller clusters",
                "Device fingerprint and payment card hash linking identifying multi-account operators",
                "Velocity tripwires blocking accounts with abnormal booking frequency",
                "Automated risk score calculation triggering SMS/ID verification challenges"
            ],
            "roadmap": [
                "Milestone 1: Identity and device telemetry ingestion pipeline",
                "Milestone 2: Circular transaction loop detector and shared attribute clustering",
                "Milestone 3: Real-time risk scoring middleware intercepting suspicious checkouts",
                "Milestone 4: Fraud simulation suite asserting detection of 5 distinct collusion attack vectors"
            ],
            "industry_rubric": "Evaluates understanding of marketplace fraud vectors, graph data modeling, and balancing fraud catch-rate against false-positive customer friction."
        }
    ],
    # -------------------------------------------------------------------------
    # 8. Cybersecurity, Ethical Hacking & Application Security (10 Projects)
    # -------------------------------------------------------------------------
    "security_cyber": [
        # Beginner 1
        {
            "id": "sec-beg-01",
            "title": "Automated Port Reconnaissance & Banner Grabbing Engine with Scapy",
            "difficulty": "Beginner",
            "hours": 16,
            "primary_skills": ["Python", "Nmap", "Wireshark", "Linux", "Git"],
            "non_tech_competencies": ["Network Security Fundamentals", "Defensive Reconnaissance", "Documentation"],
            "executive_summary": "Unsecured or misconfigured exposed ports are the leading attack vector for unauthorized intrusion. This service conducts automated network reconnaissance, grabs service banners, flags insecure open ports, and generates JSON security reports.",
            "architecture_summary": "Async networking client utilizing Python raw sockets and Scapy packet dissection with structured JSON output and pytest mock socket suite.",
            "key_features": [
                "Multi-threaded TCP SYN and connect scan across targeted subnet ranges",
                "Service banner grabbing identifying outdated software versions and CVE risks",
                "Formatted JSON security audit report with severity scoring",
                "Isolated test harness simulating open, closed, and filtered port responses"
            ],
            "roadmap": [
                "Milestone 1: Raw socket connect engine and CIDR subnet parser",
                "Milestone 2: Banner grabbing module and common service fingerprint database",
                "Milestone 3: Risk assessment scoring engine and JSON reporting output",
                "Milestone 4: Automated pytest test suite mocking network socket responses"
            ],
            "industry_rubric": "Evaluates understanding of TCP handshakes, socket timeouts, non-destructive scanning ethics, and structured logging."
        },
        # Beginner 2
        {
            "id": "sec-beg-02",
            "title": "OWASP Top 10 Web Vulnerability Fuzzer & SQLi/XSS Detection Suite",
            "difficulty": "Beginner",
            "hours": 18,
            "primary_skills": ["Python", "Burp Suite", "OWASP Top 10", "Linux", "pytest"],
            "non_tech_competencies": ["Web Security Standards", "Vulnerability Reporting", "Ethical Disclosure"],
            "executive_summary": "Web applications frequently leak data via injection flaws and unfiltered inputs. This testing suite fuzzes HTTP endpoints with safe boundary payloads to detect SQL injection, reflected Cross-Site Scripting (XSS), and path traversal.",
            "architecture_summary": "Modular security auditing tool utilizing Python HTTP client with payload dictionary generator, response differential analyzer, and test coverage.",
            "key_features": [
                "Payload generation engine testing union-based and boolean-blind SQL injection",
                "Context-aware XSS reflection scanner validating script tag sanitization",
                "Directory traversal probe verifying path boundary restrictions (../)",
                "Automated Markdown audit report generation mapping findings to OWASP Top 10 categories"
            ],
            "roadmap": [
                "Milestone 1: HTTP probe request engine and parameter discovery logic",
                "Milestone 2: Injection payload dictionaries and response anomaly detector",
                "Milestone 3: False-positive reduction heuristics and severity rating calculator",
                "Milestone 4: End-to-end test against intentional vulnerable target container"
            ],
            "industry_rubric": "Evaluates comprehension of web injection mechanisms, difference between reflected and persistent vulnerabilities, and clear remediation guidance."
        },
        # Intermediate 1
        {
            "id": "sec-int-01",
            "title": "Defensive Web Application Firewall (WAF) & Request Sanitization Proxy",
            "difficulty": "Intermediate",
            "hours": 24,
            "primary_skills": ["Python", "FastAPI", "OWASP Top 10", "Docker", "Linux"],
            "non_tech_competencies": ["Threat Modeling", "Defensive Architecture", "API Security"],
            "executive_summary": "Legacy web services often cannot be patched immediately when new exploits emerge. This reverse-proxy WAF inspects inbound HTTP requests in real-time, blocks malicious payloads, and rate-limits suspicious clients.",
            "architecture_summary": "High-performance ASGI middleware proxy utilizing FastAPI and regex pattern matching trees with security event logging and Docker deployment.",
            "key_features": [
                "Deep packet inspection of query parameters, headers, cookies, and JSON request bodies",
                "Configurable rule engine matching regex signatures for SQLi, XSS, and remote code execution",
                "Sliding-window IP reputation tracker and progressive rate limiting",
                "Structured security audit logger with RFC-5424 syslog output for SIEM integration"
            ],
            "roadmap": [
                "Milestone 1: ASGI reverse-proxy pipeline with request and response streaming",
                "Milestone 2: Security inspection ruleset and signature matching engine",
                "Milestone 3: IP velocity rate limiter and blocklist management layer",
                "Milestone 4: Comprehensive test suite verifying zero bypass of OWASP test payloads"
            ],
            "industry_rubric": "Evaluates defensive programming, balancing low proxy latency against deep inspection, and avoiding denial-of-service in regex matching."
        },
        # Intermediate 2
        {
            "id": "sec-int-02",
            "title": "Cryptographic Key Vault & Zero-Knowledge Secret Storage Service",
            "difficulty": "Intermediate",
            "hours": 26,
            "primary_skills": ["Python", "Cryptography", "TLS/SSL", "Linux", "Docker"],
            "non_tech_competencies": ["Cryptographic Governance", "Key Lifecycle Management", "Compliance"],
            "executive_summary": "Centralized credential storage requires defense-in-depth where even database compromises cannot expose raw secrets. This service implements envelope encryption with authenticated AES-256-GCM and Argon2id key derivation.",
            "architecture_summary": "REST microservice with AES-256-GCM envelope encryption, Argon2id master passphrase stretching, automated key rotation, and HMAC integrity checks.",
            "key_features": [
                "Authenticated encryption with AES-256-GCM preventing ciphertext tampering",
                "Argon2id key derivation resisting GPU/ASIC hardware brute-force attacks",
                "Envelope encryption pattern separating data encryption keys (DEK) from master keys (KEK)",
                "Cryptographic audit log signed with HMAC-SHA256 preventing log alteration"
            ],
            "roadmap": [
                "Milestone 1: Cryptographic primitive engine (AES-GCM, Argon2id, HMAC)",
                "Milestone 2: Key hierarchy management and envelope encryption workflows",
                "Milestone 3: REST API with scoped access tokens and key rotation endpoints",
                "Milestone 4: Cryptographic validation test suite asserting tamper detection and zero plain-text leaks"
            ],
            "industry_rubric": "Evaluates correct implementation of cryptographic primitives, proper IV/nonce handling, and zero memory persistence of plain-text keys."
        },
        # Intermediate 3
        {
            "id": "sec-int-03",
            "title": "Credential Stuffing & Auth Brute-Force Detection Engine with Redis",
            "difficulty": "Intermediate",
            "hours": 22,
            "primary_skills": ["Python", "Redis", "Docker", "Linux", "pytest"],
            "non_tech_competencies": ["Abuse Prevention", "Anomaly Detection", "Observability"],
            "executive_summary": "Automated credential stuffing attacks use leaked credential dumps to compromise user accounts at high velocity. This engine tracks authentication telemetry across IP, username, and device fingerprints to thwart account takeovers.",
            "architecture_summary": "Sliding-window analytics service built with Redis sorted sets, computing entropy scores across login attempts to distinguish human users from botnets.",
            "key_features": [
                "Sliding-window rate limiter tracking login failures per IP and per target username",
                "Distributed lock-out mechanism with exponential backoff and captcha challenge flags",
                "Anomaly scoring based on User-Agent entropy, request frequency, and IP subnet clustering",
                "Real-time alerting webhook notifying security operations teams of active distributed brute-force campaigns"
            ],
            "roadmap": [
                "Milestone 1: Redis sorted-set sliding window tracking engine",
                "Milestone 2: Distributed credential stuffing detection heuristics and threshold policies",
                "Milestone 3: Auth middleware integration and risk score calculator",
                "Milestone 4: Simulated botnet attack benchmark verifying detection under high load"
            ],
            "industry_rubric": "Evaluates understanding of distributed botnet attacks, balancing security barriers with user login friction, and efficient Redis query patterns."
        },
        # Intermediate 4
        {
            "id": "sec-int-04",
            "title": "Automated Container Hardening & Static Image Vulnerability Scanner",
            "difficulty": "Intermediate",
            "hours": 20,
            "primary_skills": ["Docker", "Linux", "Bash", "Python", "Git"],
            "non_tech_competencies": ["DevSecOps CI/CD", "Vulnerability Triage", "Shift-Left Security"],
            "executive_summary": "Vulnerable base images and misconfigured container manifests expose production clusters to container escapes. This scanner inspects container layers, detects root execution, audit permissions, and blocks vulnerable builds in CI.",
            "architecture_summary": "Static analysis pipeline parsing Dockerfiles, OCI image manifests, and package lockfiles, outputting SARIF reports for GitHub Actions integration.",
            "key_features": [
                "Dockerfile AST parser enforcing non-root user directives and multi-stage builds",
                "Package version cross-referencing against National Vulnerability Database (NVD) CVE feeds",
                "Detection of hardcoded secrets, private keys, and environment variables in image layers",
                "SARIF formatted output for direct integration into CI/CD security quality gates"
            ],
            "roadmap": [
                "Milestone 1: Dockerfile parser and policy compliance validator (CIS Docker Benchmark)",
                "Milestone 2: OCI image layer unpacker and file permission auditor",
                "Milestone 3: CVE database matching engine and severity threshold filter",
                "Milestone 4: GitHub Actions pipeline enforcing build failure on Critical CVEs"
            ],
            "industry_rubric": "Evaluates container isolation mechanics, understanding of Linux capabilities/cgroups, and embedding security gates seamlessly into engineering workflows."
        },
        # Advanced 1
        {
            "id": "sec-adv-01",
            "title": "Distributed Low-Interaction Honeypot Network & Threat Intelligence Sensor",
            "difficulty": "Advanced",
            "hours": 32,
            "primary_skills": ["Python", "Linux", "Docker", "Packet Analysis", "Wireshark"],
            "non_tech_competencies": ["Threat Intelligence", "Adversary TTPs", "MITRE ATT&CK Mapping"],
            "executive_summary": "Active defense requires early reconnaissance intelligence on attacker tactics. This distributed honeypot exposes fake SSH and HTTP services to capture adversary command attempts, exploit payloads, and brute-force dictionaries.",
            "architecture_summary": "Async event-driven honeypot cluster using Python asyncio, emulating vulnerable service banners, logging session telemetry, and classifying attacks via MITRE ATT&CK.",
            "key_features": [
                "Simulated interactive SSH shell capturing attacker commands, wget/curl download attempts, and keystrokes",
                "HTTP decoy endpoints trapping exploit probes for Log4j, Spring4Shell, and path traversal",
                "Automated malware payload extraction and SHA-256 fingerprint generation",
                "Real-time threat feed mapping adversary IP addresses and tactics to MITRE ATT&CK techniques"
            ],
            "roadmap": [
                "Milestone 1: Emulated SSH service listener with fake filesystem navigation",
                "Milestone 2: HTTP decoy service with fake admin panels and exploit traps",
                "Milestone 3: Threat intelligence aggregator and IOC (Indicators of Compromise) publisher",
                "Milestone 4: Attack simulation test validating payload capture and alert dispatch"
            ],
            "industry_rubric": "Evaluates defensive deception techniques, sandbox isolation preventing honeypot compromise, and structured cyber threat intelligence (STIX/TAXII)."
        },
        # Advanced 2
        {
            "id": "sec-adv-02",
            "title": "Zero-Trust Microservice Mesh Identity & Mutual TLS (mTLS) Attestation Gateway",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Go", "TLS/SSL", "Docker", "Linux", "Cryptography"],
            "non_tech_competencies": ["Zero-Trust Architecture", "PKI Governance", "Distributed Systems Security"],
            "executive_summary": "Perimeter network security is obsolete; services must verify identity on every packet. This gateway implements SPIFFE/SPIRE-compatible cryptographic workload identity with automated short-lived X.509 certificate issuance and strict mTLS encryption.",
            "architecture_summary": "High-throughput Go proxy implementing bidirectional TLS 1.3 handshake verification, cryptographic SAN certificate validation, and least-privilege service-to-service authorization.",
            "key_features": [
                "Automated Public Key Infrastructure (PKI) issuing 1-hour ephemeral X.509 workload certificates",
                "Strict mTLS enforcement with TLS 1.3 cipher suites and client certificate validation",
                "Cryptographic SPIFFE ID parsing from SAN extensions to enforce service-level authorization matrices",
                "Zero-downtime certificate rotation and automated CRL/OCSP revocation checks"
            ],
            "roadmap": [
                "Milestone 1: Internal Certificate Authority (CA) and ephemeral cert generation pipeline",
                "Milestone 2: Go mTLS reverse proxy with custom certificate verification callbacks",
                "Milestone 3: Service identity authorization matrix enforcing least-privilege communication",
                "Milestone 4: Stress test demonstrating seamless certificate rotation under active traffic"
            ],
            "industry_rubric": "Evaluates deep knowledge of TLS 1.3 handshakes, PKI architecture, non-blocking certificate rotation, and zero-trust security postures."
        },
        # Advanced 3
        {
            "id": "sec-adv-03",
            "title": "Binary Exploit Analysis & Memory Protection Bypass Research Sandbox",
            "difficulty": "Advanced",
            "hours": 34,
            "primary_skills": ["C", "Python", "Linux", "Assembly", "Reverse Engineering"],
            "non_tech_competencies": ["Offensive Security Research", "Root-Cause Analysis", "Responsible Vulnerability Disclosure"],
            "executive_summary": "Understanding memory corruption vulnerabilities is essential for offensive security research and defensive compiler hardening. This sandbox analyzes compiled ELF binaries, detects buffer overflows and format string flaws, and demonstrates return-oriented programming (ROP) concepts safely.",
            "architecture_summary": "Isolated Linux sandbox environment utilizing GDB/Python scripts, dissecting stack frames, verifying ASLR/NX/Canary protections, and generating proof-of-concept mitigation patches.",
            "key_features": [
                "Automated checksec module evaluating binary compilation flags (ASLR, Stack Canaries, NX/DEP, RELRO)",
                "Fuzzing harness triggering memory segmentation faults and analyzing core dumps",
                "Proof-of-concept payload generation demonstrating instruction pointer control in controlled environments",
                "Defensive remediation patch compiler applying safe C libraries and compiler sanitizers (-fsanitize=address)"
            ],
            "roadmap": [
                "Milestone 1: Binary inspection tool evaluating memory protections and symbol tables",
                "Milestone 2: Stack frame crash analyzer extracting registers (EIP/RIP) and stack offsets",
                "Milestone 3: Controlled proof-of-concept payload generator demonstrating memory hijack vectors",
                "Milestone 4: Automated compiler remediation pipeline compiling memory-safe patched binaries"
            ],
            "industry_rubric": "Evaluates low-level understanding of x86/x64 assembly, stack memory layouts, memory mitigations, and transforming exploit findings into defensive compiler hardening."
        },
        # Advanced 4
        {
            "id": "sec-adv-04",
            "title": "Enterprise Red Team Command & Control (C2) Detection & Network Threat Hunter",
            "difficulty": "Advanced",
            "hours": 36,
            "primary_skills": ["Python", "Wireshark", "Packet Analysis", "Linux", "Docker"],
            "non_tech_competencies": ["Threat Hunting", "Network Forensics", "SOC Incident Escalation"],
            "executive_summary": "Sophisticated adversaries bypass firewalls using encrypted C2 channels, DNS tunneling, and sleep jitter. This network hunting engine analyzes live packet captures, detects beaconing intervals, uncovers DNS exfiltration, and triggers automated incident response.",
            "architecture_summary": "High-speed packet capture and stream processing pipeline analyzing pcap streams with statistical frequency analysis (FFT) to detect periodic beaconing.",
            "key_features": [
                "Fast Fourier Transform (FFT) analysis on network flow timing detecting beaconing jitter within encrypted sessions",
                "DNS tunneling detector measuring base64 subdomain entropy and TXT record volume anomalies",
                "JA3 and JA3S TLS fingerprint extraction matching suspicious SSL client hello signatures",
                "Incident triage dashboard with automated PCAP snippet export for digital forensic investigation"
            ],
            "roadmap": [
                "Milestone 1: Pcap stream ingestion engine and protocol dissection layer",
                "Milestone 2: Statistical timing analyzer identifying periodic C2 beaconing rhythms",
                "Milestone 3: DNS entropy scanner detecting data exfiltration over UDP 53",
                "Milestone 4: End-to-end evaluation with recorded Cobalt Strike and Empire C2 traffic samples"
            ],
            "industry_rubric": "Evaluates network protocol depth, cryptographic fingerprinting (JA3), statistical anomaly detection, and actionable incident escalation."
        }
    ]
}


def get_projects_for_discipline(discipline: str) -> List[Dict[str, Any]]:
    """Returns the 10-project matrix for a given engineering discipline."""
    return TEN_PROJECT_MATRICES.get(discipline, TEN_PROJECT_MATRICES.get("backend_systems", []))
