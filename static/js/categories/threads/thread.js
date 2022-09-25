const entryForm = document.getElementById("entryForm");

const entryContent = document.getElementById("entryContent");

const inputImages = document.getElementById("images");

const submitEntry = document.getElementById("submitEntry");

userCookie = document.cookie;

userName = userCookie.split("=")[1]

let formRequest = new XMLHttpRequest();
let sent = false;

let responseText;

submitEntry.addEventListener("click",function(event){

    sent = true;

    event.preventDefault();

    formRequest.open("POST","/addEntry",false);

    a = window.location.href

    urlList = a.split("/")

    formRequest.setRequestHeader("categoryName",urlList[3])

    formRequest.setRequestHeader("threadId",urlList[4]);

    formRequest.setRequestHeader("userName",userName);

    formRequest.setRequestHeader("entryContent",encodeURIComponent(entryContent.value));

    const formData = new FormData();

    var images = inputImages.files[0];

    for(let x = 0 ;x < inputImages.files.length  ;x++){

        formData.append("images[]",inputImages.files[x]);

    }

    formRequest.send(formData)

    while(sent){

    }

    if(responseText == "entryAdded"){

        window.location.href = "/" + urlList[3] + "/" + urlList[4];

    }

})

formRequest.onreadystatechange = () =>{

    if(formRequest.readyState == 4 && formRequest.status == 200){

        sent = false;

        responseText = formRequest.responseText;

    }

}

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