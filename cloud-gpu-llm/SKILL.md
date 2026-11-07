---
name: cloud-gpu-llm
description: Run local LLMs (llama.cpp, GGUF) on a rented spot GPU VM on Google Cloud when a laptop is too slow or when you need a benchmark. Covers the gpu-vm script, the IAP SSH setup, the traps that cost time in a real run, cost, and safe access through a tunnel. Use when a local model reads prompts too slowly, when asked to benchmark a model on an A100, L4 or H100, or when asked to run llama-server in the cloud.
---

# Cloud GPU for local LLMs

Rent a spot GPU VM, serve your GGUF models on it, and reach them from your laptop through a tunnel. Stop the VM when you finish.

## When to use it

Use a cloud GPU when:

- A local model reads long prompts too slowly to work with.
- You need to benchmark a model on known hardware.
- A model does not fit in your laptop memory.

Do not use it for a one-off short prompt. Setup takes about 30 minutes, most of it the CUDA build and the model copy.

Example result, from one run of an A100 40 GB spot VM against a laptop with an M3 Pro chip:

| Model | Metric | A100 40 GB | M3 Pro |
|---|---|---|---|
| 27B, IQ2 quant, 3,000-token prompt | Prompt reading (tok/s) | 1,054 | 79 |
| 27B, IQ2 quant | Output (tok/s) | 46 | 10.3 |
| 4B, Q4 quant | Prompt reading / output (tok/s) | 5,670 / 148 | not measured |

## Before you start

You need:

- The `gcloud` CLI, signed in to an account that can create Compute Engine instances.
- Spot GPU quota in at least one region. The script checks this and skips regions without it.
- `jq` (for the quota check) and `ssh`.
- One or more `.gguf` files, or public Hugging Face model files.

Set the project and account through the environment. Never write them into a file in a public repository.

```sh
export GPU_VM_PROJECT=<your-project-id>
export GPU_VM_ACCOUNT=<your-account-email>   # optional
```

## Run it

The script is `gpu-vm` in [itsryanarmani/scripts](https://github.com/itsryanarmani/scripts). Preview first. A dry run prints every `gcloud` command and runs none.

```sh
gpu-vm up --dry-run --gpu a100 \
  --model './model-q4.gguf=8081' \
  --model './big-iq2.gguf=8082:-c 8192'
```

Then run it for real, and open the tunnel in a second terminal:

```sh
gpu-vm up     --gpu a100 --llama-commit <rev> --model './model-q4.gguf=8081'
gpu-vm tunnel --model './model-q4.gguf=8081' --local-port-offset 10000
curl http://127.0.0.1:18081/health
```

The model spec is `SOURCE=REMOTE_PORT[:EXTRA ARGS]`. `SOURCE` is a local path or `hf:OWNER/REPO/FILE.gguf`. Pass `--llama-commit` with the revision of your local build, so results match.

| Preset | Machine type | CUDA arch | Typical spot price |
|---|---|---|---|
| `l4` | `g2-standard-4` | 89 | about $0.25 per hour |
| `a100` | `a2-highgpu-1g` | 80 | about $1.10 per hour |
| `h100` | `a3-highgpu-1g` | 90 | about $2 to $3 per hour |

Other commands:

- `gpu-vm status` shows VM state, the firewall rule, and the health of each port.
- `gpu-vm stop` stops the VM. The disk stays and costs a little.
- `gpu-vm down` deletes the VM and the firewall rule. Nothing bills after this.

## Cost

Prices are approximate and change. A spot VM bills every second it runs, whether or not it serves a request. Always run `stop` or `down` when you finish. A stopped VM bills only for its 100 GB SSD disk.

A provider can stop a spot VM at any time. Run `gpu-vm up` again with the same flags. It starts the stopped VM and restarts the servers.

## Safety

- `llama-server` binds to `127.0.0.1` on the VM, never `0.0.0.0`. It has no authentication.
- Reach it only through the tunnel (`gpu-vm tunnel`).
- The firewall rule allows `tcp:22` only from Google's IAP range, and only to VMs with the rule's tag. `down` deletes it.
- Do not send source code or data you may not share to a third-party cloud. Use a project your organization approves.

## Traps

Each of these cost time in a real run. The script handles them. Know them if you work by hand.

| Trap | What happens | Fix |
|---|---|---|
| No SSH firewall rule in an organization project | Direct SSH times out | Add a rule for `tcp:22` from the IAP range to a target tag. Add the tag to the VM. Use `--tunnel-through-iap` on every `gcloud compute ssh` and `scp`. |
| `gcloud compute ssh --command 'cat > f' < file` | The remote file is empty | Use `gcloud compute scp`. |
| `nohup CMD &` inside `--command` | The job dies when SSH closes | Use `setsid nohup CMD > log 2>&1 < /dev/null & disown`. |
| A command held in a shell variable | zsh does not split it into words | Write a small wrapper script, or use an array. |
| CUDA not found during the build | The image keeps CUDA in `/usr/local/cuda/bin`, not on `PATH` | Run `export PATH=/usr/local/cuda/bin:$PATH` first. |
| No `cmake` or Docker on the image | The build fails at the first step | Install `cmake`, `build-essential` and `libcurl4-openssl-dev` with `apt-get`. |
| A zone has no spot capacity | `create` fails with a resource-pool error | Try the next zone. The script does this for capacity errors only. |
| Wrong CUDA architecture | Slow or failed kernels | Use 80 for A100, 89 for L4, 90 for H100. |

The model copy runs at about 12 MB/s over IAP. A 10.6 GB file took about 14 minutes. For a public model, use the `hf:` source to download on the VM instead.

## Verify

1. `gpu-vm status` shows the VM as `RUNNING` and each port as healthy.
2. `curl http://127.0.0.1:<local port>/health` returns `{"status":"ok"}` through the tunnel.
3. Run your benchmark prompt, and record prompt-reading and output tokens per second.
4. Run `gpu-vm stop` or `gpu-vm down`, then `gpu-vm status` again to confirm the state.
