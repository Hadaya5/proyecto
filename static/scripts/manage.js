const blockbuttons = document.querySelectorAll('ion-button')
blockbuttons.forEach( button => {
    button.addEventListener('click',(event) => {
        action = event.target.getAttribute('name')
        user = event.target.closest('.user-ion-item').getAttribute('name')
        console.log(user)
        console.log(action)
        if(action === 'unblock'){
            console.log('executing')
            fetch(`/user/blocks?user=${user}`, {
                method: "DELETE",
                body: JSON.stringify({user}),
                headers: {
                  "Content-Type": "application/json"
                }
              }).then((response) => {
                console.log(response)
                if (!response.ok) {
                    throw new Error(`Request failed with status ${reponse.status}`)
                  }else{
                    window.location = '/manage'
                    return response.json()
                  }
        
              } ).then(
                (data) => {
                    console.log(data)
                    if(data.result==='ok'){
                        window.location = '/manage'
                    }else{
                    }
                }).catch(err => {
                    console.log(err)
                } )
        }
        if(action === 'unfriend'){
            console.log('executing')
            fetch(`/user/friends?user=${user}`, {
                method: "DELETE",
                body: JSON.stringify({user}),
                headers: {
                  "Content-Type": "application/json"
                }
              }).then((response) => {
                console.log(response)
                if (!response.ok) {
                    throw new Error(`Request failed with status ${reponse.status}`)
                  }else{
                    window.location = '/manage'
                    return response.json()
                  }
        
              } ).then(
                (data) => {
                    console.log(data)
                    if(data.result==='ok'){
                        window.location = '/manage'
                    }else{
                    }
                }).catch(err => {
                    console.log(err)
                } )
        }
        if(action == 'block'){
            console.log('executing')
            fetch(`/user/blocks`, {
                method: "POST",
                body: JSON.stringify({user}),
                headers: {
                  "Content-Type": "application/json"
                }
              }).then((response) => {
                console.log(response)
                if (!response.ok) {
                    throw new Error(`Request failed with status ${reponse.status}`)
                  }else{
                    window.location = '/manage'
                    return response.json()
                  }
        
              } ).then(
                (data) => {
                    console.log(data)
                    if(data.result==='ok'){
                        window.location = '/manage'
                    }else{
                    }
                }).catch(err => {
                    console.log(err)
                } )
        }
   
   
    })
} )