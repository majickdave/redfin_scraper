import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('newest_listings.xml')
root = tree.getroot()

data = []

for child in root:
    data.append({
        'loc': child[0].text,
        'lastmod': child[1].text,
        'changefreq': child[2].text,
        'priority': child[3].text
               })
df = pd.DataFrame(data)

print(df.shape[0])

df['loc'].to_csv('urls.txt', index=False, sep='\t')