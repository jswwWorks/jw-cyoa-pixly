OBJECTIVE TRACKER FOR PIX.LY

Updated mental model:
- we're not retrieving files from the bucket, we're just trying to view files from the bucket in the browser
- to do so, we're giving anon users READ access in our bucket's permissions -- **bucket policy**

then we should be able to click on the link and see the image (that'll demonstrate that we've enabled the proper permissions)


- learn how to use s3 object


main paths:
photo manipulation - ways to download the image, store it on server so that you can make changes to it (you can't manipulate it while in bucket)
data focus - EXIF data

go onto YouTube to look for general tutorials



Tues, Jan 30, 2024
1. get a basic html going - done! 01/30/24
2. research how to submit a file in a form - done! 01/31/24
    - double check how to submit a valid *photo* file in form (validation when there's time)
3. research how to upload file to S3 - done! 01/31/24
    - double check how to upload a *photo* file to S3 - done! 01/31/24


4. research how to pull photo file from S3 (AJAX request to AWS S3 bucket) - done! 01/31/24
5. research how to show photo file from S3 on to HTML page - done! 01/31/24
    - will require getting exif data from image to get it's source text (for db purposes)

photos {
    s3_url text                     <img src={{ s3_url }}>          <-- http://matts-pixly.s3.amazon.com
}



Wed, Jan 31, 2024

1. TODO: figure out on submission of form (before uploading to S3):
    2. TODO: extract the metadata/exif data from photo
    3. TODO: store metadata/exif data into OUR database
    4. TODO: ^BEFORE ALL THIS: decide how our database schema looks
    5. TODO: implement a working db that extracts and retains info about each uploaded photo
    6. TODO: think about how to search for photo based on a given query (when was the photo taken, author of photo, aperture of photo, just search queries based on metadata/exif data)


