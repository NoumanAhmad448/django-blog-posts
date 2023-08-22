function togglePassFun(passField, passAction, iconField, iconAction, iconRemoveClass){
    if(debug){
        console.log("passField "+passField)
        console.log("passAction "+passAction)
        console.log("iconField "+iconField)
        console.log("iconAction "+iconAction)
        console.log("iconRemoveClass "+iconRemoveClass)
    }
    $(`${passField}`).attr("type",`${passAction}`)
    $(iconField).addClass(iconAction).removeClass(iconRemoveClass)
}

let passActionClass = "bi-eye-slash"
let eyeOpenClass = "bi-eye"
let togglePassField = "#togglePassword"

$(togglePassField).click(()=>{
    passwordField = "#password"

    if($(passwordField).attr("type") == "password"){
        togglePassFun(passwordField, "text", togglePassField, eyeOpenClass, passActionClass)
    }else{
        togglePassFun(passwordField, "password", togglePassField, passActionClass,eyeOpenClass)
    }
})