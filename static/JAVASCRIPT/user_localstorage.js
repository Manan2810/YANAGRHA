
function create_unique_string(string_length){
    var unique_string = "";
    var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz";
    for (var i = 0; i < string_length; i++) {
        unique_string += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return unique_string;
  }
  
  function generateUniqueString() {
    var uniqueString = create_unique_string(6);
    localStorage.setItem("unique_string", uniqueString); // Store the unique string in local storage
    document.getElementById('unique_id').innerHTML = uniqueString;}


function storeData() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
    console.log("Data stored in local storage.");
  }

