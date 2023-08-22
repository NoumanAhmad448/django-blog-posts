$(()=>{
    togglePassField = "#togglePassword01"
    $(togglePassField).click(()=>{
        passwordField = "#c_password"

        if($(passwordField).attr("type") == "password"){
            togglePassFun(passwordField, "text", togglePassField, eyeOpenClass, passActionClass)
        }else{
            togglePassFun(passwordField, "password", togglePassField, passActionClass,eyeOpenClass)
        }
    })
})