btn = document.getElementById('komen')
modalKomen = document.querySelector('.modal-komen')
close = document.querySelector('.fa-window-close')


btn.addEventListener('click', ()=>{
    modalKomen.classList.add('show')
})

close.addEventListener('click', ()=>{
    modalKomen.classList.remove('show')
})

window.addEventListener('click', ()=>{
    if (event.target == modalKomen){
        modalKomen.classList.remove('show')
    }
})