button = document.getElementById('btn')
modal = document.querySelector('.modal-login')

button.addEventListener('click', ()=>{
    modal.classList.toggle('show')
    button.classList.toggle('clicked')
})