import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import nibabel as nib


pfi_image_to_use_to_create_gif = ''  # input contour example

pfo_output_examples_folder = ''

im = nib.load(pfi_image_to_use_to_create_gif)
axis = 'y'
sampling_step = 2

assert im.get_data().ndim == 3
xx, yy, zz = im.shape

if axis == 'x':
    arr = [im.get_data()[x, ...] for x in range(0, xx, sampling_step)]
elif axis == 'y':
    arr = [im.get_data()[:, y, :] for y in range(0, yy, sampling_step)]
elif axis == 'z':
    arr = [im.get_data()[..., z] for z in range(0, zz, sampling_step)]
else:
    raise IOError

for a in arr:
    print a.ndim
print len(arr)


def save_list_of_arrays_to_png(list_arr, pfo_output, filename):

    for a_id, a in enumerate(list_arr):
        fname = os.path.join(pfo_output, '{0}_{1:03d}.png'.format(filename, a_id))

        fig = plt.figure(a_id)
        fig.set_tight_layout(True)
        print('fig size: {0} DPI, size in inches {1}'.format(fig.get_dpi(), fig.get_size_inches()))
        plt.axis('off')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off',
                        labelright='off', labelbottom='off')

        ax = fig.add_subplot(111)
        ax.imshow(a_id*a.T, origin='lower', cmap=plt.cm.autumn)  # cms.autumn

        # ax.imshow(a)
        # fig.canvas.draw()
        # plt.show()
        plt.savefig(fname, dpi=None)

save_list_of_arrays_to_png(arr[6:], "/Users/sebastiano/Desktop/z_test_gif", 'example')

os.system('convert -delay 10 -loop 0 {}/*.png {}/output.gif'.format(pfo_output_examples_folder))
