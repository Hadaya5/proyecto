const selects = document.querySelectorAll('.date-select');
const modal = document.querySelector('ion-modal');
const datetime = document.querySelector('ion-datetime')
const daySelect = document.querySelector('#day-select')
const monthSelect = document.querySelector('#month-select')
const yearSelect = document.querySelector('#year-select')

const nameInput = document.querySelector('#nameInput') 
const lastNameInput = document.querySelector('#lastNameInput') 
const emailInput = document.querySelector('#emailInput') 
const passwordInput = document.querySelector('#passwordInput') 
const confirmPasswordInput = document.querySelector('#confirmPasswordInput')
const signupButton = document.querySelector("#signupButton")
const popover = document.querySelector('ion-popover');
const emailError = document.querySelector('#emailError')
const emailErrorText = emailError.textContent
const form = document.getElementById('form')
nameInput.addEventListener('ionBlur', (event) => {
    notEmpty(nameInput)
})
lastNameInput.addEventListener('ionBlur', (event) => {
    notEmpty(lastNameInput)
})
function notEmpty(element){
    let item = element.closest("ion-item")
    markTouched(item)
    item.classList.remove('ion-valid');
    item.classList.remove('ion-invalid');
    if(element.value.length > 0){
        item.classList.add('ion-valid')
    }else{
        item.classList.add('ion-invalid')
    }

}
emailInput.addEventListener('ionBlur', (event) => {
    let item = emailInput.closest("ion-item")
    markTouched(item)
    if(validateEmail(emailInput.value)){
        markValid(item)
    }else{
        emailError.textContent = emailErrorText
        markInvalid(item)
    }
       
})
confirmPasswordInput.addEventListener('ionBlur', (event) => {
    let item = confirmPasswordInput.closest("ion-item")
    markTouched(item)
    item.classList.remove('ion-valid');
    item.classList.remove('ion-invalid');

    if(passwordsMatch()){
        item.classList.add('ion-valid')
    }else{
        item.classList.add('ion-invalid')
    }
})
passwordInput.addEventListener('ionBlur', (event) => {
    let item = passwordInput.closest("ion-item")
    markTouched(item)
    len = passwordInput.value.length
    item.classList.remove('ion-valid');
    item.classList.remove('ion-invalid');
    if(len >=8){
        confirmPasswordInput.disabled = false
        item.classList.add('ion-valid')
    }else{
        confirmPasswordInput.disabled = true
        item.classList.add('ion-invalid')
    }
})


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

function passwordsMatch(){
    return confirmPasswordInput.value === passwordInput.value
}

const validateEmail = (email) => {
    return email.match(/^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/);
};
datetime.locale = navigator.locale
datetime.min = new Date("1922-01-01").toISOString()
datetime.max = new Date().toISOString()

selects.forEach( (select) => {
    select.addEventListener('click', e => {
        e.preventDefault()
        e.stopPropagation()
        e.stopImmediatePropagation()
        console.log('click')
        modal.present();
      });
} ) 
datetime.addEventListener('ionChange',setDate)

function setDate(event){
    console.log('vamos')
    const date = new Date(datetime.value)
    console.log(date.toISOString())
    console.log(date.g)
    let element = daySelect.shadowRoot.querySelector('.select-text')
    element.textContent = date.getDate()
    element.style.opacity = 1
    element = monthSelect.shadowRoot.querySelector('.select-text')
    element.textContent = date.getMonth()+1
    element.style.opacity = 1

    element = yearSelect.shadowRoot.querySelector('.select-text')
    element.textContent = date.getFullYear()
    element.style.opacity = 1
    document.querySelectorAll('.datetime-item').forEach((item) => { markValid(item)})
}
function isValid(element){
    return element.closest("ion-item").classList.contains('ion-valid')
}
function isTouched(element){
    return element.closest("ion-item").classList.contains('ion-touched')
}
form.addEventListener("submit", (e) => {
    console.log(e)
    e.preventDefault()
    console.log("%s", JSON.stringify(e));
    e.preventDefault();
    if(!isValid(passwordInput) || !isValid(confirmPasswordInput) || !isValid(emailInput) ||
     !isValid(nameInput) || !isValid(lastNameInput)){
        console.log('mal')
        document.querySelectorAll('ion-item').forEach((item) => {
            markTouched(item)
            if(!isValid(item)){
                markInvalid(item)
            }
        })
        return
     }else{
        console.log('todo bien')
     }
    const email = emailInput.value
    const password = passwordInput.value
    const name = nameInput.value
    const lastname = lastNameInput.value
    const gender = document.querySelector('ion-radio-group').value
    const birthday = datetime.value.slice(0,10)
    let user = {email,password,name,lastname,birthday,gender}
    fetch("/signup", {
        method: "POST",
        body: JSON.stringify(user),
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
            if(data.result === "ok"){
                const alert = document.createElement('ion-alert');
                alert.header = data.message;
                alert.subHeader = data.submessage;
                // alert.message = '';
                alert.buttons = [{
                    text: 'OK',
                    role: 'confirm',
                    handler: () => { window.location = '/login' }
                }];
            
                document.body.appendChild(alert);
                alert.present().then(() => {
                    console.log('alert show')
                } )
            }else if(data.result === "emailused"){
                emailError.textContent = data.message
                markInvalid(emailInput.closest('ion-item'))
            }
        }
      )
      .catch((error) => {
        console.log(error)
      })

})
function signup(){

}