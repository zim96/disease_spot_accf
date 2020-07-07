# A segmentation method for disease spot images incorporating chrominance in Comprehensive Color Feature and Region Growing
by N. Jothiaruna, K. Joseph Abraham Sundar, B. Karthikeyan

Paper can be found at https://doi.org/10.1016/j.compag.2019.104934.

## Disclaimer
An implementation by zim96. I am implementing it in stages because I have yet to be comfortable with mathematics behind it. So, I shall list each stage with a new heading an paragraph here in the README.

## Understanding Singular Value Decomposition (SVD) and Image Compression

I implemented an image compression method using SVD in a Jupyter Notebook named `svd_image_compression`. This allowed me understand the use of SVD for images and how an SVD is calculated via Correlation Matrices. I included a block of code that produces an animation of the compressed image to visualise the change of energy state of the image.

## Decolorisation

Paper borrows decolorisation method which can be found at https://dx.doi.org/10.1007/s11760-016-0911-8. Citation below:

V. Sowmya, D. Govind, K. P. Soman, Significance of incorporating chrominance information for effective color-to-grayscale image conversion. Signal, Image and Video Processing. 11, 129–136 (2017).

It is implemented in `svd_decolorisation_jothiaruna`. Changing the value of `r` would change the truncation point of the SVD.
