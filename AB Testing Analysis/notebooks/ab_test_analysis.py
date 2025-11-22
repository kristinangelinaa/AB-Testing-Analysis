"""
A/B Testing Analysis - Marketing Campaign
Analyzes control vs test campaign performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

os.makedirs('../visualizations', exist_ok=True)

print("=" * 80)
print("A/B TESTING - MARKETING CAMPAIGN ANALYSIS")
print("=" * 80)

# ============================================
# 1. LOAD DATA
# ============================================

# Load both control and test groups
control = pd.read_csv('../../AB Testing DataSet/control_group.csv', sep=';')
test = pd.read_csv('../../AB Testing DataSet/test_group.csv', sep=';')

# Add variant labels
control['Variant'] = 'Control'
test['Variant'] = 'Test'

# Combine datasets
df = pd.concat([control, test], ignore_index=True)

# Convert date
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

# Clean column names
df.columns = df.columns.str.strip()

print("\nDataset Overview:")
print(f"Total Observations: {len(df):,}")
print(f"Control Group: {len(control):,}")
print(f"Test Group: {len(test):,}")
print(f"Date Range: {df['Date'].min().date()} to {df['Date'].max().date()}")

# ============================================
# 2. OVERALL METRICS COMPARISON
# ============================================

print("\n" + "=" * 80)
print("CAMPAIGN PERFORMANCE COMPARISON")
print("=" * 80)

summary = df.groupby('Variant').agg({
    'Spend [USD]': 'sum',
    '# of Impressions': 'sum',
    'Reach': 'sum',
    '# of Website Clicks': 'sum',
    '# of Searches': 'sum',
    '# of View Content': 'sum',
    '# of Add to Cart': 'sum',
    '# of Purchase': 'sum'
}).round(2)

# Calculate metrics
summary['CTR (%)'] = (summary['# of Website Clicks'] / summary['# of Impressions'] * 100).round(2)
summary['Conversion Rate (%)'] = (summary['# of Purchase'] / summary['# of Website Clicks'] * 100).round(2)
summary['CPC (USD)'] = (summary['Spend [USD]'] / summary['# of Website Clicks']).round(2)
summary['Cost Per Purchase (USD)'] = (summary['Spend [USD]'] / summary['# of Purchase']).round(2)

print("\nCampaign Summary:")
print(summary)

# Calculate lifts
control_summary = summary.loc['Control']
test_summary = summary.loc['Test']

print("\n" + "-" * 80)
print("KEY METRICS COMPARISON")
print("-" * 80)

metrics_to_compare = ['CTR (%)', 'Conversion Rate (%)', '# of Purchase', 'Cost Per Purchase (USD)']

for metric in metrics_to_compare:
    control_val = control_summary[metric]
    test_val = test_summary[metric]

    if 'Cost' in metric:
        lift = ((control_val - test_val) / control_val * 100)  # Lower is better
        better = "Test" if test_val < control_val else "Control"
    else:
        lift = ((test_val - control_val) / control_val * 100)  # Higher is better
        better = "Test" if test_val > control_val else "Control"

    print(f"\n{metric}:")
    print(f"  Control: {control_val:.2f}")
    print(f"  Test: {test_val:.2f}")
    print(f"  Lift: {abs(lift):.1f}% ({'↑' if lift > 0 else '↓'})")
    print(f"  Winner: {better}")

# ============================================
# 3. STATISTICAL SIGNIFICANCE - CONVERSION RATE
# ============================================

print("\n" + "=" * 80)
print("STATISTICAL SIGNIFICANCE TESTING")
print("=" * 80)

# Purchases vs Clicks (conversion rate)
control_clicks = control['# of Website Clicks'].sum()
control_purchases = control['# of Purchase'].sum()
test_clicks = test['# of Website Clicks'].sum()
test_purchases = test['# of Purchase'].sum()

# Create contingency table
contingency_table = np.array([
    [control_purchases, control_clicks - control_purchases],
    [test_purchases, test_clicks - test_purchases]
])

print("\nContingency Table (Purchases vs Non-Purchases):")
print(pd.DataFrame(contingency_table,
                  index=['Control', 'Test'],
                  columns=['Purchased', 'Did Not Purchase']))

# Chi-square test
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\nChi-Square Test Results:")
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Degrees of freedom: {dof}")

alpha = 0.05
if p_value < alpha:
    print(f"\n✓ STATISTICALLY SIGNIFICANT (p < {alpha})")
    print("  The difference in conversion rates is unlikely due to chance.")
else:
    print(f"\n✗ NOT statistically significant (p >= {alpha})")
    print("  The difference might be due to random variation.")

# ============================================
# 4. VISUALIZATIONS
# ============================================

print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Conversion funnel comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

funnel_metrics = ['# of Impressions', '# of Website Clicks', '# of View Content',
                 '# of Add to Cart', '# of Purchase']

control_funnel = control[funnel_metrics].sum()
test_funnel = test[funnel_metrics].sum()

x = np.arange(len(funnel_metrics))
width = 0.35

axes[0].bar(x - width/2, control_funnel, width, label='Control', color='#3498db', alpha=0.8)
axes[0].bar(x + width/2, test_funnel, width, label='Test', color='#2ecc71', alpha=0.8)
axes[0].set_ylabel('Count')
axes[0].set_title('Conversion Funnel Comparison', fontsize=14, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Impressions', 'Clicks', 'View Content', 'Add to Cart', 'Purchase'], rotation=45)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Conversion rates comparison
conversion_metrics = ['CTR (%)', 'Conversion Rate (%)']
control_rates = [control_summary[m] for m in conversion_metrics]
test_rates = [test_summary[m] for m in conversion_metrics]

x2 = np.arange(len(conversion_metrics))
axes[1].bar(x2 - width/2, control_rates, width, label='Control', color='#3498db', alpha=0.8)
axes[1].bar(x2 + width/2, test_rates, width, label='Test', color='#2ecc71', alpha=0.8)
axes[1].set_ylabel('Rate (%)')
axes[1].set_title('Key Conversion Rates', fontsize=14, fontweight='bold')
axes[1].set_xticks(x2)
axes[1].set_xticklabels(conversion_metrics)
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/conversion_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved: conversion_comparison.png")

# Daily trends
daily_control = control.groupby('Date')['# of Purchase'].sum()
daily_test = test.groupby('Date')['# of Purchase'].sum()

plt.figure(figsize=(14, 6))
plt.plot(daily_control.index, daily_control.values, marker='o', label='Control', linewidth=2, color='#3498db')
plt.plot(daily_test.index, daily_test.values, marker='o', label='Test', linewidth=2, color='#2ecc71')
plt.xlabel('Date')
plt.ylabel('Number of Purchases')
plt.title('Daily Purchase Trend', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizations/daily_trend.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved: daily_trend.png")

# Cost efficiency
cost_metrics = ['CPC (USD)', 'Cost Per Purchase (USD)']
control_costs = [control_summary[m] for m in cost_metrics]
test_costs = [test_summary[m] for m in cost_metrics]

plt.figure(figsize=(10, 6))
x3 = np.arange(len(cost_metrics))
plt.bar(x3 - width/2, control_costs, width, label='Control', color='#3498db', alpha=0.8)
plt.bar(x3 + width/2, test_costs, width, label='Test', color='#2ecc71', alpha=0.8)
plt.ylabel('Cost (USD)')
plt.title('Cost Efficiency Comparison', fontsize=14, fontweight='bold')
plt.xticks(x3, ['Cost Per Click', 'Cost Per Purchase'])
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/cost_efficiency.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved: cost_efficiency.png")

# ============================================
# 5. BUSINESS RECOMMENDATIONS
# ============================================

print("\n" + "=" * 80)
print("BUSINESS RECOMMENDATIONS")
print("=" * 80)

# Calculate ROI
control_roi = (control_summary['# of Purchase'] * 50 - control_summary['Spend [USD]']) / control_summary['Spend [USD]'] * 100  # Assuming $50 avg order value
test_roi = (test_summary['# of Purchase'] * 50 - test_summary['Spend [USD]']) / test_summary['Spend [USD]'] * 100

conv_rate_control = control_summary['Conversion Rate (%)']
conv_rate_test = test_summary['Conversion Rate (%)']

if p_value < alpha and conv_rate_test > conv_rate_control:
    recommendation = "IMPLEMENT TEST CAMPAIGN"
    reason = f"""
RECOMMENDATION: {recommendation}

1. STATISTICAL EVIDENCE
   - Test campaign has {conv_rate_test:.2f}% conversion rate vs {conv_rate_control:.2f}% for control
   - {((conv_rate_test - conv_rate_control) / conv_rate_control * 100):.1f}% relative improvement
   - Result is statistically significant (p = {p_value:.4f})

2. BUSINESS IMPACT
   - {test_purchases - control_purchases} additional purchases during test period
   - Cost per purchase: ${test_summary['Cost Per Purchase (USD)']:.2f} vs ${control_summary['Cost Per Purchase (USD)']:.2f}
   - Total test campaign purchases: {test_purchases}

3. IMPLEMENTATION PLAN
   - Roll out test campaign to 100% of audience
   - Monitor performance for 2 weeks
   - Track long-term metrics (retention, LTV)
   - Consider further optimization iterations

4. EXPECTED RESULTS
   - Projected {((conv_rate_test - conv_rate_control) / conv_rate_control * 100):.1f}% increase in conversions
   - Better cost efficiency: ${test_summary['Cost Per Purchase (USD)']:.2f} per purchase
   - Improved ROI: {test_roi:.1f}% vs {control_roi:.1f}%
    """
elif p_value >= alpha:
    recommendation = "CONTINUE TESTING OR ITERATE"
    reason = f"""
RECOMMENDATION: {recommendation}

1. STATISTICAL EVIDENCE
   - Results are NOT statistically significant (p = {p_value:.4f})
   - Cannot conclusively determine a winner
   - Difference may be due to random variation

2. OPTIONS
   a) Extend test duration for more data
   b) Increase sample size
   c) Make more dramatic changes to test variant
   d) Keep control campaign and test new variants

3. CURRENT PERFORMANCE
   - Control conversion: {conv_rate_control:.2f}%
   - Test conversion: {conv_rate_test:.2f}%
   - Difference: {abs(conv_rate_test - conv_rate_control):.2f}pp
    """
else:
    recommendation = "KEEP CONTROL CAMPAIGN"
    reason = f"""
RECOMMENDATION: {recommendation}

1. STATISTICAL EVIDENCE
   - Control outperforms test campaign
   - Difference is statistically significant
   - Do not implement test campaign

2. NEXT STEPS
   - Analyze why test underperformed
   - Design new test variants
   - Learn from unsuccessful elements
   - Run follow-up tests with improvements
    """

print(reason)

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
