"""Inference-time steering wrapper.

Add a control vector at selected layers during generation:
  hidden_states += coefficient * control_vector

Supports:
  - selected layer list (default = middle/late layers per repe.yaml)
  - signed coefficient (negative = suppress, zero = baseline, positive = amplify)
  - hook install / uninstall

Default layer strategy:
  default_control_layers(num_layers) ->
      [int(0.45*L), int(0.55*L), int(0.65*L), int(0.75*L)]
"""
