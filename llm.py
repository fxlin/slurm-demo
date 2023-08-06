from llama_cpp import Llama

LLAMA_30B = "/bigtemp/slurm-demo/llama-30b.ggmlv3.q8_0.bin"
LLAMA2_7B = "/bigtemp/slurm-demo/llama-2-7b.ggmlv3.q2_K.bin"

llm = Llama(model_path=LLAMA_30B, n_ctx=2048, n_gpu_layers=63, verbose=True)
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
