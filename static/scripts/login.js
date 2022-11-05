const emailInput = document.querySelector('#emailInput') 
const passwordInput = document.querySelector('#passwordInput') 
const iconShowPassword = document.querySelector('#iconShowPassword')
// iconShowPassword.addEventListener('click',togglePassword())
function togglePassword(){
    if(passwordInput.getAttribute("type") === "password"){
        iconShowPassword.setAttribute("name","eye-off-outline")
        passwordInput.setAttribute("type","text")    
    }else{
        iconShowPassword.setAttribute("name","eye-outline")
        passwordInput.setAttribute("type","password")
    }
}
emailInput.addEventListener('ionBlur', (event) => {
    let item = emailInput.closest("ion-item")
    markTouched(item)
    if(validateEmail(emailInput.value)){
        markValid(item)
    }else{
        markInvalid(item)
    }
       
})
passwordInput.addEventListener('ionBlur', (event) => {
    let item = passwordInput.closest("ion-item")
    markTouched(item)
    len = passwordInput.value.length
    if(len >=8){
        markValid(item)
    }else{
        markInvalid(item)
    }
})
const validateEmail = (email) => {
    return email.match(/^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/);
};
function markTouched(item){
    item.classList.add('ion-touched');
}
function markInvalid(item){
    item.classList.remove('ion-valid');
    item.classList.remove('ion-invalid');
    item.classList.add('ion-invalid');
}
function markValid(item){
    item.classList.remove('ion-valid');
    item.classList.remove('ion-invalid');
    item.classList.add('ion-valid');
}

function isValid(element){
    return element.closest("ion-item").classList.contains('ion-valid')
}
function isTouched(element){
    return element.closest("ion-item").classList.contains('ion-touched')
}

function login(){
    if(!isValid(emailInput) || !isValid(passwordInput)){
        markTouched(emailInput.closest('ion-item'))
        markInvalid(emailInput.closest('ion-item'))
        markTouched(passwordInput.closest('ion-item'))
        markInvalid(passwordInput.closest('ion-item'))
        return
    }
    const email = emailInput.value
    const password = passwordInput.value
    let credentials = {email,password}
    fetch("/login", {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
          "Content-Type": "application/json"
        }
      }).then((response) => {
        console.log(response)
        if (!response.ok) {
            throw new Error(`Request failed with status ${reponse.status}`)
          }else{
            return response.json()
          }

      } ).then(
        (data) => {
            if(data.result==='ok'){
                console.log(data)
                date = new Date(data.expires)
                expires = "; expires=" + date.toUTCString();
                document.cookie = `token=${data.token}` + expires
                document.cookie = `uid=${data.uid}` + expires
                window.location = '/'
            }else{
                console.log('invalid login')
            }
        }
      )
      .catch((error) => {
        console.log(error)
      })

}