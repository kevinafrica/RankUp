'use strict'

// var fileSelect = document.getElementById("fileSelect"),
//   fileElem = document.getElementById("fileElem");
// //   let fileName = 'choose file to upload';

// fileSelect.addEventListener("click", function (e) {
//     console.log(fileElem);
//   if (fileElem) {
//     fileElem.click();
//   }
// }, false);

var typed1 = new Typed('#sl-typed', {
    strings: ["a squad leader.^3000", "a platoon sergeant.^3000", "a military spouse.^3000"],
    typeSpeed: 100,
    loop: true
  });
  var typed2 = new Typed('#shift-typed', {
    strings: ["a nuclear engineer.^3000", "a software engineer.^2750", "an Uber driver.^2750"],
    typeSpeed: 100,
    loop: true
  });

//   fileName.toHtml = function() {
//     let template = Handlebars.compile($('#fileName-template').text());

//     return template(this);
//   };
window.URL = window.URL || window.webkitURL;

var fileSelect = document.getElementById("fileSelect"),
    fileElem = document.getElementById("fileElem"),
    fileList = document.getElementById("fileList");

fileSelect.addEventListener("click", function (e) {
  if (fileElem) {
    fileElem.click();
  }
  e.preventDefault(); // prevent navigation to "#"
}, false);

function handleFiles(files) {
  if (!files.length) {
    fileList.innerHTML = "<p>No files selected!</p>";
  } else {
    fileList.innerHTML = "";
    var list = document.createElement("ul");
    fileList.appendChild(list);
    for (var i = 0; i < files.length; i++) {
      var li = document.createElement("li");
      list.appendChild(li);
      
      var img = document.createElement("file-name");
      img.src = window.URL.createObjectURL(files[i]);
      img.height = 60;
      img.onload = function() {
        window.URL.revokeObjectURL(this.src);
      }
      li.appendChild(img);
      var info = document.createElement("span");
      info.innerHTML = files[i].name;
      li.appendChild(info);
    }
  }
}
