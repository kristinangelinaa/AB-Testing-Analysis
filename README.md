# A/B Testing Statistical Analysis

A comprehensive A/B testing analysis project demonstrating statistical hypothesis testing, experimental design, and data-driven decision making for product features.

## Project Overview

This project showcases rigorous statistical analysis of an A/B test experiment. It demonstrates skills essential for data analyst and business analyst roles in tech companies, particularly those with experimentation cultures (SaaS, e-commerce, product companies).

### What is A/B Testing?

A/B testing is a method of comparing two versions of a product feature to determine which performs better. This project analyzes a test where:
- **Variant A (Control)**: Original product experience
- **Variant B (Treatment)**: New feature variant
- **Goal**: Increase conversion rate

## Business Context

The experiment tests a new product feature designed to improve user conversion. Key questions:
1. Does Variant B increase conversion rate?
2. Is the result statistically significant?
3. What is the expected business impact?
4. Should we ship Variant B to all users?

## Dataset

**10,000 users** randomly assigned to variants over **14 days**

### Features

**Experiment Data**
- User ID
- Assignment Date
- Variant (A or B)
- Converted (0 or 1)

**User Attributes**
- Device (Mobile, Desktop, Tablet)
- Country (USA, UK, Canada, Germany, France)
- User Segment (New, Returning)

**Engagement Metrics**
- Time on Page (seconds)
- Pages Viewed
- Revenue (if converted)

## Technologies Used

- **Python**: Pandas, NumPy, SciPy
- **Statistics**: Chi-square test, Z-test for proportions
- **Data Visualization**: Matplotlib, Seaborn
- **SQL**: Experiment results queries
- **Statistical Concepts**: Hypothesis testing, confidence intervals, p-values

## Project Structure

```
05-AB-Testing-Analysis/
├── data/
│   └── ab_test_results.csv           # Experiment data
├── sql/
│   └── ab_test_queries.sql           # SQL analysis queries
├── notebooks/
│   └── ab_test_analysis.py           # Statistical analysis script
├── visualizations/                    # Generated charts
├── generate_data.py                   # Data generation script
├── requirements.txt                   # Dependencies
└── README.md                          # This file
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Experiment Data

```bash
python generate_data.py
```

Creates realistic A/B test data with known effect size.

### 3. Run Statistical Analysis

```bash
cd notebooks
python ab_test_analysis.py
```

This performs:
- Conversion rate analysis
- Statistical significance testing
- Confidence interval calculation
- Segment analysis
- Business recommendations

### 4. SQL Analysis (Optional)

```bash
sqlite3 abtest.db
.mode csv
.import data/ab_test_results.csv ab_test
```

Run queries from `sql/ab_test_queries.sql`.

## Statistical Methodology

### Hypothesis Testing

**Null Hypothesis (H0)**: Conversion rate of A = Conversion rate of B
**Alternative Hypothesis (H1)**: Conversion rate of A ≠ Conversion rate of B

### Tests Performed

1. **Chi-Square Test**
   - Tests independence between variant and conversion
   - Provides overall significance measure

2. **Z-Test for Proportions**
   - Compares two conversion rates
   - More specific to A/B testing scenarios

3. **Confidence Intervals**
   - 95% CI for each variant's conversion rate
   - CI for lift (difference between variants)

### Significance Criteria

- **Significance Level (α)**: 0.05 (5%)
- **Confidence Level**: 95%
- **Decision Rule**: Reject H0 if p-value < 0.05

## Sample Results

### Overall Metrics
- **Variant A (Control)**: 12.0% conversion rate
- **Variant B (Treatment)**: 13.8% conversion rate
- **Absolute Lift**: 1.8 percentage points
- **Relative Lift**: 15%

### Statistical Significance
- **Chi-Square Statistic**: ~8.2
- **P-value**: ~0.004
- **Result**: STATISTICALLY SIGNIFICANT ✓
- **Conclusion**: Variant B significantly outperforms Variant A

### Confidence Intervals
- **Variant A**: [11.2%, 12.8%]
- **Variant B**: [12.9%, 14.7%]
- **Lift**: [0.6pp, 3.0pp]

### Segment Analysis
All segments show positive trends:
- **Mobile**: +16% lift
- **Desktop**: +14% lift
- **New Users**: +18% lift
- **Returning Users**: +13% lift

## Business Impact

### Projected Annual Impact (example)
- **Current Conversions**: 120,000/year
- **With Variant B**: 138,000/year
- **Additional Conversions**: 18,000/year
- **Revenue Impact**: $1.4M+ (at $80 avg order value)

### Recommendation
✓ **Implement Variant B** - Statistically significant improvement with high confidence

## Visualizations

The project generates:
1. **Conversion Rate Comparison**: Bar chart with confidence intervals
2. **Users vs Conversions**: Funnel visualization
3. **Segment Analysis**: Device and user segment breakdowns
4. **Daily Trends**: Time series of conversion rates

## SQL Queries Included

- Overall test results by variant
- Conversion rates by device, segment, country
- Daily conversion trends
- Revenue analysis
- Engagement metrics comparison
- Statistical significance calculations
- Winner determination logic

## Key Concepts Demonstrated

### Statistical Rigor
- Proper hypothesis formulation
- Multiple statistical tests
- Confidence interval interpretation
- P-value understanding
- Type I/II error awareness

### Business Acumen
- Translating statistics into business impact
- Clear recommendations
- Risk assessment
- Implementation planning

### Experimental Design
- Random assignment verification
- Sample size considerations
- Segment analysis
- Metric selection

## Common A/B Testing Mistakes (Avoided)

1. ✓ **Proper Randomization**: 50/50 split verified
2. ✓ **Sufficient Sample Size**: 10,000 users provides adequate power
3. ✓ **Statistical Testing**: Formal hypothesis tests, not just eyeballing
4. ✓ **Segment Analysis**: Check for Simpson's Paradox
5. ✓ **Confidence Intervals**: Quantify uncertainty
6. ✓ **Business Context**: Results tied to actionable recommendations

## Skills Demonstrated

- **Statistical Analysis**: Hypothesis testing, confidence intervals
- **Python**: SciPy, statistical computing
- **SQL**: Experiment analysis queries
- **Data Visualization**: Clear, actionable charts
- **Communication**: Technical results → business recommendations
- **Experimental Design**: A/B test best practices
- **Business Analysis**: ROI calculation, impact assessment

## Extensions & Future Work

- **Bayesian A/B Testing**: Alternative to frequentist approach
- **Multi-Armed Bandit**: Adaptive allocation during test
- **Sequential Testing**: Early stopping rules
- **Multi-Variant Testing**: A/B/C/D tests
- **Long-term Effects**: Retention, lifetime value analysis
- **Sample Size Calculator**: Pre-test power analysis tool

## Real-World Applications

This methodology applies to testing:
- Product features and UI changes
- Marketing campaigns and messaging
- Pricing strategies
- Recommendation algorithms
- Email subject lines and content
- Landing page designs

## Resources

### Statistical Concepts
- Type I Error (False Positive): Incorrectly rejecting H0
- Type II Error (False Negative): Failing to reject false H0
- Statistical Power: Probability of detecting true effect
- Effect Size: Magnitude of difference

### When to Use A/B Testing
- Clear success metric (conversion, revenue, engagement)
- Sufficient traffic for statistical power
- Ability to randomize users
- Meaningful business question

## License

This project is open source and available for portfolio purposes.
