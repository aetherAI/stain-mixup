# Stain Mix-up

This repository provide the core idea of [Stain Mix-Up: Domanin Generalization for Histopathology Images](https://link.springer.com/chapter/10.1007/978-3-030-87199-4_11).

## Publication
Chang, J.-R., Wu, M.-S., Yu, W.-H., Chen, C.-C., Yang, C.-K., Lin, Y.-Y., & Yeh, C.-Y. (2021). Stain mix-up: Unsupervised domain generalization for histopathology images. Medical Image Computing and Computer Assisted Intervention – MICCAI 2021, 117–126. https://doi.org/10.1007/978-3-030-87199-4_11

## License
Copyright (C) 2021 aetherAI Co., Ltd. All rights reserved. Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

## Examples
[Examples of the source domain and the target domain](./imgs/examples.png)
[Example of source image to convert](./imgs/image_to_convert.png)
[Augmented results](./imgs/augmented_example1.png)

## Installation

## Usage
1. Get stain matrix.
You can derive your stain matrix by different methods such as Vahadane or Macenko.
```python
from stain_mixup.utils import get_stain_matrix


stain_matrix = get_stain_matrix(image)
```
2. Convert image from the source domain to target domain.
```python
from stain_mixup.augment import stain_mixup

...

augmented_image = stain_mixup(
    image,
    source_stain_matrix,
    target_stain_matrix,
)
```

## Contributors
Jia-Ren Chang, Min-Shen Wu, Wei-Hsiang Yu, Chi-Chung Chen, Che-Ming Wu

