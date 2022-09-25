var c = document.cookie

let arrC = document.cookie.split("=");

let req = new XMLHttpRequest();
let reqSent = false;

function deleteCookie(){

    reqSent = false;

    req.open("POST","/deleteCookie",false);

    req.setRequestHeader("erase","true");

    req.send();

    reqSent = true;

    while(true){

        if(req.readyState == 4 && req.status == 200){

           break;

        }

    }

}

const cookieDuration = 90;
//cookieDuration is the number of seconds before cookie is deleted and in this case before user lose
//the access to the account,
//after this duration one of these two processes has to be repeated,
//without this cookie an account has to be signed in every time the page is refreshed
//this part is refreshing the expiration date of original cookie got by sign up or sign in
//the duration of original cookie is determined in the main flaskManager.py file

if(document.cookie.indexOf('currentUser=') != -1){
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 1000*cookieDuration;
    now.setTime(expireTime);

    document.cookie = "currentUser="+ arrC[1]/*document.cookie.split("=")[1]*/ +";" + "expires="+now.toUTCString()+";"+"path=/";

}

const signInText = document.getElementById("signInText");

const signInPassword = document.getElementById("signInPassword");

const signInSubmit = document.getElementById("signInSubmit");

const signInForm = document.getElementById("signInForm");

let signInRequest = new XMLHttpRequest();
let signInSent = false;
let signInStatus = "-1";

function callCookie(givenValue,givenDate){

     var now = new Date();
     var time = now.getTime();
     var expireTime = time + 1000*5;
     now.setTime(expireTime);

     document.cookie = "accountId="+ givenValue +";" + "expires="+now.toUTCString()+";";

}

if(document.cookie.indexOf("currentUser") == -1){

signInSubmit.addEventListener("click",function(event){

    if(signInText.value != "" && signInPassword.value != "" && !signInSent){

        signInSent = true;

        signInStatus = "-1";

        signInRequest.open("POST","/signInStatus",false);

        signInRequest.setRequestHeader("userName",signInText.value);

        signInRequest.setRequestHeader("userPassword",signInPassword.value);

        signInRequest.send();

        let count = 0;

        while(signInSent){

        }

        if(signInStatus == "-1"){

          event.preventDefault();

        }else if(signInStatus == "-2"){

          event.preventDefault();

        }else{

          signInForm.action = "/user/" + signInStatus;

          signInForm.submit();
          event.preventDefault();

        }

        event.preventDefault();

    }

})

signInRequest.onreadystatechange = () => {

    if(signInRequest.readyState == 4 && signInRequest.status == 200){

        signInStatus = signInRequest.responseText;

        signInSent = false;

    }

}
}

//------------------------------------------------------------------------------------------------------

let searchRequest = new XMLHttpRequest();

const searchBar = document.getElementById("searchBar");

function searchFunction(){

console.log("func is activated",searchRequest);

     searchRequest.open("POST","/search",false);

     searchRequest.setRequestHeader("searchTerm",searchBar.value);

     searchRequest.send();

}

searchRequest.onreadystatechange = () =>{

    if(searchRequest.readyState == 4 && searchRequest.status == 200){

        response = searchRequest.responseText;

        if(response != "-1"){

        }

        let foundTerms = [];

          const temp = response.trim().split("|");

        for(let i = 0; i < temp.length; i++){

              if(temp[i] == "@"){

                  foundTerms.push(["@",temp[i+1]]);

              }else if(temp[i] == "$"){

                  foundTerms.push(["$",temp[i+1],temp[i+2],temp[i+3]]);

              }

        }

        let documentTempTerms = document.getElementsByClassName("foundTerm");
        let documentTempLinks = document.getElementsByClassName("foundTermLink");

        for(let t = 0; t < documentTempTerms.length; t++){

              documentTempTerms[t].style.display = "none";

        }

        for(let j = 0; j < Math.min(foundTerms.length,documentTempTerms.length); j++){

              if(foundTerms[j][0] == "@"){

                  documentTempTerms[j].innerHTML = "@ " + foundTerms[j][1];
                  documentTempLinks[j].href = "/user/" + foundTerms[j][1];

              }else if(foundTerms[j][0] == "$"){

                  documentTempTerms[j].innerHTML = foundTerms[j][3];
                  documentTempLinks[j].href = "/" + foundTerms[j][1] + "/" + foundTerms[j][2];

              }

              documentTempTerms[j].style.display = "block";

        }
    }
}

