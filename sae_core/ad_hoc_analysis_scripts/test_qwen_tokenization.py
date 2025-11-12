"""
Test to understand what's happening with Qwen tokenization
"""
from transformer_lens import HookedTransformer

print("Loading Qwen model...")
model = HookedTransformer.from_pretrained("Qwen/Qwen2.5-0.5B")

# Test 1: Single short text
print("\n" + "="*80)
print("TEST 1: Single short paragraph")
print("="*80 + "\n")

text = "This is a test paragraph about physics."
print(f"Input text: {repr(text)}")

tokens_with_bos = model.to_tokens([text], prepend_bos=True)
tokens_no_bos = model.to_tokens([text], prepend_bos=False)

print(f"\nWith prepend_bos=True:")
token_strs_with = [model.to_string(t) for t in tokens_with_bos[0]]
print(f"  Tokens: {token_strs_with}")
print(f"  Count: {len(token_strs_with)}")
print(f"  <|endoftext|> count: {sum(1 for t in token_strs_with if '<|endoftext|>' in t)}")

print(f"\nWith prepend_bos=False:")
token_strs_no = [model.to_string(t) for t in tokens_no_bos[0]]
print(f"  Tokens: {token_strs_no}")
print(f"  Count: {len(token_strs_no)}")
print(f"  <|endoftext|> count: {sum(1 for t in token_strs_no if '<|endoftext|>' in t)}")

# Test 2: Batch of texts
print("\n" + "="*80)
print("TEST 2: Batch of 3 paragraphs")
print("="*80 + "\n")

batch_texts = [
    "First paragraph.",
    "Second paragraph is longer with more words.",
    "Third paragraph.",
]

batch_tokens = model.to_tokens(batch_texts, prepend_bos=True)
print(f"Batch shape: {batch_tokens.shape}")

for i, text in enumerate(batch_texts):
    token_strs = [model.to_string(t) for t in batch_tokens[i]]
    endoftext_count = sum(1 for t in token_strs if '<|endoftext|>' in t)
    print(f"\nText {i}: {repr(text)}")
    print(f"  Tokens: {token_strs}")
    print(f"  <|endoftext|> count: {endoftext_count}")

# Test 3: Check if padding causes it
print("\n" + "="*80)
print("TEST 3: Checking padding behavior")
print("="*80 + "\n")

# Different length texts will get padded
short = "Short."
long = "This is a much longer text with many more words in it."

batch = [short, long]
tokens = model.to_tokens(batch, prepend_bos=True)

print(f"Batch shape: {tokens.shape}")
print(f"\nShort text tokens:")
short_strs = [model.to_string(t) for t in tokens[0]]
print(f"  {short_strs}")
print(f"  <|endoftext|> count: {sum(1 for t in short_strs if '<|endoftext|>' in t)}")

print(f"\nLong text tokens:")
long_strs = [model.to_string(t) for t in tokens[1]]
print(f"  {long_strs}")
print(f"  <|endoftext|> count: {sum(1 for t in long_strs if '<|endoftext|>' in t)}")

# Check what the padding token is
print(f"\n" + "="*80)
print("PADDING TOKEN IDENTITY")
print("="*80 + "\n")

pad_token = model.tokenizer.pad_token
pad_token_id = model.tokenizer.pad_token_id
eos_token_id = model.tokenizer.eos_token_id
bos_token_id = model.tokenizer.bos_token_id

print(f"Pad token: {repr(pad_token)} (ID: {pad_token_id})")
print(f"EOS token ID: {eos_token_id}")
print(f"BOS token ID: {bos_token_id}")

if pad_token_id == eos_token_id:
    print("\n🚨 CRITICAL: PAD TOKEN == EOS TOKEN")
    print("   → When padding short sequences, they get filled with <|endoftext|>!")
    print("   → This explains the massive number of <|endoftext|> tokens!")

# Test 4: Simulate what happens with different length texts in a batch
print("\n" + "="*80)
print("TEST 4: Simulating batch with varying lengths")
print("="*80 + "\n")

texts = [
    "A" * 10,   # 10 chars
    "B" * 50,   # 50 chars
    "C" * 100,  # 100 chars
]

tokens = model.to_tokens(texts, prepend_bos=True)
print(f"Batch shape: {tokens.shape}")

for i, text in enumerate(texts):
    token_strs = [model.to_string(t) for t in tokens[i]]
    endoftext_count = sum(1 for t in token_strs if '<|endoftext|>' in t)
    total_tokens = len(token_strs)
    print(f"\nText {i} ({len(text)} chars):")
    print(f"  Total tokens: {total_tokens}")
    print(f"  <|endoftext|> tokens: {endoftext_count}")
    print(f"  Ratio: {endoftext_count/total_tokens*100:.1f}%")
    print(f"  Last 5 tokens: {token_strs[-5:]}")