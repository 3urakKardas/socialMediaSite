const signUpUserName = document.getElementById("signUpUserName");

signUpUserName.value = "";

let oldUserName = signUpUserName.value;
let newUserName = signUpUserName.value;

let userNameAvailableRequest = new XMLHttpRequest();
let userNameSent = false;
let userNameAvailable = "False";

function checkChangeInUserName(){

    userNameSent = false

    newUserName = signUpUserName.value;

    if(newUserName != oldUserName){

        if(!userNameSent){

            userNameAvailable = false;

            userNameAvailableRequest.open("POST","/userNameStatus",true);

            userNameAvailableRequest.setRequestHeader("possibleUserName",signUpUserName.value);

            userNameAvailableRequest.send();

        }

        oldUserName = newUserName;

    }

}

let userNameNotAvailableMessage = document.getElementById("userNameNotAvailableMessage");

function resetAnimation() {

  userNameNotAvailableMessage.style.animation = "none";
  userNameNotAvailableMessage.offsetHeight;
  userNameNotAvailableMessage.style.animation = null;
}


userNameAvailableRequest.onreadystatechange = () => {

    if (userNameAvailableRequest.readyState == 4 && userNameAvailableRequest.status == 200)
    {

        userNameAvailable = userNameAvailableRequest.responseText;

        userNameSent = false;

        if(userNameAvailable == "False"){

            resetAnimation();

            userNameNotAvailableMessage.classList.remove("toPopUp");

            userNameNotAvailableMessage.classList.add("toPopUp");

        }
    }

}

const checkChangeInUserNameInterval = setInterval(checkChangeInUserName,10);

const signUpPassword = document.getElementById("signUpPassword");

const signUpSubmit = document.getElementById("signUpSubmit");

const signUpForm = document.getElementById("signUpForm");

let saveAccountRequest = new XMLHttpRequest();
let accountSent = false;
let accountSaved = "-1";

signUpSubmit.addEventListener("click",function(event){

     accountSaved = "-1";

     if(userNameAvailable == "False" || signUpUserName == ""){

         event.preventDefault();

     }else if(!accountSent){

         accountSent = true;

         saveAccountRequest.open("POST","/saveAccount",false);

         saveAccountRequest.setRequestHeader("userName",signUpUserName.value);

         saveAccountRequest.setRequestHeader("userPassword",signUpPassword.value);

         saveAccountRequest.send();

         while(accountSent){

         }

         if(accountSaved != "-1"){

         signUpForm.action = "/user/" + accountSaved;

         signUpForm.submit();

         }else{

         }

         event.preventDefault()

     }

});

saveAccountRequest.onreadystatechange = () =>  {

    if (saveAccountRequest.readyState == 4 && saveAccountRequest.status == 200){

        accountSaved = saveAccountRequest.responseText;

        accountSent = false;

    }

}







