const inputfile = document.querySelector('#inputfile')
const inputContent = document.querySelector('.custom-input')
const btPublicar = document.querySelector('.bt-publicar')
const modal = document.querySelector('ion-modal');
const imgPreview = document.querySelector('.img-preview')
inputfile.addEventListener('change', (event) => {
    if(event.target.files){
        console.log('files do work')
        file = event.target.files[0]
        const fr = new FileReader()
        fr.onload = () => {
            const dataUrl = fr.result.toString()
            console.log('setting')
            imgPreview.setAttribute('src',dataUrl)
            imgPreview.style.display = 'block';
            document.querySelector('.image-container').style.display = 'block';
        }
        fr.readAsDataURL(file)
    }
})
inputContent.addEventListener('keypress', (event) => {
    if(event.target.value){
        btPublicar.setAttribute('disabled','false')
    }else{
        btPublicar.setAttribute('disabled','true')
    }
})
modal.addEventListener('willDismiss', (ev) => {
    if (ev.detail.role === 'confirm') {
      const message = document.querySelector('#message');
      message.textContent = `Hello ${ev.detail.data}!`;
    }
  });
btPublicar.addEventListener('click', (event) => {
    const file = (inputfile.files[0])
    const content = (inputContent.value)
    if(file && content){
        const uploadData = new FormData()
        uploadData.append('file',file)
        uploadData.append('content',content)
        uploadData.append('privacity',0)
        console.log(file)
        console.log(uploadData)

        fetch('/post',{
            method: 'post',
            body: uploadData
        }).then(response => {
            console.log(response)
        }).catch(err => {
            console.log(err)
        })
    }
})
