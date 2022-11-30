const emailInput = document.querySelector('#emailInput') 
const passwordInput = document.querySelector('#passwordInput') 
const iconShowPassword = document.querySelector('#iconShowPassword')
const itemChangePassword = document.querySelector('item-change-password')
async function changePasswordClick() {
    const alert = document.createElement('ion-alert');
    alert.header = 'Reset password';
    alert.buttons = ['OK'];
    alert.inputs = [
      {
        placeholder: 'Email',
        name: 'email',
        id: 'email'
      }
    ];

    document.body.appendChild(alert);
    await alert.present();
    dismiss = await alert.onDidDismiss();
    if(!dismiss.data)
        return;
    console.log(dismiss.data.values.email)
    fetch('/reset-password',{
    method: "POST",
    body: JSON.stringify({email:dismiss.data.values.email}),
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
        console.log(data)
        if(data.result==='ok'){
            const alert = document.createElement('ion-alert');
            alert.header = 'Email Sent!';
            alert.subHeader = 'check inbox'
            alert.buttons = ['OK'];
        
            document.body.appendChild(alert);
            alert.present();
        
        }else{
            console.log(error)
            const alert = document.createElement('ion-alert');
            alert.header = 'Error!';
            alert.subHeader = 'Email invalid'
            alert.buttons = ['OK'];
        
            document.body.appendChild(alert);
            alert.present();
        }
    }
  )
  .catch((error) => {
    console.log(error)
  })

  }
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
            console.log(data)
            if(data.result==='ok'){
                console.log(data)
                date = new Date(new Date(data.expires).getTime() + new Date().getTime())
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