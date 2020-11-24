
document.getElementById('contact').addEventListener('submit', function(evt){
    evt.preventDefault();
    sendData();
})


function sendData() {
    // Initiate Variables With Form Content
    var name = document.getElementById("cp_name").value;
    var email = document.getElementById("cp_email").value;
    var message = document.getElementById("cp_message").value;
    var phone = document.getElementById("cp_phone").value;
    var data = {
      "senderName": name,
      "email": email,
      "phone" : phone,
      "message": message,
      "category": 2
};
  var newXHR = new XMLHttpRequest();
  // "load" is fired when the response to our request is completed without error.
  newXHR.addEventListener( 'load', formSuccess);
  
  var formatedData = JSON.stringify(data);
  console.log(formatedData)

  newXHR.open( 'POST', 'https://kz14jdq4d7.execute-api.eu-central-1.amazonaws.com/development/sendEmail' );
  newXHR.setRequestHeader( 'Content-Type', 'application/json' );
  
  newXHR.send(formatedData);
}

function formSuccess(){
  document.getElementById('msgSubmit').classList.remove("hidden");
  document.getElementById('contact').reset();
}
