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
})
