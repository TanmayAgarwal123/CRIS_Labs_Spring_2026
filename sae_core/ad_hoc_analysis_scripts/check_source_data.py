"""
Quick check: Does your physics dataset contain literal '<|endoftext|>' strings?
"""
import json
from pathlib import Path

# Load your processed data
DATA_PATH = 'sae_core/data/processed_data/processed_physics_all.json'

print("="*80)
print("CHECKING SOURCE DATA FOR SPECIAL TOKENS")
print("="*80 + "\n")

# Load the dataset
print(f"Loading: {DATA_PATH}")
with open(DATA_PATH, 'r') as f:
    dataset = json.load(f)

print(f"✓ Loaded {len(dataset)} texts\n")

# Check first few texts
print("="*80)
print("FIRST TEXT INSPECTION")
print("="*80 + "\n")

first_text = dataset[0]
print(f"Length: {len(first_text)} characters")
print(f"\nFirst 500 characters:")
print("-"*80)
print(repr(first_text[:500]))
print("-"*80)

# Count special tokens in source
print(f"\n" + "="*80)
print("SPECIAL TOKEN COUNT IN SOURCE DATA")
print("="*80 + "\n")

special_tokens = {
    '<|endoftext|>': 0,
    '<|im_start|>': 0,
    '<|im_end|>': 0,
    '<s>': 0,
    '</s>': 0,
}

for text in dataset:
    for token in special_tokens:
        special_tokens[token] += text.count(token)

print("Occurrences in raw text data:")
for token, count in special_tokens.items():
    if count > 0:
        print(f"  {token:20s}: {count:,}")

total_special = sum(special_tokens.values())
if total_special > 0:
    print(f"\n🚨 FOUND {total_special:,} special token strings in source data!")
    print("   → These need to be removed before tokenization")
    
    # Find examples
    print("\n" + "="*80)
    print("EXAMPLES OF TEXTS CONTAINING SPECIAL TOKENS")
    print("="*80 + "\n")
    
    for i, text in enumerate(dataset[:20]):
        if '<|endoftext|>' in text or '<|im_end|>' in text:
            print(f"Text {i}:")
            print(f"  Length: {len(text)}")
            print(f"  <|endoftext|> count: {text.count('<|endoftext|>')}")
            print(f"  First 200 chars: {repr(text[:200])}")
            print()
            if i >= 5:  # Show first 5 examples
                break
else:
    print("✓ No special tokens found in source data")
    print("   → The issue is only from prepend_bos=True")

# Check for other patterns that might be problematic
print("\n" + "="*80)
print("CHECKING FOR OTHER PATTERNS")
print("="*80 + "\n")

# Check if texts are unusually short
short_texts = [t for t in dataset if len(t) < 50]
print(f"Texts shorter than 50 chars: {len(short_texts)} ({len(short_texts)/len(dataset)*100:.1f}%)")

if short_texts:
    print("\nFirst 5 short texts:")
    for i, text in enumerate(short_texts[:5]):
        print(f"  {i+1}. ({len(text)} chars): {repr(text)}")

# Check average length
avg_len = sum(len(t) for t in dataset) / len(dataset)
print(f"\nAverage text length: {avg_len:.1f} characters")

# Summary
print("\n" + "="*80)
print("DIAGNOSIS")
print("="*80 + "\n")

if total_special > 0:
    print("🚨 CRITICAL ISSUE: Source data contains special token strings")
    print("   → Your markdown files have literal '<|endoftext|>' in them")
    print("   → This is likely from incorrect preprocessing")
    print("\n   FIX: Clean the source data before processing")
elif avg_len < 100:
    print("⚠️  WARNING: Texts are very short (avg {avg_len:.0f} chars)")
    print("   → Each short text gets a BOS token")
    print("   → Consider merging paragraphs for longer sequences")
else:
    print("✓ Source data looks clean")
    print("   → The only issue is prepend_bos=True adding one <|endoftext|> per text")
    print("   → With 4,249 texts, this should only add 4,249 tokens (~0.5%)")
    print("   → But you have 659,169, so there must be another source")

print("\n" + "="*80)