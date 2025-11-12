"""
Analyze how texts were split during activation collection
This will reveal why we have 155x more <|endoftext|> tokens than expected
"""
import pickle
from collections import Counter, defaultdict

DB_PATH = 'original_analysis/analysis/activation_database/activation_db_20251104_210231.pkl'

print("Loading database...")
with open(DB_PATH, 'rb') as f:
    data = pickle.load(f)

token_metadata = data['token_metadata']

print(f"Total tokens: {len(token_metadata):,}")
print(f"Total texts: 4,249 (expected)")

# Analyze by text_idx
print("\nAnalyzing token distribution per text...")

text_token_counts = defaultdict(lambda: {'total': 0, 'endoftext': 0, 'normal': 0})

for metadata in token_metadata:
    text_idx = metadata.text_idx
    token_str = metadata.token_str
    
    text_token_counts[text_idx]['total'] += 1
    
    if '<|endoftext|>' in token_str:
        text_token_counts[text_idx]['endoftext'] += 1
    else:
        text_token_counts[text_idx]['normal'] += 1

# Statistics
endoftext_per_text = [info['endoftext'] for info in text_token_counts.values()]
tokens_per_text = [info['total'] for info in text_token_counts.values()]

import numpy as np

print("\n" + "="*80)
print("PER-TEXT STATISTICS")
print("="*80)
print(f"Number of unique text_idx values: {len(text_token_counts)}")
print(f"\nTokens per text:")
print(f"  Mean:   {np.mean(tokens_per_text):.1f}")
print(f"  Median: {np.median(tokens_per_text):.1f}")
print(f"  Min:    {np.min(tokens_per_text)}")
print(f"  Max:    {np.max(tokens_per_text)}")

print(f"\n<|endoftext|> per text:")
print(f"  Mean:   {np.mean(endoftext_per_text):.1f}")
print(f"  Median: {np.median(endoftext_per_text):.1f}")
print(f"  Min:    {np.min(endoftext_per_text)}")
print(f"  Max:    {np.max(endoftext_per_text)}")

# Show examples
print("\n" + "="*80)
print("EXAMPLE TEXTS (first 10):")
print("="*80)
for text_idx in sorted(text_token_counts.keys())[:10]:
    info = text_token_counts[text_idx]
    print(f"Text {text_idx:4d}: {info['total']:4d} tokens, {info['endoftext']:4d} <|endoftext|>, {info['normal']:4d} normal")

# Check if texts were over-split
unique_texts = len(text_token_counts)
expected_texts = 4249

print("\n" + "="*80)
print("DIAGNOSIS")
print("="*80)
print(f"Expected texts: {expected_texts:,}")
print(f"Actual text_idx values: {unique_texts:,}")

if unique_texts > expected_texts:
    print(f"\n🚨 CRITICAL: Text indices exceed expected count by {unique_texts - expected_texts:,}")
    print("   → Texts were split into multiple chunks during processing")
    print(f"   → Average splits per text: {unique_texts / expected_texts:.1f}x")
elif unique_texts < expected_texts:
    print(f"\n⚠️  WARNING: Fewer text_idx values than expected")
    print("   → Some texts may not have been processed")
else:
    print(f"\n✓ Text count matches, but <|endoftext|> ratio is {np.mean(endoftext_per_text):.1f}x too high")
    print("   → Problem is in tokenization, not chunking")

# Check position distribution
print("\n" + "="*80)
print("CHECKING POSITION PATTERNS")
print("="*80)

# Sample one text with many endoftext tokens
high_endoftext_text = max(text_token_counts.keys(), 
                          key=lambda k: text_token_counts[k]['endoftext'])

print(f"\nSampling text {high_endoftext_text} (has {text_token_counts[high_endoftext_text]['endoftext']} <|endoftext|>)")

# Get all tokens from this text
text_tokens = [(m.position, m.token_str) for m in token_metadata 
               if m.text_idx == high_endoftext_text]
text_tokens.sort()

print(f"Total tokens: {len(text_tokens)}")
print("\nFirst 20 tokens:")
for pos, token in text_tokens[:20]:
    marker = " ← SPECIAL" if '<|' in token else ""
    print(f"  [{pos:3d}] {token:30s}{marker}")

print("\nLast 20 tokens:")
for pos, token in text_tokens[-20:]:
    marker = " ← SPECIAL" if '<|' in token else ""
    print(f"  [{pos:3d}] {token:30s}{marker}")