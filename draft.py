import pandas as pd

# Sample DataFrame with your HTML column
df = pd.DataFrame({
    'location_html': [
        '<span class="sub-nav-cta__meta-text">Arlington, VA</span>',
        '<span class="sub-nav-cta__meta-text">United States</span>',
        '<span class="sub-nav-cta__meta-text">New York, NY</span>'
    ]
})

# Extract location in one line
df['clean_location'] = df['location_html'].str.extract(r'>([^<]+)<')

print(df[['location_html', 'clean_location']])