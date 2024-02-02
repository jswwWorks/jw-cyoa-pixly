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


some changes to make soon:
- add a button on homepage that links to upload section
- make sure to update db to accomodate larger varchar for model col



Thursday, Feb 1, 2024
- try to coerce num vals to strings then back to numbers and alter database schema (so user can search by # val)
- add button linking to upload section
- searching for exif data
- picking lightning talk topic

TODO: reconfigure HTML as needed
TODO: add alt image tags to site for accessibility



TODO: 1. make buttons that direct to upload page and button to redirect to homepage
TODO: 2. make links to photos to bring them to their own page to see their metadata and potential edits
TODO: 3. make button to return to homepage on single photo page
TODO: 3.5 recongifure base.html and put appropriate non-base.html templates elsewhere
TODO: 4. on editing photo, redirect to homepage?




Friday | Feb 2, 2024
1. TODO: handle merge conflicts in main repo
2. TODO: *after submitting a search term in form, the search category should still be the same from the previous search
3. TODO: *CSS nice-to-haves
4. TODO: deploy to render
5. TODO: work on lightning talk/presentation
6. TODO: ******** add a second photo filter
7. TODO: Keep Pixly app description only on base.html