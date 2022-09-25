const startThreadForm = document.getElementById("startThreadForm");

const threadTitle = document.getElementById("threadTitle");

const threadFirstEntry = document.getElementById("threadFirstEntry");

const images = document.getElementById("images");

const startThreadSubmit = document.getElementById("startThreadSubmit");

const geocode = document.getElementById("selectedCategoryDiv").dataset.geocode;

let startThreadRequest = new XMLHttpRequest();

startThreadSubmit.addEventListener("click",function(event){

    event.preventDefault();

    startThreadRequest.open("POST","/createThread",false);

    startThreadRequest.setRequestHeader("threadTitle",encodeURIComponent(threadTitle.value));

    startThreadRequest.setRequestHeader("entryContent",encodeURIComponent(threadFirstEntry.value));

    startThreadRequest.setRequestHeader("threadCategory",geocode);

    const formData = new FormData();

   for(let x = 0; x < images.files.length ; x++){

       formData.append("images[]",images.files[x]);

   }

   startThreadRequest.send(formData);

})

startThreadRequest.onreadystatechange = () => {

    if(startThreadRequest.readyState == 4 && startThreadRequest.status == 200){

        let listOfResponse = startThreadRequest.responseText.trim().split(" ");

        if(listOfResponse[0] == "threadCreated"){

              a = window.location.href

              urlList = a.split("/")

              window.location.href = "/" + urlList[3] + "/" + listOfResponse[1];

    }

    }

}

//-----------------------------------------------------------------------------------------------

var likeDislikeRequest = new XMLHttpRequest();

let like = document.getElementsByClassName("like");

let dislike = document.getElementsByClassName("dislike");

for(let i = 0; i < like.length;i++){

    like[i].addEventListener("click",function(event){

    event.preventDefault();

    var entryId = event.target.id.trim().split("_")[1];

    likeDislikeRequest.open("POST","/like/" + entryId,false);

    likeDislikeRequest.send();

})
}

for(let j = 0; j < dislike.length;j++){

    dislike[j].addEventListener("click",function(event){

    event.preventDefault();

    var entryId = event.target.id.trim().split("_")[1];

    likeDislikeRequest.open("POST","/dislike/" + entryId,false);

    likeDislikeRequest.send();


})
}

likeDislikeRequest.onreadystatechange = () =>{

    if(likeDislikeRequest.readyState == 4 && likeDislikeRequest.status == 200){

        let responseList = likeDislikeRequest.responseText.trim().split(" ");

        responseText = likeDislikeRequest.responseText;

        if(responseList[0] == "-1"){

        }else{

            let likesValues = document.getElementById("likes_"+responseList[0]);

            let disLikesValues = document.getElementById("dislikes_"+responseList[0]);

            likesValues.innerHTML = responseList[2];

            disLikesValues.innerHTML = responseList[4];

        }

    }

}