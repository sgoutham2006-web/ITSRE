function login() {

    let role = document.getElementById("role").value;
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if(role === "" || username === "" || password === "") {
        alert("Please fill all fields");
        return;
    }

    // Teacher Login
    if(role === "teacher" && username === "teacher1" && password === "1234") {
        window.location.href = "teacher.html";
    }

    // Admin Login
    else if(role === "admin" && username === "admin1" && password === "1234") {
        window.location.href = "admin.html";
    }

    else {
        alert("Invalid Login ID or Password");
    }
}
