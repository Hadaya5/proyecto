const select = document.querySelector('#selectLanguage');
const inputs = document.querySelectorAll('.config-input');
const icons = document.querySelectorAll('.save-icon');
function edit(){
  
}
icons.forEach( icon => {
  icon.addEventListener('click', (event) => {
    console.log(event.target.parentNode)
    const input = event.target.parentNode.querySelector('.config-input')
    // text = input.value
    const name = input.name
    const value = input.value
    config = {}
    config[name] = value
    console.log('updating',input.name,input.value)
    data = {config}
    fetch("/edit", {
      method: "POST",
      body: JSON.stringify(data),
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
            event.target.style.visibility = 'hidden';
          }else{
              console.log('error')
          }
      }
    )
    .catch((error) => {
      console.log(error)
    })
  
  })
} )
inputs.forEach( input => {
  input.addEventListener('keyup', (event) => {
    console.log(event)
    const icon = event.target.parentNode.parentNode.querySelector('.save-icon')
    if(event.target.parentNode.value ){
      icon.style.visibility = 'visible'


    }else{
      icon.style.visibility = 'hidden'

    }
  })
})
select.addEventListener('ionChange', e => {
  console.log(`ionChange fired with value: ${e.detail.value}`);
  data = {config:{"language":e.detail.value}}
  fetch("/config", {
    method: "POST",
    body: JSON.stringify(data),
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
            window.location.reload(true)
        }else{
            console.log('error')
        }
    }
  )
  .catch((error) => {
    console.log(error)
  })

});
