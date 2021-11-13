from aitextgen import aitextgen

ai = aitextgen(model_folder="trained_model", tokenizer_file="aitextgen.tokenizer.json")
ai.generate(10, prompt="")