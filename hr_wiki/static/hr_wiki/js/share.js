const btn = document.getElementById('share')
const modalShare = document.querySelector('.modal-share')
const close = document.querySelector('.fa-window-close')


btn.addEventListener('click', ()=>{
    modalShare.classList.add('show')
})

close.addEventListener('click', ()=>{
    modalShare.classList.remove('show')
})

window.addEventListener('click', ()=>{
    if (event.target == modalShare){
        modalShare.classList.remove('show')
    }
})