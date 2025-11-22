"""
A/B Test Data Generator
Generates user experiment data for A/B testing analysis
Simulates a product feature test with realistic conversion differences
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# Experiment parameters
num_users = 10000
start_date = datetime(2024, 6, 1)
experiment_duration_days = 14

# Treatment effect: variant B has 15% higher conversion rate
control_conversion_rate = 0.12  # 12% baseline
treatment_lift = 0.15  # 15% relative lift
variant_conversion_rate = control_conversion_rate * (1 + treatment_lift)  # ~13.8%

users = []

for user_id in range(1, num_users + 1):
    # Random assignment (50/50 split)
    variant = random.choice(['A', 'B'])

    # Random assignment date during experiment
    days_offset = random.randint(0, experiment_duration_days - 1)
    assignment_date = start_date + timedelta(days=days_offset)

    # User characteristics
    device = random.choice(['Mobile', 'Desktop', 'Tablet'], p=[0.6, 0.35, 0.05])
    country = random.choice(['USA', 'UK', 'Canada', 'Germany', 'France'],
                           p=[0.5, 0.2, 0.15, 0.1, 0.05])
    user_segment = random.choice(['New', 'Returning'], p=[0.4, 0.6])

    # Device and segment influence conversion
    device_boost = {'Mobile': 0, 'Desktop': 0.02, 'Tablet': -0.01}
    segment_boost = {'New': -0.01, 'Returning': 0.02}

    # Calculate conversion probability
    if variant == 'A':
        base_rate = control_conversion_rate
    else:
        base_rate = variant_conversion_rate

    conversion_prob = base_rate + device_boost[device] + segment_boost[user_segment]
    conversion_prob = max(0, min(1, conversion_prob))  # Clamp to [0,1]

    # Determine conversion
    converted = 1 if random.random() < conversion_prob else 0

    # Engagement metrics
    if converted:
        time_on_page = max(30, np.random.normal(180, 60))  # Converters spend more time
        pages_viewed = random.randint(3, 10)
    else:
        time_on_page = max(5, np.random.normal(45, 30))
        pages_viewed = random.randint(1, 4)

    # Revenue (only if converted)
    if converted:
        # Variant B users spend slightly more
        if variant == 'B':
            revenue = max(10, np.random.normal(85, 25))
        else:
            revenue = max(10, np.random.normal(80, 25))
    else:
        revenue = 0

    users.append({
        'user_id': f'USER_{user_id:05d}',
        'assignment_date': assignment_date,
        'variant': variant,
        'device': device,
        'country': country,
        'user_segment': user_segment,
        'converted': converted,
        'revenue': round(revenue, 2),
        'time_on_page_seconds': round(time_on_page, 1),
        'pages_viewed': pages_viewed
    })

df = pd.DataFrame(users)
df = df.sort_values('assignment_date').reset_index(drop=True)

# Save to CSV
df.to_csv('data/ab_test_results.csv', index=False)

print("=" * 70)
print("A/B TEST DATA GENERATED")
print("=" * 70)
print(f"\nTotal Users: {len(df):,}")
print(f"Experiment Duration: {experiment_duration_days} days")
print(f"Date Range: {df['assignment_date'].min().date()} to {df['assignment_date'].max().date()}")

print("\n" + "-" * 70)
print("VARIANT DISTRIBUTION")
print("-" * 70)
print(df['variant'].value_counts())

print("\n" + "-" * 70)
print("CONVERSION RATES")
print("-" * 70)
conversion_by_variant = df.groupby('variant')['converted'].agg(['sum', 'mean', 'count'])
conversion_by_variant.columns = ['conversions', 'conversion_rate', 'total_users']
conversion_by_variant['conversion_rate_pct'] = conversion_by_variant['conversion_rate'] * 100
print(conversion_by_variant)

print("\n" + "-" * 70)
print("REVENUE METRICS")
print("-" * 70)
revenue_by_variant = df.groupby('variant')['revenue'].agg(['sum', 'mean'])
revenue_by_variant.columns = ['total_revenue', 'avg_revenue_per_user']
print(revenue_by_variant)

print(f"\nExpected lift: {treatment_lift*100:.1f}%")
actual_lift = (conversion_by_variant.loc['B', 'conversion_rate'] / conversion_by_variant.loc['A', 'conversion_rate'] - 1) * 100
print(f"Actual lift: {actual_lift:.1f}%")

print("\n" + "=" * 70)
print("Dataset saved to 'data/ab_test_results.csv'")
print("=" * 70)
