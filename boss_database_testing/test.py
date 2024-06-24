import numpy as np
import intern

array = intern.array

# em_channel = array("bossdb://nguyen_thomas2022/cb2/em")
segmentation_channel = array("bossdb://nguyen_thomas2022/cb2_seg/seg")

# volume = em_channel[600:606, 111362:112386, 123826:124850]

seg_volume = segmentation_channel[-1280:-1200, 0, 0]
pass
