"""
Inspect original physics textbook data to find source of <|endoftext|> tokens
"""
import re

def check_source_data():
    """Check if <|endoftext|> appears in source texts"""
    
    # You'll need to point this to wherever your physics texts are loaded from
    # This is a template - adjust paths as needed
    
    print("="*80)
    print("SOURCE DATA INSPECTION")
    print("="*80 + "\n")
    
    print("Checking for <|endoftext|> in source data...\n")
    
    # Example: if you're loading from files
    # from datasets import load_dataset
    # dataset = load_dataset(...)
    
    # Or if loading from a Python list/file
    # For now, let's check what the SAE analyzer dataset looks like
    
    print("TO DEBUG THIS, PLEASE PROVIDE:")
    print("1. How do you load the physics textbooks?")
    print("2. What does texts[0] look like (first 500 chars)?")
    print("3. Are you using load_dataset, load_from_disk, or custom loader?")
    print("\nPlease run this:")
    print("-" * 80)
    print("""
# Add this to your script where you create the SAE analyzer:
dataset = [...]  # however you load it
print(f"First text length: {len(dataset[0])}")
print(f"First text preview:")
print(dataset[0][:500])
print()
print(f"Count of '<|endoftext|>' in first text: {dataset[0].count('<|endoftext|>')}")
print(f"Count of '<|im_end|>' in first text: {dataset[0].count('<|im_end|>')}")
    """)
    print("-" * 80)

def check_model_tokenizer():
    """Check if the model tokenizer is the culprit"""
    from transformer_lens import HookedTransformer
    
    print("\n" + "="*80)
    print("TOKENIZER INSPECTION")
    print("="*80 + "\n")
    
    model_name = "Qwen/Qwen2.5-0.5B"  # or whatever you're using
    print(f"Loading model: {model_name}")
    model = HookedTransformer.from_pretrained(model_name)
    
    # Test tokenization
    test_texts = [
        "This is a normal physics sentence about momentum.",
        "# Strategy\nWe can solve this problem.",
        "The force equals mass times acceleration.",
    ]
    
    print("\nTesting tokenization of normal text:")
    print("-" * 80)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text[:60]}...")
        
        # Tokenize
        tokens = model.to_tokens([text], prepend_bos=True)
        token_strs = [model.to_string(t) for t in tokens[0]]
        
        print(f"  Length: {len(token_strs)} tokens")
        print(f"  Tokens: {token_strs[:10]}")
        
        # Count special tokens
        endoftext_count = sum(1 for t in token_strs if '<|endoftext|>' in t)
        if endoftext_count > 0:
            print(f"  ⚠️  WARNING: {endoftext_count} <|endoftext|> tokens found!")
        else:
            print(f"  ✓ No <|endoftext|> tokens")
    
    # Check tokenizer vocabulary
    print("\n" + "="*80)
    print("CHECKING TOKENIZER VOCABULARY")
    print("="*80)
    
    special_tokens = model.tokenizer.all_special_tokens
    print(f"\nSpecial tokens: {special_tokens}")
    
    if '<|endoftext|>' in model.tokenizer.get_vocab():
        token_id = model.tokenizer.convert_tokens_to_ids('<|endoftext|>')
        print(f"\n<|endoftext|> is token ID: {token_id}")
        
        # Test if it appears in normal tokenization
        test = "Hello world"
        tokens = model.to_tokens([test], prepend_bos=True)
        token_ids = tokens[0].tolist()
        
        if token_id in token_ids:
            print(f"⚠️  WARNING: <|endoftext|> (ID {token_id}) appears when tokenizing normal text!")
        else:
            print(f"✓ <|endoftext|> does not appear in normal tokenization")

def check_dataset_format():
    """Check how the dataset was prepared"""
    
    print("\n" + "="*80)
    print("LIKELY CAUSE: DATASET PREPARATION")
    print("="*80 + "\n")
    
    print("Based on the pattern, your dataset likely has one of these issues:")
    print()
    print("❌ ISSUE 1: Raw text contains literal '<|endoftext|>' strings")
    print("   Example: 'Chapter 1<|endoftext|>Chapter 2<|endoftext|>Chapter 3'")
    print("   → The tokenizer treats these as special tokens")
    print()
    print("❌ ISSUE 2: Dataset was pre-tokenized incorrectly")
    print("   Example: Texts were joined with special tokens during data prep")
    print("   → When tokenized again, special tokens get preserved")
    print()
    print("❌ ISSUE 3: Using a dataset format meant for training, not inference")
    print("   Example: Some HuggingFace datasets include special tokens in the text field")
    print("   → These should be removed before SAE analysis")
    print()
    
    print("TO FIX THIS:")
    print("-" * 80)
    print("1. Check your dataset loading code")
    print("2. Print the first few texts to see if they contain '<|endoftext|>'")
    print("3. If yes, clean them with: text.replace('<|endoftext|>', '')")
    print("4. Rebuild the activation database with clean data")

if __name__ == "__main__":
    check_source_data()
    
    try:
        check_model_tokenizer()
    except Exception as e:
        print(f"\nCouldn't load model for tokenizer check: {e}")
    
    check_dataset_format()