@echo off
cd /d %~dp0
.\llama.cpp\llama-server.exe -m llama.cpp\models\Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf --n-gpu-layers 20 --ctx-size 4096 --port 8001 --host 0.0.0.0 --top_k 40 --top_p 0.9
pause