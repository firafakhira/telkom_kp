// MODAL LOGIN
button = document.getElementById('btn')
modal = document.querySelector('.modal')
nav = document.querySelector('nav')

button.addEventListener('click', ()=>{
    modal.classList.toggle('show')
    button.classList.toggle('clicked')
})

window.addEventListener('click', ()=>{
    if (event.target == modal || event.target == nav){
        modal.classList.toggle('show')
        button.classList.toggle('clicked')
    }
})