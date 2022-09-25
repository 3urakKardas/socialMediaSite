const startThreadForm = document.getElementById("startThreadForm");

const threadTitle = document.getElementById("threadTitle");

const threadFirstEntry = document.getElementById("threadFirstEntry");

const threadCategory = document.getElementById("threadCategory");

const startThreadSubmit = document.getElementById("startThreadSubmit");

const images = document.getElementById("images");

const startThreadHttpRequest = new XMLHttpRequest();
let requestSent = false;

const inputImages = document.getElementById("images");

if(startThreadSubmit != undefined){

startThreadSubmit.addEventListener("click",function(event){

    requestSent = true;

    event.preventDefault();

    startThreadHttpRequest.open("POST","/createThread",false)

    startThreadHttpRequest.setRequestHeader("entryContent",encodeURIComponent(threadFirstEntry.value));

    startThreadHttpRequest.setRequestHeader("threadTitle",encodeURIComponent(threadTitle.value));

    startThreadHttpRequest.setRequestHeader("threadCategory",threadCategory.value);

    const formData = new FormData();

    var images = inputImages.files[0];

    for(let x = 0 ;x < inputImages.files.length  ;x++){

        formData.append("images[]",inputImages.files[x]);

    }

    startThreadHttpRequest.send(formData);

    while(requestSent){

    }

})

startThreadHttpRequest.onreadystatechange = () =>{

console.log("w",startThreadHttpRequest.responseText," ");

    if(startThreadHttpRequest.readyState == 4 && startThreadHttpRequest.status == 200){

        requestSent = false;

        window.location.href = "/" + threadCategory.value + "/" + startThreadHttpRequest.responseText.split(" ")[1];

    }

}

}



const createMessageThreadForm = document.getElementById("createMessageThreadForm");

const createMessageThreadText = document.getElementById("createMessageThreadText");

const createMessageThreadSubmit = document.getElementById("createMessageThreadSubmit");

let createMessageThreadRequest = new XMLHttpRequest()
let sent = false

if(createMessageThreadSubmit != undefined){

createMessageThreadSubmit.addEventListener("click",function(event){

    event.preventDefault();

    createMessageThreadRequest.open("POST","/createMessageThread",false);

    a = window.location.href;

    urlList = a.split("/")

    createMessageThreadRequest.setRequestHeader("targetAccountName",urlList[4]);

    createMessageThreadRequest.setRequestHeader("messageContent",encodeURIComponent(createMessageThreadText.value));

    createMessageThreadRequest.send();

    sent = false;

    while(sent){

    }



})

createMessageThreadRequest.onreadystatechange = () =>{

console.log("w",createMessageThreadRequest.responseText," ");

    if(createMessageThreadRequest.readyState == 4 && createMessageThreadRequest.status == 200){

        sent = false;

        console.log(createMessageThreadRequest.responseText)

    }

}
}

