import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate T20 player data
np.random.seed(42)
players = [f'Player_{i}' for i in range(1, 21)]
matches = [f'Match_{j}' for j in range(1, 11)]

data = []
for player in players:
    for match in matches:
        runs = np.random.poisson(lam=30)
        wickets = np.random.binomial(1, 0.3)
        catches = np.random.binomial(1, 0.2)
        data.append([player, match, runs, wickets, catches])

df = pd.DataFrame(data, columns=['Player', 'Match', 'Runs', 'Wickets', 'Catches'])
df['FantasyPoints'] = df['Runs'] + df['Wickets'] * 25 + df['Catches'] * 10
df.to_csv('fantasy_cricket_data.csv', index=False)

# Player summary
summary_df = df.groupby('Player').agg({
    'Runs': 'mean',
    'Wickets': 'sum',
    'Catches': 'sum',
    'FantasyPoints': ['mean', 'std']
}).reset_index()

summary_df.columns = ['Player', 'AvgRuns', 'TotalWickets', 'TotalCatches', 'AvgPoints', 'StdPoints']
summary_df['ConsistencyScore'] = (summary_df['AvgPoints'] / (summary_df['StdPoints'] + 1)).round(2)
summary_df.to_csv('player_summary.csv', index=False)

# Plot
plt.figure(figsize=(12, 6))
top_players = summary_df.sort_values(by='AvgPoints', ascending=False).head(10)
sns.barplot(x='Player', y='AvgPoints', data=top_players)
plt.title('Top 10 Players by Average Fantasy Points')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top10_fantasy_players.png')
