## Phase 1: Document & Understand
*Code Reading Session*
    * Read `sae_config.py` top to bottom
        * List every field and its purpose in a notebook
        * Note which fields are being used where
    * Read `train_config.py` top to bottom
        * List every field and its purpose
        * Note default values and why they might be chosen

*SAE Architecture Deep Dive*
    * Read `sae_base.py: SAE` class method by method
        * `__init__`: What gets initialized and why?
        * `initialize_weights`: Why tied weights? Why kaiming init?
        * `encode`: Why subtract b_dec before encoding? - Idk Anthropic did it lol - there's some mathematical explanation I don't recall
        * `decode`: Simple linear transform
        * `forward`: Understand the flow
        * `normalize_decoder`: Why normalize? When is this called?
        * `training_forward`: What's returned and why?
        * `update_inactive_features`: How does dead feature tracking work?
        * `get_auxiliary_loss`: What's this hook for?
    * Read `sae_base.py: BatchTopKSAE` class method by method
        * `__init__`: What extra state is tracked?
        * `encode`: Why no encoder bias here?
        * `forward`: How does top-k selection work?
        * `update_inactive_features`: How is num_batches_not_active updated?
        * `get_auxiliary_loss`: Understand the dead feature revival mechanism
        * `project_decoder_gradients`: Why project gradients to tangent space?
*Deliverable:* Create `ARCHITECTURE_NOTES.md` with my understanding

*Training Loop Deep Dive*
    * Read `training.py: train_sae` line by line
        * Understand `forward_batch` helper function
        * Trace data flow: batch-> activations -> SAE -> losses
        * List every loss term and when it's computed
        * Understand the validation loop
        * Map out checkpoint saving logic
    * Read `training.py: compute_kl_divergence`
        * Understand the masking mechanism
        * Verify: Is the argument order correct?
        * Research KL(P||Q) vs. KL(Q||P)
*Deliverable:* Create `TRAINING_LOOP_NOTES.md` with flow diagram

*Data Pipeline Deep Dive*
    * Read `sae_train.py: WindowedTextDataset`
        * How does pre-tokenization work?
        * How are windows created?
        * What happens with texts shorter than max_length?
        * What happens with texts longer than max_length?
    * Read `sae_train.py: SAETrainer`
        * What does the trainer orchestrate?
        * How are dataloaders configured?
        * Trace the full `train()` method
*Deliverable:* Create `DATA_PIPELINE_NOTES.md`

## Phase 2: Validate Understanding
*Write Explanation Documents*
    * Create `HOW_IT_WORKS.md` explaining the pipeline to a colleague
        * Section 1: What is an SAE?
        * Section 2: Why train SAEs on LLM activations?
        * Section 3: How does this pipeline work?
        * Section 4: What are the key hyperparameters?
        * Section 5: What are the common failure modes?
*Create Architecture Diagrams*
    * Draw data flow diagram
    * Draw SAE architecture diagram
    * Draw training loop flow diagram

*Answer My Own Questions*
    * Go back to `PROJECT_MAP.md` and answer every question listed
        * Architecture, training, data

## Phase 3: Document Decisions
*Create Troubleshooting Guide*
    * Create `TROUBLESHOOTING.md`
        * High dead feature percentage -> Try lower sparsity penalty, topK
        * Poor reconstruction -> Try higher reconstruction weight
        * OOM errors -> Reduce batch_size or activation_batch_size (if the latter even does anything)
        * NaN losses -> Check learning rate, check for numerical instability
        * Model not learning -> Check hook spec is correct
        * KL divergence exploding -> Check temperature, check masking


## Phase 4: Validation Experiments
*Baseline Experiment*
    * Train vanilla SAE on dataset
    * Document training curves
    * Measure dead features over time
    * Save experiment as a baseline
*BatchTopKSAE Experiment*
    * Train BatchTopKSAE on same dataset
    * Compare results to baseline
    * Does auxiliary loss help dead features?
    * Analyze sparsity-reconstruction tradeoff
*Hyperparameter Tuning*
    * l1_coefficient
    * Top K
*Plotting*
    * Standardize how experiments are run
    * Standardize how results are saved
    * Create plotting utility functions