const avatarImg = document.querySelector('.perfil-icon-img')
const editButton = document.querySelector('.edit-icon-button')
const itemProfile = document.querySelector('.item-profile')
const avatarDiv = document.querySelector('.avatar')
const inputFileElement = document.querySelector('#inputfile')
avatarImg.addEventListener('click',(event) => {
    console.log('click')
})
avatarDiv.addEventListener('click',(event) => {
    inputFileElement.click()

})
inputFileElement.addEventListener('change', (event) => {
    console.log(event.target.files)
    const file = event.target.files[0]
    if(file){
        const uploadData = new FormData()
        uploadData.append('file',file)
        console.log(file)
        console.log(uploadData)

        fetch('/pic',{
            method: 'post',
            body: uploadData
        }).then(response => {
            console.log(response)
            window.location = window.location
        }).catch(err => {
            console.log(err)
        })
    }

})
