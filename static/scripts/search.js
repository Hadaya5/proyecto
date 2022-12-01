addFriends = document.querySelectorAll('.button-add-friend')

addFriends.forEach(button => {
    button.addEventListener('click',(event) => {
        event.stopPropagation();
        let user = event.target.closest('ion-card').getAttribute('name')
        console.log(user)
        fetch("/user/friends", {
            method: "POST",
            body: JSON.stringify({user}),
            headers: {
              "Content-Type": "application/json"
            }
          }).then((response) => {
            const alert = document.createElement('ion-alert');
            alert.header = 'Sucess!';
            alert.subHeader = 'Got a new friend!'
            alert.buttons = ['OK'];
        
            document.body.appendChild(alert);
            alert.present();
          
        }).catch(err => {
            console.log(err)
        })
    })
}) 