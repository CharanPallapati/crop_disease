
"""
Model-agnostic Grad-CAM helper template.

After training, identify the final convolutional layer with:
  for layer in model.layers:
      print(layer.name, layer.__class__.__name__)

Set that layer name in your deployment config, then implement:
  - feature maps from the target layer
  - gradient of selected class score
  - channel-weighted activation
  - resize + overlay

We intentionally don't guess a layer name because model architectures can differ.
"""
TARGET_LAYER = os.getenv("GRADCAM_LAYER", "")
