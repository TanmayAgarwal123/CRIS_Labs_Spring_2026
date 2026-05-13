"""Forward-hook based residual-stream steering for Qwen-style decoder LMs.

Each hook adds `coefficient * vector` to the OUTPUT of one transformer
block (i.e. the residual stream immediately after that block). Vectors
were trained on the post-block hidden state in Phase 8 with the same
indexing, so vectors[block_idx] is exactly the right direction for the
hook on model.model.layers[block_idx].

  install_control_hooks(model, vectors, layer_indices, coefficient) -> handles
  remove_hooks(handles)
  default_control_layers(num_blocks) -> [int, int, int, int]   (45/55/65/75%)
"""

from typing import List

import torch


def default_control_layers(num_blocks: int) -> List[int]:
    return [int(num_blocks * f) for f in (0.45, 0.55, 0.65, 0.75)]


def _make_hook(direction: torch.Tensor, coefficient: float):
    direction = direction.detach()

    def hook(module, inputs, output):
        # Qwen-style decoder block returns (hidden_states, ...). Handle both
        # tuple and plain-tensor returns to stay generic.
        if isinstance(output, tuple):
            h = output[0]
            h = h + coefficient * direction.to(h.device).to(h.dtype)
            return (h,) + output[1:]
        return output + coefficient * direction.to(output.device).to(output.dtype)

    return hook


def install_control_hooks(model, vectors, layer_indices, coefficient):
    """Register forward hooks on model.model.layers[i] for each i in
    layer_indices, adding coefficient * vectors[i] to the residual stream.

    vectors:        Tensor[n_blocks, hidden]
    layer_indices:  list[int]
    coefficient:    float
    """
    handles = []
    blocks = model.model.layers
    for li in layer_indices:
        v = vectors[li]
        h = blocks[li].register_forward_hook(_make_hook(v, float(coefficient)))
        handles.append(h)
    return handles


def remove_hooks(handles):
    for h in handles:
        h.remove()
