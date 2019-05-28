button = document.getElementById('btn')
modal = document.querySelector('.modal')

button.addEventListener('click', ()=>{
    modal.classList.toggle('show')
    button.classList.toggle('clicked')
})