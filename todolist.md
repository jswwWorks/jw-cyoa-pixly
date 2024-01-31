OBJECTIVE TRACKER FOR PIX.LY

Updated mental model:
- we're not retrieving files from the bucket, we're just trying to view files from the bucket in the browser
- to do so, we're giving anon users READ access in our bucket's permissions

- learn how to use s3 object


Tues, Jan 30, 2024
1. get a basic html going - done!
2. TODO: research how to submit a file in a form
    - double check how to submit a valid *photo* file in form
3. TODO: research how to upload file to S3
    - double check how to upload a *photo* file to S3


4. TODO: research how to pull photo file from S3 (AJAX request to AWS S3 bucket)
5. TODO: research how to show photo file from S3 on to HTML page
    - will require getting exif data from image to get it's source text

photos {
    s3_url text                     <img src={{ s3_url }}>          <-- http://matts-pixly.s3.amazon.com
}