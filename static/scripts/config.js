const select = document.querySelector('#selectLanguage');

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
