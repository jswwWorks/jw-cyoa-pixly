"use strict";

const $resizeBtn = $("#resize-img");
const filename = $resizeBtn.data("filename");

console.log('This is filename from JS: ', filename);

async function resizeImage() {

  console.log('We got into resizeImage fn!');

  const resp = await fetch('/resize_image', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      filename: filename
    })
  });

  if (!resp.ok) throw new Error('Failed to resize image');

  location.reload();

  const results = await resp.json();
  console.log('Results from click: ', results);

  return results;
}



$resizeBtn.on("click", resizeImage);