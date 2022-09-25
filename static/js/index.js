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