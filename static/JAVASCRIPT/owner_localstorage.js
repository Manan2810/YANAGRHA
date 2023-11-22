function storeData1() {
    var username = document.getElementById("email").value;
    var password = document.getElementById("name").value;
    var mobileno = document.getElementById("Mobile_no").value;
    var loc = document.getElementById("location").value;
    localStorage.setItem("email", username);
    localStorage.setItem("name", password);
    localStorage.setItem("mobile_no", mobileno);
    localStorage.setItem("address", loc);

    console.log("Data stored in local storage.");
  }
