const changeProfileImage = document.getElementById("changeProfileImage");

const newProfileImage = document.getElementById("newProfileImage");

const submitButton = document.getElementById("submitButton");

let changeProfileImageRequest = new XMLHttpRequest();

submitButton.addEventListener("click",function(event){

    event.preventDefault();

    changeProfileImageRequest.open("POST","/changeProfileImage",false);

    changeProfileImageRequest.setRequestHeader("a","b");

    const formData = new FormData();

    formData.append("image",newProfileImage.files[0]);

    changeProfileImageRequest.send(formData);

    sent.sent = true;

})

changeProfileImageRequest.onreadystatechange = (sent) =>{

    if(changeProfileImageRequest.readyState == 4 && changeProfileImageRequest.status == 200){

        sent.sent = false;

    }

}

//----------------------------------------------------------------------------------------------------------------

changeProfileDescription = document.getElementById("changeProfileDescription");

userDescription = document.getElementById("userDescription");

submitUserDescriptionButton = document.getElementById("submitUserDescriptionButton");

let changeUserDescriptionRequest = new XMLHttpRequest();

submitUserDescriptionButton.addEventListener("click",function(event){

     event.preventDefault();

     changeUserDescriptionRequest.open("POST","/changeUserDescription",false);

     changeUserDescriptionRequest.setRequestHeader("userDescription",encodeURIComponent(userDescription.value));

     changeUserDescriptionRequest.send();

})

changeUserDescriptionRequest.onreadystatechange = () => {

    if(changeUserDescriptionRequest.readyState == 4 && changeUserDescriptionRequest.status == 200){

        console.log(changeUserDescriptionRequest.responseText);

    }

}






