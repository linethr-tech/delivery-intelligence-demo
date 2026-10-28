# Data Quality & Anomaly Detection – Beyond Basic Outlier Detection

## Overview

This repository is a small proof of concept illustrating how Data Science can complement existing Data Quality and anomaly-detection capabilities already available in modern data platforms such as Snowflake.

The objective is **not to rebuild functionality that already exists in Snowflake**, but to demonstrate where additional Data Science capabilities can provide value on top of the data platform.

Snowflake already provides Machine Learning functions for anomaly detection directly on time-series data. Therefore, a Data Science capability should focus on cases where additional analytical logic, business context, explainability, or domain-specific models are required.

---

## Why This Example?

A common Data Quality requirement is detecting unusual values or unexpected behaviour in data.

Examples include:

- unusual delivery delays
- unexpected quantities
- abnormal process durations
- unusual operational behaviour
- sudden changes in business KPIs

Basic anomaly detection can already be performed using native Snowflake capabilities.

The interesting Data Science question is therefore not simply:

> "Can we detect an outlier?"

but rather:

> "Can we understand why something is unusual, determine whether it matters to the business, and use that information to support a decision?"

---

## Example Use Case

For this small demonstration, we use a fictitious operational dataset containing observations such as:

- `date`
- `customer`
- `region`
- `planned_delivery_days`
- `actual_delivery_days`
- `delay_days`
- `quantity`

Most deliveries behave normally.

A small number of observations contain unusual delivery behaviour.

The objective is to identify those observations and explore how an analytical layer could distinguish between:

1. **Data Quality issues**
2. **Statistical anomalies**
3. **Potential business/process anomalies**

This distinction is important.

A value can be statistically unusual while still being perfectly valid data. Conversely, a Data Quality problem can exist without representing an interesting business anomaly.

---

## Architecture

```text
Operational Data
       |
       v
   Snowflake
       |
       +----------------------------+
       |                            |
       v                            v
Data Quality Checks        Snowflake ML
                         Anomaly Detection
                                   |
                                   v
                     Data Science Layer
                                   |
                    +--------------+--------------+
                    |              |              |
                    v              v              v
              Business       Explainability    Advanced
               Context                        ML Models
                    |
                    v
              Actionable Insight
```

The idea is to **reuse platform capabilities first** and introduce custom Data Science only when there is a clear additional business value.

---

## What Snowflake Already Provides

Snowflake includes native Machine Learning capabilities for anomaly detection.

For time-series data, `SNOWFLAKE.ML.ANOMALY_DETECTION` can be used to train an anomaly detection model and identify observations that deviate from expected behaviour.

Conceptually:

```sql
CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION delivery_anomaly_model(
    INPUT_DATA => TABLE(training_data),
    TIMESTAMP_COLNAME => 'DATE',
    TARGET_COLNAME => 'DELAY_DAYS',
    LABEL_COLNAME => ''
);
```

Anomalies can then be detected using the model's `DETECT_ANOMALIES` method.

The objective of this repository is therefore **not to replace Snowflake ML**.

---

## Where Data Science Adds Value

Once existing platform capabilities have been considered, Data Science can extend the solution in several directions.

### 1. Business-aware anomaly detection

An unusual value does not automatically mean there is a problem.

The relevance of an anomaly may depend on:

- customer
- product
- region
- supplier
- expected lead time
- operational constraints
- historical behaviour

Adding this context makes anomaly detection more useful for business decisions.

### 2. Explainability

Instead of only identifying an unusual observation, an analytical layer can help investigate:

> Why was this observation flagged?

Potential contributing factors could then be investigated and communicated to the business.

### 3. Root-cause analysis

The next analytical question after detecting a problem is:

> What factors are associated with the deviation?

This moves the use case from simple detection toward diagnostic analytics.

### 4. Predictive use cases

Once reliable historical patterns exist, the same analytical environment could evolve toward predictive use cases.

For example:

> Can we identify deliveries that are at risk before they become late?

This would represent a different business objective from Data Quality or retrospective outlier detection and would require appropriate validation before operational use.

---

## Repository Structure

```text
data-quality-anomaly-demo/
│
├── README.md
├── data/
│   └── delivery_data.csv
│
├── notebooks/
│   └── anomaly_detection_demo.ipynb
│
└── requirements.txt
```

---

## Technology

This small proof of concept uses:

- Python
- pandas
- scikit-learn
- Jupyter Notebook
- GitHub
- GitHub Copilot

The example intentionally remains lightweight.

The focus is not the complexity of the machine-learning model, but the **Data Science approach and how it complements the existing enterprise data platform**.

---

## Example Python Approach

For demonstration purposes, an Isolation Forest can be used on the fictitious dataset.

```python
from sklearn.ensemble import IsolationForest

features = [
    "planned_delivery_days",
    "actual_delivery_days",
    "delay_days",
    "quantity"
]

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df["anomaly"] = model.fit_predict(df[features])
```

This is intentionally a simple example.

In a real enterprise scenario, the first decision would be whether native Snowflake capabilities already satisfy the requirement.

A custom model should only be introduced when it provides additional value.

---

## Key Principle

> **Do not build Machine Learning simply because we can. Build it when it adds measurable value beyond existing platform capabilities.**

The proposed approach is:

**Reuse → Evaluate → Extend**

### Reuse

Use existing Snowflake Data Quality and ML capabilities whenever they satisfy the requirement.

### Evaluate

Understand the business problem and identify gaps that cannot be addressed adequately by existing platform functionality.

### Extend

Develop custom Data Science models only where they provide additional analytical or business value.

---

## From Data Quality to Delivery Intelligence

This example also illustrates a broader opportunity.

Rather than limiting Data Science to detecting incorrect or unusual data, the same capabilities can support operational intelligence.

For example:

**Data Quality**

"Is this delivery record unusual?"

↓

**Diagnostic Analytics**

"Why are some deliveries arriving late?"

↓

**Predictive Analytics**

"Which deliveries may be at risk?"

↓

**Delivery Intelligence**

"What information can help the business anticipate and manage delivery risk?"

This progression illustrates how Data Science can complement the data platform while remaining focused on business outcomes.

---

## Scope

This repository is intentionally a **small proof of concept**.

It is not intended to represent a production architecture or a complete Data Quality framework.

Its purpose is to demonstrate:

- understanding of existing platform capabilities
- pragmatic use of Data Science
- avoidance of duplicated functionality
- separation between Data Quality and business analytics
- the potential evolution from anomaly detection to business-oriented intelligence

---

## References

Snowflake ML – Anomaly Detection  
https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection

Snowflake ML – ANOMALY_DETECTION Class  
https://docs.snowflake.com/en/sql-reference/classes/anomaly_detection

Snowflake ML Functions  
https://docs.snowflake.com/en/guides-overview-ml-functions

---

## Author

**Dr. Lineth Rodriguez Pelliere**

Business Intelligence & Data Science

Proof of Concept – Data Quality / Anomaly Detection
