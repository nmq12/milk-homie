from pathlib import Path

from spacy.cli import evaluate
from tokenizers.processors import BertProcessing
from tokenizers.implementations import ByteLevelBPETokenizer
from torch.utils.data import Dataset

# paths = [str(x) for x in Path("./data/").glob("**/*.txt")]
#
# # Initialize a tokenizer
# tokenizer = ByteLevelBPETokenizer()
#
# # Customize training
# tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
#     "<s>",
#     "<pad>",
#     "</s>",
#     "<unk>",
#     "<mask>",
# ])
#
# # Save files to disk
# tokenizer.save_model(".", "milk")

tokenizer = ByteLevelBPETokenizer(
    vocab="milk-vocab.json",
    merges="./milk-merges.txt"
)

tokenizer.post_processor = BertProcessing(
    ("</s>", tokenizer.token_to_id("</s>")),
    ("<s>", tokenizer.token_to_id("<s>")),
)

tokenizer.enable_truncation(max_length=512)

examples = []
src_files = Path("./data/").glob("*-eval.txt") if evaluate else Path("./data/").glob("*-train.txt")
for src_file in src_files:
    print("🔥", src_file)
    lines = src_file.read_text(encoding="utf-8").splitlines()
    examples += [x.ids for x in tokenizer.encode_batch(lines)]

